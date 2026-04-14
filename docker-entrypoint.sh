#!/usr/bin/env bash

set -e
VENV_PYTHON="/app/.venv/bin/python"

echo "Collect static files"
$VENV_PYTHON lesson_scheduler_api/manage.py collectstatic --noinput

echo "Apply database migrations"
$VENV_PYTHON lesson_scheduler_api/manage.py migrate --noinput


# 👇 THIS LINE IS KEY
exec "$@"