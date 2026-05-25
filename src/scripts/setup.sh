#!/usr/bin/env bash
set -euo pipefail

echo "=== DeFi Lending Aggregator Setup ==="

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js required"; exit 1; }
command -v go >/dev/null 2>&1 || { echo "Go required"; exit 1; }

# Python dependencies
echo "Installing Python dependencies..."
cd src/engine && pip install -r ../../requirements.txt && cd ../..

# Node dependencies
echo "Installing Node dependencies..."
cd src/web && npm install && cd ../..

# Go dependencies
echo "Installing Go dependencies..."
cd src/scanner && go mod download && cd ../..

# Database setup
if command -v psql >/dev/null 2>&1; then
    echo "Setting up database..."
    psql "${DATABASE_URL:-postgresql://localhost:5432/defi_rates}" -f src/db/schema.sql
    psql "${DATABASE_URL:-postgresql://localhost:5432/defi_rates}" -f src/db/seed.sql
fi

echo "Setup complete!"
