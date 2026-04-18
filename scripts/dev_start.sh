#!/usr/bin/env bash
set -euo pipefail

# scripts/dev_start.sh
# Run backend docker-compose on the host if docker/docker-compose is available.
# If not available, print instructions.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/backend/docker-compose.yml"

echo "Checking for docker on host..."
if command -v docker >/dev/null 2>&1; then
  echo "Found docker"
else
  echo "Docker CLI not found on host. Please install Docker to run docker-compose services." >&2
  exit 1
fi

# Prefer 'docker compose' (plugin) if available, else try 'docker-compose' binary
if docker compose version >/dev/null 2>&1; then
  echo "Using 'docker compose' to bring up services from $COMPOSE_FILE"
  docker compose -f "$COMPOSE_FILE" up -d
  exit 0
fi

if command -v docker-compose >/dev/null 2>&1; then
  echo "Using 'docker-compose' to bring up services from $COMPOSE_FILE"
  docker-compose -f "$COMPOSE_FILE" up -d
  exit 0
fi

echo "Neither 'docker compose' nor 'docker-compose' found, but docker CLI is present."
echo "If you have Docker Compose as a plugin, ensure it's enabled, or install the standalone 'docker-compose'."
echo "You can still start services manually with: docker compose -f $COMPOSE_FILE up -d"
exit 1
