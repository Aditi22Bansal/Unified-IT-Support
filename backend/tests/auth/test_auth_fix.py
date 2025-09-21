#!/usr/bin/env python3
"""
Test script to verify authentication fix
"""

import requests
import json

def test_auth_fix():
    """Test that authentication properly returns the logged-in user instead of demo user"""

    base_url = "http://127.0.0.1:8002"

    print("🧪 Testing Authentication Fix")
    print("=" * 50)

    # Test 1: Login with custom user
    print("\n1. Testing login with custom user...")
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }

    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user = data.get("user", {})
            print(f"✅ Login successful!")
            print(f"   User: {user.get('username')} ({user.get('full_name')})")
            print(f"   Token: {token[:20]}...")

            # Test 2: Get current user with token
            print("\n2. Testing get current user with token...")
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{base_url}/api/auth/me", headers=headers)

            if me_response.status_code == 200:
                me_data = me_response.json()
                print(f"✅ Get current user successful!")
                print(f"   User: {me_data.get('username')} ({me_data.get('full_name')})")
                print(f"   Role: {me_data.get('role')}")

                # Verify it's the same user
                if me_data.get('username') == user.get('username'):
                    print("✅ User persistence working correctly!")
                else:
                    print("❌ User mismatch - still getting demo user")
            else:
                print(f"❌ Get current user failed: {me_response.status_code}")
                print(f"   Response: {me_response.text}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_auth_fix()
