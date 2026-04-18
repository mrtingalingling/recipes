#!/usr/bin/env bash
set -euo pipefail

# scripts/smoke-test.sh
# Wait for 'dev' service to be healthy and run simple curl checks against
# backend and frontend.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/backend/docker-compose.yml"
TIMEOUT=${TIMEOUT:-60}
SLEEP=${SLEEP:-1}

echo "Running smoke tests against backend and frontend"

ELAPSED=0
while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  # check if dev service container exists
  CID=$(docker compose -f "$COMPOSE_FILE" ps -q dev 2>/dev/null || true)
  if [ -n "$CID" ]; then
    # get health status if present
    STATE=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}unknown{{end}}' "$CID" 2>/dev/null || true)
    if [ "$STATE" = "healthy" ] || [ "$STATE" = "unknown" ]; then
      echo "dev service state: $STATE"
      break
    fi
  fi
  sleep "$SLEEP"
  ELAPSED=$((ELAPSED+SLEEP))
done

if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
  echo "Timed out waiting for dev service to become healthy" >&2
  exit 1
fi

# Run backend check
if curl -fsS http://localhost:8000/recipes >/dev/null 2>&1; then
  echo "Backend /recipes OK"
else
  echo "Backend /recipes FAILED" >&2
  exit 2
fi

# Run frontend check
if curl -fsS http://localhost:3000/ >/dev/null 2>&1; then
  echo "Frontend root OK"
else
  echo "Frontend root FAILED" >&2
  exit 3
fi
