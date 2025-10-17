#!/bin/bash

# Server restart script for after Cyberduck upload
# Run this on your server after uploading files via Cyberduck

echo "🔄 Restarting server with updated files..."

# Navigate to project directory
cd /root/kip

# Kill existing Daphne process
echo "🛑 Stopping existing server..."
pkill -f daphne

# Wait a moment for process to stop
sleep 3

# Start server with production settings
echo "🚀 Starting server with production settings..."
export DJANGO_SETTINGS_MODULE=backend.settings_production
source venv/bin/activate
daphne -b 0.0.0.0 -p 8010 backend.asgi:application &

echo "✅ Server restarted successfully!"
echo "🌐 Server running on: http://72.60.209.172:8010"
echo "📊 Test endpoint: http://72.60.209.172:8010/api/dashboard/services/"

# Show server status
sleep 2
echo ""
echo "📋 Server Status:"
ps aux | grep daphne | grep -v grep
