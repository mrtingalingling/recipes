#!/bin/bash

# Start MCP Server for recipes application
# Usage: ./scripts/start-mcp-server.sh [--dev]

set -e

HOST=${MCP_HOST:-localhost}
PORT=${MCP_PORT:-3001}

if [ "$1" == "--dev" ]; then
    echo "Starting MCP Server in development mode on $HOST:$PORT with auto-reload..."
    python -m uvicorn backend.mcp.server:app --reload --host "$HOST" --port "$PORT"
else
    echo "Starting MCP Server on $HOST:$PORT..."
    python -m backend.mcp.server
fi
