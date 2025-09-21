#!/usr/bin/env python3
"""
Test script specifically for aditi_bansal user
"""

import requests
import json

def test_aditi_user():
    """Test authentication with aditi_bansal user"""

    base_url = "http://127.0.0.1:8002"

    print("🧪 Testing Authentication for aditi_bansal")
    print("=" * 50)

    # Test 1: Login with aditi_bansal
    print("\n1. Testing login with aditi_bansal...")
    login_data = {
        "username": "aditi_bansal",
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
            print(f"   Token: {token[:30]}...")

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
                    print("🎉 aditi_bansal should now persist on page reload!")
                else:
                    print("❌ User mismatch - still getting demo user")
                    print(f"   Expected: {user.get('username')}")
                    print(f"   Got: {me_data.get('username')}")
            else:
                print(f"❌ Get current user failed: {me_response.status_code}")
                print(f"   Response: {me_response.text}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on port 8002")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_aditi_user()
