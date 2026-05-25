#!/usr/bin/env bash
set -euo pipefail

echo "=== Service Health Check ==="

check_port() {
    local name=$1 port=$2
    if nc -z localhost "$port" 2>/dev/null; then
        echo "✓ $name (port $port) is running"
    else
        echo "✗ $name (port $port) is DOWN"
    fi
}

check_port "Engine API" 8000
check_port "Scanner" 8001
check_port "Frontend" 3000
check_port "PostgreSQL" 5432
check_port "Redis" 6379

echo ""
echo "=== Disk Usage ==="
df -h / | tail -1

echo ""
echo "=== Memory Usage ==="
free -h | head -2
