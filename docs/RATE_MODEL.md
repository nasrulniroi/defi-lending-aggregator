# Rate Model Documentation

## Overview

The DeFi Lending Aggregator tracks lending and borrowing rates across multiple DeFi protocols. This document describes the data model, calculation methodology, and risk assessment framework.

## Core Rate Model

### Lending Rate
```
LendingRate {
    protocol: string       // Protocol identifier (e.g., "aave-v3")
    chain: string          // Blockchain (e.g., "ethereum")
    asset: string          // Token symbol (e.g., "USDC")
    supply_apy: float      // Annualized supply yield (%)
    borrow_apy: float      // Annualized borrow cost (%)
    total_supply: float    // Total supplied in USD
    total_borrow: float    // Total borrowed in USD
    utilization_rate: float // total_borrow / total_supply
}
```

### Rate Calculation

**Supply APY** is calculated from the supply rate per block:
```
supply_apy = ((1 + supply_rate_per_block) ^ blocks_per_year - 1) * 100
```

**Borrow APY** is calculated from the borrow rate per block:
```
borrow_apy = ((1 + borrow_rate_per_block) ^ blocks_per_year - 1) * 100
```

**Utilization Rate**:
```
utilization = total_borrow / total_supply
```

## Risk Model

### Utilization Risk (0-10)
Higher utilization means less liquidity available for withdrawals:
- 0-50%: Low risk (0-2)
- 50-80%: Medium risk (2-5)
- 80-95%: High risk (5-8)
- 95%+ : Critical risk (8-10)

### Protocol Risk (0-10)
Based on protocol maturity and security:
- TVL weight: Higher TVL = lower risk
- Age weight: Older protocols = lower risk
- Audit count: More audits = lower risk
- Historical incidents: Past exploits increase risk

### Chain Risk (0-10)
Based on chain security and decentralization:
- Validator count
- Nakamoto coefficient
- Historical downtime
- Bridge security

### Composite Risk Score
```
composite_risk = (utilization_risk * 0.4) + (protocol_risk * 0.35) + (chain_risk * 0.25)
```

## Yield Optimization

The optimizer finds opportunities where you can:
1. Supply on Protocol A (higher supply APY)
2. Borrow on Protocol B (lower borrow APY)
3. Net positive spread after accounting for risk

### Opportunity Score
```
opportunity_score = net_apy / (1 + risk_score)
```

Higher scores indicate better risk-adjusted returns.
