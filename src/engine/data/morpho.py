"""Morpho Blue protocol rate fetcher.

Fetches peer-to-peer and pool lending rates from Morpho Blue markets.
"""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

import aiohttp

from engine.models.lending_rate import Asset, AssetCategory, LendingRate
from engine.models.protocol import Protocol

logger = logging.getLogger(__name__)

# Morpho Blue market identifiers
MORPHO_MARKETS = {
    "ethereum": [
        {
            "id": "weth-usdc",
            "collateral": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "loan": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "symbol": "USDC",
            "decimals": 6,
            "category": AssetCategory.STABLECOIN,
        },
        {
            "id": "weth-wsteth",
            "collateral": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
            "loan": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "symbol": "WETH",
            "decimals": 18,
            "category": AssetCategory.WRAPPED,
        },
    ],
    "base": [
        {
            "id": "weth-usdbc",
            "collateral": "0x4200000000000000000000000000000000000006",
            "loan": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
            "symbol": "USDbC",
            "decimals": 6,
            "category": AssetCategory.STABLECOIN,
        },
    ],
}


class MorphoFetcher:
    """Fetches lending rates from Morpho Blue markets.

    Morpho Blue uses a peer-to-peer matching layer on top of a base
    lending pool, often offering better rates than the underlying pool.

    Attributes:
        protocol: Morpho protocol configuration.
        chain: Target chain identifier.
        rpc_url: Chain RPC endpoint.
    """

    def __init__(self, protocol: Protocol, chain: str) -> None:
        """Initialize Morpho fetcher.

        Args:
            protocol: Morpho protocol configuration.
            chain: Chain to fetch from.
        """
        self.protocol = protocol
        self.chain = chain
        env_key = f"{chain.upper()}_RPC_URL"
        self.rpc_url = os.environ.get(env_key, "")

    async def fetch(self) -> list[LendingRate]:
        """Fetch current rates from Morpho Blue markets.

        Returns:
            List of LendingRate objects.
        """
        if not self.rpc_url:
            logger.warning("No RPC URL for chain %s", self.chain)
            return []

        markets = MORPHO_MARKETS.get(self.chain, [])
        if not markets:
            return []

        rates = []
        async with aiohttp.ClientSession() as session:
            for market_config in markets:
                try:
                    rate = await self._fetch_market(session, market_config)
                    if rate is not None:
                        rates.append(rate)
                except Exception as exc:
                    logger.error(
                        "Failed to fetch Morpho market %s: %s",
                        market_config["id"], exc,
                    )

        logger.info("Fetched %d Morpho rates on %s", len(rates), self.chain)
        return rates

    async def _fetch_market(
        self,
        session: aiohttp.ClientSession,
        market_config: dict,
    ) -> Optional[LendingRate]:
        """Fetch rate data for a single Morpho market.

        Args:
            session: HTTP session.
            market_config: Market configuration.

        Returns:
            LendingRate or None.
        """
        try:
            morpho_blue = self.protocol.contracts.get(
                self.chain, {}
            ).get("morpho_blue", "")
            if not morpho_blue:
                return None

            rate_data = await self._fetch_market_data(
                session, morpho_blue, market_config
            )
            if rate_data is None:
                return None

            asset = Asset(
                symbol=market_config["symbol"],
                address=market_config["loan"],
                decimals=market_config["decimals"],
                chain=self.chain,
                category=market_config["category"],
            )

            return LendingRate(
                protocol="morpho",
                chain=self.chain,
                asset=asset,
                supply_apy=rate_data["supply_apy"],
                borrow_apy=rate_data["borrow_apy"],
                supply_apr=rate_data["supply_apr"],
                borrow_apr=rate_data["borrow_apr"],
                total_supply=rate_data["total_supply"],
                total_borrow=rate_data["total_borrow"],
                utilization=rate_data["utilization"],
                timestamp=datetime.utcnow(),
            )
        except Exception as exc:
            logger.error("Morpho market fetch error: %s", exc)
            return None

    async def _fetch_market_data(
        self,
        session: aiohttp.ClientSession,
        morpho_address: str,
        market_config: dict,
    ) -> Optional[dict]:
        """Fetch market data from Morpho Blue contract.

        Args:
            session: HTTP session.
            morpho_address: Morpho Blue contract address.
            market_config: Market configuration.

        Returns:
            Rate data dict or None.
        """
        try:
            # In production: call market(bytes32) on Morpho Blue
            # to get market balances, then compute rates from the
            # interest rate model
            # Simulated data for demo:
            return {
                "supply_apy": 5.82,
                "borrow_apy": 7.15,
                "supply_apr": 5.65,
                "borrow_apr": 6.92,
                "total_supply": 120_000_000,
                "total_borrow": 78_000_000,
                "utilization": 65.0,
            }
        except Exception as exc:
            logger.error("Morpho data fetch failed: %s", exc)
            return None
