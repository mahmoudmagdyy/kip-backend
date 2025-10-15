#!/bin/bash

# Build script for Render.com deployment
# This script handles the Pillow installation issue

echo "🚀 Starting build process..."

# Upgrade pip first
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install system dependencies for Pillow
echo "🔧 Installing system dependencies..."
apt-get update
apt-get install -y libjpeg-dev zlib1g-dev libpng-dev

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=backend.settings_production

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.settings_production

echo "✅ Build completed successfully!"
