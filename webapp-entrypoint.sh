#!/bin/bash

# Check database started
python -c "import utils.wait_database"

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser if not exists
python manage.py shell -c "import utils.init_admin"

# Start server
echo "Starting server"
#python manage.py runserver 0.0.0.0:8083
exec gunicorn --access-logfile - --workers 1 --timeout 30 --bind unix:./webapp.sock webapp.wsgi:application
