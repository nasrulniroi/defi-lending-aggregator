// Package rpc provides a JSON-RPC client for EVM chains.
package rpc

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync/atomic"
	"time"
)

// Request represents a JSON-RPC request.
type Request struct {
	JSONRPC string        `json:"jsonrpc"`
	ID      uint64        `json:"id"`
	Method  string        `json:"method"`
	Params  []interface{} `json:"params"`
}

// Response represents a JSON-RPC response.
type Response struct {
	JSONRPC string          `json:"jsonrpc"`
	ID      uint64          `json:"id"`
	Result  json.RawMessage `json:"result"`
	Error   *RPCError       `json:"error,omitempty"`
}

// RPCError represents a JSON-RPC error.
type RPCError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

func (e *RPCError) Error() string {
	return fmt.Sprintf("RPC error %d: %s", e.Code, e.Message)
}

// Client is a JSON-RPC client for EVM chains.
type Client struct {
	rpcURL    string
	http      *http.Client
	idCounter atomic.Uint64
	timeout   time.Duration
}

// NewClient creates a new JSON-RPC client.
func NewClient(rpcURL string) *Client {
	return &Client{
		rpcURL: rpcURL,
		http: &http.Client{
			Timeout: 15 * time.Second,
		},
		timeout: 15 * time.Second,
	}
}

// Call sends a JSON-RPC request and returns the raw result.
func (c *Client) Call(ctx context.Context, method string, params ...interface{}) (json.RawMessage, error) {
	id := c.idCounter.Add(1)

	req := Request{
		JSONRPC: "2.0",
		ID:      id,
		Method:  method,
		Params:  params,
	}

	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, "POST", c.rpcURL, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := c.http.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("send request: %w", err)
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("read response: %w", err)
	}

	var rpcResp Response
	if err := json.Unmarshal(respBody, &rpcResp); err != nil {
		return nil, fmt.Errorf("unmarshal response: %w", err)
	}

	if rpcResp.Error != nil {
		return nil, rpcResp.Error
	}

	return rpcResp.Result, nil
}

// EthCall performs an eth_call to a contract.
func (c *Client) EthCall(ctx context.Context, to string, data string) (string, error) {
	params := []interface{}{
		map[string]string{"to": to, "data": data},
		"latest",
	}

	result, err := c.Call(ctx, "eth_call", params...)
	if err != nil {
		return "", err
	}

	var hexResult string
	if err := json.Unmarshal(result, &hexResult); err != nil {
		return "", fmt.Errorf("decode result: %w", err)
	}

	return hexResult, nil
}

// GetBlockNumber returns the latest block number.
func (c *Client) GetBlockNumber(ctx context.Context) (uint64, error) {
	result, err := c.Call(ctx, "eth_blockNumber")
	if err != nil {
		return 0, err
	}

	var hexNum string
	if err := json.Unmarshal(result, &hexNum); err != nil {
		return 0, fmt.Errorf("decode block number: %w", err)
	}

	var blockNum uint64
	fmt.Sscanf(hexNum, "0x%x", &blockNum)
	return blockNum, nil
}

// GetBalance returns the ETH balance of an address.
func (c *Client) GetBalance(ctx context.Context, address string) (string, error) {
	result, err := c.Call(ctx, "eth_getBalance", address, "latest")
	if err != nil {
		return "", err
	}

	var hexBalance string
	if err := json.Unmarshal(result, &hexBalance); err != nil {
		return "", fmt.Errorf("decode balance: %w", err)
	}

	return hexBalance, nil
}
