#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_URL="${DATABASE_URL:-postgresql://localhost:5432/defi_rates}"

mkdir -p "$BACKUP_DIR"

echo "Backing up database..."
pg_dump "$DB_URL" -Fc -f "$BACKUP_DIR/defi_rates_${TIMESTAMP}.dump"

echo "Backing up config..."
tar czf "$BACKUP_DIR/config_${TIMESTAMP}.tar.gz" config/

# Cleanup old backups (keep 7 days)
find "$BACKUP_DIR" -name "*.dump" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Backup complete: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"/*_${TIMESTAMP}*
