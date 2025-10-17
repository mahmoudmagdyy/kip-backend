#!/bin/bash

# Upload script for updating server files
# Replace YOUR_SERVER_PASSWORD with your actual server password

SERVER="72.60.209.172"
USER="root"
PROJECT_DIR="/root/kip"

echo "🚀 Uploading updated files to server..."

# Upload core files
echo "📁 Uploading core files..."
scp core/views_dashboard.py $USER@$SERVER:$PROJECT_DIR/core/
scp core/serializer.py $USER@$SERVER:$PROJECT_DIR/core/
scp core/utils.py $USER@$SERVER:$PROJECT_DIR/core/

# Upload backend files
echo "📁 Uploading backend files..."
scp backend/settings_production.py $USER@$SERVER:$PROJECT_DIR/backend/

echo "✅ All files uploaded successfully!"
echo "🔄 Next step: SSH into server and restart the application"
echo ""
echo "To connect to server:"
echo "ssh $USER@$SERVER"
echo ""
echo "To restart server:"
echo "cd $PROJECT_DIR"
echo "pkill -f daphne"
echo "export DJANGO_SETTINGS_MODULE=backend.settings_production && source venv/bin/activate && daphne -b 0.0.0.0 -p 8010 backend.asgi:application"
