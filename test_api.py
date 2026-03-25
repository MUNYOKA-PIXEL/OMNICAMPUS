import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register():
    """Test registration"""
    data = {
        "student_id": "TEST001",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@student.edu",
        "phone": "1234567890",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/student/register", json=data)
        print(f"Register: {response.status_code}")
        print(response.json())
        return response.status_code == 201
    except Exception as e:
        print(f"Register failed: {e}")
        return False

def test_login():
    """Test login"""
    data = {
        "username": "TEST001",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/student/login", json=data)
        print(f"Login: {response.status_code}")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Login failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("=" * 50)
    
    if test_health():
        print("✓ Health check passed")
    else:
        print("✗ Health check failed - server might not be running")
    
    print("=" * 50)
    test_register()
    print("=" * 50)
    test_login()