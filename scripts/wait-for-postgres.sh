#!/usr/bin/env bash
set -euo pipefail

# scripts/wait-for-postgres.sh
# Wait for Postgres inside the compose postgres container to be ready using pg_isready.
# Supports 'docker compose' plugin, 'docker-compose', or fallback to 'docker exec'.

COMPOSE_FILE="$(cd "$(dirname "$0")/.." && pwd)/backend/docker-compose.yml"
MAX=${MAX:-60}
SLEEP=${SLEEP:-1}
TRIES=0

echo "Waiting for Postgres to become ready (max $MAX seconds)..."

while true; do
  # prefer docker compose exec
  if docker compose -f "$COMPOSE_FILE" version >/dev/null 2>&1; then
    if docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U recipeuser -d recipesdb >/dev/null 2>&1; then
      echo "Postgres is ready (via docker compose exec)"
      exit 0
    fi
  elif command -v docker-compose >/dev/null 2>&1; then
    if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U recipeuser -d recipesdb >/dev/null 2>&1; then
      echo "Postgres is ready (via docker-compose exec)"
      exit 0
    fi
  else
    # fallback to docker exec by container name
    POST_CID=$(docker ps -qf "name=postgres" || true)
    if [ -n "$POST_CID" ]; then
      if docker exec -i "$POST_CID" pg_isready -U recipeuser -d recipesdb >/dev/null 2>&1; then
        echo "Postgres is ready (via docker exec)"
        exit 0
      fi
    else
      echo "Postgres container not found yet"
    fi
  fi

  TRIES=$((TRIES+1))
  if [ "$TRIES" -ge "$MAX" ]; then
    echo "Timed out waiting for Postgres after $MAX seconds" >&2
    exit 1
  fi
  sleep "$SLEEP"
done
