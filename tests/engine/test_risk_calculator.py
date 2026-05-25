"""Tests for the risk calculator module."""
import pytest
from src.engine.risk_calculator import RiskCalculator


@pytest.fixture
def calculator():
    return RiskCalculator()


class TestRiskCalculator:
    """Test suite for RiskCalculator."""

    def test_low_utilization_low_risk(self, calculator):
        """Low utilization should result in low risk score."""
        score = calculator.calculate_utilization_risk(0.3)
        assert score < 3.0

    def test_high_utilization_high_risk(self, calculator):
        """High utilization should result in high risk score."""
        score = calculator.calculate_utilization_risk(0.95)
        assert score > 7.0

    def test_medium_utilization_medium_risk(self, calculator):
        """Medium utilization should result in moderate risk."""
        score = calculator.calculate_utilization_risk(0.6)
        assert 3.0 <= score <= 6.0

    def test_protocol_risk_with_tvl(self, calculator):
        """Higher TVL should reduce protocol risk."""
        risk_high_tvl = calculator.calculate_protocol_risk(tvl=10e9, age_days=365, audit_count=5)
        risk_low_tvl = calculator.calculate_protocol_risk(tvl=1e6, age_days=30, audit_count=0)
        assert risk_high_tvl < risk_low_tvl

    def test_composite_risk_score(self, calculator):
        """Composite risk should be weighted average of factors."""
        score = calculator.calculate_composite_risk(
            utilization_risk=5.0,
            protocol_risk=3.0,
            chain_risk=2.0,
        )
        assert 2.0 <= score <= 5.0

    def test_risk_score_bounds(self, calculator):
        """Risk scores should be bounded between 0 and 10."""
        score = calculator.calculate_composite_risk(
            utilization_risk=15.0,
            protocol_risk=20.0,
            chain_risk=-5.0,
        )
        assert 0.0 <= score <= 10.0
