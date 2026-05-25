#!/usr/bin/env bash
set -euo pipefail

# Health check for Docker/monitoring
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    echo "Healthy"
    exit 0
else
    echo "Unhealthy (HTTP $HTTP_CODE)"
    exit 1
fi
