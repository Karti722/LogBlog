#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting LogBlog build process..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Train ML models for tutorial generation
echo "🧠 Training ML models for tutorial generation..."
python manage.py train_ml_models --force

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗃️ Running database migrations..."
python manage.py migrate

# Build frontend
echo "⚛️ Building React frontend..."
cd ../frontend
npm install
npm run build

# Copy built frontend to Django static files
echo "📋 Copying frontend build to Django static files..."
mkdir -p ../backend/staticfiles
cp -r dist/* ../backend/staticfiles/

echo "✅ Build process completed successfully!"
echo "🎉 LogBlog with ML-based tutorial generation is ready!"
