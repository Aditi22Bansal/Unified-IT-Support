#!/usr/bin/env python3
"""
Test registration with a new email
"""
import requests
import json
import random

def test_new_email():
    """Test registration with a new email"""
    url = "http://127.0.0.1:8002/api/auth/register"

    # Generate new email
    random_id = random.randint(1000, 9999)
    test_data = {
        "email": f"newuser{random_id}@example.com",
        "password": "TestPassword123!",
        "phone_number": "+919305667949",
        "account_type": "customer",
        "full_name": "New User"
    }

    try:
        print(f"Sending request to: {url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}!")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_new_email()


