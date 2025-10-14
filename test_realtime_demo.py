#!/usr/bin/env python3
"""
Real-time Booking Demo Script
This script demonstrates how to create bookings that will trigger WebSocket notifications
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta

# Server configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/booking/create/"

# Sample booking data
SAMPLE_BOOKINGS = [
    {
        "service_name": "Hair Cut",
        "booking_date": "Dec 15, 2024",
        "booking_time": "10:00 AM",
        "notes": "Regular trim and styling"
    },
    {
        "service_name": "Facial Treatment",
        "booking_date": "Dec 16, 2024", 
        "booking_time": "2:00 PM",
        "notes": "Deep cleansing facial"
    },
    {
        "service_name": "Massage",
        "booking_date": "Dec 17, 2024",
        "booking_time": "3:00 PM",
        "notes": "Relaxing full body massage"
    },
    {
        "service_name": "Hair Coloring",
        "booking_date": "Dec 18, 2024",
        "booking_time": "11:00 AM",
        "notes": "Highlights and color treatment"
    },
    {
        "service_name": "Manicure",
        "booking_date": "Dec 19, 2024",
        "booking_time": "4:00 PM",
        "notes": "French manicure with nail art"
    }
]

def create_booking(booking_data):
    """Create a booking via API"""
    try:
        print(f"📤 Creating booking: {booking_data['service_name']} on {booking_data['booking_date']} at {booking_data['booking_time']}")
        
        response = requests.post(API_ENDPOINT, json=booking_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Booking created successfully! ID: {result.get('data', {}).get('id', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to create booking: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_realtime_bookings():
    """Demonstrate real-time booking creation"""
    print("🚀 Real-time Booking Demo")
    print("=" * 50)
    print("This script will create bookings that should appear instantly in your dashboard!")
    print("Make sure you have the dashboard open at: http://localhost:8000/static/test_dashboard.html")
    print()
    
    input("Press Enter to start creating bookings...")
    
    for i, booking in enumerate(SAMPLE_BOOKINGS, 1):
        print(f"\n📋 Creating booking {i}/{len(SAMPLE_BOOKINGS)}")
        success = create_booking(booking)
        
        if success:
            print("🎉 Check your dashboard - the booking should appear instantly!")
        
        # Wait between bookings
        if i < len(SAMPLE_BOOKINGS):
            print("⏳ Waiting 3 seconds before next booking...")
            time.sleep(3)
    
    print("\n🎯 Demo completed!")
    print("All bookings should now be visible in your dashboard with real-time updates!")

def create_random_booking():
    """Create a random booking for testing"""
    services = ["Hair Cut", "Facial Treatment", "Massage", "Manicure", "Pedicure", "Hair Styling"]
    times = ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM", "4:00 PM"]
    
    # Create booking for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime("%b %d, %Y")
    
    booking_data = {
        "service_name": random.choice(services),
        "booking_date": date_str,
        "booking_time": random.choice(times),
        "notes": f"Random booking created at {datetime.now().strftime('%H:%M:%S')}"
    }
    
    return create_booking(booking_data)

if __name__ == "__main__":
    print("🎯 Real-time Booking Demo")
    print("Choose an option:")
    print("1. Run full demo (5 bookings)")
    print("2. Create single random booking")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        demo_realtime_bookings()
    elif choice == "2":
        print("\n🎲 Creating random booking...")
        create_random_booking()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")
