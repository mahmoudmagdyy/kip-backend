#!/usr/bin/env python3
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/Users/mahmoud/kip')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test_direct_websocket():
    print("🚀 Testing Direct WebSocket Notification")
    print("======================================")
    
    try:
        # Get channel layer
        channel_layer = get_channel_layer()
        print(f"Channel layer: {channel_layer}")
        
        if channel_layer:
            # Test data
            test_data = {
                "id": 999,
                "service_name": "Direct Test Service",
                "booking_date": "2025-10-25",
                "booking_time": "12:00:00",
                "duration_minutes": 60,
                "status": "upcoming",
                "notes": "Direct WebSocket test",
                "created_at": "2025-10-14T11:50:00.000000Z",
                "user_details": {
                    "id": 1,
                    "username": "testuser",
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "test@example.com",
                    "phone": "1234567890",
                    "is_active": True,
                    "date_joined": "2025-10-10T12:00:00.000000Z",
                    "gender": "male",
                    "country": "USA"
                }
            }
            
            print("Sending WebSocket notification...")
            
            # Send WebSocket notification
            async_to_sync(channel_layer.group_send)(
                'admin_bookings',
                {
                    'type': 'booking_created',
                    'data': test_data
                }
            )
            
            print("✅ WebSocket notification sent successfully!")
        else:
            print("❌ No channel layer available")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_direct_websocket()
