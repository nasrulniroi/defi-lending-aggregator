"""APY optimization engine.

Analyzes current rates across protocols and chains to identify the
highest risk-adjusted yield opportunities for lenders.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from engine.models.lending_rate import LendingRate
from engine.models.opportunity import (
    Confidence,
    OpportunityType,
    YieldOpportunity,
)
from engine.models.protocol import Protocol
from engine.risk_calculator import RiskAssessment, RiskCalculator

logger = logging.getLogger(__name__)


@dataclass
class OptimizerConfig:
    """Configuration for the APY optimizer.

    Attributes:
        min_apy: Minimum APY to consider (percentage).
        max_risk_score: Maximum acceptable risk score (1-10).
        diversification_bonus: APY bonus for using multiple protocols.
        rebalance_threshold: Minimum APY gain to recommend rebalancing.
        gas_estimate_usd: Default gas cost estimate in USD.
        position_size: Assumed position size for ROI calculations.
    """
    min_apy: float = 0.5
    max_risk_score: float = 7.0
    diversification_bonus: float = 0.1
    rebalance_threshold: float = 1.0
    gas_estimate_usd: float = 25.0
    position_size: float = 10_000.0


class APYOptimizer:
    """Finds optimal lending positions across protocols and chains.

    Compares rates, filters by risk tolerance, and recommends the
    best risk-adjusted yield opportunities.

    Attributes:
        risk_calc: Risk calculator for scoring positions.
        config: Optimizer configuration.
    """

    def __init__(
        self,
        risk_calc: RiskCalculator,
        config: Optional[OptimizerConfig] = None,
    ) -> None:
        """Initialize the APY optimizer.

        Args:
            risk_calc: Risk calculator for position scoring.
            config: Optimizer settings.
        """
        self.risk_calc = risk_calc
        self.config = config or OptimizerConfig()

    def find_opportunities(
        self,
        rates: dict[str, list[LendingRate]],
        protocols: dict[str, Protocol],
        current_positions: Optional[dict[str, LendingRate]] = None,
    ) -> list[YieldOpportunity]:
        """Find the best yield optimization opportunities.

        Args:
            rates: All current rates keyed by protocol ID.
            protocols: Protocol configurations keyed by ID.
            current_positions: Optional current user positions.

        Returns:
            Sorted list of YieldOpportunity objects (best first).
        """
        opportunities: list[YieldOpportunity] = []

        # Group rates by asset across protocols
        asset_rates: dict[str, list[tuple[str, LendingRate]]] = {}
        for proto_id, proto_rates in rates.items():
            for rate in proto_rates:
                key = rate.asset.symbol
                if key not in asset_rates:
                    asset_rates[key] = []
                asset_rates[key].append((proto_id, rate))

        # For each asset, find the best rates
        for asset_symbol, proto_rates in asset_rates.items():
            if len(proto_rates) < 2:
                continue

            # Sort by supply APY descending
            proto_rates.sort(key=lambda x: x[1].supply_apy, reverse=True)
            best_proto, best_rate = proto_rates[0]

            # Compare against all other protocols
            for other_proto, other_rate in proto_rates[1:]:
                apy_gain = best_rate.supply_apy - other_rate.supply_apy
                if apy_gain < self.config.rebalance_threshold:
                    continue

                # Check risk
                best_protocol = protocols.get(best_proto)
                if best_protocol is None:
                    continue

                risk = self.risk_calc.assess_protocol(best_protocol)
                if risk.composite_score > self.config.max_risk_score:
                    continue

                # Determine opportunity type
                if best_rate.chain != other_rate.chain:
                    opp_type = OpportunityType.CROSS_CHAIN
                else:
                    opp_type = OpportunityType.PROTOCOL_SWITCH

                # Estimate breakeven
                daily_gain = (
                    self.config.position_size
                    * (apy_gain / 100.0)
                    / 365.0
                )
                breakeven = (
                    int(self.config.gas_estimate_usd / daily_gain)
                    if daily_gain > 0 else 999
                )

                # Confidence based on rate stability
                confidence = self._assess_confidence(best_rate, other_rate)

                opp = YieldOpportunity(
                    id=str(uuid.uuid4())[:8],
                    type=opp_type,
                    asset=asset_symbol,
                    source_protocol=other_proto,
                    target_protocol=best_proto,
                    source_chain=other_rate.chain,
                    target_chain=best_rate.chain,
                    current_apy=other_rate.supply_apy,
                    target_apy=best_rate.supply_apy,
                    apy_gain=apy_gain,
                    risk_score=risk.composite_score,
                    confidence=confidence,
                    estimated_gas=self.config.gas_estimate_usd,
                    breakeven_days=breakeven,
                    description=self._generate_description(
                        asset_symbol, other_proto, best_proto,
                        other_rate, best_rate, apy_gain,
                    ),
                )
                opportunities.append(opp)

        # Sort by risk-adjusted APY gain
        opportunities.sort(
            key=lambda o: o.apy_gain / max(o.risk_score, 1.0),
            reverse=True,
        )

        logger.info("Found %d optimization opportunities", len(opportunities))
        return opportunities

    def _assess_confidence(
        self, rate_a: LendingRate, rate_b: LendingRate
    ) -> Confidence:
        """Assess confidence in the opportunity based on rate stability.

        Args:
            rate_a: Current best rate.
            rate_b: Alternative rate.

        Returns:
            Confidence level.
        """
        # Check if we have historical data
        if rate_a.supply_apy_7d is None or rate_b.supply_apy_7d is None:
            return Confidence.LOW

        # Check stability: small 7d change = higher confidence
        a_change = abs(rate_a.supply_apy - rate_a.supply_apy_7d)
        b_change = abs(rate_b.supply_apy - rate_b.supply_apy_7d)

        if a_change < 0.5 and b_change < 0.5:
            return Confidence.HIGH
        elif a_change < 2.0 and b_change < 2.0:
            return Confidence.MEDIUM
        return Confidence.LOW

    def _generate_description(
        self,
        asset: str,
        source_proto: str,
        target_proto: str,
        source_rate: LendingRate,
        target_rate: LendingRate,
        apy_gain: float,
    ) -> str:
        """Generate human-readable description of the opportunity.

        Args:
            asset: Asset symbol.
            source_proto: Source protocol ID.
            target_proto: Target protocol ID.
            source_rate: Current rate data.
            target_rate: Better rate data.
            apy_gain: APY improvement.

        Returns:
            Description string.
        """
        if source_rate.chain != target_rate.chain:
            return (
                f"Move {asset} from {source_proto} on {source_rate.chain} "
                f"({source_rate.supply_apy:.2f}%) to {target_proto} on "
                f"{target_rate.chain} ({target_rate.supply_apy:.2f}%) "
                f"for +{apy_gain:.2f}% APY gain."
            )
        return (
            f"Switch {asset} from {source_proto} ({source_rate.supply_apy:.2f}%) "
            f"to {target_proto} ({target_rate.supply_apy:.2f}%) on "
            f"{target_rate.chain} for +{apy_gain:.2f}% APY gain."
        )
