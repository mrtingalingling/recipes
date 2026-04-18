Development workflow

This project uses Docker Compose to run Postgres and a `dev` service that runs
both the backend (FastAPI) and the frontend dev server. VS Code devcontainer
is configured to attach to the same `dev` compose service.

Quick commands

- Start Postgres only:

  ```bash
  make up
  # or
  ./scripts/dev_start.sh
  ```

- Start full dev environment (recommended):

  ```bash
  make dev
  ```

  `make dev` will:
  1. Start the backend services (Postgres) via compose.
  2. Wait until Postgres accepts connections.
  3. Start the `dev` service (builds the dev image if necessary) which runs
     the backend and frontend.

- Tail logs:

  ```bash
  make dev-logs
  ```

- Stop and remove dev container:

  ```bash
  make clean
  ```

- Full reset (DESTROYS Postgres data):

  ```bash
  make purge
  ```

Notes

- The compose file (`backend/docker-compose.yml`) runs Postgres in a container
  and defines a `dev` service. Services discover each other by service name
  (`postgres`) via Docker Compose networking.

- VS Code devcontainer is configured to use Docker Compose (`.devcontainer/devcontainer.json`)
  and will create the same `dev` service when you use 'Reopen in Container'.

- If you run Postgres outside Docker (on the host), set `DATABASE_URL` to point
  to your host database and you can skip `make up`/`make dev` as needed.

Troubleshooting

- If the dev service exits immediately, view logs:

  ```bash
  docker compose -f backend/docker-compose.yml logs --tail=200 dev
  ```

- If `docker compose` is not installed, the scripts will try `docker-compose`.
  Install one of them before running the Makefile targets.

## Devcontainer Startup Flow

When you run the devcontainer in VS Code, here's what happens step-by-step:

### 1. **VS Code Initialization**
- You click "Reopen in Container" in VS Code
- VS Code reads `.devcontainer/devcontainer.json`
- It sees the docker-compose setup and identifies the `dev` service to attach to

### 2. **Docker Compose Startup**
- Docker Compose starts the **postgres** service first
  - Creates a PostgreSQL 15 container
  - Runs healthcheck (`pg_isready`) — waits until it passes
  - Creates a persistent volume (`pgdata`) for the database
  - Listens on port 5432 (inside compose network)

### 3. **Dev Container Build**
- Once postgres is healthy, Docker builds the **dev** service image (if not already built)
  - Uses Dockerfile from `.devcontainer/Dockerfile`
  - Installs Node.js, Python, curl, git, etc.
  - Installs Python dependencies from `backend/requirements.txt`
  - Copies the entire repository into `/app`
  - Installs npm dependencies for the frontend
  - Sets the entrypoint to `/usr/local/bin/wait-for-db.sh`

### 4. **Dev Container Startup**
- The dev container starts and runs the entrypoint script:
  - `wait-for-db.sh` checks if postgres port (5432) is open
  - Once ready, it executes the container's CMD

### 5. **Application Servers Start**
The CMD runs the script that launches two servers in parallel:

**Backend Server (Port 8000):**
```bash
cd /app/backend && uvicorn api_server:app --host 0.0.0.0 --port 8000
```
- FastAPI server with hot-reload enabled
- Connects to postgres on startup via `DATABASE_URL`
- Creates database tables via `Base.metadata.create_all()`
- Ready to serve `/recipes` and other endpoints

**Frontend Dev Server (Port 5173, mapped to 3000):**
```bash
cd /app/frontend && npm run dev -- --host 0.0.0.0
```
- Vite dev server starts
- Hosts the Svelte app with hot module replacement (HMR)
- Port 5173 internally, exposed as 3000 to host
- Loads `src/main.js` → `src/App.svelte` with components

### 6. **VS Code Connects**
- VS Code attaches to the running dev container
- You get a full dev environment with:
  - VS Code editor running inside the container
  - Terminal access to the container
  - Extensions and settings from your config

### 7. **Post-Create Command**
The `postCreateCommand` runs (if it didn't during build):
```bash
pip install -r backend/requirements.txt && (cd frontend && npm install)
```
- Ensures all dependencies are installed
- If you added packages, this keeps things in sync

### 8. **Healthcheck Verification**
- Docker Compose runs the healthcheck on the dev container:
  ```bash
  curl -fsS http://localhost:8000/recipes || exit 1
  ```
- If it returns 200, the container is marked "healthy"

### 9. **Development Ready**
You now have:
- ✅ **Postgres** running in a separate container (mimics remote DB)
- ✅ **Backend API** at `http://localhost:8000` with hot-reload
- ✅ **Frontend** at `http://localhost:3000` with HMR
- ✅ **VS Code editor** inside the container
- ✅ **Port forwarding** so host browser can access the app
- ✅ **Live code editing** — changes reload automatically

### 10. **When You Close VS Code**
- `shutdownAction: stopCompose` kicks in
- All services stop gracefully (postgres saved data to `pgdata` volume)
- Containers are removed
- Network is cleaned up

### 11. **Next Time You Open**
- Docker Compose reuses the `pgdata` volume
- Database state is preserved from last session
- Services start fresh with the same data

## Key Points

- **Postgres is persistent** — data survives container restarts via the `pgdata` volume
- **Code changes sync** — the repo is mounted into `/app`, so edits on your host machine appear immediately in the container
- **Hot reload enabled** — both backend (uvicorn with `--reload`) and frontend (Vite HMR) auto-restart on code changes
- **Isolated network** — postgres, backend, and frontend communicate via docker compose's internal network (`backend_default`)
- **Deployment ready** — the same compose file can also run the `backend` and `frontend` services separately for production


