#!/bin/bash

set -euo pipefail

if [[ ! -f client_secrets.json ]]; then
    echo "client_secrets.json not found. Please create one and put it in the project root directory."
    exit 1
fi

COMPOSE_PROFILES=dev

docker compose down
docker compose build
docker compose up -d
