#!/usr/bin/env python3
"""
Test registration with detailed error reporting
"""
import requests
import json
import random

def test_registration_with_details():
    """Test registration with detailed error reporting"""
    url = "http://127.0.0.1:8001/api/auth/register"

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
        print(f"Response Headers: {dict(response.headers)}")

        # Always try to print response text
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful!")
            try:
                response_data = response.json()
                print(f"User created: {json.dumps(response_data, indent=2)}")
            except:
                print("Response is not JSON")
            return True
        elif response.status_code == 422:
            print("❌ Validation Error (422)!")
            try:
                error_data = response.json()
                print(f"Validation errors: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse validation error as JSON")
            return False
        else:
            print(f"❌ Registration failed with status {response.status_code}!")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 8001")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_registration_with_details()
