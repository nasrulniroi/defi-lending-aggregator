"""Risk calculation engine for DeFi lending protocols.

Computes composite risk scores based on protocol metrics including
TVL, utilization, audit history, smart contract complexity, and
governance structure.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from engine.models.lending_rate import LendingRate
from engine.models.protocol import Protocol, RiskLevel

logger = logging.getLogger(__name__)


@dataclass
class RiskWeights:
    """Weights for risk score components.

    Attributes:
        protocol_age: Weight for protocol age factor.
        tvl: Weight for total value locked factor.
        audit_count: Weight for audit count factor.
        utilization: Weight for pool utilization factor.
        smart_contract_risk: Weight for smart contract complexity.
        governance_risk: Weight for governance centralization.
    """
    protocol_age: float = 0.15
    tvl: float = 0.20
    audit_count: float = 0.15
    utilization: float = 0.20
    smart_contract_risk: float = 0.15
    governance_risk: float = 0.15

    def validate(self) -> bool:
        """Check that weights sum to approximately 1.0.

        Returns:
            True if weights are valid.
        """
        total = (
            self.protocol_age + self.tvl + self.audit_count
            + self.utilization + self.smart_contract_risk
            + self.governance_risk
        )
        return abs(total - 1.0) < 0.01


@dataclass
class RiskAssessment:
    """Complete risk assessment for a position.

    Attributes:
        protocol_id: Protocol identifier.
        chain: Chain identifier.
        asset: Asset symbol.
        composite_score: Overall risk score (1-10).
        risk_level: Categorical risk level.
        components: Individual risk component scores.
        warnings: List of risk warnings.
        timestamp: Assessment timestamp.
    """
    protocol_id: str
    chain: str
    asset: str
    composite_score: float
    risk_level: RiskLevel
    components: dict[str, float]
    warnings: list[str]
    timestamp: datetime

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "protocol_id": self.protocol_id,
            "chain": self.chain,
            "asset": self.asset,
            "composite_score": round(self.composite_score, 2),
            "risk_level": self.risk_level.value,
            "components": {k: round(v, 2) for k, v in self.components.items()},
            "warnings": self.warnings,
            "timestamp": self.timestamp.isoformat(),
        }


class RiskCalculator:
    """Computes composite risk scores for DeFi lending positions.

    Uses a weighted multi-factor model to assess protocol, chain,
    and position-level risk.

    Attributes:
        weights: Risk factor weights.
        tvl_threshold: TVL above which risk is minimized (USD).
    """

    def __init__(
        self,
        weights: Optional[RiskWeights] = None,
        tvl_threshold: float = 1_000_000_000.0,
    ) -> None:
        """Initialize risk calculator.

        Args:
            weights: Custom risk factor weights.
            tvl_threshold: TVL threshold for maximum safety score.
        """
        self.weights = weights or RiskWeights()
        self.tvl_threshold = tvl_threshold

        if not self.weights.validate():
            logger.warning("Risk weights do not sum to 1.0, normalizing")
            self._normalize_weights()

    def _normalize_weights(self) -> None:
        """Normalize weights to sum to 1.0."""
        total = (
            self.weights.protocol_age + self.weights.tvl
            + self.weights.audit_count + self.weights.utilization
            + self.weights.smart_contract_risk + self.weights.governance_risk
        )
        if total > 0:
            self.weights.protocol_age /= total
            self.weights.tvl /= total
            self.weights.audit_count /= total
            self.weights.utilization /= total
            self.weights.smart_contract_risk /= total
            self.weights.governance_risk /= total

    def assess_protocol(self, protocol: Protocol) -> RiskAssessment:
        """Compute risk assessment for a protocol.

        Args:
            protocol: Protocol to assess.

        Returns:
            Complete RiskAssessment with scores and warnings.
        """
        warnings: list[str] = []
        components: dict[str, float] = {}

        # Age factor: older is safer, max score at 2+ years
        age_years = protocol.age_days / 365.0
        age_score = min(age_years / 2.0, 1.0) * 10.0
        components["protocol_age"] = 10.0 - age_score  # Lower is better
        if age_years < 1.0:
            warnings.append(f"Protocol is less than 1 year old ({age_years:.1f}y)")

        # TVL factor: higher TVL is safer
        if protocol.tvl_usd > 0:
            tvl_ratio = protocol.tvl_usd / self.tvl_threshold
            tvl_score = min(-math.log(max(tvl_ratio, 0.001)) / 3.0, 10.0)
            components["tvl"] = tvl_score
            if protocol.tvl_usd < 10_000_000:
                warnings.append(f"Low TVL: ${protocol.tvl_usd:,.0f}")
        else:
            components["tvl"] = 7.0  # Unknown TVL is concerning
            warnings.append("TVL data unavailable")

        # Audit factor: more audits is safer
        audit_score = max(10.0 - protocol.audit_count * 2.0, 1.0)
        components["audit_count"] = audit_score
        if protocol.audit_count < 2:
            warnings.append(f"Only {protocol.audit_count} audits")

        # Utilization factor: near-100% utilization is risky
        # (will be overridden per-position if rate data available)
        components["utilization"] = 5.0

        # Smart contract risk: protocol-specific base score
        components["smart_contract_risk"] = protocol.risk_score

        # Governance risk: based on protocol category
        components["governance_risk"] = self._governance_risk(protocol)

        # Composite score
        composite = (
            self.weights.protocol_age * components["protocol_age"]
            + self.weights.tvl * components["tvl"]
            + self.weights.audit_count * components["audit_count"]
            + self.weights.utilization * components["utilization"]
            + self.weights.smart_contract_risk * components["smart_contract_risk"]
            + self.weights.governance_risk * components["governance_risk"]
        )

        risk_level = self._classify_risk(composite)

        return RiskAssessment(
            protocol_id=protocol.id,
            chain="",
            asset="",
            composite_score=composite,
            risk_level=risk_level,
            components=components,
            warnings=warnings,
            timestamp=datetime.utcnow(),
        )

    def assess_position(
        self, protocol: Protocol, rate: LendingRate
    ) -> RiskAssessment:
        """Compute risk assessment for a specific lending position.

        Args:
            protocol: Protocol configuration.
            rate: Current lending rate data.

        Returns:
            RiskAssessment with position-specific utilization risk.
        """
        assessment = self.assess_protocol(protocol)
        assessment.chain = rate.chain
        assessment.asset = rate.asset.symbol

        # Override utilization with actual data
        util = rate.utilization_rate
        if util > 95.0:
            assessment.components["utilization"] = 9.0
            assessment.warnings.append(
                f"Critical utilization: {util:.1f}%"
            )
        elif util > 85.0:
            assessment.components["utilization"] = 6.0
            assessment.warnings.append(
                f"High utilization: {util:.1f}%"
            )
        elif util > 70.0:
            assessment.components["utilization"] = 3.5
        else:
            assessment.components["utilization"] = 2.0

        # Recalculate composite
        assessment.composite_score = sum(
            getattr(self.weights, k.replace("_score", ""), 0.2) * v
            for k, v in assessment.components.items()
            if hasattr(self.weights, k)
        )
        assessment.risk_level = self._classify_risk(assessment.composite_score)
        return assessment

    def _governance_risk(self, protocol: Protocol) -> float:
        """Estimate governance centralization risk.

        Args:
            protocol: Protocol to assess.

        Returns:
            Risk score from 1.0 to 10.0.
        """
        # Simplified heuristic based on known governance structures
        governance_scores = {
            "aave": 3.0,       # AAVE token governance, fairly decentralized
            "compound": 3.5,   # COMP governance
            "morpho": 5.0,     # Newer, more centralized
            "benqi": 5.5,      # Smaller governance community
            "radiant": 6.0,    # Cross-chain governance complexity
        }
        return governance_scores.get(protocol.id, 5.0)

    def _classify_risk(self, score: float) -> RiskLevel:
        """Classify a numeric risk score into a risk level.

        Args:
            score: Composite risk score (1-10).

        Returns:
            RiskLevel classification.
        """
        if score <= 3.0:
            return RiskLevel.LOW
        elif score <= 5.0:
            return RiskLevel.MEDIUM
        elif score <= 7.5:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL
