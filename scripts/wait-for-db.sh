#!/usr/bin/env bash
set -euo pipefail

# scripts/wait-for-db.sh
# Wait for the DB host/port extracted from DATABASE_URL to accept TCP connections,
# then exec the given command. This avoids needing psql/pg_isready in the image.

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is not set. Skipping wait." >&2
  exec "$@"
fi

# Extract host and port from DATABASE_URL
# Examples:
# postgresql+asyncpg://user:pass@postgres:5432/recipesdb
# postgresql://user:pass@localhost/recipesdb

DB_HOST=$(echo "$DATABASE_URL" | sed -E 's#^[^:]+://[^@]*@([^:/]+)(:([0-9]+))?/.*#\1#')
DB_PORT=$(echo "$DATABASE_URL" | sed -E 's#^[^:]+://[^@]*@([^:/]+)(:([0-9]+))?/.*#\3#')
DB_PORT=${DB_PORT:-5432}

echo "Waiting for database at $DB_HOST:$DB_PORT"

TRIES=0
MAX=60
SLEEP=1
while true; do
  if bash -c "</dev/tcp/$DB_HOST/$DB_PORT" >/dev/null 2>&1; then
    echo "Database $DB_HOST:$DB_PORT is accepting TCP connections"
    break
  fi
  TRIES=$((TRIES+1))
  if [ "$TRIES" -ge "$MAX" ]; then
    echo "Timed out waiting for database at $DB_HOST:$DB_PORT after $MAX seconds" >&2
    exit 1
  fi
  sleep $SLEEP
done

# Exec the original container command
exec "$@"
