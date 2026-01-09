#!/bin/bash
set -e
set -x

# Activate Conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate xtrader-env

echo "Waiting for DB..."
python manage.py wait_for_db

# Wait for the Redis service to be healthy
while ! nc -z redis 6379; do
  echo "Waiting for Redis to be ready..."
  sleep 1
done
echo "Redis is ready! ✅"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
