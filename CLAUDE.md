# Claude Code Project Configuration

## Project Overview
DeFi Lending Rate Aggregator — multi-chain, multi-protocol real-time rate comparison tool.

## Development Tools
- **Claude Code** — primary development assistant for code generation, refactoring, and debugging
- **Hermes Agent** — orchestration, task delegation, and automated workflows

## Tech Stack
- **Python 3.11+** — rate fetching engine, risk models, APY optimization
- **Go 1.21+** — high-performance chain scanner and RPC client
- **Next.js 14** (App Router) — web dashboard and API routes
- **PostgreSQL 15** — rate history and protocol metadata
- **Redis 7** — caching and real-time rate storage
- **Docker** — containerized deployment

## Code Style

### Python
- PEP 8, type hints on all functions
- Google-style docstrings
- Use `dataclass` or Pydantic for models
- Async where possible (`aiohttp`, `asyncpg`)

### Go
- Standard Go conventions (`gofmt`, `go vet`)
- Table-driven tests
- Context propagation
- Error wrapping with `fmt.Errorf("...: %w", err)`

### TypeScript
- Strict mode enabled
- Functional components only
- Tailwind CSS for styling
- Indigo/violet theme (`#818cf8`)

## API Response Format
All API responses follow:
```json
{
  "data": {},
  "error": null,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Environment Variables
- `ETHEREUM_RPC_URL` — Ethereum RPC endpoint
- `ARBITRUM_RPC_URL` — Arbitrum RPC endpoint
- `POLYGON_RPC_URL` — Polygon RPC endpoint
- `BASE_RPC_URL` — Base RPC endpoint
- `AVALANCHE_RPC_URL` — Avalanche RPC endpoint
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- `NEXT_PUBLIC_API_URL` — API base URL for frontend

## Testing
- Python: `pytest` with fixtures and mocks
- Go: `go test ./...` with table-driven tests
- TypeScript: Jest + React Testing Library

## Common Tasks
- `make dev` — run all services locally
- `make test` — run all test suites
- `make lint` — run all linters
- `make build` — build all containers
