package protocol

import (
	"testing"
)

func TestAggregator_MergeRates(t *testing.T) {
	tests := []struct {
		name     string
		input    []Rate
		wantLen  int
		wantErr  bool
	}{
		{
			name: "merge different protocols",
			input: []Rate{
				{Protocol: "aave", Chain: "ethereum", Asset: "USDC", SupplyAPY: 4.5},
				{Protocol: "compound", Chain: "ethereum", Asset: "USDC", SupplyAPY: 3.8},
			},
			wantLen: 2,
		},
		{
			name: "dedup same protocol chain asset",
			input: []Rate{
				{Protocol: "aave", Chain: "ethereum", Asset: "USDC", SupplyAPY: 4.5},
				{Protocol: "aave", Chain: "ethereum", Asset: "USDC", SupplyAPY: 4.6},
			},
			wantLen: 1,
		},
		{
			name:    "empty input",
			input:   []Rate{},
			wantLen: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			agg := NewAggregator()
			result := agg.MergeRates(tt.input)
			if len(result) != tt.wantLen {
				t.Errorf("MergeRates() got %d rates, want %d", len(result), tt.wantLen)
			}
		})
	}
}

func TestAggregator_SortBySupplyAPY(t *testing.T) {
	agg := NewAggregator()
	rates := []Rate{
		{Protocol: "aave", SupplyAPY: 3.0},
		{Protocol: "compound", SupplyAPY: 5.0},
		{Protocol: "morpho", SupplyAPY: 4.0},
	}

	sorted := agg.SortBySupplyAPY(rates)
	for i := 1; i < len(sorted); i++ {
		if sorted[i].SupplyAPY > sorted[i-1].SupplyAPY {
			t.Errorf("Not sorted: %f > %f at index %d", sorted[i].SupplyAPY, sorted[i-1].SupplyAPY, i)
		}
	}
}

func TestAggregator_FilterByChain(t *testing.T) {
	agg := NewAggregator()
	rates := []Rate{
		{Protocol: "aave", Chain: "ethereum", Asset: "USDC"},
		{Protocol: "aave", Chain: "arbitrum", Asset: "USDC"},
		{Protocol: "compound", Chain: "ethereum", Asset: "USDC"},
	}

	filtered := agg.FilterByChain(rates, "ethereum")
	if len(filtered) != 2 {
		t.Errorf("FilterByChain() got %d, want 2", len(filtered))
	}
}
