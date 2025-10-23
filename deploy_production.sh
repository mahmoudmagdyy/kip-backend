#!/bin/bash

# Production deployment script
echo "Starting production deployment..."

# Set production environment variables
export DJANGO_SETTINGS_MODULE=backend.settings_production
export DEBUG=False

# Install production requirements
echo "Installing production requirements..."
pip install -r requirements_production.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=backend.settings_production

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.settings_production

# Create superuser if needed (optional)
# python manage.py createsuperuser --noinput --settings=backend.settings_production

echo "Production deployment completed!"
echo "Starting server with daphne..."
daphne -b 0.0.0.0 -p $PORT backend.asgi:application
