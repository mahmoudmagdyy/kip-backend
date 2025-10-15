# 🌐 WebSocket Configuration for Render.com

## 🔧 **Current WebSocket Setup**

Your WebSocket is already configured in the code, but needs proper deployment settings.

## ✅ **Step 1: Check Current Configuration**

### **In `backend/settings_production.py`:**
```python
# Channels configuration for production
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
```

### **In `backend/asgi.py`:**
```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django ASGI application early
django_asgi_app = get_asgi_application()

# Import routing after Django is set up
import core.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})
```

### **In `core/routing.py`:**
```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/admin/bookings/$', consumers.BookingConsumer.as_asgi()),
]
```

## 🚀 **Step 2: Configure Render.com for WebSocket**

### **Update Build Command:**
```bash
mkdir -p media/offers media/uploads media/users && chmod 755 media && chmod 755 media/offers && chmod 755 media/uploads && chmod 755 media/users && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
```

### **Update Start Command:**
```bash
daphne -b 0.0.0.0 -p $PORT backend.asgi:application
```

### **Set Environment Variables:**
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=kip-backend.onrender.com
```

## 🧪 **Step 3: Test WebSocket Connection**

### **Test 1: Basic Connection**
```javascript
// Test WebSocket connection
const ws = new WebSocket('wss://kip-backend.onrender.com/ws/admin/bookings/');

ws.onopen = function() {
    console.log('WebSocket connected!');
    // Send a test message
    ws.send(JSON.stringify({type: 'get_bookings'}));
};

ws.onmessage = function(event) {
    console.log('Message received:', event.data);
};

ws.onerror = function(error) {
    console.log('WebSocket error:', error);
};

ws.onclose = function() {
    console.log('WebSocket disconnected');
};
```

### **Test 2: Using curl**
```bash
# Test WebSocket endpoint
curl -I "https://kip-backend.onrender.com/ws/admin/bookings/"
```

### **Test 3: Create Test HTML Page**
Create a file called `websocket_test.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>WebSocket Test</h1>
    <div id="status">Connecting...</div>
    <div id="messages"></div>
    
    <script>
        const ws = new WebSocket('wss://kip-backend.onrender.com/ws/admin/bookings/');
        const status = document.getElementById('status');
        const messages = document.getElementById('messages');
        
        ws.onopen = function() {
            status.textContent = 'Connected!';
            ws.send(JSON.stringify({type: 'get_bookings'}));
        };
        
        ws.onmessage = function(event) {
            const message = document.createElement('div');
            message.textContent = 'Received: ' + event.data;
            messages.appendChild(message);
        };
        
        ws.onerror = function(error) {
            status.textContent = 'Error: ' + error;
        };
        
        ws.onclose = function() {
            status.textContent = 'Disconnected';
        };
    </script>
</body>
</html>
```

## 🔧 **Step 4: Alternative WebSocket Configuration**

### **Option 1: Use Redis (If Available)**
```python
# In settings_production.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```

### **Option 2: Use InMemoryChannelLayer (Current)**
```python
# In settings_production.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
```

## 🧪 **Step 5: Test WebSocket Functionality**

### **Test Real-time Notifications:**
```bash
# Create a booking to test WebSocket
curl -X POST "https://kip-backend.onrender.com/api/agent/booking/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "1234567890",
    "service_name": "Test Service",
    "booking_date": "2025-10-20",
    "booking_time": "14:00"
  }'
```

### **Test WebSocket Response:**
The WebSocket should receive a `booking_created` message with the booking data.

## 📋 **Step 6: Troubleshooting**

### **If WebSocket Doesn't Connect:**

1. **Check Render.com logs** for errors
2. **Verify start command** uses Daphne
3. **Check environment variables** are set
4. **Test with different WebSocket URL**

### **If WebSocket Connects But No Messages:**

1. **Check if booking creation** sends notifications
2. **Verify WebSocket consumer** is working
3. **Test with different message types**

### **If WebSocket Disconnects:**

1. **Check for timeout issues**
2. **Verify WebSocket URL** is correct
3. **Test with different browsers**

## 🚀 **Step 7: Production WebSocket URL**

Your WebSocket will be available at:
```
wss://kip-backend.onrender.com/ws/admin/bookings/
```

## 📋 **Complete WebSocket Setup Checklist**

- [ ] **Daphne server** is running (not Gunicorn)
- [ ] **ASGI configuration** is correct
- [ ] **Channel layers** are configured
- [ ] **WebSocket routing** is set up
- [ ] **Environment variables** are set
- [ ] **Build command** includes all dependencies
- [ ] **Start command** uses Daphne
- [ ] **WebSocket URL** is accessible

## 🎯 **Quick Test Commands**

### **Test WebSocket Endpoint:**
```bash
curl -I "https://kip-backend.onrender.com/ws/admin/bookings/"
```

### **Test WebSocket with wscat:**
```bash
# Install wscat
npm install -g wscat

# Connect to WebSocket
wscat -c wss://kip-backend.onrender.com/ws/admin/bookings/
```

### **Test WebSocket in Browser:**
```javascript
const ws = new WebSocket('wss://kip-backend.onrender.com/ws/admin/bookings/');
ws.onopen = () => console.log('Connected!');
ws.onmessage = (event) => console.log('Message:', event.data);
```

## 🚀 **Ready to Deploy!**

Your WebSocket is now properly configured for Render.com deployment! 🎯
