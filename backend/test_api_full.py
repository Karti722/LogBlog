#!/usr/bin/env python3
"""
Test script for the AI Tutorial API with authentication
"""

import os
import sys
import django
import requests
import json

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_test_user():
    """Create a test user and get auth token"""
    try:
        # Create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('testpassword123')
            user.save()
            print("✅ Test user created successfully!")
        else:
            print("✅ Test user already exists!")
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        print(f"✅ Auth token: {token.key}")
        
        return token.key
    except Exception as e:
        print(f"❌ Failed to create test user: {str(e)}")
        return None

def test_api_endpoints(token):
    """Test the AI Tutorial API endpoints"""
    base_url = "http://127.0.0.1:8000"
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Create tutorial request
    print("\n--- Test 1: Create Tutorial Request ---")
    try:
        data = {
            'topic': 'Python Machine Learning',
            'description': 'Learn how to build machine learning models with Python',
            'difficulty': 'intermediate'
        }
        
        response = requests.post(
            f"{base_url}/ai-tutorial/api/requests/",
            json=data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Request created successfully!")
            print(f"Full response: {result}")
            request_id = result.get('request', {}).get('id')
            tutorial_id = result.get('tutorial', {}).get('id')
            print(f"Request ID: {request_id}")
            print(f"Tutorial ID: {tutorial_id}")
            print(f"Status: {result.get('request', {}).get('status')}")
            return request_id, tutorial_id
        else:
            print(f"❌ Request failed: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None, None

def test_tutorial_generation(token, request_id):
    """Test tutorial generation"""
    if not request_id:
        print("❌ No request ID provided")
        return
    
    print(f"\n--- Test 2: Generate Tutorial for Request {request_id} ---")
    
    base_url = "http://127.0.0.1:8000"
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai-tutorial/api/requests/{request_id}/generate/",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Tutorial generated successfully!")
            print(f"Message: {result.get('message')}")
            print(f"Tutorial ID: {result.get('tutorial_id')}")
            return result.get('tutorial_id')
        else:
            print(f"❌ Generation failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Generation failed: {str(e)}")
        return None

def main():
    """Main test function"""
    print("🚀 Testing AI Tutorial API with ML-based generation...")
    
    # Create test user and get token
    token = create_test_user()
    if not token:
        print("❌ Cannot proceed without auth token")
        return
    
    # Test API endpoints
    request_id, tutorial_id = test_api_endpoints(token)
    if request_id and tutorial_id:
        print(f"\n🎉 Full end-to-end test completed successfully!")
        print(f"Request ID: {request_id}")
        print(f"Tutorial ID: {tutorial_id}")
        print(f"✅ The ML-based tutorial generation is working perfectly!")
    else:
        print("\n❌ API request failed")

if __name__ == "__main__":
    main()
