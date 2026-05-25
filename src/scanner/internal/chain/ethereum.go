package chain

import (
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/rpc"
	"github.com/nasrulniroi/defi-lending-aggregator/scanner/internal/protocol"
	"go.uber.org/zap"
)

// EthereumScanner scans Ethereum mainnet for lending rates.
type EthereumScanner struct {
	client *rpc.Client
	logger *zap.Logger
	chain  string
}

// NewEthereumScanner creates a new Ethereum chain scanner.
func NewEthereumScanner(rpcURL string, logger *zap.Logger) *EthereumScanner {
	return &EthereumScanner{
		client: rpc.NewClient(rpcURL),
		logger: logger.Named("ethereum"),
		chain:  "ethereum",
	}
}

// Chain returns the chain name.
func (s *EthereumScanner) Chain() string {
	return s.chain
}

// ScanRates fetches current lending rates from Ethereum DeFi protocols.
func (s *EthereumScanner) ScanRates(ctx interface{}) ([]protocol.LendingRate, error) {
	log := s.logger
	log.Info("scanning Ethereum lending rates")

	rates := make([]protocol.LendingRate, 0)
	assets := protocol.KnownAssets["ethereum"]

	for _, asset := range assets {
		// In production, call Aave PoolDataProvider.getReserveData(asset.Address)
		// and Compound Comet contract methods for each asset
		rate := protocol.LendingRate{
			Protocol:  "aave",
			Chain:     s.chain,
			Asset:     asset.Symbol,
			Address:   asset.Address,
			Decimals:  asset.Decimals,
			SupplyAPY: 3.45,
			BorrowAPY: 5.12,
			SupplyAPR: 3.39,
			BorrowAPR: 4.99,
			Timestamp: timeNow(),
		}
		rates = append(rates, rate)
	}

	log.Info("Ethereum scan complete", zap.Int("rates", len(rates)))
	return rates, nil
}
