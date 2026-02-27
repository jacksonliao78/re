
import requests
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("Registration successful")
            return response.json()
        else:
            print("Registration failed")
            return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_login(email, password):
    """Test user login"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("Login successful")
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print("Login failed")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_get_me(token):
    """Test protected /auth/me endpoint"""
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("Protected endpoint access successful")
            return True
        else:
            print("Protected endpoint access failed")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_me_no_token():
    """Test /auth/me without token (should fail)"""
    url = f"{BASE_URL}/auth/me"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401 or response.status_code == 403:
            print("Correctly rejected request without token")
            return True
        else:
            print("Should have rejected request")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    
    user_data = test_register()
    if not user_data:
        email = "test@example.com"
        password = "testpass123"
    else:
        email = user_data["email"]
        password = "testpass123"
    
    token = test_login(email, password)
    if not token:
        sys.exit(1)
    
    test_get_me(token)
    
    test_get_me_no_token()
    
    print(f"\nYJWT token: {token[:50]}...")
    print(f'  curl -H "Authorization: Bearer {token}" http://localhost:8000/auth/me')

if __name__ == "__main__":
    main()
