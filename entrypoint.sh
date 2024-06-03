#!/bin/sh

echo "Make migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate

echo "Seeding database..."
python manage.py seed

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 bookLand_microservice.wsgi:application