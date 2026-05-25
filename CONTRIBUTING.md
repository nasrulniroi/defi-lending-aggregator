# Contributing to DeFi Lending Rate Aggregator

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USER/defi-lending-aggregator.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `make test`
6. Submit a pull request

## Development Setup

```bash
# Install dependencies
make setup

# Start development environment
make dev

# Run tests
make test
```

## Code Standards

### Python
- PEP 8 compliant
- Type hints required on all functions
- Google-style docstrings
- Tests required for new functionality

### Go
- `gofmt` and `golangci-lint` passing
- Table-driven tests
- Context propagation for cancellable operations

### TypeScript
- Strict TypeScript (`strict: true`)
- Functional React components
- Tailwind CSS for styling
- Tests with Jest + React Testing Library

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure CI passes
4. Request review from a maintainer

## Reporting Issues

Use GitHub Issues with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
