#!/usr/bin/env python3
"""
Simple WebSocket test to verify notifications work
"""
import asyncio
import websockets
import json
import requests
from datetime import datetime, timedelta

# Configuration
WEBSOCKET_URL = "ws://localhost:8000/ws/admin/bookings/"
API_BASE_URL = "http://localhost:8000/api/"

# Replace with a valid JWT token
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0OTE0MDQwNDYwLCJpYXQiOjE3NjA0NDA0NjAsImp0aSI6IjUwMGM3MzcxNjBjZTQzNTFiNmNlNmJhNmQ4MjcwYTUzIiwidXNlcl9pZCI6IjEifQ.gymeKE8OwHj-lZ-Frjhxo6dOqnPg5kbRMhi8_PVvRhk"
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

async def test_websocket_simple():
    print("🚀 Simple WebSocket Test")
    print("=======================")

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

            # 3. Create a mobile app booking
            print("3. Creating mobile app booking...")
            now = datetime.now()
            booking_date = (now + timedelta(days=5)).strftime('%b %d, %Y')
            booking_time = "12:00 AM"
            
            booking_data = {
                "service_name": "Simple WebSocket Test",
                "booking_date": booking_date,
                "booking_time": booking_time,
                "notes": "Simple WebSocket test"
            }
            
            # Send mobile booking creation request
            response = requests.post(API_BASE_URL + "reserved/", json=booking_data, headers=HEADERS)
            
            if response.status_code in [200, 201]:
                booking_result = response.json()
                print(f"✅ Mobile booking created: {booking_result['data']['id']}")
                
                # Wait for WebSocket notification
                print("4. Waiting for WebSocket notification...")
                try:
                    notification = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    notification_data = json.loads(notification)
                    print(f"🔔 Received notification: {notification_data['type']}")
                    
                    if notification_data['type'] == 'booking_created':
                        print("🎉 SUCCESS: WebSocket notification received!")
                    else:
                        print(f"⚠️  Unexpected notification type: {notification_data['type']}")
                        
                except asyncio.TimeoutError:
                    print("❌ TIMEOUT: No WebSocket notification received within 10 seconds")
                    
            else:
                print(f"❌ Failed to create mobile booking: {response.status_code} - {response.text}")
                
    except websockets.exceptions.ConnectionRefused:
        print("❌ ERROR: Could not connect to WebSocket. Make sure the ASGI server is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_simple())
