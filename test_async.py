"""
Test script to verify the async tutorial generation system
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ai_tutorial.models import AITutorialRequest
from ai_tutorial.async_generator import threaded_generator
from django.contrib.auth.models import User
import time

def test_async_generation():
    """Test the async tutorial generation system"""
    
    print("Testing Async Tutorial Generation System")
    print("=" * 50)
    
    # Create a test user if needed
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={'email': 'test@example.com'}
    )
    if created:
        print("Created test user")
    
    # Create a test tutorial request
    request = AITutorialRequest.objects.create(
        user=user,
        topic="Test Topic",
        description="Test description for async generation",
        difficulty="beginner"
    )
    
    print(f"Created tutorial request: {request.id}")
    print(f"Initial status: {request.status}")
    
    # Start async generation
    print("\nStarting async generation...")
    thread = threaded_generator.generate_tutorial_async(request.id)
    
    print(f"Thread started: {thread.is_alive()}")
    print(f"Active tasks: {threaded_generator.get_active_tasks()}")
    
    # Monitor progress
    print("\nMonitoring progress...")
    for i in range(10):  # Check for up to 10 seconds
        time.sleep(1)
        
        # Refresh the request from database
        request.refresh_from_db()
        
        print(f"Second {i+1}: Status = {request.status}")
        
        if request.status == 'completed':
            print(f"✅ Tutorial completed: {request.generated_tutorial.title}")
            break
        elif request.status == 'failed':
            print(f"❌ Tutorial failed: {request.error_message}")
            break
    
    print(f"\nFinal status: {request.status}")
    print(f"Thread still active: {threaded_generator.is_task_active(request.id)}")
    
    # Cleanup
    request.delete()
    print("Test completed and cleaned up")

if __name__ == "__main__":
    test_async_generation()
