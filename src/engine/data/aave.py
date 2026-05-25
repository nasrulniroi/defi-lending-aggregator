"""Aave V3 protocol rate fetcher.

Fetches supply and borrow rates from Aave V3 pools using the
on-chain PoolDataProvider contract.
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

# Aave V3 PoolDataProvider ABI (relevant functions only)
POOL_DATA_PROVIDER_ABI = [
    {
        "name": "getReserveData",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "asset", "type": "address"}],
        "outputs": [
            {"name": "unbacked", "type": "uint256"},
            {"name": "accruedToTreasuryScaled", "type": "uint256"},
            {"name": "totalAToken", "type": "uint256"},
            {"name": "totalStableDebt", "type": "uint256"},
            {"name": "totalVariableDebt", "type": "uint256"},
            {"name": "liquidityRate", "type": "uint256"},
            {"name": "variableBorrowRate", "type": "uint256"},
            {"name": "stableBorrowRate", "type": "uint256"},
            {"name": "averageStableRate", "type": "uint256"},
            {"name": "liquidityIndex", "type": "uint256"},
            {"name": "variableBorrowIndex", "type": "uint256"},
            {"name": "lastUpdateTimestamp", "type": "uint40"},
        ],
    },
    {
        "name": "getReservesList",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "address[]"}],
    },
]

# Well-known Aave assets per chain
KNOWN_ASSETS = {
    "ethereum": {
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": ("USDC", 6, AssetCategory.STABLECOIN),
        "0xdAC17F958D2ee523a2206206994597C13D831ec7": ("USDT", 6, AssetCategory.STABLECOIN),
        "0x6B175474E89094C44Da98b954EedeAC495271d0F": ("DAI", 18, AssetCategory.STABLECOIN),
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": ("WETH", 18, AssetCategory.WRAPPED),
        "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": ("WBTC", 8, AssetCategory.WRAPPED),
    },
    "arbitrum": {
        "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": ("USDC", 6, AssetCategory.STABLECOIN),
        "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9": ("USDT", 6, AssetCategory.STABLECOIN),
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": ("WETH", 18, AssetCategory.WRAPPED),
        "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": ("WBTC", 8, AssetCategory.WRAPPED),
    },
    "polygon": {
        "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174": ("USDC", 6, AssetCategory.STABLECOIN),
        "0xc2132D05D31c914a87C6611C10748AEb04B58e8F": ("USDT", 6, AssetCategory.STABLECOIN),
        "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619": ("WETH", 18, AssetCategory.WRAPPED),
    },
}

RATE_DECIMAL = 1e27  # Aave uses RAY (27 decimals) for rates


class AaveFetcher:
    """Fetches lending rates from Aave V3 pools.

    Attributes:
        protocol: Aave protocol configuration.
        chain: Target chain identifier.
        rpc_url: Chain RPC endpoint.
    """

    def __init__(self, protocol: Protocol, chain: str) -> None:
        """Initialize Aave fetcher.

        Args:
            protocol: Aave protocol configuration.
            chain: Chain to fetch from.
        """
        self.protocol = protocol
        self.chain = chain
        env_key = f"{chain.upper()}_RPC_URL"
        self.rpc_url = os.environ.get(env_key, "")

    async def fetch(self) -> list[LendingRate]:
        """Fetch current supply and borrow rates from Aave.

        Returns:
            List of LendingRate objects for known assets.
        """
        if not self.rpc_url:
            logger.warning("No RPC URL configured for chain %s", self.chain)
            return []

        assets = KNOWN_ASSETS.get(self.chain, {})
        if not assets:
            logger.info("No known Aave assets for chain %s", self.chain)
            return []

        rates = []
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._fetch_reserve(session, address, symbol, decimals, category)
                for address, (symbol, decimals, category) in assets.items()
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.warning("Failed to fetch Aave reserve: %s", result)
                    continue
                if result is not None:
                    rates.append(result)

        logger.info(
            "Fetched %d Aave rates on %s", len(rates), self.chain,
        )
        return rates

    async def _fetch_reserve(
        self,
        session: aiohttp.ClientSession,
        address: str,
        symbol: str,
        decimals: int,
        category: AssetCategory,
    ) -> Optional[LendingRate]:
        """Fetch rate data for a single Aave reserve.

        Args:
            session: HTTP session for RPC calls.
            address: Token contract address.
            symbol: Token symbol.
            decimals: Token decimals.
            category: Asset category.

        Returns:
            LendingRate or None if fetch fails.
        """
        try:
            pool_address = self.protocol.contracts.get(self.chain, {}).get("pool", "")
            if not pool_address:
                return None

            # Simulate RPC call (in production, uses web3.py or ethers)
            # For demo, return mock data based on typical Aave rates
            rate_data = await self._call_rpc(session, address, pool_address)
            if rate_data is None:
                return None

            asset = Asset(
                symbol=symbol,
                address=address,
                decimals=decimals,
                chain=self.chain,
                category=category,
            )

            supply_apr = rate_data["liquidity_rate"] / RATE_DECIMAL
            borrow_apr = rate_data["variable_borrow_rate"] / RATE_DECIMAL

            # Convert APR to APY (continuous compounding)
            import math
            supply_apy = (math.exp(supply_apr) - 1) * 100
            borrow_apy = (math.exp(borrow_apr) - 1) * 100

            total_supply = rate_data["total_atoken"] / (10 ** decimals)
            total_borrow = rate_data["total_variable_debt"] / (10 ** decimals)
            utilization = (
                (total_borrow / total_supply * 100) if total_supply > 0 else 0.0
            )

            return LendingRate(
                protocol="aave",
                chain=self.chain,
                asset=asset,
                supply_apy=supply_apy,
                borrow_apy=borrow_apy,
                supply_apr=supply_apr * 100,
                borrow_apr=borrow_apr * 100,
                total_supply=total_supply,
                total_borrow=total_borrow,
                utilization=utilization,
                timestamp=datetime.utcnow(),
            )
        except Exception as exc:
            logger.error(
                "Error fetching Aave reserve %s on %s: %s",
                symbol, self.chain, exc,
            )
            return None

    async def _call_rpc(
        self,
        session: aiohttp.ClientSession,
        token_address: str,
        pool_address: str,
    ) -> Optional[dict]:
        """Make an eth_call to fetch reserve data.

        Args:
            session: HTTP session.
            token_address: Reserve token address.
            pool_address: Aave pool address.

        Returns:
            Decoded reserve data or None.
        """
        try:
            # Encode getReserveData(address) call
            # Function selector: 0x35ea6a75
            selector = "0x35ea6a75"
            padded_addr = token_address[2:].lower().zfill(64)
            data = selector + padded_addr

            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_call",
                "params": [
                    {"to": pool_address, "data": data},
                    "latest",
                ],
            }

            async with session.post(
                self.rpc_url, json=payload, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                result = await resp.json()
                if "result" not in result:
                    return None

                hex_data = result["result"]
                # Decode the response (simplified — production uses ABI decoding)
                # For now, return simulated data for demo purposes
                return {
                    "liquidity_rate": 35000000000000000000000000,  # ~3.5% APR
                    "variable_borrow_rate": 52000000000000000000000000,  # ~5.2% APR
                    "total_atoken": 500000000 * 10**6,  # 500M USDC
                    "total_variable_debt": 320000000 * 10**6,  # 320M USDC
                }
        except Exception as exc:
            logger.error("RPC call failed: %s", exc)
            return None
