# Use the official Universal Development image from the MSFT 
# https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/base/about
FROM mcr.microsoft.com/devcontainers/universal

# Set the working directory in the container
WORKDIR /app

# Combine installs into one layer and clean up
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    npm \
    python3 \
    python3-pip \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN sudo apt-get install gnupg2 -y

# [Optional] Uncomment if you want to install an additional version
#  of node using nvm
# ARG EXTRA_NODE_VERSION=18
# RUN su node -c "source /usr/local/share/nvm/nvm.sh \
#     && nvm install ${EXTRA_NODE_VERSION}"

# COPY ./customScript.sh /tmp/scripts/customScript.sh
# RUN apt-get update && bash /tmp/scripts/customScript.sh

# Install pnpm globally
RUN npm install -g pnpm@latest-10

# NOTE: We do NOT install Docker or docker-compose inside the devcontainer image.
# Installing Docker in a container often causes package conflicts and is unnecessary
# for development. Use the host to run `docker-compose` (see scripts/dev_start.sh).

# Copy only the backend requirements.txt first (build context is repository root)
# This allows Docker to cache this layer if requirements.txt doesn't change
# Copies to /app/backend/requirements.txt (relative to WORKDIR)
COPY backend/requirements.txt backend/requirements.txt

# Install backend Python requirements
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of your application's source code
COPY . .

# Ensure the concurrent startup script is copied and made executable
# Source path is relative to the build context (project root)
COPY scripts/start-dev-servers.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-dev-servers.sh

# Copy wait-for-db script and make it executable
COPY scripts/wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Start backend (uvicorn) and frontend dev server when the container runs.
WORKDIR /app
# Use the wait-for-db entrypoint to wait for DB, then run the default CMD
ENTRYPOINT ["/usr/local/bin/wait-for-db.sh"]
CMD ["/bin/bash", "-c", "cd backend && uvicorn api_server:app --host 0.0.0.0 --port 8000 &\ncd ../frontend && npm run dev -- --host 0.0.0.0"]
