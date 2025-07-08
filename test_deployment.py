#!/usr/bin/env python3
"""
Comprehensive deployment test script for LogBlog ML-based tutorial generation
This script tests all major functionality before and after deployment
"""

import os
import sys
import django
import requests
import json
import time
from datetime import datetime
import subprocess

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.management import call_command
from django.db import connection

class DeploymentTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {message}")
        
    def test_django_setup(self):
        """Test Django configuration"""
        try:
            # Test settings
            assert hasattr(settings, 'USE_ML_GENERATOR')
            assert hasattr(settings, 'ML_MODEL_PATH')
            assert hasattr(settings, 'ML_DEVICE')
            self.log_test("Django Configuration", True, "All ML settings configured")
        except Exception as e:
            self.log_test("Django Configuration", False, str(e))
            
    def test_database_connection(self):
        """Test database connectivity"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                assert result[0] == 1
            self.log_test("Database Connection", True, "Database accessible")
        except Exception as e:
            self.log_test("Database Connection", False, str(e))
            
    def test_ml_models(self):
        """Test ML model availability and functionality"""
        try:
            from ai_tutorial.ml_models import MLTutorialGenerator
            generator = MLTutorialGenerator()
            
            # Test generation
            tutorial = generator.generate_tutorial(
                "Test Python Tutorial",
                "Learn Python basics",
                "beginner"
            )
            
            assert 'title' in tutorial
            assert 'steps' in tutorial
            assert len(tutorial['steps']) > 0
            
            self.log_test("ML Model Generation", True, f"Generated tutorial with {len(tutorial['steps'])} steps")
        except Exception as e:
            self.log_test("ML Model Generation", False, str(e))
            
    def test_static_files(self):
        """Test static files collection"""
        try:
            static_root = settings.STATIC_ROOT
            if static_root and os.path.exists(static_root):
                file_count = sum(len(files) for _, _, files in os.walk(static_root))
                self.log_test("Static Files", True, f"Found {file_count} static files")
            else:
                self.log_test("Static Files", False, "Static files directory not found")
        except Exception as e:
            self.log_test("Static Files", False, str(e))
            
    def test_health_endpoints(self):
        """Test health check endpoints"""
        endpoints = [
            ('/health/', 'Health Check'),
            ('/ready/', 'Readiness Check'),
            ('/alive/', 'Liveness Check')
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"Status: {data.get('status', 'unknown')}")
                else:
                    self.log_test(name, False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(name, False, str(e))
                
    def test_api_authentication(self):
        """Test API authentication system"""
        try:
            # Create test user
            user, created = User.objects.get_or_create(
                username='deployment_test_user',
                defaults={'email': 'test@example.com'}
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                
            # Get or create token
            token, _ = Token.objects.get_or_create(user=user)
            
            # Test authenticated request
            headers = {'Authorization': f'Token {token.key}'}
            response = requests.get(
                f"{self.base_url}/ai-tutorial/api/requests/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                self.log_test("API Authentication", True, "Token authentication working")
                return token.key
            else:
                self.log_test("API Authentication", False, f"HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("API Authentication", False, str(e))
            return None
            
    def test_tutorial_generation_api(self, token):
        """Test tutorial generation via API"""
        if not token:
            self.log_test("Tutorial Generation API", False, "No authentication token")
            return
            
        try:
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'topic': 'Deployment Test Tutorial',
                'description': 'Testing tutorial generation during deployment',
                'difficulty': 'beginner'
            }
            
            response = requests.post(
                f"{self.base_url}/ai-tutorial/api/requests/",
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                tutorial_id = result.get('tutorial', {}).get('id')
                self.log_test("Tutorial Generation API", True, f"Created tutorial ID: {tutorial_id}")
            else:
                self.log_test("Tutorial Generation API", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Tutorial Generation API", False, str(e))
            
    def test_admin_interface(self):
        """Test Django admin interface"""
        try:
            response = requests.get(f"{self.base_url}/admin/", timeout=10)
            if response.status_code == 200:
                self.log_test("Admin Interface", True, "Admin interface accessible")
            else:
                self.log_test("Admin Interface", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Admin Interface", False, str(e))
            
    def test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            headers = {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'GET'
            }
            
            response = requests.options(
                f"{self.base_url}/ai-tutorial/api/requests/",
                headers=headers,
                timeout=10
            )
            
            if 'Access-Control-Allow-Origin' in response.headers:
                self.log_test("CORS Configuration", True, "CORS headers present")
            else:
                self.log_test("CORS Configuration", False, "CORS headers missing")
                
        except Exception as e:
            self.log_test("CORS Configuration", False, str(e))
            
    def run_all_tests(self):
        """Run all deployment tests"""
        print("🚀 Starting LogBlog Deployment Tests...")
        print("=" * 50)
        
        # Local tests (no server required)
        print("\n📋 Local Configuration Tests:")
        self.test_django_setup()
        self.test_database_connection()
        self.test_ml_models()
        self.test_static_files()
        
        # Server tests (require running server)
        print(f"\n🌐 Server Tests ({self.base_url}):")
        self.test_health_endpoints()
        self.test_admin_interface()
        self.test_cors_configuration()
        
        # API tests
        print("\n🔐 API Tests:")
        token = self.test_api_authentication()
        self.test_tutorial_generation_api(token)
        
        # Generate report
        self.generate_report()
        
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 50)
        print("📊 DEPLOYMENT TEST REPORT")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save detailed report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'results': self.test_results
        }
        
        with open('deployment_test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: deployment_test_report.json")
        
        if failed_tests == 0:
            print("\n🎉 All tests passed! Deployment is ready!")
            return True
        else:
            print(f"\n⚠️  {failed_tests} tests failed. Please review before deployment.")
            return False

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LogBlog Deployment Test Suite')
    parser.add_argument('--url', default='http://127.0.0.1:8000', 
                       help='Base URL for server tests (default: http://127.0.0.1:8000)')
    parser.add_argument('--local-only', action='store_true',
                       help='Run only local tests (no server required)')
    
    args = parser.parse_args()
    
    tester = DeploymentTester(args.url)
    
    if args.local_only:
        print("🏠 Running local tests only...")
        tester.test_django_setup()
        tester.test_database_connection()
        tester.test_ml_models()
        tester.test_static_files()
        tester.generate_report()
    else:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
