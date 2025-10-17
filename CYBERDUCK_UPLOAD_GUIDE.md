# Cyberduck Upload Guide

## Files to Upload

You need to upload these 4 files to your server:

### 1. Core Files (3 files)
- `core/views_dashboard.py` → Upload to `/root/kip/core/`
- `core/serializer.py` → Upload to `/root/kip/core/`
- `core/utils.py` → Upload to `/root/kip/core/`

### 2. Backend Files (1 file)
- `backend/settings_production.py` → Upload to `/root/kip/backend/`

## Cyberduck Connection Settings

1. **Open Cyberduck**
2. **Click "Open Connection"**
3. **Enter connection details:**
   - **Server**: `72.60.209.172`
   - **Port**: `22`
   - **Username**: `root`
   - **Password**: [Your server password]
   - **Protocol**: SFTP

4. **Click "Connect"**

## Upload Steps

### Step 1: Upload Core Files
1. Navigate to `/root/kip/core/` folder on server
2. Drag and drop these files from your local machine:
   - `core/views_dashboard.py`
   - `core/serializer.py` 
   - `core/utils.py`

### Step 2: Upload Backend Files
1. Navigate to `/root/kip/backend/` folder on server
2. Drag and drop this file from your local machine:
   - `backend/settings_production.py`

### Step 3: Restart Server
After uploading, you need to restart the server. You can do this by:

1. **SSH into your server** (using Cyberduck's terminal or separate SSH client)
2. **Run these commands:**
   ```bash
   cd /root/kip
   pkill -f daphne
   export DJANGO_SETTINGS_MODULE=backend.settings_production
   source venv/bin/activate
   daphne -b 0.0.0.0 -p 8010 backend.asgi:application &
   ```

## Test the Updated Endpoint

After restarting, test the endpoint:
```bash
curl -s http://72.60.209.172:8010/api/dashboard/services/ | python3 -m json.tool
```

You should see the raw array format with correct server URLs!
