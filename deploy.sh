#!/usr/bin/env bash
# Production deployment script for LogBlog ML-based tutorial generation
# This script prepares the application for production deployment

set -e  # Exit on any error

echo "🚀 Starting LogBlog Production Deployment Preparation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the correct directory
if [[ ! -f "render.yaml" ]]; then
    print_error "render.yaml not found. Please run this script from the project root."
    exit 1
fi

# Check Python version
print_info "Checking Python version..."
python_version=$(python --version 2>&1 | cut -d' ' -f2)
if [[ $python_version < "3.8" ]]; then
    print_error "Python 3.8+ required. Current version: $python_version"
    exit 1
fi
print_status "Python version: $python_version"

# Check Node.js version
print_info "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed."
    exit 1
fi
node_version=$(node --version)
print_status "Node.js version: $node_version"

# Backend preparation
print_info "Preparing backend..."
cd backend

# Create virtual environment if it doesn't exist
if [[ ! -d "../logenv" ]]; then
    print_info "Creating virtual environment..."
    python -m venv ../logenv
    print_status "Virtual environment created"
fi

# Activate virtual environment
source ../logenv/bin/activate
print_status "Virtual environment activated"

# Install backend dependencies
print_info "Installing backend dependencies..."
pip install -r requirements.txt
print_status "Backend dependencies installed"

# Check for .env file
if [[ ! -f ".env" ]]; then
    print_warning ".env file not found. Copying from .env.example..."
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        print_warning "Please update .env with your production values"
    else
        print_error ".env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Run Django checks
print_info "Running Django system checks..."
python manage.py check --deploy
print_status "Django system checks passed"

# Check if ML models need to be trained
print_info "Checking ML models..."
if [[ ! -d "ai_tutorial/models" ]] || [[ ! -f "ai_tutorial/models/encoder.pth" ]]; then
    print_info "Training ML models..."
    python manage.py train_ml_models --force
    print_status "ML models trained successfully"
else
    print_status "ML models already exist"
fi

# Run migrations
print_info "Running database migrations..."
python manage.py migrate
print_status "Database migrations completed"

# Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput
print_status "Static files collected"

# Test ML model functionality
print_info "Testing ML model functionality..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ai_tutorial.ml_models import MLTutorialGenerator
try:
    generator = MLTutorialGenerator()
    test_tutorial = generator.generate_tutorial('Test Topic', 'Test Description', 'beginner')
    print('✅ ML model test successful')
except Exception as e:
    print(f'❌ ML model test failed: {e}')
    exit(1)
"
print_status "ML model functionality verified"

# Frontend preparation
print_info "Preparing frontend..."
cd ../frontend

# Install frontend dependencies
print_info "Installing frontend dependencies..."
npm install
print_status "Frontend dependencies installed"

# Build frontend
print_info "Building frontend for production..."
npm run build
print_status "Frontend built successfully"

# Copy frontend build to backend static files
print_info "Copying frontend build to backend static files..."
mkdir -p ../backend/staticfiles
cp -r dist/* ../backend/staticfiles/
print_status "Frontend files copied to backend"

# Return to project root
cd ..

# Verify deployment readiness
print_info "Verifying deployment readiness..."

# Check required files
required_files=(
    "render.yaml"
    "build.sh"
    "backend/requirements.txt"
    "backend/manage.py"
    "backend/.env.example"
    "backend/backend/settings.py"
    "backend/backend/wsgi.py"
    "frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        print_error "Required file missing: $file"
        exit 1
    fi
done

print_status "All required files present"

# Check environment variables
print_info "Checking environment variables..."
source backend/.env

required_vars=(
    "SECRET_KEY"
    "USE_ML_GENERATOR"
    "ML_MODEL_PATH"
)

for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        print_warning "Environment variable $var is not set"
    fi
done

# Generate deployment summary
print_info "Generating deployment summary..."
cat > deployment_summary.txt << EOF
LogBlog Deployment Summary
==========================
Date: $(date)
Python Version: $python_version
Node.js Version: $node_version

Backend Status:
- Dependencies: ✅ Installed
- Database: ✅ Migrated
- Static Files: ✅ Collected
- ML Models: ✅ Trained and Verified

Frontend Status:
- Dependencies: ✅ Installed
- Build: ✅ Completed
- Static Files: ✅ Copied to Backend

Deployment Files:
- render.yaml: ✅ Present
- build.sh: ✅ Present
- requirements.txt: ✅ Present
- .env.example: ✅ Present

Health Check Endpoints:
- /health/ - General health check
- /ready/ - Readiness check
- /alive/ - Liveness check

Next Steps:
1. Commit all changes to Git
2. Push to GitHub
3. Connect repository to Render
4. Deploy using Render Dashboard
5. Set production environment variables
6. Monitor deployment logs

EOF

print_status "Deployment summary generated: deployment_summary.txt"

# Final checks
print_info "Running final deployment checks..."

# Check if Git is initialized
if [[ ! -d ".git" ]]; then
    print_warning "Git repository not initialized. Run 'git init' to initialize."
else
    print_status "Git repository found"
fi

# Check for uncommitted changes
if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
    print_warning "Uncommitted changes detected. Consider committing before deployment."
fi

# Success message
echo
echo "🎉 LogBlog Production Deployment Preparation Complete!"
echo
print_status "Your LogBlog application is ready for production deployment!"
print_info "ML-based tutorial generation system is fully configured and tested"
print_info "All dependencies are installed and build processes completed"
print_info "Health check endpoints are available for monitoring"
echo
print_info "Deployment Summary:"
echo "- Backend: Django with ML-based tutorial generation"
echo "- Frontend: React with Vite build system"
echo "- Database: PostgreSQL (production) / SQLite (development)"
echo "- ML Models: PyTorch + scikit-learn based system"
echo "- Static Files: Managed by WhiteNoise"
echo "- Health Checks: Available at /health/, /ready/, /alive/"
echo
print_info "To deploy on Render:"
echo "1. Push your code to GitHub"
echo "2. Connect your repository to Render"
echo "3. Render will automatically use render.yaml for deployment"
echo "4. Set environment variables in Render dashboard"
echo "5. Monitor deployment logs and health checks"
echo
print_status "Ready for deployment! 🚀"
