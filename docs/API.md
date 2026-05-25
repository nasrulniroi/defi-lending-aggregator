# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### GET /rates
Fetch all current lending rates.

**Query Parameters:**
- `chain` (optional): Filter by chain (ethereum, arbitrum, polygon, base, avalanche)
- `protocol` (optional): Filter by protocol name
- `asset` (optional): Filter by asset symbol
- `min_supply_apy` (optional): Minimum supply APY
- `sort` (optional): Sort field (supply_apy, borrow_apy, utilization, tvl)
- `order` (optional): Sort order (asc, desc)

**Response:**
```json
{
  "data": [
    {
      "protocol": "Aave V3",
      "chain": "ethereum",
      "asset": "USDC",
      "supply_apy": 4.32,
      "borrow_apy": 6.18,
      "total_supply": 1250000000,
      "total_borrow": 680000000,
      "utilization_rate": 0.544,
      "last_updated": "2024-01-15T10:30:00Z"
    }
  ],
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /protocols
Fetch all supported protocols.

**Response:**
```json
{
  "data": [
    {
      "name": "Aave V3",
      "chains": ["ethereum", "arbitrum", "polygon"],
      "category": "lending",
      "tvl": 12500000000,
      "avg_supply_apy": 4.12,
      "avg_borrow_apy": 5.98,
      "asset_count": 28,
      "status": "active"
    }
  ],
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /opportunities
Fetch yield optimization opportunities.

**Query Parameters:**
- `min_net_apy` (optional): Minimum net APY threshold
- `max_risk` (optional): Maximum risk score (0-10)
- `asset` (optional): Filter by asset

### GET /history/{protocol}/{chain}/{asset}
Fetch historical rate data.

**Query Parameters:**
- `period`: Time period (1h, 1d, 7d, 30d, 90d)
- `resolution`: Data point resolution (5m, 15m, 1h, 1d)

### POST /alerts
Create a new alert.

**Request Body:**
```json
{
  "protocol": "Aave V3",
  "chain": "ethereum",
  "asset": "USDC",
  "alert_type": "rate_above",
  "threshold": 5.0,
  "severity": "info"
}
```

### GET /alerts
Fetch user alerts.

### PATCH /alerts/{id}/read
Mark an alert as read.

## Error Responses

All errors follow the format:
```json
{
  "data": null,
  "error": "Human-readable error message",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Common HTTP codes:
- `400` - Bad request (invalid parameters)
- `404` - Resource not found
- `429` - Rate limited
- `500` - Internal server error
