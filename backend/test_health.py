#!/usr/bin/env python3
"""
Test health endpoint
"""
import requests

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://127.0.0.1:8001/health")
        print(f"Health check - Status: {response.status_code}")
        print(f"Health check - Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    test_health()
