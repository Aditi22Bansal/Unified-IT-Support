#!/usr/bin/env python3
"""
Test registration with the updated frontend format
"""
import requests
import json
import random

def test_updated_format():
    """Test registration with the updated frontend format"""
    url = "http://127.0.0.1:8002/api/auth/register"

    # Generate new email
    random_id = random.randint(1000, 9999)

    # This matches the updated frontend form structure
    test_data = {
        "email": f"test{random_id}@example.com",
        "password": "TestPassword123!",
        "phone_number": "+919305667949",
        "account_type": "customer",
        "full_name": "Test User"
    }

    try:
        print(f"Sending request to: {url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful with updated format!")
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
    test_updated_format()


