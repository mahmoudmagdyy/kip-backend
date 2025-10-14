#!/usr/bin/env python3
"""
Test WebSocket notifications for admin bookings
"""
import asyncio
import websockets
import json
import requests
from datetime import datetime, timedelta

# Configuration
WEBSOCKET_URL = "ws://localhost:8000/ws/admin/bookings/"
API_BASE_URL = "http://localhost:8000/api/"
ADMIN_BOOKING_ENDPOINT = API_BASE_URL + "booking/create/"

# Replace with a valid JWT token
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0OTE0MDQwNDYwLCJpYXQiOjE3NjA0NDA0NjAsImp0aSI6IjUwMGM3MzcxNjBjZTQzNTFiNmNlNmJhNmQ4MjcwYTUzIiwidXNlcl9pZCI6IjEifQ.gymeKE8OwHj-lZ-Frjhxo6dOqnPg5kbRMhi8_PVvRhk"
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

async def test_admin_websocket_notifications():
    print("🚀 Testing Admin WebSocket Notifications")
    print("=======================================")

    try:
        # 1. Connect to WebSocket
        print("1. Connecting to WebSocket...")
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✅ WebSocket connected successfully!")

            # 2. Request current bookings
            print("2. Requesting current bookings...")
            await websocket.send(json.dumps({"type": "get_bookings"}))
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📊 Received {len(data.get('data', []))} current bookings")

            # 3. Create an admin booking
            print("3. Creating admin booking...")
            now = datetime.now()
            booking_date = (now + timedelta(days=10)).strftime('%Y-%m-%d')
            booking_time = "16:00"
            
            booking_data = {
                "service_name": "WebSocket Admin Test",
                "booking_date": booking_date,
                "booking_time": booking_time,
                "user_id": 1,
                "notes": "WebSocket notification test from admin"
            }
            
            # Send admin booking creation request
            response = requests.post(ADMIN_BOOKING_ENDPOINT, json=booking_data, headers=HEADERS)
            
            if response.status_code in [200, 201]:
                booking_result = response.json()
                print(f"✅ Admin booking created: {booking_result['data']['id']}")
                
                # Wait for WebSocket notification
                print("4. Waiting for WebSocket notification...")
                try:
                    notification = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    notification_data = json.loads(notification)
                    print(f"🔔 Received notification: {notification_data['type']}")
                    print(f"📝 Notification data: {json.dumps(notification_data, indent=2)}")
                    
                    if notification_data['type'] == 'booking_created':
                        print("🎉 SUCCESS: WebSocket notification received for admin booking!")
                    else:
                        print(f"⚠️  Unexpected notification type: {notification_data['type']}")
                        
                except asyncio.TimeoutError:
                    print("❌ TIMEOUT: No WebSocket notification received within 5 seconds")
                    
            else:
                print(f"❌ Failed to create admin booking: {response.status_code} - {response.text}")
                
    except websockets.exceptions.ConnectionRefused:
        print("❌ ERROR: Could not connect to WebSocket. Make sure the ASGI server is running.")
        print("   Run: DJANGO_SETTINGS_MODULE=backend.settings python3 -m daphne -b 127.0.0.1 -p 8000 backend.asgi:application")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_admin_websocket_notifications())
