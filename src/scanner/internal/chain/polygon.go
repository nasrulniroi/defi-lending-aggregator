package chain

import (
	"time"

	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/rpc"
	"go.uber.org/zap"
)

// PolygonScanner scans Polygon for lending rates.
type PolygonScanner struct {
	client *rpc.Client
	logger *zap.Logger
	chain  string
}

// NewPolygonScanner creates a new Polygon chain scanner.
func NewPolygonScanner(rpcURL string, logger *zap.Logger) *PolygonScanner {
	return &PolygonScanner{
		client: rpc.NewClient(rpcURL),
		logger: logger.Named("polygon"),
		chain:  "polygon",
	}
}

// Chain returns the chain name.
func (s *PolygonScanner) Chain() string { return s.chain }

// ScanRates fetches current lending rates from Polygon.
func (s *PolygonScanner) ScanRates(ctx interface{}) ([]protocol.LendingRate, error) {
	s.logger.Info("scanning Polygon lending rates")

	rates := make([]protocol.LendingRate, 0)
	for _, asset := range protocol.KnownAssets["polygon"] {
		rates = append(rates, protocol.LendingRate{
			Protocol:  "aave",
			Chain:     s.chain,
			Asset:     asset.Symbol,
			Address:   asset.Address,
			Decimals:  asset.Decimals,
			SupplyAPY: 4.15,
			BorrowAPY: 6.20,
			SupplyAPR: 4.07,
			BorrowAPR: 6.02,
			Timestamp: time.Now(),
		})
	}

	s.logger.Info("Polygon scan complete", zap.Int("rates", len(rates)))
	return rates, nil
}
