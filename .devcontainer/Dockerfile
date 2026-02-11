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
    docker.io \
    docker-compose \
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

# NOTE: Docker and docker-compose are now installed to enable Docker-in-Docker (DinD).
# The host's Docker socket is mounted to provide access to the Docker daemon.

# Copy project root to /app
COPY . .

# Install backend Python requirements
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Ensure the startup scripts are executable
RUN chmod +x /app/scripts/start-dev-servers.sh
RUN chmod +x /app/scripts/wait-for-db.sh

# Make scripts available in PATH
RUN cp /app/scripts/start-dev-servers.sh /usr/local/bin/ && \
    cp /app/scripts/wait-for-db.sh /usr/local/bin/

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Configure Docker socket permissions
# The docker socket will be mounted from the host
RUN groupadd -f docker 2>/dev/null || true

# Reset working directory to app root
WORKDIR /app
