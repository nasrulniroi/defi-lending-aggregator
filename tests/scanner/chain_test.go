package chain

import (
	"context"
	"testing"
)

func TestEthereumScanner_ChainID(t *testing.T) {
	tests := []struct {
		name    string
		chain   string
		wantID  int
		wantErr bool
	}{
		{"ethereum mainnet", "ethereum", 1, false},
		{"arbitrum one", "arbitrum", 42161, false},
		{"polygon", "polygon", 137, false},
		{"base", "base", 8453, false},
		{"avalanche", "avalanche", 43114, false},
		{"unsupported", "solana", 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			registry := NewRegistry()
			scanner, err := registry.GetScanner(tt.chain)
			if (err != nil) != tt.wantErr {
				t.Errorf("GetScanner() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && scanner.ChainID() != tt.wantID {
				t.Errorf("ChainID() = %d, want %d", scanner.ChainID(), tt.wantID)
			}
		})
	}
}

func TestEthereumScanner_SupportedProtocols(t *testing.T) {
	scanner := NewEthereumScanner("https://rpc.ankr.com/eth")
	protocols := scanner.SupportedProtocols()

	if len(protocols) == 0 {
		t.Error("Expected at least one supported protocol")
	}

	expected := map[string]bool{"aave-v3": true, "compound-v3": true, "morpho-blue": true}
	for _, p := range protocols {
		if !expected[p] {
			t.Errorf("Unexpected protocol: %s", p)
		}
	}
}

func TestScanner_FetchRates_Timeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 0)
	defer cancel()

	scanner := NewEthereumScanner("https://invalid.rpc.url")
	_, err := scanner.FetchRates(ctx, "USDC")
	if err == nil {
		t.Error("Expected timeout error for invalid RPC")
	}
}
