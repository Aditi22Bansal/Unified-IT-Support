#!/usr/bin/env python3
"""
Detailed test script for registration endpoint
"""
import requests
import json

def test_registration():
    """Test the registration endpoint with detailed error reporting"""
    url = "http://127.0.0.1:8000/api/auth/register"

    test_data = {
        "username": "testuser",
        "email": "test@example.com",
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
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            # Try to parse error details
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_registration()
