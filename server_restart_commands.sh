#!/bin/bash

# Server restart commands
# Run these commands on your server after uploading files

echo "🔄 Restarting server with updated files..."

# Kill existing Daphne process
echo "🛑 Stopping existing server..."
pkill -f daphne

# Wait a moment
sleep 2

# Start server with production settings
echo "🚀 Starting server with production settings..."
cd /root/kip
export DJANGO_SETTINGS_MODULE=backend.settings_production
source venv/bin/activate
daphne -b 0.0.0.0 -p 8010 backend.asgi:application &

echo "✅ Server restarted successfully!"
echo "🌐 Server running on: http://72.60.209.172:8010"
echo "📊 Test endpoint: http://72.60.209.172:8010/api/dashboard/services/"
