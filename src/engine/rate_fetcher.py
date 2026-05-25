"""Rate fetching engine for DeFi lending protocols.

Provides the main orchestration layer for fetching rates from multiple
protocols across multiple chains concurrently.
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime
from typing import Optional

from engine.models.lending_rate import Asset, AssetCategory, LendingRate
from engine.models.protocol import Protocol
from engine.protocol_registry import ProtocolRegistry
from engine.data.aave import AaveFetcher
from engine.data.compound import CompoundFetcher
from engine.data.morpho import MorphoFetcher
from engine.data.cache import RateCache
from engine.utils.logging import get_logger

logger = get_logger(__name__)


class RateFetchError(Exception):
    """Raised when rate fetching fails for a protocol."""

    def __init__(self, protocol: str, chain: str, message: str) -> None:
        self.protocol = protocol
        self.chain = chain
        super().__init__(f"Failed to fetch rates for {protocol} on {chain}: {message}")


class RateFetcher:
    """Orchestrates rate fetching across all configured protocols.

    Manages concurrent fetching, caching, error handling, and retry logic
    for DeFi lending protocol rate data.

    Attributes:
        registry: Protocol registry with configuration.
        cache: Redis-backed rate cache.
        max_concurrent: Maximum concurrent fetch operations.
        retry_count: Number of retries per failed fetch.
    """

    def __init__(
        self,
        registry: ProtocolRegistry,
        cache: Optional[RateCache] = None,
        max_concurrent: int = 10,
        retry_count: int = 3,
    ) -> None:
        """Initialize the rate fetcher.

        Args:
            registry: Protocol registry with all configured protocols.
            cache: Optional rate cache for deduplication and speed.
            max_concurrent: Max concurrent fetch operations.
            retry_count: Number of retries on failure.
        """
        self.registry = registry
        self.cache = cache
        self.max_concurrent = max_concurrent
        self.retry_count = retry_count
        self._fetchers: dict[str, type] = {
            "aave": AaveFetcher,
            "compound": CompoundFetcher,
            "morpho": MorphoFetcher,
        }
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._stats = {
            "total_fetches": 0,
            "successful": 0,
            "failed": 0,
            "cache_hits": 0,
            "avg_latency_ms": 0.0,
        }

    async def fetch_all_rates(self) -> dict[str, list[LendingRate]]:
        """Fetch rates from all configured protocols across all chains.

        Returns:
            Dictionary mapping protocol ID to list of LendingRate objects.

        Raises:
            RateFetchError: If a protocol fetch fails after all retries.
        """
        start_time = time.monotonic()
        all_rates: dict[str, list[LendingRate]] = {}
        tasks = []

        for protocol in self.registry.get_all_protocols():
            if protocol.id not in self._fetchers:
                logger.warning("No fetcher for protocol %s, skipping", protocol.id)
                continue

            for chain in protocol.chains:
                task = self._fetch_with_retry(protocol, chain)
                tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.error("Fetch task failed: %s", result)
                self._stats["failed"] += 1
                continue
            protocol_id, rates = result
            if protocol_id not in all_rates:
                all_rates[protocol_id] = []
            all_rates[protocol_id].extend(rates)
            self._stats["successful"] += 1

        elapsed_ms = (time.monotonic() - start_time) * 1000
        self._stats["total_fetches"] += len(tasks)
        self._stats["avg_latency_ms"] = (
            (self._stats["avg_latency_ms"] * (self._stats["total_fetches"] - len(tasks))
             + elapsed_ms) / max(self._stats["total_fetches"], 1)
        )
        logger.info(
            "Fetched rates from %d protocols in %.1fms",
            len(all_rates), elapsed_ms,
        )
        return all_rates

    async def fetch_protocol_rates(
        self, protocol_id: str, chain: str
    ) -> list[LendingRate]:
        """Fetch rates for a specific protocol on a specific chain.

        Args:
            protocol_id: Protocol identifier.
            chain: Chain identifier.

        Returns:
            List of LendingRate objects.

        Raises:
            RateFetchError: If the fetch fails after retries.
            ValueError: If the protocol is not registered.
        """
        protocol = self.registry.get_protocol(protocol_id)
        if protocol is None:
            raise ValueError(f"Unknown protocol: {protocol_id}")

        if not protocol.supports_chain(chain):
            raise ValueError(
                f"Protocol {protocol_id} does not support chain {chain}"
            )

        # Check cache first
        if self.cache:
            cached = await self.cache.get_rates(protocol_id, chain)
            if cached is not None:
                self._stats["cache_hits"] += 1
                return cached

        _, rates = await self._fetch_with_retry(protocol, chain)

        if self.cache:
            await self.cache.set_rates(protocol_id, chain, rates)

        return rates

    async def _fetch_with_retry(
        self, protocol: Protocol, chain: str
    ) -> tuple[str, list[LendingRate]]:
        """Fetch rates with retry logic.

        Args:
            protocol: Protocol to fetch from.
            chain: Chain to fetch on.

        Returns:
            Tuple of (protocol_id, rates).

        Raises:
            RateFetchError: After all retries exhausted.
        """
        fetcher_class = self._fetchers.get(protocol.id)
        if fetcher_class is None:
            raise RateFetchError(protocol.id, chain, "No fetcher available")

        last_error: Optional[Exception] = None
        for attempt in range(self.retry_count):
            try:
                async with self._semaphore:
                    fetcher = fetcher_class(protocol, chain)
                    rates = await fetcher.fetch()
                    logger.debug(
                        "Fetched %d rates from %s/%s (attempt %d)",
                        len(rates), protocol.id, chain, attempt + 1,
                    )
                    return protocol.id, rates
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Attempt %d/%d failed for %s/%s: %s",
                    attempt + 1, self.retry_count, protocol.id, chain, exc,
                )
                if attempt < self.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)

        raise RateFetchError(
            protocol.id, chain,
            f"All {self.retry_count} attempts failed: {last_error}"
        )

    @property
    def stats(self) -> dict:
        """Return fetcher statistics.

        Returns:
            Dictionary with fetch statistics.
        """
        return dict(self._stats)
