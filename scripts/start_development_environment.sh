#!/bin/bash

set -euo pipefail

COMPOSE_PROFILES=dev

docker compose down
docker compose build
docker compose up -d
