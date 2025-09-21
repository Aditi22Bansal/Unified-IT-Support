#!/usr/bin/env python3
"""
Test script for registration endpoint
"""
import requests
import json

def test_registration():
    """Test the registration endpoint"""
    url = "http://127.0.0.1:8000/api/auth/register"

    test_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "customer"
    }

    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_registration()
