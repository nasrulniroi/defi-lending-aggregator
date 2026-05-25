"""Compound V3 (Comet) rate fetcher.

Fetches supply and borrow rates from Compound V3 markets.
"""

from __future__ import annotations

import asyncio
import logging
import math
import os
from datetime import datetime
from typing import Optional

import aiohttp

from engine.models.lending_rate import Asset, AssetCategory, LendingRate
from engine.models.protocol import Protocol

logger = logging.getLogger(__name__)

# Compound V3 base token addresses
COMET_MARKETS = {
    "ethereum": {
        "USDC": {
            "comet": "0xc3d688B66703497DAA19211EEdff47f25384cdc3",
            "base_token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "decimals": 6,
        },
    },
    "arbitrum": {
        "USDC": {
            "comet": "0xA5EDBDD9646f8dFF606d7448e414884C7d905dCA",
            "base_token": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "decimals": 6,
        },
    },
    "base": {
        "USDC": {
            "comet": "0xb125E6687d4313864e53df431d5425969c15Eb2F",
            "base_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "decimals": 6,
        },
    },
}

# Compound uses a different rate scaling
SECONDS_PER_YEAR = 365.25 * 24 * 3600


class CompoundFetcher:
    """Fetches lending rates from Compound V3 Comet markets.

    Attributes:
        protocol: Compound protocol configuration.
        chain: Target chain identifier.
        rpc_url: Chain RPC endpoint.
    """

    def __init__(self, protocol: Protocol, chain: str) -> None:
        """Initialize Compound fetcher.

        Args:
            protocol: Compound protocol configuration.
            chain: Chain to fetch from.
        """
        self.protocol = protocol
        self.chain = chain
        env_key = f"{chain.upper()}_RPC_URL"
        self.rpc_url = os.environ.get(env_key, "")

    async def fetch(self) -> list[LendingRate]:
        """Fetch current supply and borrow rates from Compound V3.

        Returns:
            List of LendingRate objects for Compound markets.
        """
        if not self.rpc_url:
            logger.warning("No RPC URL configured for chain %s", self.chain)
            return []

        markets = COMET_MARKETS.get(self.chain, {})
        if not markets:
            return []

        rates = []
        async with aiohttp.ClientSession() as session:
            for symbol, market_config in markets.items():
                try:
                    rate = await self._fetch_market(
                        session, symbol, market_config
                    )
                    if rate is not None:
                        rates.append(rate)
                except Exception as exc:
                    logger.error(
                        "Failed to fetch Compound %s on %s: %s",
                        symbol, self.chain, exc,
                    )

        logger.info("Fetched %d Compound rates on %s", len(rates), self.chain)
        return rates

    async def _fetch_market(
        self,
        session: aiohttp.ClientSession,
        symbol: str,
        market_config: dict,
    ) -> Optional[LendingRate]:
        """Fetch rate data for a single Compound market.

        Args:
            session: HTTP session for RPC calls.
            symbol: Base token symbol.
            market_config: Market configuration dict.

        Returns:
            LendingRate object or None.
        """
        comet_address = market_config["comet"]
        decimals = market_config["decimals"]

        # Fetch utilization and rates from Comet contract
        rate_data = await self._call_comet(session, comet_address)
        if rate_data is None:
            return None

        asset = Asset(
            symbol=symbol,
            address=market_config["base_token"],
            decimals=decimals,
            chain=self.chain,
            category=AssetCategory.STABLECOIN,
        )

        # Compound V3 supply APY = base rate + utilization * slope
        supply_apy = rate_data.get("supply_apy", 0.0)
        borrow_apy = rate_data.get("borrow_apy", 0.0)

        total_supply = rate_data.get("total_supply", 0.0) / (10 ** decimals)
        total_borrow = rate_data.get("total_borrow", 0.0) / (10 ** decimals)

        return LendingRate(
            protocol="compound",
            chain=self.chain,
            asset=asset,
            supply_apy=supply_apy,
            borrow_apy=borrow_apy,
            supply_apr=supply_apy * 0.95,  # Approximate APR
            borrow_apr=borrow_apy * 0.95,
            total_supply=total_supply,
            total_borrow=total_borrow,
            utilization=rate_data.get("utilization", 0.0),
            timestamp=datetime.utcnow(),
        )

    async def _call_comet(
        self, session: aiohttp.ClientSession, comet_address: str
    ) -> Optional[dict]:
        """Fetch data from Compound Comet contract.

        Args:
            session: HTTP session.
            comet_address: Comet contract address.

        Returns:
            Rate data dict or None.
        """
        try:
            # In production, multiple eth_calls for:
            # - totalSupply(), totalBorrow(), getUtilization()
            # - supplyRate(), borrowRate()
            # Simulated data for demo:
            return {
                "supply_apy": 4.12,
                "borrow_apy": 6.35,
                "total_supply": 800_000_000 * 10**6,
                "total_borrow": 520_000_000 * 10**6,
                "utilization": 65.0,
            }
        except Exception as exc:
            logger.error("Comet call failed: %s", exc)
            return None
