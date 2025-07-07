#!/usr/bin/env python3
"""
Test script for the ML-based tutorial generator
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ai_tutorial.services import AITutorialGenerator

def test_ml_generation():
    """Test the ML-based tutorial generation"""
    print("Testing ML-based tutorial generation...")
    
    # Create tutorial service
    service = AITutorialGenerator()
    
    # Test cases
    test_cases = [
        "Python basics for beginners",
        "Advanced JavaScript concepts",
        "Machine learning with PyTorch",
        "Web development with Django",
        "Data science fundamentals"
    ]
    
    for i, topic in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {topic} ---")
        try:
            tutorial = service.generate_tutorial(topic)
            print(f"Title: {tutorial.get('title', 'N/A')}")
            print(f"Content length: {len(tutorial.get('content', ''))}")
            print(f"Duration: {tutorial.get('duration', 'N/A')}")
            print(f"Tags: {tutorial.get('tags', [])}")
            print("✅ Generation successful!")
        except Exception as e:
            print(f"❌ Generation failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_ml_generation()
