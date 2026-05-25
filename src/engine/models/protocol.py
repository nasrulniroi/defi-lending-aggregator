"""Data models for DeFi lending protocols."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    """Protocol risk classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProtocolStatus(Enum):
    """Protocol operational status."""
    ACTIVE = "active"
    DEGRADED = "degraded"
    PAUSED = "paused"
    OFFLINE = "offline"


@dataclass(frozen=True)
class ProtocolContract:
    """On-chain contract reference."""
    chain: str
    address: str
    name: str
    abi_version: str = "v1"


@dataclass
class Protocol:
    """DeFi lending protocol metadata.

    Attributes:
        id: Unique protocol identifier (e.g., 'aave', 'compound').
        name: Human-readable protocol name.
        version: Protocol version string.
        chains: List of supported chain identifiers.
        risk_score: Base risk score from 1.0 (safest) to 10.0 (riskiest).
        audit_count: Number of completed security audits.
        launch_date: Protocol launch date.
        status: Current operational status.
        tvl_usd: Total value locked in USD.
        website: Protocol website URL.
    """
    id: str
    name: str
    version: str
    chains: list[str]
    risk_score: float
    audit_count: int
    launch_date: datetime
    status: ProtocolStatus = ProtocolStatus.ACTIVE
    tvl_usd: float = 0.0
    website: str = ""
    contracts: dict[str, dict[str, str]] = field(default_factory=dict)

    def supports_chain(self, chain: str) -> bool:
        """Check if protocol supports a given chain.

        Args:
            chain: Chain identifier.

        Returns:
            True if the protocol is deployed on the chain.
        """
        return chain.lower() in [c.lower() for c in self.chains]

    @property
    def risk_level(self) -> RiskLevel:
        """Classify risk level based on risk score.

        Returns:
            RiskLevel enum value.
        """
        if self.risk_score <= 3.0:
            return RiskLevel.LOW
        elif self.risk_score <= 5.0:
            return RiskLevel.MEDIUM
        elif self.risk_score <= 7.5:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    @property
    def age_days(self) -> int:
        """Calculate protocol age in days.

        Returns:
            Number of days since launch.
        """
        return (datetime.utcnow() - self.launch_date).days

    def to_dict(self) -> dict:
        """Serialize protocol to dictionary.

        Returns:
            Dictionary representation of the protocol.
        """
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "chains": self.chains,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "audit_count": self.audit_count,
            "launch_date": self.launch_date.isoformat(),
            "status": self.status.value,
            "tvl_usd": self.tvl_usd,
            "website": self.website,
            "age_days": self.age_days,
        }
