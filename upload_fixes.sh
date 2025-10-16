#!/bin/bash

# Upload Fixed Files to Server
echo "🚀 Uploading fixed files to server..."

# Upload service dashboard fixes
echo "📁 Uploading service dashboard fixes..."
scp core/views_dashboard.py root@72.60.209.172:/root/kip/core/views_dashboard.py

# Upload offer fixes
echo "🎯 Uploading offer fixes..."
scp core/views_admin_offers.py root@72.60.209.172:/root/kip/core/views_admin_offers.py

# Upload public offers fixes
echo "🌐 Uploading public offers fixes..."
scp core/views_public.py root@72.60.209.172:/root/kip/core/views_public.py
scp core/views.py root@72.60.209.172:/root/kip/core/views.py

echo "✅ All fixes uploaded successfully!"
echo "🔄 Please restart the server on the remote machine."
