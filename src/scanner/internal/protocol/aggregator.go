package protocol

import (
	"sort"
	"sync"
	"time"

	"go.uber.org/zap"
)

// Aggregator collects and deduplicates lending rates from multiple chains.
type Aggregator struct {
	mu     sync.RWMutex
	rates  map[string]LendingRate // keyed by "protocol:chain:asset"
	logger *zap.Logger
}

// NewAggregator creates a new rate aggregator.
func NewAggregator(logger *zap.Logger) *Aggregator {
	return &Aggregator{
		rates:  make(map[string]LendingRate),
		logger: logger,
	}
}

// AddRates adds rates to the aggregator (keeps highest supply APY per asset).
func (a *Aggregator) AddRates(rates ...LendingRate) {
	a.mu.Lock()
	defer a.mu.Unlock()

	for _, rate := range rates {
		key := rateKey(rate)
		if existing, ok := a.rates[key]; ok {
			if rate.SupplyAPY > existing.SupplyAPY {
				a.rates[key] = rate
			}
		} else {
			a.rates[key] = rate
		}
	}
}

// ReplaceRates replaces all rates for a given chain.
func (a *Aggregator) ReplaceRates(chain string, rates ...LendingRate) {
	a.mu.Lock()
	defer a.mu.Unlock()

	// Remove old rates for this chain
	for key, rate := range a.rates {
		if rate.Chain == chain {
			delete(a.rates, key)
		}
	}

	// Add new rates
	for _, rate := range rates {
		key := rateKey(rate)
		a.rates[key] = rate
	}
}

// GetAllRates returns all aggregated rates sorted by protocol and asset.
func (a *Aggregator) GetAllRates() []LendingRate {
	a.mu.RLock()
	defer a.mu.RUnlock()

	result := make([]LendingRate, 0, len(a.rates))
	for _, rate := range a.rates {
		result = append(result, rate)
	}

	sort.Slice(result, func(i, j int) bool {
		if result[i].Protocol != result[j].Protocol {
			return result[i].Protocol < result[j].Protocol
		}
		if result[i].Chain != result[j].Chain {
			return result[i].Chain < result[j].Chain
		}
		return result[i].Asset < result[j].Asset
	})

	return result
}

// GetRatesByProtocol returns all rates for a specific protocol.
func (a *Aggregator) GetRatesByProtocol(protocol string) []LendingRate {
	a.mu.RLock()
	defer a.mu.RUnlock()

	var result []LendingRate
	for _, rate := range a.rates {
		if rate.Protocol == protocol {
			result = append(result, rate)
		}
	}
	return result
}

// GetRatesByChain returns all rates for a specific chain.
func (a *Aggregator) GetRatesByChain(chain string) []LendingRate {
	a.mu.RLock()
	defer a.mu.RUnlock()

	var result []LendingRate
	for _, rate := range a.rates {
		if rate.Chain == chain {
			result = append(result, rate)
		}
	}
	return result
}

// GetBestSupplyRate returns the highest supply APY for a given asset across all protocols.
func (a *Aggregator) GetBestSupplyRate(asset string) *LendingRate {
	a.mu.RLock()
	defer a.mu.RUnlock()

	var best *LendingRate
	for _, rate := range a.rates {
		if rate.Asset == asset {
			if best == nil || rate.SupplyAPY > best.SupplyAPY {
				r := rate
				best = &r
			}
		}
	}
	return best
}

// Count returns the total number of unique rates.
func (a *Aggregator) Count() int {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return len(a.rates)
}

// StaleRateCount returns the number of rates older than the given duration.
func (a *Aggregator) StaleRateCount(maxAge time.Duration) int {
	a.mu.RLock()
	defer a.mu.RUnlock()

	count := 0
	cutoff := time.Now().Add(-maxAge)
	for _, rate := range a.rates {
		if rate.Timestamp.Before(cutoff) {
			count++
		}
	}
	return count
}

func rateKey(rate LendingRate) string {
	return rate.Protocol + ":" + rate.Chain + ":" + rate.Asset
}
