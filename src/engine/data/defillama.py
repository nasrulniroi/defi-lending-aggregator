"""DeFiLlama API client for TVL and protocol metadata.

Fetches aggregated protocol data from the DeFiLlama API including
TVL, chain breakdowns, and protocol metadata.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

DEFILLAMA_BASE_URL = "https://api.llama.fi"
REQUEST_TIMEOUT = 15


class DeFiLlamaClient:
    """Client for the DeFiLlama API.

    Provides methods to fetch TVL data, protocol metadata, and
    historical metrics from DeFiLlama.

    Attributes:
        base_url: API base URL.
        cache_ttl: Cache time-to-live for responses.
    """

    def __init__(
        self,
        base_url: str = DEFILLAMA_BASE_URL,
        cache_ttl: int = 300,
    ) -> None:
        """Initialize DeFiLlama client.

        Args:
            base_url: API base URL override.
            cache_ttl: Cache TTL in seconds.
        """
        self.base_url = base_url
        self.cache_ttl = cache_ttl
        self._cache: dict[str, tuple[datetime, dict]] = {}

    async def get_protocol_tvl(self, protocol_slug: str) -> Optional[float]:
        """Get current TVL for a protocol.

        Args:
            protocol_slug: DeFiLlama protocol slug (e.g., 'aave-v3').

        Returns:
            TVL in USD, or None if unavailable.
        """
        data = await self._fetch(f"/protocol/{protocol_slug}")
        if data is None:
            return None
        return data.get("tvl", 0.0)

    async def get_protocol_chains(self, protocol_slug: str) -> dict[str, float]:
        """Get TVL breakdown by chain for a protocol.

        Args:
            protocol_slug: DeFiLlama protocol slug.

        Returns:
            Dictionary mapping chain name to TVL in USD.
        """
        data = await self._fetch(f"/protocol/{protocol_slug}")
        if data is None:
            return {}

        chain_tvls = data.get("chainTvls", {})
        return {chain: tvl for chain, tvl in chain_tvls.items()}

    async def get_all_lending_protocols(self) -> list[dict]:
        """Get all lending protocol data from DeFiLlama.

        Returns:
            List of protocol data dictionaries.
        """
        data = await self._fetch("/protocols")
        if data is None:
            return []

        lending_protocols = [
            p for p in data
            if "Lending" in p.get("category", "")
        ]
        return lending_protocols

    async def get_historical_tvl(
        self, protocol_slug: str, days: int = 30
    ) -> list[dict]:
        """Get historical TVL data for a protocol.

        Args:
            protocol_slug: DeFiLlama protocol slug.
            days: Number of days of history.

        Returns:
            List of {date, tvl} dicts.
        """
        data = await self._fetch(f"/protocol/{protocol_slug}")
        if data is None:
            return []

        tvl_history = data.get("tvl", [])
        if isinstance(tvl_history, list):
            cutoff = datetime.utcnow() - timedelta(days=days)
            return [
                {"date": entry.get("date"), "tvl": entry.get("totalLiquidityUSD")}
                for entry in tvl_history
                if datetime.utcfromtimestamp(entry.get("date", 0)) > cutoff
            ]
        return []

    async def _fetch(self, endpoint: str) -> Optional[dict]:
        """Fetch data from DeFiLlama API with caching.

        Args:
            endpoint: API endpoint path.

        Returns:
            Response data dict or None on failure.
        """
        # Check cache
        cache_key = endpoint
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if (datetime.utcnow() - cached_time).total_seconds() < self.cache_ttl:
                return cached_data

        try:
            url = f"{self.base_url}{endpoint}"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as resp:
                    if resp.status != 200:
                        logger.error(
                            "DeFiLlama API error: %d %s", resp.status, endpoint
                        )
                        return None
                    data = await resp.json()
                    self._cache[cache_key] = (datetime.utcnow(), data)
                    return data
        except Exception as exc:
            logger.error("DeFiLlama fetch failed for %s: %s", endpoint, exc)
            return None
