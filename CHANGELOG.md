# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - 2024-03-15

### Added
- APY Optimizer with risk-adjusted yield scoring
- Rate alert system with configurable thresholds
- Historical rate charts (7d, 30d, 90d)
- Base chain support
- Morpho protocol integration
- Redis caching for rate data

### Changed
- Improved rate fetching reliability with retry logic
- Updated risk model to include utilization factor
- Migrated to Next.js 14 App Router

### Fixed
- Stale rate display on slow networks
- Incorrect borrow APY calculation for variable rate protocols

## [0.4.0] - 2024-02-20

### Added
- Benqi protocol support (Avalanche)
- Radiant protocol support (Arbitrum)
- Protocol health dashboard
- Docker Compose production config

### Changed
- Refactored Go scanner for better chain abstraction
- Improved API response caching (Redis TTL: 30s)

## [0.3.0] - 2024-01-28

### Added
- Multi-chain support (Ethereum, Arbitrum, Polygon, Avalanche)
- Risk calculator with protocol health scoring
- Rate comparison table view
- Database migrations system

### Changed
- Unified rate model across all protocols
- Improved error handling in fetchers

## [0.2.0] - 2024-01-10

### Added
- Compound protocol integration
- Go scanner for on-chain data
- PostgreSQL for rate history
- Basic web dashboard

### Changed
- Separated engine and scanner services
- Added async rate fetching

## [0.1.0] - 2023-12-15

### Added
- Initial project structure
- Aave protocol integration (Ethereum)
- Basic rate fetching engine (Python)
- Next.js web frontend skeleton
- Docker development environment
