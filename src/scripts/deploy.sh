#!/usr/bin/env bash
set -euo pipefail

echo "=== Deploying DeFi Lending Aggregator ==="

# Build frontend
echo "Building frontend..."
cd src/web && npm run build && cd ../..

# Build scanner
echo "Building scanner..."
cd src/scanner && go build -o ../../bin/scanner main.go && cd ../..

# Run migrations
if [ -n "${DATABASE_URL:-}" ]; then
    echo "Running migrations..."
    for f in src/db/migrations/*.sql; do
        psql "$DATABASE_URL" -f "$f"
    done
fi

echo "Build complete. Starting services..."

# Start engine
cd src/engine && python main.py &
ENGINE_PID=$!

# Start scanner
../../bin/scanner serve &
SCANNER_PID=$!

# Start frontend
cd ../web && npm start &
WEB_PID=$!

echo "All services started (PIDs: $ENGINE_PID, $SCANNER_PID, $WEB_PID)"
wait
