"""Optimization opportunity models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class OpportunityType(Enum):
    """Classification of yield optimization opportunity."""
    RATE_ARB = "rate_arbitrage"
    LEVERAGED_YIELD = "leveraged_yield"
    STABLECOIN_LOOP = "stablecoin_loop"
    CROSS_CHAIN = "cross_chain"
    PROTOCOL_SWITCH = "protocol_switch"


class Confidence(Enum):
    """Confidence level of the opportunity assessment."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class YieldOpportunity:
    """A yield optimization opportunity.

    Attributes:
        id: Unique opportunity identifier.
        type: Classification of the opportunity.
        asset: Asset symbol involved.
        source_protocol: Protocol currently holding the asset.
        target_protocol: Recommended protocol for the asset.
        source_chain: Current chain.
        target_chain: Recommended chain.
        current_apy: Current yield being earned.
        target_apy: Expected yield after optimization.
        apy_gain: Percentage point improvement.
        risk_score: Risk score of the target position (1-10).
        confidence: Confidence in the opportunity assessment.
        estimated_gas: Estimated gas cost in USD.
        breakeven_days: Days to recover gas costs.
        description: Human-readable explanation.
        timestamp: When the opportunity was identified.
    """
    id: str
    type: OpportunityType
    asset: str
    source_protocol: str
    target_protocol: str
    source_chain: str
    target_chain: str
    current_apy: float
    target_apy: float
    apy_gain: float
    risk_score: float
    confidence: Confidence
    estimated_gas: float = 0.0
    breakeven_days: int = 0
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_profitable(self) -> bool:
        """Check if opportunity is profitable after gas costs.

        Returns:
            True if APY gain justifies the gas cost within 30 days.
        """
        if self.estimated_gas <= 0:
            return self.apy_gain > 0
        daily_gain_pct = self.apy_gain / 365.0
        return self.breakeven_days <= 30

    @property
    def roi_30d(self) -> float:
        """Estimate 30-day ROI assuming $10,000 position.

        Returns:
            Estimated net return in USD over 30 days.
        """
        position = 10_000.0
        gross_return = position * (self.apy_gain / 100.0) * (30.0 / 365.0)
        return gross_return - self.estimated_gas

    @property
    def confidence_score(self) -> float:
        """Numeric confidence score.

        Returns:
            Score from 0.0 to 1.0.
        """
        mapping = {
            Confidence.HIGH: 0.9,
            Confidence.MEDIUM: 0.65,
            Confidence.LOW: 0.35,
        }
        return mapping[self.confidence]

    def to_dict(self) -> dict:
        """Serialize opportunity to dictionary.

        Returns:
            Dictionary representation for API responses.
        """
        return {
            "id": self.id,
            "type": self.type.value,
            "asset": self.asset,
            "source_protocol": self.source_protocol,
            "target_protocol": self.target_protocol,
            "source_chain": self.source_chain,
            "target_chain": self.target_chain,
            "current_apy": round(self.current_apy, 4),
            "target_apy": round(self.target_apy, 4),
            "apy_gain": round(self.apy_gain, 4),
            "risk_score": round(self.risk_score, 1),
            "confidence": self.confidence.value,
            "confidence_score": self.confidence_score,
            "estimated_gas": round(self.estimated_gas, 2),
            "breakeven_days": self.breakeven_days,
            "is_profitable": self.is_profitable,
            "roi_30d": round(self.roi_30d, 2),
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
        }
