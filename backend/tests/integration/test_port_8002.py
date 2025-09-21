#!/usr/bin/env python3
"""
Test registration on port 8002
"""
import requests
import json
import random

def test_registration_port_8002():
    """Test registration on port 8002"""
    url = "http://127.0.0.1:8002/api/auth/register"

    # Generate unique username and email
    random_id = random.randint(1000, 9999)
    test_data = {
        "username": f"testuser{random_id}",
        "email": f"test{random_id}@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "customer"
    }

    try:
        print(f"Sending request to: {url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful on port 8002!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}!")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_registration_port_8002()


