"""Redis-backed rate cache for deduplication and performance.

Provides async caching layer for lending rate data with configurable
TTL and cache invalidation strategies.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional

from engine.models.lending_rate import Asset, AssetCategory, LendingRate

logger = logging.getLogger(__name__)


class RateCache:
    """Cache for lending rate data backed by Redis.

    Stores serialized rate data with TTL-based expiration to avoid
    redundant protocol API calls and reduce latency.

    Attributes:
        redis_url: Redis connection URL.
        prefix: Key prefix for namespacing.
        default_ttl: Default cache TTL in seconds.
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        prefix: str = "defi:rates:",
        default_ttl: int = 60,
    ) -> None:
        """Initialize rate cache.

        Args:
            redis_url: Redis connection URL.
            prefix: Cache key prefix.
            default_ttl: Default TTL in seconds.
        """
        self.redis_url = redis_url
        self.prefix = prefix
        self.default_ttl = default_ttl
        self._local_cache: dict[str, tuple[datetime, list[LendingRate]]] = {}
        self._local_ttl = 30  # Local cache TTL in seconds

    async def get_rates(
        self, protocol: str, chain: str
    ) -> Optional[list[LendingRate]]:
        """Get cached rates for a protocol/chain combination.

        Args:
            protocol: Protocol identifier.
            chain: Chain identifier.

        Returns:
            List of cached LendingRate objects, or None if cache miss.
        """
        cache_key = f"{protocol}:{chain}"

        # Check local in-memory cache first
        if cache_key in self._local_cache:
            cached_time, cached_rates = self._local_cache[cache_key]
            age = (datetime.utcnow() - cached_time).total_seconds()
            if age < self._local_ttl:
                logger.debug(
                    "Local cache hit for %s (%.1fs old)", cache_key, age
                )
                return cached_rates

        # In production, check Redis
        # redis = await aioredis.from_url(self.redis_url)
        # data = await redis.get(f"{self.prefix}{cache_key}")
        # if data:
        #     return self._deserialize(json.loads(data))

        return None

    async def set_rates(
        self,
        protocol: str,
        chain: str,
        rates: list[LendingRate],
        ttl: Optional[int] = None,
    ) -> None:
        """Cache rates for a protocol/chain combination.

        Args:
            protocol: Protocol identifier.
            chain: Chain identifier.
            rates: List of LendingRate objects to cache.
            ttl: Optional TTL override in seconds.
        """
        cache_key = f"{protocol}:{chain}"

        # Update local cache
        self._local_cache[cache_key] = (datetime.utcnow(), rates)

        # In production, store in Redis
        # redis = await aioredis.from_url(self.redis_url)
        # serialized = json.dumps(self._serialize(rates))
        # await redis.setex(
        #     f"{self.prefix}{cache_key}",
        #     ttl or self.default_ttl,
        #     serialized,
        # )
        logger.debug("Cached %d rates for %s", len(rates), cache_key)

    async def invalidate(self, protocol: str, chain: str) -> None:
        """Invalidate cached data for a protocol/chain.

        Args:
            protocol: Protocol identifier.
            chain: Chain identifier.
        """
        cache_key = f"{protocol}:{chain}"
        self._local_cache.pop(cache_key, None)
        logger.debug("Invalidated cache for %s", cache_key)

    async def invalidate_all(self) -> None:
        """Invalidate all cached rate data."""
        self._local_cache.clear()
        logger.info("Cache invalidated")

    def _serialize(self, rates: list[LendingRate]) -> list[dict]:
        """Serialize rates for cache storage.

        Args:
            rates: List of LendingRate objects.

        Returns:
            List of serializable dictionaries.
        """
        return [rate.to_dict() for rate in rates]

    def _deserialize(self, data: list[dict]) -> list[LendingRate]:
        """Deserialize cached rate data.

        Args:
            data: List of rate dictionaries from cache.

        Returns:
            List of LendingRate objects.
        """
        rates = []
        for item in data:
            asset = Asset(
                symbol=item["asset"]["symbol"],
                address=item["asset"]["address"],
                decimals=item["asset"]["decimals"],
                chain=item["chain"],
                category=AssetCategory(item["asset"]["category"]),
            )
            rate = LendingRate(
                protocol=item["protocol"],
                chain=item["chain"],
                asset=asset,
                supply_apy=item["supply_apy"],
                borrow_apy=item["borrow_apy"],
                supply_apr=item.get("supply_apr", 0.0),
                borrow_apr=item.get("borrow_apr", 0.0),
                total_supply=item.get("total_supply", 0.0),
                total_borrow=item.get("total_borrow", 0.0),
                utilization=item.get("utilization", 0.0),
                timestamp=datetime.fromisoformat(item["timestamp"]),
                block_number=item.get("block_number", 0),
            )
            rates.append(rate)
        return rates

    @property
    def stats(self) -> dict:
        """Return cache statistics.

        Returns:
            Dictionary with cache metrics.
        """
        return {
            "local_entries": len(self._local_cache),
            "prefix": self.prefix,
            "default_ttl": self.default_ttl,
        }
