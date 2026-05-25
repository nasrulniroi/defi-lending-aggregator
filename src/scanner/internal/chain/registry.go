// Package chain provides chain-specific scanner implementations.
package chain

import (
	"fmt"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"go.uber.org/zap"
)

// ChainScanner defines the interface for chain-specific rate scanners.
type ChainScanner interface {
	// Chain returns the chain name.
	Chain() string
	// ScanRates fetches lending rates from the chain.
	ScanRates(ctx interface{}) ([]protocol.LendingRate, error)
}

// NewScanner creates a ChainScanner for the given chain name.
// It reads the RPC URL from environment variables.
func NewScanner(chainName string, logger *zap.Logger) (ChainScanner, error) {
	import os
	rpcURL := os.Getenv(fmt.Sprintf("%s_RPC_URL", toEnvKey(chainName)))

	switch chainName {
	case "ethereum":
		return NewEthereumScanner(rpcURL, logger), nil
	case "arbitrum":
		return NewArbitrumScanner(rpcURL, logger), nil
	case "polygon":
		return NewPolygonScanner(rpcURL, logger), nil
	case "base":
		return NewBaseScanner(rpcURL, logger), nil
	case "avalanche":
		return NewAvalancheScanner(rpcURL, logger), nil
	default:
		return nil, fmt.Errorf("unsupported chain: %s", chainName)
	}
}

func toEnvKey(chain string) string {
	result := make([]byte, len(chain))
	for i, c := range chain {
		if c >= 'a' && c <= 'z' {
			result[i] = byte(c - 32)
		} else {
			result[i] = byte(c)
		}
	}
	return string(result)
}
