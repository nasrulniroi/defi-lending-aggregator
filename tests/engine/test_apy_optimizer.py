"""Tests for the APY optimizer module."""
import pytest
from src.engine.apy_optimizer import ApyOptimizer
from src.engine.models.lending_rate import LendingRate


@pytest.fixture
def optimizer():
    return ApyOptimizer()


@pytest.fixture
def sample_rates():
    return [
        LendingRate(protocol="Aave", chain="ethereum", asset="USDC", supply_apy=4.5, borrow_apy=6.2, total_supply=1e9, total_borrow=5e8, utilization_rate=0.5),
        LendingRate(protocol="Compound", chain="base", asset="USDC", supply_apy=6.2, borrow_apy=8.9, total_supply=1.2e8, total_borrow=7.2e7, utilization_rate=0.6),
        LendingRate(protocol="Spark", chain="ethereum", asset="USDC", supply_apy=5.0, borrow_apy=6.8, total_supply=6.7e8, total_borrow=3.8e8, utilization_rate=0.57),
        LendingRate(protocol="Aave", chain="ethereum", asset="WETH", supply_apy=2.9, borrow_apy=4.2, total_supply=8.9e8, total_borrow=4.2e8, utilization_rate=0.47),
        LendingRate(protocol="Morpho", chain="ethereum", asset="WETH", supply_apy=3.1, borrow_apy=4.6, total_supply=3.2e8, total_borrow=1.5e8, utilization_rate=0.47),
    ]


class TestApyOptimizer:
    """Test suite for ApyOptimizer."""

    def test_find_opportunities_returns_list(self, optimizer, sample_rates):
        """find_opportunities should return a list of opportunities."""
        opps = optimizer.find_opportunities(sample_rates)
        assert isinstance(opps, list)

    def test_opportunity_has_positive_net_apy(self, optimizer, sample_rates):
        """All returned opportunities should have positive net APY."""
        opps = optimizer.find_opportunities(sample_rates)
        for opp in opps:
            assert opp.net_apy > 0

    def test_opportunities_sorted_by_net_apy(self, optimizer, sample_rates):
        """Opportunities should be sorted by net APY descending."""
        opps = optimizer.find_opportunities(sample_rates)
        if len(opps) > 1:
            for i in range(len(opps) - 1):
                assert opps[i].net_apy >= opps[i + 1].net_apy

    def test_same_asset_different_protocols(self, optimizer, sample_rates):
        """Opportunities should borrow and supply on different protocols."""
        opps = optimizer.find_opportunities(sample_rates)
        for opp in opps:
            assert opp.supply_protocol != opp.borrow_protocol or opp.supply_chain != opp.borrow_chain

    def test_empty_rates_no_opportunities(self, optimizer):
        """Empty rates should yield no opportunities."""
        opps = optimizer.find_opportunities([])
        assert opps == []
