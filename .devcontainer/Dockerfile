# Use the official Ubuntu image from the MSFT 
# https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/base/about
# FROM ubuntu:latest
# FROM mcr.microsoft.com/devcontainers/base:ubuntu

ARG VARIANT="22-bookworm"
FROM mcr.microsoft.com/devcontainers/typescript-node:1-${VARIANT}

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends npm

RUN sudo apt-get install gnupg2 -y

# [Optional] Uncomment if you want to install an additional version
#  of node using nvm
ARG EXTRA_NODE_VERSION=18
RUN su node -c "source /usr/local/share/nvm/nvm.sh \
    && nvm install ${EXTRA_NODE_VERSION}"

RUN npm install -g pnpm@latest-10

# COPY ./customScript.sh /tmp/scripts/customScript.sh
# RUN apt-get update && bash /tmp/scripts/customScript.sh

# Copy only the requirements.txt file first
# This allows Docker to cache this layer if requirements.txt doesn't change
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code
COPY . .

# Install Docker Compose
RUN apt-get update && apt-get install -y docker-compose

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Start backend database and frontend server on container start
WORKDIR /app
CMD ["/bin/bash", "-c", "cd backend && docker-compose up -d && cd ../frontend && npm run dev"]
