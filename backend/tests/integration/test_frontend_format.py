#!/usr/bin/env python3
"""
Test registration with frontend data format
"""
import requests
import json

def test_frontend_format():
    """Test registration with the format your frontend sends"""
    url = "http://127.0.0.1:8002/api/auth/register"

    # Test data matching your frontend form
    test_data = {
        "email": "aditibansal1408@gmail.com",
        "password": "TestPassword123!",
        "phone_number": "+919305667949",
        "account_type": "customer",
        "full_name": "Aditi Bansal"
    }

    try:
        print(f"Sending request to: {url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful with frontend format!")
            try:
                response_data = response.json()
                print(f"User created: {json.dumps(response_data, indent=2)}")
            except:
                print("Response is not JSON")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}!")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_frontend_format()


