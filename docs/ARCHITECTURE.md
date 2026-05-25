# Architecture Overview

## System Components

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Next.js Web   │────▶│   Engine API     │────▶│   PostgreSQL    │
│   (Frontend)    │     │   (Python)       │     │   (Database)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                         │
                               ▼                         ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │   Go Scanner     │────▶│     Redis       │
                        │   (On-chain)     │     │   (Cache)       │
                        └──────────────────┘     └─────────────────┘
```

### Python Engine (src/engine/)
Core business logic for rate aggregation and analysis:
- **Rate Fetcher**: Collects rates from protocol APIs and subgraphs
- **Risk Calculator**: Computes protocol, chain, and utilization risk scores
- **APY Optimizer**: Finds yield opportunities across protocols
- **Anomaly Detector**: Identifies unusual rate movements
- **Protocol Registry**: Manages protocol metadata and configurations

### Go Scanner (src/scanner/)
High-performance on-chain data collection:
- **Chain Scanners**: Per-chain implementations (Ethereum, Arbitrum, Polygon, Base, Avalanche)
- **Protocol Handlers**: Direct smart contract interaction for rate data
- **RPC Client**: Connection pooling and retry logic for JSON-RPC calls
- **Rate Aggregator**: Merges and deduplicates rates from multiple sources

### Next.js Frontend (src/web/)
Dashboard UI with real-time data:
- **App Router**: File-based routing with server components
- **API Routes**: Backend-for-frontend endpoints
- **Components**: Reusable UI components with Tailwind CSS
- **Real-time Updates**: Polling-based data refresh

## Data Flow

1. **Collection**: Go Scanner reads on-chain data via JSON-RPC
2. **Enrichment**: Python Engine fetches protocol metadata from DeFiLlama
3. **Storage**: Rates stored in PostgreSQL with time-series history
4. **Caching**: Hot data cached in Redis with 60s TTL
5. **Serving**: Next.js API routes serve cached data to frontend
6. **Alerting**: Engine monitors for threshold breaches and notifies users

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14, React, Tailwind CSS | Dashboard UI |
| Backend | Python 3.11+, FastAPI | Rate engine, risk models |
| Scanner | Go 1.21+ | On-chain data collection |
| Database | PostgreSQL 15+ | Persistent storage |
| Cache | Redis 7+ | Rate limiting, hot data |
| Infra | Docker, Docker Compose | Containerization |
