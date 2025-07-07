#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ai_tutorial.models import AITutorialRequest
from ai_tutorial.services import AITutorialGenerator
from django.contrib.auth.models import User

def test_tutorial_generation():
    print("Testing AI tutorial generation...")
    
    # Create a test user if one doesn't exist
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    print(f"User {'created' if created else 'retrieved'}: {user.username}")
    
    # Create a test tutorial request
    request_obj = AITutorialRequest.objects.create(
        user=user,
        topic='React Components',
        description='Learn how to build reusable React components',
        difficulty='intermediate'
    )
    print(f"Tutorial request created: {request_obj.topic}")
    
    # Test the tutorial generation
    generator = AITutorialGenerator()
    try:
        tutorial = generator.generate_tutorial(request_obj)
        print(f"Tutorial created successfully: {tutorial.title}")
        print(f"Tutorial ID: {tutorial.id}")
        print(f"Description: {tutorial.description}")
        print(f"Difficulty: {tutorial.difficulty}")
        print(f"Duration: {tutorial.estimated_duration} minutes")
        print(f"Number of steps: {tutorial.steps.count()}")
        print(f"Request status: {request_obj.status}")
        print(f"Is AI Generated: {tutorial.is_ai_generated}")
        
        print("\nFirst few steps:")
        for i, step in enumerate(tutorial.steps.all()[:3]):
            print(f"  {i+1}. {step.title}")
            print(f"     {step.content[:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        print(f"Request status: {request_obj.status}")
        print(f"Error message: {request_obj.error_message}")

if __name__ == "__main__":
    test_tutorial_generation()
