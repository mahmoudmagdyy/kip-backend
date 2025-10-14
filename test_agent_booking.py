#!/usr/bin/env python3
"""
Test script for the Agent Booking Endpoint
Demonstrates how to use the public agent booking endpoint
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000/api/"
AGENT_BOOKING_ENDPOINT = API_BASE_URL + "agent/booking/create/"

def test_agent_booking():
    """Test the agent booking endpoint"""
    print("🚀 Testing Agent Booking Endpoint")
    print("=================================")
    
    # Test data
    test_cases = [
        {
            "name": "New User Creation",
            "data": {
                "phone": "9999999999",
                "first_name": "Agent",
                "last_name": "Test",
                "email": "agent.test@example.com",
                "service_name": "Legal Consultation",
                "booking_date": "2025-10-23",
                "booking_time": "14:00",
                "notes": "Agent created booking for new user"
            }
        },
        {
            "name": "Existing User Booking",
            "data": {
                "phone": "9999999999",  # Same phone as above
                "first_name": "Agent",
                "last_name": "Test",
                "email": "agent.test@example.com",
                "service_name": "Medical Consultation",
                "booking_date": "2025-10-24",
                "booking_time": "15:00",
                "notes": "Second booking for existing user"
            }
        },
        {
            "name": "Different Date Format",
            "data": {
                "phone": "8888888888",
                "first_name": "Format",
                "last_name": "Test",
                "email": "format.test@example.com",
                "service_name": "Legal Consultation",
                "booking_date": "25/10/2025",  # DD/MM/YYYY format
                "booking_time": "16:00",
                "notes": "Different date format test"
            }
        },
        {
            "name": "Different Time Format",
            "data": {
                "phone": "7777777777",
                "first_name": "Time",
                "last_name": "Test",
                "email": "time.test@example.com",
                "service_name": "Medical Consultation",
                "booking_date": "2025-10-26",
                "booking_time": "2:00 PM",  # 12-hour format
                "notes": "Different time format test"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(AGENT_BOOKING_ENDPOINT, json=test_case['data'])
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Success: {result.get('success')}")
                print(f"📝 Message: {result.get('message')}")
                print(f"👤 User Created: {result.get('user_created')}")
                print(f"🆔 User ID: {result.get('user_id')}")
                print(f"📅 Booking ID: {result.get('booking_id')}")
                
                if result.get('data'):
                    booking = result['data'].get('booking', {})
                    user = result['data'].get('user', {})
                    print(f"📋 Service: {booking.get('service_name')}")
                    print(f"📅 Date: {booking.get('booking_date')}")
                    print(f"⏰ Time: {booking.get('booking_time')}")
                    print(f"👤 User: {user.get('first_name')} {user.get('last_name')}")
                    print(f"📧 Email: {user.get('email')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"📝 Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

def test_error_cases():
    """Test error cases"""
    print("\n🧪 Testing Error Cases")
    print("=====================")
    
    error_cases = [
        {
            "name": "Missing Required Field",
            "data": {
                "service_name": "Legal Consultation",
                "booking_date": "2025-10-27",
                "booking_time": "14:00"
                # Missing phone
            }
        },
        {
            "name": "Invalid Date Format",
            "data": {
                "phone": "6666666666",
                "service_name": "Legal Consultation",
                "booking_date": "invalid-date",
                "booking_time": "14:00"
            }
        },
        {
            "name": "Invalid Time Format",
            "data": {
                "phone": "5555555555",
                "service_name": "Legal Consultation",
                "booking_date": "2025-10-27",
                "booking_time": "invalid-time"
            }
        },
        {
            "name": "Outside Working Hours",
            "data": {
                "phone": "4444444444",
                "service_name": "Legal Consultation",
                "booking_date": "2025-10-27",
                "booking_time": "20:00"  # Outside 12-17 working hours
            }
        }
    ]
    
    for i, test_case in enumerate(error_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(AGENT_BOOKING_ENDPOINT, json=test_case['data'])
            result = response.json()
            print(f"❌ Expected Error: {result.get('success')}")
            print(f"📝 Message: {result.get('message')}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

if __name__ == "__main__":
    print("🔧 Agent Booking Endpoint Test Suite")
    print("====================================")
    print(f"Endpoint: {AGENT_BOOKING_ENDPOINT}")
    print()
    
    # Test successful cases
    test_agent_booking()
    
    # Test error cases
    test_error_cases()
    
    print("\n✅ Test completed!")
    print("\n📚 For more information, see AGENT_BOOKING_ENDPOINT.md")
