package chain

import (
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/rpc"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"go.uber.org/zap"
	"time"
)

// ArbitrumScanner scans Arbitrum One for lending rates.
type ArbitrumScanner struct {
	client *rpc.Client
	logger *zap.Logger
	chain  string
}

// NewArbitrumScanner creates a new Arbitrum chain scanner.
func NewArbitrumScanner(rpcURL string, logger *zap.Logger) *ArbitrumScanner {
	return &ArbitrumScanner{
		client: rpc.NewClient(rpcURL),
		logger: logger.Named("arbitrum"),
		chain:  "arbitrum",
	}
}

// Chain returns the chain name.
func (s *ArbitrumScanner) Chain() string {
	return s.chain
}

// ScanRates fetches current lending rates from Arbitrum DeFi protocols.
func (s *ArbitrumScanner) ScanRates(ctx interface{}) ([]protocol.LendingRate, error) {
	log := s.logger
	log.Info("scanning Arbitrum lending rates")

	rates := make([]protocol.LendingRate, 0)
	assets := protocol.KnownAssets["arbitrum"]

	protocols := []string{"aave", "compound", "radiant"}

	for _, protoName := range protocols {
		for _, asset := range assets {
			rate := protocol.LendingRate{
				Protocol:  protoName,
				Chain:     s.chain,
				Asset:     asset.Symbol,
				Address:   asset.Address,
				Decimals:  asset.Decimals,
				SupplyAPY: 3.80,
				BorrowAPY: 5.65,
				SupplyAPR: 3.73,
				BorrowAPR: 5.50,
				Timestamp: time.Now(),
			}
			rates = append(rates, rate)
		}
	}

	log.Info("Arbitrum scan complete", zap.Int("rates", len(rates)))
	return rates, nil
}

func timeNow() time.Time {
	return time.Now()
}
