#!/usr/bin/env python3
"""
Test script to verify WebSocket notifications are working
"""
import asyncio
import websockets
import json
import requests
import time

async def test_websocket_notifications():
    """Test WebSocket connection and booking notifications"""
    
    print("🔴 Testing WebSocket Notifications")
    print("=" * 50)
    
    # WebSocket URL
    websocket_url = "ws://localhost:8000/ws/admin/bookings/"
    
    # API endpoint for creating bookings
    api_url = "http://localhost:8000/api/booking/create/"
    
    # JWT Token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo0OTE0MDM2NjI4LCJpYXQiOjE3NjA0MzY2MjgsImp0aSI6ImM5MGMyN2Q0NjA4NzQyMDM4MzlmOTkzMmMyYmM3ZDdmIiwidXNlcl9pZCI6IjEifQ.zJPx7eGk-b82H_j6co0UO0DijibV4F2tAVEFYBf1L6g"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print("1. Connecting to WebSocket...")
        async with websockets.connect(websocket_url) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Request current bookings
            print("2. Requesting current bookings...")
            await websocket.send(json.dumps({"type": "get_bookings"}))
            
            # Wait for response
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📊 Received {len(data.get('data', []))} current bookings")
            
            # Create a test booking
            print("3. Creating test booking...")
            booking_data = {
                "service_name": "WebSocket Test Service",
                "booking_date": "2025-10-16",
                "booking_time": "16:00",
                "user_id": 1,
                "notes": "WebSocket notification test"
            }
            
            # Send booking creation request
            response = requests.post(api_url, json=booking_data, headers=headers)
            
            if response.status_code in [200, 201]:
                booking_result = response.json()
                print(f"✅ Booking created: {booking_result['data']['id']}")
                
                # Wait for WebSocket notification
                print("4. Waiting for WebSocket notification...")
                try:
                    notification = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    notification_data = json.loads(notification)
                    print(f"🔔 Received notification: {notification_data['type']}")
                    print(f"📝 Notification data: {json.dumps(notification_data, indent=2)}")
                    
                    if notification_data['type'] == 'booking_created':
                        print("🎉 SUCCESS: WebSocket notification received for booking creation!")
                    else:
                        print(f"⚠️  Unexpected notification type: {notification_data['type']}")
                        
                except asyncio.TimeoutError:
                    print("❌ TIMEOUT: No WebSocket notification received within 5 seconds")
                    
            else:
                print(f"❌ Failed to create booking: {response.status_code} - {response.text}")
                
    except websockets.exceptions.ConnectionRefused:
        print("❌ ERROR: Could not connect to WebSocket. Make sure the ASGI server is running.")
        print("   Run: DJANGO_SETTINGS_MODULE=backend.settings python3 -m daphne -b 127.0.0.1 -p 8000 backend.asgi:application")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("🚀 Starting WebSocket Notification Test")
    print("Make sure the ASGI server is running with: python3 -m daphne -b 127.0.0.1 -p 8000 backend.asgi:application")
    print()
    
    asyncio.run(test_websocket_notifications())
