#!/usr/bin/env bash
set -e

echo "Collect static files"
uv run lesson_scheduler_api/manage.py collectstatic --noinput

echo "Apply database migrations"
uv run lesson_scheduler_api/manage.py migrate --noinput


# 👇 THIS LINE IS KEY
exec "$@"