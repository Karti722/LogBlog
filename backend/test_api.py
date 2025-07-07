import requests
import json

# Test the AI tutorial request API
url = "http://127.0.0.1:8000/ai-tutorial/api/requests/"

# First, let's try to get existing requests (should work without auth)
try:
    response = requests.get(url)
    print(f"GET request status: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Error making GET request: {e}")

# Test creating a new tutorial request
# Note: This will require authentication in a real scenario
test_data = {
    "topic": "Django REST API",
    "description": "Learn how to build a REST API with Django",
    "difficulty": "intermediate"
}

try:
    response = requests.post(url, data=json.dumps(test_data), headers={
        'Content-Type': 'application/json'
    })
    print(f"\nPOST request status: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Error making POST request: {e}")
