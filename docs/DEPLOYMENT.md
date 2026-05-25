# Deployment Guide

## Prerequisites
- Docker 24+ and Docker Compose v2
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Go 1.21+ (for local development)
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

## Quick Start (Docker)

```bash
# Clone and configure
cp .env.example .env
# Edit .env with your RPC URLs and database credentials

# Start all services
docker-compose up -d

# Check health
./src/scripts/monitor.sh
```

## Local Development

```bash
# Install dependencies
./src/scripts/setup.sh

# Start database
docker run -d --name postgres -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:15
docker run -d --name redis -p 6379:6379 redis:7

# Run migrations
psql -U postgres -f src/db/schema.sql
psql -U postgres -f src/db/seed.sql

# Terminal 1: Engine
cd src/engine && python main.py

# Terminal 2: Scanner
cd src/scanner && go run main.go scan

# Terminal 3: Frontend
cd src/web && npm run dev
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `REDIS_URL` | Yes | - | Redis connection string |
| `ETHEREUM_RPC_URL` | Yes | - | Ethereum JSON-RPC endpoint |
| `ARBITRUM_RPC_URL` | Yes | - | Arbitrum JSON-RPC endpoint |
| `POLYGON_RPC_URL` | Yes | - | Polygon JSON-RPC endpoint |
| `BASE_RPC_URL` | Yes | - | Base JSON-RPC endpoint |
| `AVALANCHE_RPC_URL` | Yes | - | Avalanche JSON-RPC endpoint |
| `PORT` | No | 8000 | Engine API port |
| `LOG_LEVEL` | No | info | Logging level |
| `FETCH_INTERVAL` | No | 60 | Rate fetch interval (seconds) |

## Production Checklist

- [ ] All environment variables configured
- [ ] Database migrations applied
- [ ] Redis running and accessible
- [ ] RPC endpoints have sufficient rate limits
- [ ] SSL/TLS configured for public endpoints
- [ ] Monitoring and alerting configured
- [ ] Backup strategy in place
- [ ] Log aggregation configured
