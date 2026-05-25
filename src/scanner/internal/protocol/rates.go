package protocol

import (
	"encoding/json"
	"fmt"
	"strings"
)

// RateJSON represents the JSON structure for rate API responses.
type RateJSON struct {
	Protocol    string  `json:"protocol"`
	Chain       string  `json:"chain"`
	Asset       string  `json:"asset"`
	SupplyAPY   float64 `json:"supply_apy"`
	BorrowAPY   float64 `json:"borrow_apy"`
	Utilization float64 `json:"utilization"`
}

// FormatRates returns a formatted string representation of rates.
func FormatRates(rates []LendingRate) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("%-12s %-12s %-8s %10s %10s %10s\n",
		"Protocol", "Chain", "Asset", "Supply APY", "Borrow APY", "Util%"))
	sb.WriteString(strings.Repeat("-", 65) + "\n")

	for _, r := range rates {
		sb.WriteString(fmt.Sprintf("%-12s %-12s %-8s %9.2f%% %9.2f%% %9.1f%%\n",
			r.Protocol, r.Chain, r.Asset,
			r.SupplyAPY, r.BorrowAPY, r.Utilization))
	}
	return sb.String()
}

// ToJSON serializes rates to JSON bytes.
func ToJSON(rates []LendingRate) ([]byte, error) {
	return json.MarshalIndent(rates, "", "  ")
}

// FilterByMinAPY returns rates above a minimum supply APY threshold.
func FilterByMinAPY(rates []LendingRate, minAPY float64) []LendingRate {
	var filtered []LendingRate
	for _, r := range rates {
		if r.SupplyAPY >= minAPY {
			filtered = append(filtered, r)
		}
	}
	return filtered
}

// FilterByAsset returns rates for a specific asset symbol.
func FilterByAsset(rates []LendingRate, asset string) []LendingRate {
	var filtered []LendingRate
	for _, r := range rates {
		if strings.EqualFold(r.Asset, asset) {
			filtered = append(filtered, r)
		}
	}
	return filtered
}

// GroupByAsset groups rates by asset symbol.
func GroupByAsset(rates []LendingRate) map[string][]LendingRate {
	grouped := make(map[string][]LendingRate)
	for _, r := range rates {
		grouped[r.Asset] = append(grouped[r.Asset], r)
	}
	return grouped
}
