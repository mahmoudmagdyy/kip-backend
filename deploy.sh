#!/bin/bash

# Deployment script for KIP Backend
# This script prepares the project for production deployment

echo "🚀 Starting deployment preparation..."

# Set environment
export DJANGO_SETTINGS_MODULE=backend.settings_production

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_production.txt

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=backend.settings_production

# Create superuser (optional)
echo "👤 Creating superuser..."
python manage.py shell --settings=backend.settings_production << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.settings_production

# Create initial data
echo "📊 Creating initial data..."
python manage.py shell --settings=backend.settings_production << EOF
from core.models import BookingSettings
if not BookingSettings.objects.exists():
    BookingSettings.objects.create(
        WORKING_HOURS_START=12,
        WORKING_HOURS_END=17,
        DEFAULT_RESERVATION_DURATION_MINUTES=60,
        OFF_DAYS='s',  # Sunday
        is_active=True
    )
    print('Booking settings created')
else:
    print('Booking settings already exist')
EOF

# Set permissions
echo "🔐 Setting permissions..."
chmod 755 logs
chmod 755 staticfiles
chmod 755 media

echo "✅ Deployment preparation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Set environment variables in your deployment platform"
echo "2. Configure your database URL"
echo "3. Set up Redis for WebSocket support"
echo "4. Configure your domain in ALLOWED_HOSTS"
echo "5. Set up SSL certificates"
echo ""
echo "🌐 Your application is ready for deployment!"
