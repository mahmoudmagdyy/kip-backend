#!/usr/bin/env python3
"""
Test manual WebSocket notification
"""
import asyncio
import websockets
import json
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

async def test_manual_websocket():
    print("🚀 Manual WebSocket Test")
    print("=======================")

    try:
        # 1. Connect to WebSocket
        print("1. Connecting to WebSocket...")
        async with websockets.connect("ws://localhost:8000/ws/admin/bookings/") as websocket:
            print("✅ WebSocket connected successfully!")

            # 2. Request current bookings
            print("2. Requesting current bookings...")
            await websocket.send(json.dumps({"type": "get_bookings"}))
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📊 Received {len(data.get('data', []))} current bookings")

            # 3. Send manual WebSocket notification
            print("3. Sending manual WebSocket notification...")
            channel_layer = get_channel_layer()
            print(f"Channel layer: {channel_layer}")
            
            if channel_layer:
                test_data = {
                    "id": 999,
                    "service_name": "Manual Test",
                    "booking_date": "2025-10-26",
                    "booking_time": "12:00:00",
                    "status": "upcoming",
                    "notes": "Manual WebSocket test"
                }
                
                async_to_sync(channel_layer.group_send)(
                    'admin_bookings',
                    {
                        'type': 'booking_created',
                        'data': test_data
                    }
                )
                print("✅ Manual notification sent")
                
                # Wait for WebSocket notification
                print("4. Waiting for WebSocket notification...")
                try:
                    notification = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    notification_data = json.loads(notification)
                    print(f"🔔 Received notification: {notification_data['type']}")
                    
                    if notification_data['type'] == 'booking_created':
                        print("🎉 SUCCESS: Manual WebSocket notification received!")
                    else:
                        print(f"⚠️  Unexpected notification type: {notification_data['type']}")
                        
                except asyncio.TimeoutError:
                    print("❌ TIMEOUT: No WebSocket notification received within 5 seconds")
            else:
                print("❌ No channel layer available")
                
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_manual_websocket())
