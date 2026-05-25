"""Tests for the rate fetcher module."""
import pytest
from unittest.mock import AsyncMock, patch
from src.engine.rate_fetcher import RateFetcher
from src.engine.models.lending_rate import LendingRate


@pytest.fixture
def fetcher():
    return RateFetcher()


class TestRateFetcher:
    """Test suite for RateFetcher."""

    @pytest.mark.asyncio
    async def test_fetch_all_rates_returns_list(self, fetcher):
        """fetch_all_rates should return a list of LendingRate objects."""
        with patch.object(fetcher, "_fetch_protocol_rates", new_callable=AsyncMock, return_value=[]):
            rates = await fetcher.fetch_all_rates()
            assert isinstance(rates, list)

    @pytest.mark.asyncio
    async def test_fetch_by_protocol_filters(self, fetcher):
        """fetch_by_protocol should only return rates for the specified protocol."""
        mock_rates = [
            LendingRate(protocol="Aave", chain="ethereum", asset="USDC", supply_apy=4.5, borrow_apy=6.2, total_supply=1e9, total_borrow=5e8, utilization_rate=0.5),
            LendingRate(protocol="Compound", chain="ethereum", asset="USDC", supply_apy=3.8, borrow_apy=5.5, total_supply=8e8, total_borrow=4e8, utilization_rate=0.5),
        ]
        with patch.object(fetcher, "fetch_all_rates", new_callable=AsyncMock, return_value=mock_rates):
            rates = await fetcher.fetch_by_protocol("Aave")
            assert len(rates) == 1
            assert rates[0].protocol == "Aave"

    @pytest.mark.asyncio
    async def test_fetch_by_chain_filters(self, fetcher):
        """fetch_by_chain should only return rates for the specified chain."""
        mock_rates = [
            LendingRate(protocol="Aave", chain="ethereum", asset="USDC", supply_apy=4.5, borrow_apy=6.2, total_supply=1e9, total_borrow=5e8, utilization_rate=0.5),
            LendingRate(protocol="Aave", chain="arbitrum", asset="USDC", supply_apy=5.1, borrow_apy=7.4, total_supply=3e8, total_borrow=1.5e8, utilization_rate=0.5),
        ]
        with patch.object(fetcher, "fetch_all_rates", new_callable=AsyncMock, return_value=mock_rates):
            rates = await fetcher.fetch_by_chain("arbitrum")
            assert len(rates) == 1
            assert rates[0].chain == "arbitrum"

    @pytest.mark.asyncio
    async def test_empty_rates_on_error(self, fetcher):
        """Should return empty list when all fetchers fail."""
        with patch.object(fetcher, "_fetch_protocol_rates", new_callable=AsyncMock, side_effect=Exception("API down")):
            rates = await fetcher.fetch_all_rates()
            assert rates == []

    def test_lending_rate_model(self):
        """LendingRate model should calculate spread correctly."""
        rate = LendingRate(
            protocol="Aave", chain="ethereum", asset="USDC",
            supply_apy=4.5, borrow_apy=6.2,
            total_supply=1e9, total_borrow=5e8, utilization_rate=0.5,
        )
        assert rate.spread == pytest.approx(1.7)
