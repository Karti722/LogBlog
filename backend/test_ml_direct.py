#!/usr/bin/env python3
"""
Simple test script for the ML-based tutorial generator
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ai_tutorial.ml_models import MLTutorialGenerator

def test_ml_generator():
    """Test the ML-based tutorial generator directly"""
    print("Testing ML-based tutorial generation...")
    
    # Create ML generator
    try:
        generator = MLTutorialGenerator()
        print("✅ ML Generator initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize ML Generator: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Test cases
    test_cases = [
        ("Python basics for beginners", "Learn Python fundamentals", "beginner"),
        ("Advanced JavaScript concepts", "Master advanced JS techniques", "advanced"),
        ("Machine learning with PyTorch", "Build ML models with PyTorch", "intermediate"),
        ("Web development with Django", "Create web apps with Django", "intermediate"),
        ("Data science fundamentals", "Learn data science basics", "beginner")
    ]
    
    for i, (topic, description, difficulty) in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {topic} ---")
        try:
            tutorial = generator.generate_tutorial(topic, description, difficulty)
            print(f"Title: {tutorial.get('title', 'N/A')}")
            print(f"Description: {tutorial.get('description', 'N/A')}")
            print(f"Steps count: {len(tutorial.get('steps', []))}")
            print(f"Duration: {tutorial.get('estimated_duration', 'N/A')} minutes")
            print("✅ Generation successful!")
        except Exception as e:
            print(f"❌ Generation failed: {str(e)}")

if __name__ == "__main__":
    test_ml_generator()
