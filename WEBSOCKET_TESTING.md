# 🔌 WebSocket Real-time Testing Guide

## **📋 Complete WebSocket Testing Instructions**

### **🌐 WebSocket Connection Details**

**WebSocket URL:** `ws://localhost:8000/ws/admin/bookings/`

---

### **🧪 Method 1: Browser Console Testing**

#### **Step 1: Open Browser Console**
1. Open your browser (Chrome, Firefox, Safari)
2. Go to `http://localhost:8000/test/` or any page
3. Press `F12` to open Developer Tools
4. Go to the **Console** tab

#### **Step 2: Connect to WebSocket**
```javascript
// Create WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/admin/bookings/');

// Connection event handlers
ws.onopen = function(event) {
    console.log('✅ WebSocket Connected!');
    console.log('Connection opened:', event);
    
    // Request current bookings
    ws.send(JSON.stringify({
        type: 'get_bookings'
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('📨 Message received:', data);
    
    // Handle different message types
    switch(data.type) {
        case 'booking_created':
            console.log('🆕 New booking created:', data.data);
            console.log('User:', data.data.user_details.first_name, data.data.user_details.last_name);
            console.log('Service:', data.data.service_name);
            console.log('Date:', data.data.booking_date, 'at', data.data.booking_time);
            break;
            
        case 'booking_updated':
            console.log('✏️ Booking updated:', data.data);
            break;
            
        case 'booking_deleted':
            console.log('🗑️ Booking deleted:', data.data);
            break;
            
        case 'bookings_data':
            console.log('📊 Bookings data:', data.data);
            console.log('Total bookings:', data.data.length);
            break;
            
        default:
            console.log('❓ Unknown message type:', data.type);
    }
};

ws.onclose = function(event) {
    console.log('❌ WebSocket Disconnected');
    console.log('Close code:', event.code);
    console.log('Close reason:', event.reason);
};

ws.onerror = function(error) {
    console.error('💥 WebSocket Error:', error);
};
```

#### **Step 3: Test Real-time Updates**
1. Keep the console open
2. Open another browser tab
3. Go to `http://localhost:8000/test/`
4. Create a booking using the form
5. **Watch the console!** You should see the real-time notification**

---

### **🧪 Method 2: Postman WebSocket Testing**

#### **Step 1: Open Postman**
1. Open Postman
2. Click **New** → **WebSocket Request**
3. Enter URL: `ws://localhost:8000/ws/admin/bookings/`
4. Click **Connect**

#### **Step 2: Send Test Messages**
```json
{
    "type": "get_bookings"
}
```

#### **Step 3: Monitor Messages**
- You'll see incoming messages in the **Messages** tab
- Each message will show the real-time booking updates

---

### **🧪 Method 3: wscat Command Line Testing**

#### **Step 1: Install wscat**
```bash
# Install wscat globally
npm install -g wscat
```

#### **Step 2: Connect to WebSocket**
```bash
# Connect to WebSocket
wscat -c ws://localhost:8000/ws/admin/bookings/
```

#### **Step 3: Send Test Messages**
```bash
# Send message to request bookings
{"type": "get_bookings"}
```

#### **Step 4: Monitor Real-time Updates**
- Keep wscat running
- Create bookings from another terminal or browser
- Watch the real-time messages appear

---

### **🧪 Method 4: Custom HTML Test Page**

#### **Step 1: Create Test HTML File**
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .connected { background: #d4edda; color: #155724; }
        .disconnected { background: #f8d7da; color: #721c24; }
        .message { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 4px solid #007bff; }
        .booking { background: #d1ecf1; border-left-color: #17a2b8; }
        .error { background: #f8d7da; border-left-color: #dc3545; }
        button { padding: 10px 20px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        #messages { max-height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
    <h1>WebSocket Real-time Test</h1>
    
    <div id="status" class="status disconnected">
        Disconnected
    </div>
    
    <div>
        <button onclick="connect()">Connect</button>
        <button onclick="disconnect()">Disconnect</button>
        <button onclick="requestBookings()">Request Bookings</button>
        <button onclick="clearMessages()">Clear Messages</button>
    </div>
    
    <div id="messages"></div>

    <script>
        let ws = null;

        function connect() {
            if (ws) {
                ws.close();
            }
            
            ws = new WebSocket('ws://localhost:8000/ws/admin/bookings/');
            
            ws.onopen = function(event) {
                updateStatus('Connected', 'connected');
                addMessage('WebSocket connected successfully', 'info');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
            
            ws.onclose = function(event) {
                updateStatus('Disconnected', 'disconnected');
                addMessage(`WebSocket disconnected. Code: ${event.code}`, 'error');
            };
            
            ws.onerror = function(error) {
                addMessage(`WebSocket error: ${error}`, 'error');
            };
        }

        function disconnect() {
            if (ws) {
                ws.close();
            }
        }

        function requestBookings() {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'get_bookings'
                }));
                addMessage('Requested bookings data', 'info');
            } else {
                addMessage('WebSocket not connected', 'error');
            }
        }

        function handleMessage(data) {
            switch(data.type) {
                case 'booking_created':
                    addMessage(`🆕 NEW BOOKING: ${data.data.user_details.first_name} ${data.data.user_details.last_name} booked ${data.data.service_name} for ${data.data.booking_date} at ${data.data.booking_time}`, 'booking');
                    break;
                case 'booking_updated':
                    addMessage(`✏️ BOOKING UPDATED: ${data.data.user_details.first_name} ${data.data.user_details.last_name}`, 'booking');
                    break;
                case 'booking_deleted':
                    addMessage(`🗑️ BOOKING DELETED: ${data.data.user_details.first_name} ${data.data.user_details.last_name}`, 'booking');
                    break;
                case 'bookings_data':
                    addMessage(`📊 BOOKINGS DATA: Received ${data.data.length} bookings`, 'info');
                    break;
                default:
                    addMessage(`❓ Unknown message: ${data.type}`, 'error');
            }
        }

        function updateStatus(text, className) {
            const status = document.getElementById('status');
            status.textContent = text;
            status.className = `status ${className}`;
        }

        function addMessage(text, type) {
            const messages = document.getElementById('messages');
            const message = document.createElement('div');
            message.className = `message ${type}`;
            message.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
            messages.appendChild(message);
            messages.scrollTop = messages.scrollHeight;
        }

        function clearMessages() {
            document.getElementById('messages').innerHTML = '';
        }

        // Auto-connect on page load
        window.onload = function() {
            connect();
        };
    </script>
</body>
</html>
```

#### **Step 2: Save and Open**
1. Save the HTML code above as `websocket_test.html`
2. Open it in your browser
3. Click **Connect** to establish WebSocket connection
4. Click **Request Bookings** to get current data

---

### **🧪 Method 5: Python WebSocket Client**

#### **Step 1: Install websockets**
```bash
pip install websockets
```

#### **Step 2: Create Python Test Script**
```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/admin/bookings/"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket Connected!")
            
            # Request bookings
            await websocket.send(json.dumps({"type": "get_bookings"}))
            print("📤 Sent: get_bookings request")
            
            # Listen for messages
            async for message in websocket:
                data = json.loads(message)
                print(f"📨 Received: {data['type']}")
                
                if data['type'] == 'booking_created':
                    booking = data['data']
                    print(f"🆕 NEW BOOKING:")
                    print(f"   User: {booking['user_details']['first_name']} {booking['user_details']['last_name']}")
                    print(f"   Service: {booking['service_name']}")
                    print(f"   Date: {booking['booking_date']} at {booking['booking_time']}")
                    print()
                
                elif data['type'] == 'booking_updated':
                    print(f"✏️ BOOKING UPDATED: {data['data']['user_details']['first_name']}")
                
                elif data['type'] == 'booking_deleted':
                    print(f"🗑️ BOOKING DELETED: {data['data']['user_details']['first_name']}")
                
                elif data['type'] == 'bookings_data':
                    print(f"📊 BOOKINGS DATA: {len(data['data'])} bookings received")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

# Run the test
asyncio.run(test_websocket())
```

#### **Step 3: Run the Script**
```bash
python websocket_test.py
```

---

### **🎯 Complete Testing Workflow**

#### **Step 1: Start the Server**
```bash
cd /Users/mahmoud/kip
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

#### **Step 2: Open WebSocket Connection**
- Use any of the methods above to connect to WebSocket
- You should see "Connected" status

#### **Step 3: Create a Test Booking**
```bash
# Create a booking using curl
curl -X POST http://localhost:8000/api/booking/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "service_name": "Test Service",
    "booking_date": "2025-10-15",
    "booking_time": "14:00",
    "notes": "WebSocket test booking"
  }'
```

#### **Step 4: Watch Real-time Updates**
- **Immediately** after creating the booking, you should see:
  - WebSocket message: `booking_created`
  - Real-time notification in your WebSocket client
  - Booking appears in admin dashboard without refresh

#### **Step 5: Test Multiple Connections**
1. Open multiple WebSocket connections (different browser tabs)
2. Create a booking from one connection
3. **All other connections** should receive the notification instantly

---

### **🔍 Expected WebSocket Messages**

#### **Connection Established:**
```json
{
    "type": "connection_established",
    "message": "Connected to admin bookings room"
}
```

#### **New Booking Created:**
```json
{
    "type": "booking_created",
    "data": {
        "id": 15,
        "user_id": 1,
        "service_name": "Test Service",
        "booking_date": "2025-10-15",
        "booking_time": "14:00",
        "duration_minutes": 60,
        "status": "upcoming",
        "notes": "WebSocket test booking",
        "created_at": "2025-10-13T06:30:45.123456+00:00",
        "user_details": {
            "id": 1,
            "username": "1234567890",
            "first_name": "John",
            "last_name": "Doe",
            "email": "1234567890",
            "phone": "1234567890",
            "is_active": true,
            "date_joined": "2025-10-10T12:42:51.949986Z",
            "gender": "male",
            "country": "Egypt"
        }
    }
}
```

#### **Booking Updated:**
```json
{
    "type": "booking_updated",
    "data": {
        "id": 15,
        "status": "completed",
        "user_details": { ... }
    }
}
```

#### **Booking Deleted:**
```json
{
    "type": "booking_deleted",
    "data": {
        "id": 15,
        "user_details": { ... }
    }
}
```

---

### **🚨 Troubleshooting**

#### **Connection Failed:**
- Check if Django server is running on port 8000
- Verify WebSocket URL: `ws://localhost:8000/ws/admin/bookings/`
- Check browser console for CORS errors

#### **No Real-time Updates:**
- Ensure WebSocket connection is established
- Check if booking creation was successful
- Verify WebSocket message handlers are working

#### **WebSocket Disconnects:**
- Check network connection
- Verify server is still running
- Check for firewall issues

**Your real-time WebSocket system is ready for comprehensive testing! 🚀**
