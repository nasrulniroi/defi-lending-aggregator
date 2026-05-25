// Package protocol defines rate types and aggregation for the scanner.
package protocol

import "time"

// RateType represents the type of lending rate.
type RateType string

const (
	RateTypeSupply   RateType = "supply"
	RateTypeBorrow   RateType = "borrow_variable"
	RateTypeBorrowSt RateType = "borrow_stable"
)

// LendingRate represents a single lending rate data point.
type LendingRate struct {
	Protocol    string    `json:"protocol"`
	Chain       string    `json:"chain"`
	Asset       string    `json:"asset"`
	Address     string    `json:"address"`
	Decimals    int       `json:"decimals"`
	SupplyAPY   float64   `json:"supply_apy"`
	BorrowAPY   float64   `json:"borrow_apy"`
	SupplyAPR   float64   `json:"supply_apr"`
	BorrowAPR   float64   `json:"borrow_apr"`
	TotalSupply float64   `json:"total_supply"`
	TotalBorrow float64   `json:"total_borrow"`
	Utilization float64   `json:"utilization"`
	Timestamp   time.Time `json:"timestamp"`
	BlockNumber uint64    `json:"block_number"`
}

// ChainConfig holds configuration for a specific chain.
type ChainConfig struct {
	Name          string `yaml:"name"`
	ChainID       int    `yaml:"chain_id"`
	RPCURL        string `yaml:"rpc_url"`
	ExplorerURL   string `yaml:"explorer_url"`
	BlockTime     float64 `yaml:"block_time"`
	NativeToken   string `yaml:"native_token"`
	WrappedNative string `yaml:"wrapped_native"`
}

// ProtocolConfig holds contract addresses for a protocol on a chain.
type ProtocolConfig struct {
	Name      string            `yaml:"name"`
	Version   string            `yaml:"version"`
	Contracts map[string]string `yaml:"contracts"`
}

// AssetInfo describes a token on a specific chain.
type AssetInfo struct {
	Symbol   string `json:"symbol"`
	Address  string `json:"address"`
	Decimals int    `json:"decimals"`
}

// KnownAssets maps chain names to their well-known token lists.
var KnownAssets = map[string][]AssetInfo{
	"ethereum": {
		{Symbol: "USDC", Address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", Decimals: 6},
		{Symbol: "USDT", Address: "0xdAC17F958D2ee523a2206206994597C13D831ec7", Decimals: 6},
		{Symbol: "DAI", Address: "0x6B175474E89094C44Da98b954EedeAC495271d0F", Decimals: 18},
		{Symbol: "WETH", Address: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", Decimals: 18},
		{Symbol: "WBTC", Address: "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", Decimals: 8},
	},
	"arbitrum": {
		{Symbol: "USDC", Address: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", Decimals: 6},
		{Symbol: "USDT", Address: "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9", Decimals: 6},
		{Symbol: "WETH", Address: "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", Decimals: 18},
	},
	"polygon": {
		{Symbol: "USDC", Address: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", Decimals: 6},
		{Symbol: "USDT", Address: "0xc2132D05D31c914a87C6611C10748AEb04B58e8F", Decimals: 6},
		{Symbol: "WETH", Address: "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619", Decimals: 18},
	},
	"base": {
		{Symbol: "USDC", Address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", Decimals: 6},
		{Symbol: "WETH", Address: "0x4200000000000000000000000000000000000006", Decimals: 18},
	},
	"avalanche": {
		{Symbol: "USDC", Address: "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E", Decimals: 6},
		{Symbol: "USDT", Address: "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7", Decimals: 6},
		{Symbol: "WETH", Address: "0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB", Decimals: 18},
		{Symbol: "WAVAX", Address: "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", Decimals: 18},
	},
}
