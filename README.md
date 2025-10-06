# recipes

## Development

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
