# DeFi Lending Rate Aggregator

Real-time lending and borrowing rate aggregator across major DeFi protocols on multiple EVM chains.

## Overview

Aggregates and compares lending/borrowing rates from **Aave**, **Compound**, **Morpho**, **Benqi**, and **Radiant** across **Ethereum**, **Arbitrum**, **Polygon**, **Base**, and **Avalanche**.

Find the best yields, optimize your lending strategy, and get alerts when rates change.

## Features

- **Multi-protocol rate aggregation** — real-time supply and borrow APY from 5 protocols
- **Multi-chain support** — Ethereum, Arbitrum, Polygon, Base, Avalanche
- **APY Optimizer** — find the highest risk-adjusted yield opportunities
- **Risk scoring** — protocol health, utilization, and smart contract risk metrics
- **Rate alerts** — notifications when rates hit your thresholds
- **Historical charts** — track rate trends over time
- **REST API** — JSON endpoints for all rate data

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Next.js Web │   │ Python Engine│   │  Go Scanner  │
│  (Frontend)  │◄──│ (Rate Logic) │◄──│ (Chain Data) │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                   │
       ▼                  ▼                   ▼
┌──────────────────────────────────────────────────┐
│              PostgreSQL + Redis                    │
└──────────────────────────────────────────────────┘
```

- **Python Engine** — rate fetching, risk calculation, APY optimization
- **Go Scanner** — high-performance on-chain data collection
- **Next.js Web** — dashboard, charts, API routes

## Quick Start

```bash
# Clone and setup
git clone https://github.com/nasrulniroi/defi-lending-aggregator.git
cd defi-lending-aggregator

# Copy environment config
cp .env.example .env
# Edit .env with your RPC endpoints

# Docker (recommended)
docker-compose up -d

# Or manual setup
make setup
make dev
```

## API

```bash
# Get all current rates
curl http://localhost:3000/api/rates

# Get rates for specific protocol
curl http://localhost:3000/api/rates?protocol=aave&chain=ethereum

# Get optimization opportunities
curl http://localhost:3000/api/opportunities
```

See [docs/API.md](docs/API.md) for full API documentation.

## Development

```bash
# Run all services
make dev

# Run tests
make test

# Python engine tests
cd src/engine && python -m pytest ../../tests/engine/

# Go scanner tests
cd src/scanner && go test ./...

# Web tests
cd src/web && npm test
```

## Configuration

All configuration lives in `config/`:
- `default.yaml` — shared settings
- `chains.yaml` — chain RPC endpoints and block times
- `protocols.yaml` — protocol contract addresses and parameters

## Deployment

```bash
# Build and deploy
make build
make deploy

# Or use Docker
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment guide.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE)

## Acknowledgments

- Built with [MiMo V2.5](https://github.com/XiaomiMiMo/MiMo)
- Developed using Claude Code + Hermes Agent
- Data sourced from DeFiLlama, on-chain oracles, and protocol subgraphs
- Inspired by DeFi Rate, Lido, and the broader DeFi community
