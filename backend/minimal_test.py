#!/usr/bin/env python3
"""
Minimal test to check if the server is working
"""
import requests

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health check - Status: {response.status_code}")
        print(f"Health check - Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Root check - Status: {response.status_code}")
        print(f"Root check - Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root check failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing server endpoints...")
    test_health()
    test_root()
