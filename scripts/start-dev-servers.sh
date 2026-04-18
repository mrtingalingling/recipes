#!/bin/bash

# start-dev-servers.sh
# This script starts the backend (port 8000) and frontend (port 5173) concurrently,
# and ensures the container stays alive as long as they run.

# --- Trap Signal Handlers ---
function cleanup {
  echo "Caught SIGTERM, stopping servers..."
  # Kill the uvicorn and npm processes
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit 0
}
trap cleanup SIGTERM

# --- 1. Start Backend Server (Uvicorn) ---
echo "Starting Backend API on port 8000..."

# CRITICAL FIX: Change directory to /app (the project root) and use package path (backend.api_server)
# This allows Python to treat 'backend' as a package and resolve relative imports like 'from .db import...'
cd /app
uvicorn backend.api_server:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# --- 2. Start Frontend Dev Server ---
echo "Starting Frontend Dev Server on internal port 5173 (mapped externally to 3000)..."
cd /app/frontend
# Running in the background
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# --- 3. Keep the Script Running and Wait ---
wait -n $BACKEND_PID $FRONTEND_PID

if [ $? -ne 0 ]; then
  echo "One of the background servers failed unexpectedly. Exiting."
  exit 1
fi

echo "All services shut down gracefully."
