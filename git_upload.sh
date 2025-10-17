#!/bin/bash

# Git upload method - Recommended
echo "🚀 Using Git to upload changes..."

# Commit changes locally
echo "📝 Committing changes locally..."
git add core/views_dashboard.py core/serializer.py core/utils.py backend/settings_production.py
git commit -m "Update dashboard services endpoint and icon URL handling

- Modified dashboard_services to return raw array format
- Added get_server_media_url function to utils.py
- Updated serializers to handle icon URLs properly
- Added SERVER_DOMAIN and SERVER_PROTOCOL to production settings"

# Push to remote repository
echo "📤 Pushing to remote repository..."
git push origin main

echo "✅ Changes pushed to repository!"
echo ""
echo "🔄 Next: SSH into server and pull changes:"
echo "ssh root@72.60.209.172"
echo "cd /root/kip"
echo "git pull origin main"
echo "pkill -f daphne"
echo "export DJANGO_SETTINGS_MODULE=backend.settings_production && source venv/bin/activate && daphne -b 0.0.0.0 -p 8010 backend.asgi:application"
