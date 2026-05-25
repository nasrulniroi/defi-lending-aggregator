"""Lending rate data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class RateType(Enum):
    """Type of lending rate."""
    SUPPLY = "supply"
    BORROW_VARIABLE = "borrow_variable"
    BORROW_STABLE = "borrow_stable"


class AssetCategory(Enum):
    """Asset classification."""
    STABLECOIN = "stablecoin"
    NATIVE = "native"
    WRAPPED = "wrapped"
    GOVERNANCE = "governance"
    LP_TOKEN = "lp_token"
    OTHER = "other"


@dataclass(frozen=True)
class Asset:
    """On-chain asset reference.

    Attributes:
        symbol: Asset ticker symbol (e.g., 'USDC', 'WETH').
        address: On-chain contract address.
        decimals: Token decimal places.
        chain: Chain identifier.
        category: Asset classification.
    """
    symbol: str
    address: str
    decimals: int
    chain: str
    category: AssetCategory = AssetCategory.OTHER

    @property
    def display_name(self) -> str:
        """Human-readable asset name with chain suffix.

        Returns:
            Formatted string like 'USDC (Ethereum)'.
        """
        return f"{self.symbol} ({self.chain.title()})"


@dataclass
class LendingRate:
    """Real-time lending/borrowing rate for a specific asset on a protocol.

    Attributes:
        protocol: Protocol identifier.
        chain: Chain identifier.
        asset: The asset being lent/borrowed.
        supply_apy: Current supply APY as a percentage.
        borrow_apy: Current variable borrow APY as a percentage.
        supply_apr: Current supply APR (non-compounded).
        borrow_apr: Current variable borrow APR.
        total_supply: Total supply of the asset in the pool.
        total_borrow: Total borrow from the pool.
        utilization: Pool utilization percentage (0-100).
        supply_apy_1d: Supply APY 24 hours ago.
        borrow_apy_1d: Borrow APY 24 hours ago.
        supply_apy_7d: Supply APY 7 days ago.
        borrow_apy_7d: Borrow APY 7 days ago.
        timestamp: When this rate was fetched.
        block_number: Block number at fetch time.
    """
    protocol: str
    chain: str
    asset: Asset
    supply_apy: float
    borrow_apy: float
    supply_apr: float = 0.0
    borrow_apr: float = 0.0
    total_supply: float = 0.0
    total_borrow: float = 0.0
    utilization: float = 0.0
    supply_apy_1d: Optional[float] = None
    borrow_apy_1d: Optional[float] = None
    supply_apy_7d: Optional[float] = None
    borrow_apy_7d: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    block_number: int = 0

    @property
    def net_apy(self) -> float:
        """Calculate net APY (supply - borrow spread).

        Returns:
            Net spread in percentage points.
        """
        return self.supply_apy - self.borrow_apy

    @property
    def utilization_rate(self) -> float:
        """Calculate utilization rate from supply and borrow.

        Returns:
            Utilization as a percentage (0-100).
        """
        if self.total_supply <= 0:
            return 0.0
        return (self.total_borrow / self.total_supply) * 100.0

    @property
    def supply_change_1d(self) -> Optional[float]:
        """Supply APY change in the last 24 hours.

        Returns:
            Percentage point change, or None if historical data unavailable.
        """
        if self.supply_apy_1d is None:
            return None
        return self.supply_apy - self.supply_apy_1d

    @property
    def borrow_change_1d(self) -> Optional[float]:
        """Borrow APY change in the last 24 hours.

        Returns:
            Percentage point change, or None if historical data unavailable.
        """
        if self.borrow_apy_1d is None:
            return None
        return self.borrow_apy - self.borrow_apy_1d

    @property
    def is_stale(self) -> bool:
        """Check if rate data is older than 5 minutes.

        Returns:
            True if the data may be outdated.
        """
        age = (datetime.utcnow() - self.timestamp).total_seconds()
        return age > 300

    def to_dict(self) -> dict:
        """Serialize lending rate to dictionary.

        Returns:
            Dictionary representation suitable for JSON API responses.
        """
        return {
            "protocol": self.protocol,
            "chain": self.chain,
            "asset": {
                "symbol": self.asset.symbol,
                "address": self.asset.address,
                "decimals": self.asset.decimals,
                "category": self.asset.category.value,
            },
            "supply_apy": round(self.supply_apy, 4),
            "borrow_apy": round(self.borrow_apy, 4),
            "supply_apr": round(self.supply_apr, 4),
            "borrow_apr": round(self.borrow_apr, 4),
            "net_apy": round(self.net_apy, 4),
            "total_supply": self.total_supply,
            "total_borrow": self.total_borrow,
            "utilization": round(self.utilization_rate, 2),
            "supply_change_1d": self.supply_change_1d,
            "borrow_change_1d": self.borrow_change_1d,
            "timestamp": self.timestamp.isoformat(),
            "block_number": self.block_number,
        }
