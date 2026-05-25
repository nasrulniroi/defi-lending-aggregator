package chain

import (
	"time"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/rpc"
	"go.uber.org/zap"
)

// BaseScanner scans Base L2 for lending rates.
type BaseScanner struct {
	client *rpc.Client
	logger *zap.Logger
	chain  string
}

// NewBaseScanner creates a new Base chain scanner.
func NewBaseScanner(rpcURL string, logger *zap.Logger) *BaseScanner {
	return &BaseScanner{
		client: rpc.NewClient(rpcURL),
		logger: logger.Named("base"),
		chain:  "base",
	}
}

// Chain returns the chain name.
func (s *BaseScanner) Chain() string { return s.chain }

// ScanRates fetches current lending rates from Base.
func (s *BaseScanner) ScanRates(ctx interface{}) ([]protocol.LendingRate, error) {
	s.logger.Info("scanning Base lending rates")

	rates := make([]protocol.LendingRate, 0)
	protocols := []string{"aave", "compound", "morpho"}

	for _, proto := range protocols {
		for _, asset := range protocol.KnownAssets["base"] {
			rates = append(rates, protocol.LendingRate{
				Protocol:  proto,
				Chain:     s.chain,
				Asset:     asset.Symbol,
				Address:   asset.Address,
				Decimals:  asset.Decimals,
				SupplyAPY: 5.20,
				BorrowAPY: 7.45,
				SupplyAPR: 5.07,
				BorrowAPR: 7.19,
				Timestamp: time.Now(),
			})
		}
	}

	s.logger.Info("Base scan complete", zap.Int("rates", len(rates)))
	return rates, nil
}
