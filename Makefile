
.PHONY: build dev up db clean wait-for-postgres

# Build the dev image (using docker compose build dev). This is separate so
# you can rebuild only when Dockerfile or dependencies change.
build:
	@echo "Building dev image (recipes-dev) via docker compose..."
	@if docker compose -f backend/docker-compose.yml version >/dev/null 2>&1; then \
		docker compose -f backend/docker-compose.yml build dev || (echo "docker compose build failed, falling back to docker build" && docker build -f .devcontainer/Dockerfile -t recipes-dev .); \
	elif command -v docker-compose >/dev/null 2>&1; then \
		docker-compose -f backend/docker-compose.yml build dev || (echo "docker-compose build failed, falling back to docker build" && docker build -f .devcontainer/Dockerfile -t recipes-dev .); \
	else \
		echo "No docker compose CLI found, using docker build"; \
		docker build -f .devcontainer/Dockerfile -t recipes-dev .; \
	fi

dev: build up wait-for-postgres
	@echo "Starting dev container (frontend + backend)"
	# Use docker compose to start the dev service so compose manages network and lifecycle
	@echo "Starting 'dev' service via docker compose..."
	@if docker compose -f backend/docker-compose.yml version >/dev/null 2>&1; then \
		docker compose -f backend/docker-compose.yml up -d dev; \
	else \
		docker-compose -f backend/docker-compose.yml up -d dev; \
	fi

up:
	@echo "Starting backend services (Postgres) via docker-compose..."
	./scripts/dev_start.sh


# Wait until Postgres is accepting connections. This uses pg_isready inside the postgres container.
# It supports the 'docker compose' plugin, the standalone 'docker-compose', or falls back to docker exec.
wait-for-postgres:
	@./scripts/wait-for-postgres.sh

db:
	@echo "Open psql client for Postgres"
	# Try docker-compose exec first (safer), fall back to docker exec by container name
	if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then \
		docker-compose -f backend/docker-compose.yml exec -T postgres psql -U recipeuser recipesdb || true; \
	else \
		docker exec -it $$(docker ps -qf "name=postgres") psql -U recipeuser recipesdb || true; \
	fi

clean:
	@echo "Removing dev container"
	docker rm -f recipes-dev-container || true

purge:
	@echo "Stopping compose services and removing volumes (this will delete Postgres data)"
	@if docker compose -f backend/docker-compose.yml version >/dev/null 2>&1; then \
		docker compose -f backend/docker-compose.yml down -v; \
	else \
		docker-compose -f backend/docker-compose.yml down -v; \
	fi

dev-logs:
	@echo "Tailing logs for dev and postgres (ctrl-c to exit)"
	@if docker compose -f backend/docker-compose.yml version >/dev/null 2>&1; then \
		docker compose -f backend/docker-compose.yml logs -f dev postgres; \
	else \
		docker-compose -f backend/docker-compose.yml logs -f dev postgres; \
	fi


.PHONY: smoke-test
smoke-test:
	@./scripts/smoke-test.sh
