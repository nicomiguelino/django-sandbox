#!/bin/bash

set -euo pipefail

poetry run python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
    poetry run python manage.py createsuperuser --noinput || true

poetry run python manage.py runserver 0.0.0.0:8000
