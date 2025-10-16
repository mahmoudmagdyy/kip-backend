#!/usr/bin/env python3
"""
Test script to verify sub-service creation and retrieval
"""

import requests
import json

# Replace with your actual API base URL
BASE_URL = "http://localhost:8000/api"  # Update this with your actual URL

def test_subservice_creation():
    """Test sub-service creation and retrieval"""
    
    print("🧪 Testing Sub-Service Creation and Retrieval")
    print("=" * 50)
    
    # Step 1: Get all services to find a service ID
    print("\n1. Getting all services...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/services/")
        if response.status_code == 200:
            services_data = response.json()
            if services_data.get('success') and services_data.get('data'):
                services = services_data['data']
                print(f"✅ Found {len(services)} services")
                if services:
                    service_id = services[0]['id']
                    print(f"📋 Using service ID: {service_id}")
                else:
                    print("❌ No services found. Please create a service first.")
                    return
            else:
                print("❌ Failed to get services")
                return
        else:
            print(f"❌ Failed to get services: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting services: {e}")
        return
    
    # Step 2: Create a sub-service
    print(f"\n2. Creating sub-service for service ID {service_id}...")
    
    # Prepare form data for sub-service creation
    sub_service_data = {
        'service': str(service_id),
        'title_ar': 'خدمة فرعية للاختبار',
        'title_en': 'Test Sub-Service',
        'description_ar': 'وصف الخدمة الفرعية للاختبار',
        'description_en': 'Test sub-service description',
        'is_active': 'true',
        'is_vib': 'false',
        'order': '0'
    }
    
    # Create a simple test image (you can replace this with an actual image file)
    # For testing purposes, we'll create a simple text file as "image"
    test_image_content = b"Test image content for sub-service"
    
    try:
        # Create multipart form data
        files = {
            'image': ('test_image.jpg', test_image_content, 'image/jpeg')
        }
        
        response = requests.post(
            f"{BASE_URL}/dashboard/sub-services/create/",
            data=sub_service_data,
            files=files
        )
        
        print(f"📤 Response Status: {response.status_code}")
        print(f"📤 Response Body: {response.text}")
        
        if response.status_code == 201:
            response_data = response.json()
            if response_data.get('success'):
                sub_service_id = response_data['data']['id']
                print(f"✅ Sub-service created successfully with ID: {sub_service_id}")
            else:
                print(f"❌ Sub-service creation failed: {response_data.get('message')}")
                return
        else:
            print(f"❌ Failed to create sub-service: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error creating sub-service: {e}")
        return
    
    # Step 3: Get sub-services for the service
    print(f"\n3. Getting sub-services for service ID {service_id}...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/services/{service_id}/sub-services/")
        print(f"📤 Response Status: {response.status_code}")
        print(f"📤 Response Body: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('success'):
                sub_services = response_data['data']
                print(f"✅ Found {len(sub_services)} sub-services")
                if sub_services:
                    print("📋 Sub-services found:")
                    for sub_service in sub_services:
                        print(f"   - ID: {sub_service['id']}, Title: {sub_service['title_en']}")
                else:
                    print("❌ No sub-services found - this indicates the issue!")
            else:
                print(f"❌ Failed to get sub-services: {response_data.get('message')}")
        else:
            print(f"❌ Failed to get sub-services: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting sub-services: {e}")
    
    # Step 4: Get the service with sub-services
    print(f"\n4. Getting service with sub-services...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/services/{service_id}/")
        print(f"📤 Response Status: {response.status_code}")
        print(f"📤 Response Body: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('success'):
                service_data = response_data['data']
                sub_services = service_data.get('sub_services', [])
                print(f"✅ Service has {len(sub_services)} sub-services")
                if sub_services:
                    print("📋 Sub-services in service:")
                    for sub_service in sub_services:
                        print(f"   - ID: {sub_service['id']}, Title: {sub_service['title_en']}")
                else:
                    print("❌ No sub-services in service - this indicates the issue!")
            else:
                print(f"❌ Failed to get service: {response_data.get('message')}")
        else:
            print(f"❌ Failed to get service: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting service: {e}")

if __name__ == "__main__":
    test_subservice_creation()
