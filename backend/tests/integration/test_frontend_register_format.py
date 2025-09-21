#!/usr/bin/env python3
"""
Test registration with the actual frontend Register component format
"""
import requests
import json
import random

def test_frontend_register_format():
    """Test registration with the format your Register component sends"""
    url = "http://127.0.0.1:8002/api/auth/register"
    
    # Generate new email
    random_id = random.randint(1000, 9999)
    
    # This is the format your Register component sends (based on formData structure)
    test_data = {
        "username": f"user{random_id}",  # This is in your formData
        "email": f"test{random_id}@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "role": "customer"  # This is in your formData
    }
    
    try:
        print(f"Sending request to: {url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful with Register component format!")
            try:
                response_data = response.json()
                print(f"User created: {json.dumps(response_data, indent=2)}")
            except:
                print("Response is not JSON")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}!")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_frontend_register_format()


