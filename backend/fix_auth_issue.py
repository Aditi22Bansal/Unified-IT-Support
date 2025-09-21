#!/usr/bin/env python3
"""
Quick fix script for authentication issue
This script will help you test and fix the demo user issue
"""

import requests
import json
import time

def test_and_fix_auth():
    """Test authentication and provide fix instructions"""

    print("🔧 Authentication Issue Fix Script")
    print("=" * 50)

    # Test different servers
    servers = [
        {"name": "Working Server (Port 8002)", "url": "http://127.0.0.1:8002"},
        {"name": "Main Dynamic (Port 8001)", "url": "http://127.0.0.1:8001"},
        {"name": "Enhanced Server (Port 8001)", "url": "http://127.0.0.1:8001"}
    ]

    print("\n🔍 Checking which servers are running...")

    for server in servers:
        try:
            response = requests.get(f"{server['url']}/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {server['name']} is running")

                # Test authentication with aditi_bansal
                print(f"\n🧪 Testing authentication with aditi_bansal on {server['name']}...")

                # Login
                login_data = {
                    "username": "aditi_bansal",
                    "password": "testpass"
                }

                login_response = requests.post(f"{server['url']}/api/auth/login", json=login_data)

                if login_response.status_code == 200:
                    login_result = login_response.json()
                    token = login_result.get("access_token")
                    user = login_result.get("user", {})

                    print(f"   ✅ Login successful!")
                    print(f"   👤 User: {user.get('username')} ({user.get('full_name')})")
                    print(f"   🔑 Token: {token[:30] if token else 'None'}...")

                    if token:
                        # Test get current user
                        headers = {"Authorization": f"Bearer {token}"}
                        me_response = requests.get(f"{server['url']}/api/auth/me", headers=headers)

                        if me_response.status_code == 200:
                            me_data = me_response.json()
                            print(f"   ✅ Get current user successful!")
                            print(f"   👤 User: {me_data.get('username')} ({me_data.get('full_name')})")

                            if me_data.get('username') == 'aditi_bansal':
                                print(f"   🎉 SUCCESS! Authentication working correctly!")
                                print(f"   💡 Use this server: {server['name']}")
                                return server
                            else:
                                print(f"   ❌ Still getting demo user: {me_data.get('username')}")
                        else:
                            print(f"   ❌ Get current user failed: {me_response.status_code}")
                    else:
                        print(f"   ❌ No token received")
                else:
                    print(f"   ❌ Login failed: {login_response.status_code}")
            else:
                print(f"❌ {server['name']} is not responding")

        except requests.exceptions.ConnectionError:
            print(f"❌ {server['name']} is not running")
        except Exception as e:
            print(f"❌ Error testing {server['name']}: {e}")

    print("\n" + "=" * 50)
    print("🔧 Fix Instructions:")
    print("=" * 50)
    print("1. Start the working server:")
    print("   cd backend")
    print("   python working_server.py")
    print()
    print("2. In another terminal, test authentication:")
    print("   cd backend/tests/auth")
    print("   python test_aditi_user.py")
    print()
    print("3. If still getting demo user, the issue is in the server code.")
    print("   The authentication fixes have been applied but may need restart.")
    print()
    print("4. For persistent storage, use the database server:")
    print("   python main_dynamic.py")
    print("   python migrate_to_database.py")

    return None

if __name__ == "__main__":
    test_and_fix_auth()
