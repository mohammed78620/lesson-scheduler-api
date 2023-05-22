#!/bin/bash

# Collect static files
echo "Collect static files"
python lesson_scheduler_api/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python lesson_scheduler_api/manage.py migrate --noinput

#Start service
python -Wd lesson_scheduler_api/manage.py runserver 0.0.0.0:8000