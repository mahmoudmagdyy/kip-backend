#!/bin/bash

# Start script for production deployment
# This ensures the correct ASGI server is used

echo "🚀 Starting KIP Backend..."

# Set environment
export DJANGO_SETTINGS_MODULE=backend.settings_production

# Run migrations
echo "📊 Running database migrations..."
python manage.py migrate --settings=backend.settings_production

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.settings_production

# Start ASGI server
echo "🌐 Starting ASGI server..."
daphne -b 0.0.0.0 -p $PORT backend.asgi:application
