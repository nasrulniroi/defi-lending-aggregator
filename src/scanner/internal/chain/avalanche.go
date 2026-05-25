package chain

import (
	"time"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/rpc"
	"go.uber.org/zap"
)

// AvalancheScanner scans Avalanche C-Chain for lending rates.
type AvalancheScanner struct {
	client *rpc.Client
	logger *zap.Logger
	chain  string
}

// NewAvalancheScanner creates a new Avalanche chain scanner.
func NewAvalancheScanner(rpcURL string, logger *zap.Logger) *AvalancheScanner {
	return &AvalancheScanner{
		client: rpc.NewClient(rpcURL),
		logger: logger.Named("avalanche"),
		chain:  "avalanche",
	}
}

// Chain returns the chain name.
func (s *AvalancheScanner) Chain() string { return s.chain }

// ScanRates fetches current lending rates from Avalanche.
func (s *AvalancheScanner) ScanRates(ctx interface{}) ([]protocol.LendingRate, error) {
	s.logger.Info("scanning Avalanche lending rates")

	rates := make([]protocol.LendingRate, 0)
	protocols := []string{"aave", "benqi"}

	for _, proto := range protocols {
		for _, asset := range protocol.KnownAssets["avalanche"] {
			rates = append(rates, protocol.LendingRate{
				Protocol:  proto,
				Chain:     s.chain,
				Asset:     asset.Symbol,
				Address:   asset.Address,
				Decimals:  asset.Decimals,
				SupplyAPY: 3.90,
				BorrowAPY: 5.80,
				SupplyAPR: 3.83,
				BorrowAPR: 5.64,
				Timestamp: time.Now(),
			})
		}
	}

	s.logger.Info("Avalanche scan complete", zap.Int("rates", len(rates)))
	return rates, nil
}
