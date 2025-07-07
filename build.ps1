# PowerShell build script for local testing on Windows
Write-Host "🚀 Starting LogBlog build process..." -ForegroundColor Green

# Install backend dependencies
Write-Host "📦 Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt

# Collect static files
Write-Host "📂 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Run migrations
Write-Host "🗃️ Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Build frontend
Write-Host "⚛️ Building React frontend..." -ForegroundColor Yellow
Set-Location ../frontend
npm install
npm run build

# Copy built frontend to Django static files
Write-Host "📋 Copying frontend build to Django static files..." -ForegroundColor Yellow
if (!(Test-Path "../backend/staticfiles")) {
    New-Item -ItemType Directory -Path "../backend/staticfiles"
}
Copy-Item -Path "dist/*" -Destination "../backend/staticfiles/" -Recurse -Force

Write-Host "✅ Build process completed successfully!" -ForegroundColor Green
