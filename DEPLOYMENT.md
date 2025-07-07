# LogBlog Deployment Guide for Render

This comprehensive guide will walk you through deploying your Django + React LogBlog application to Render with detailed step-by-step instructions.

## 🚀 Overview

**LogBlog** is a full-stack application consisting of:
- **Backend**: Django REST API with authentication, blog posts, and AI-powered tutorials
- **Frontend**: React application built with Vite and Tailwind CSS
- **Database**: PostgreSQL (managed by Render)

**Example Production URLs:**
- Main App: `https://logblog-app.onrender.com`
- Admin Panel: `https://logblog-app.onrender.com/admin/`
- API: `https://logblog-app.onrender.com/api/`

## 📋 Prerequisites

Before starting, ensure you have:
1. A **Render account** (https://render.com - free tier available)
2. Your code pushed to a **GitHub repository**
3. An **OpenAI API key** (from https://platform.openai.com/api-keys)
4. Basic knowledge of Django and React

## 🛠️ Step 1: Prepare Your Application for Production

### 1.1 Update Backend Requirements

Your application needs additional packages for production deployment:

```bash
# Navigate to your backend directory
cd backend
```

Add these production dependencies to your `requirements.txt`:

```txt
Django==5.2.4
djangorestframework==3.15.2
django-cors-headers==4.6.0
python-dotenv==1.0.0
dj-database-url==3.0.1
psycopg2-binary==2.9.9
openai==1.54.5
requests==2.32.4
Pillow==11.0.0
django-filter==24.3
whitenoise==6.6.0
gunicorn==21.2.0
```

### 1.2 Update Django Settings for Production

Your `settings.py` needs modifications to work in both development and production:

**Key Changes Needed:**
1. Dynamic ALLOWED_HOSTS based on environment
2. Production-ready static file serving
3. Flexible CORS settings
4. Database configuration that works locally and in production

### 1.3 Create Environment Files

You'll need different environment configurations for development and production.

## 🔧 Step 2: Configure Environment Variables

### 2.1 Local Development Environment

Create a `.env` file in your `backend/` directory with these contents:

```env
# Local Development Configuration
SECRET_KEY=django-insecure-local-dev-key-change-in-production-please
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
OPENAI_API_KEY=your-openai-api-key-here
FRONTEND_URL=http://localhost:5174
ALLOWED_HOSTS=localhost,127.0.0.1,*
```

### 2.2 Production Environment Variables

For Render deployment, you'll set these in the Render dashboard:

```env
# Production Configuration (Set in Render Dashboard)
SECRET_KEY=your-super-secure-production-key-min-50-characters-long
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your-openai-api-key-here
FRONTEND_URL=https://logblog-app.onrender.com
ALLOWED_HOSTS=logblog-app.onrender.com,localhost,127.0.0.1
```

## 🏗️ Step 3: Create Build Scripts

### 3.1 Main Build Script (`build.sh`)

Create this file in your project root:

```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting LogBlog build process..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

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
```

### 3.2 Windows Build Script (`build.ps1`)

For local testing on Windows:

```powershell
# PowerShell build script for local testing
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
```

## 🗄️ Step 4: Set Up Database on Render

### 4.1 Create PostgreSQL Database

1. **Log into Render Dashboard**
   - Go to https://render.com and sign in
   - Click the "New +" button in the top right

2. **Create Database**
   - Select "PostgreSQL"
   - Configure your database:
     - **Name**: `logblog-database`
     - **Database**: `logblog_db`
     - **User**: `logblog_user`
     - **Region**: Choose closest to your target audience
     - **PostgreSQL Version**: 14 (or latest)
     - **Plan**: Free (for testing) or paid (for production)

3. **Get Database URL**
   - After creation, go to your database dashboard
   - Copy the "External Database URL" from the "Connections" section
   - It will look like: `postgresql://user:password@host:port/database`
   - **Save this URL** - you'll need it for the web service

### 4.2 Database Configuration Notes

- **Free Tier**: 1GB storage, 100 connections max
- **Paid Tier**: More storage, connections, and automatic backups
- **Connection Pooling**: Automatically handled by Django with `conn_max_age=600`

## 🌐 Step 5: Deploy Web Service to Render

### 5.1 Create Web Service

1. **In Render Dashboard**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository and branch

2. **Basic Configuration**
   - **Name**: `logblog-app` (this will be your subdomain)
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

3. **Advanced Settings**
   - **Plan**: Free (for testing) or paid (for production)
   - **Auto-Deploy**: Yes (recommended)
   - **Environment**: Python 3.11 or later

### 5.2 Configure Environment Variables

In your web service settings, go to "Environment" and add these variables:

```env
SECRET_KEY=your-super-secure-production-key-at-least-50-characters-long-use-a-generator
DEBUG=False
DATABASE_URL=postgresql://logblog_user:your_password@dpg-xxxxx-a.oregon-postgres.render.com/logblog_db
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FRONTEND_URL=https://logblog-app.onrender.com
ALLOWED_HOSTS=logblog-app.onrender.com,localhost,127.0.0.1
```

**🔐 Important Security Notes:**
- **SECRET_KEY**: Generate a new one using Django's `get_random_secret_key()` or online tools
- **DATABASE_URL**: Use the exact URL from your PostgreSQL database
- **OPENAI_API_KEY**: Get this from OpenAI's platform
- **Replace `logblog-app`** with your actual Render service name

### 5.3 Deploy Application

1. **Start Deployment**
   - Click "Create Web Service"
   - Render will automatically clone your repo and start building

2. **Monitor Build Process**
   - Watch the build logs in the "Events" tab
   - Common build time: 3-5 minutes
   - Look for "✅ Build process completed successfully!"

3. **Check Deployment Status**
   - Once deployed, your app will be available at `https://your-app-name.onrender.com`
   - The service will show "Live" status when ready

## 🔧 Step 6: Post-Deployment Configuration

### 6.1 Create Django Superuser

After successful deployment, create an admin account:

1. **Access Render Shell**
   - Go to your web service dashboard
   - Click on "Shell" tab
   - Wait for shell to connect

2. **Create Superuser**
   ```bash
   cd backend
   python manage.py createsuperuser
   ```
   - Follow prompts to create username, email, and password
   - This account will access `/admin/` panel

### 6.2 Test Your Deployment

Visit these URLs to verify everything works:

1. **Main Application**: `https://logblog-app.onrender.com`
2. **Admin Panel**: `https://logblog-app.onrender.com/admin/`
3. **API Root**: `https://logblog-app.onrender.com/api/`
4. **User Registration**: Test the signup form
5. **Blog Posts**: Create and view blog posts
6. **AI Features**: Test AI tutorial generation

## 🎨 Step 7: Frontend Configuration

### 7.1 Update Frontend API Base URL

In your React app, update the API base URL for production:

**Example in `frontend/src/services/api.js`:**
```javascript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://logblog-app.onrender.com/api'
  : 'http://localhost:8000/api';
```

### 7.2 Frontend Environment Variables

If you need frontend environment variables, create `frontend/.env`:

```env
VITE_API_URL=https://logblog-app.onrender.com/api
VITE_APP_NAME=LogBlog
```

## 🔒 Step 8: Security Configuration

### 8.1 Production Security Settings

Your settings should include these security measures:

```python
# In production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 8.2 CORS Configuration

Update CORS settings for production:

```python
CORS_ALLOWED_ORIGINS = [
    "https://logblog-app.onrender.com",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
]
```

## 🐛 Step 9: Troubleshooting

### 9.1 Common Issues and Solutions

**❌ Build Fails**
- **Check**: Build logs in Render dashboard
- **Fix**: Ensure all dependencies are in `requirements.txt`
- **Debug**: Test build script locally first

**❌ Database Connection Errors**
- **Check**: DATABASE_URL is correct and database is running
- **Fix**: Verify PostgreSQL database is created and accessible
- **Debug**: Test connection in Render shell

**❌ Static Files Not Loading**
- **Check**: `collectstatic` runs successfully in build script
- **Fix**: Ensure `STATIC_ROOT` is set correctly
- **Debug**: Check staticfiles directory exists

**❌ CORS Errors**
- **Check**: CORS_ALLOWED_ORIGINS includes your domain
- **Fix**: Add production domain to CORS settings
- **Debug**: Check browser network tab for specific errors

**❌ Frontend Not Loading**
- **Check**: Build script copies frontend files to staticfiles
- **Fix**: Verify `npm run build` completes successfully
- **Debug**: Check if dist/ directory is created

### 9.2 Debugging Steps

1. **Check Render Logs**
   - Go to service dashboard → "Logs" tab
   - Look for error messages and stack traces

2. **Use Render Shell**
   - Access shell from service dashboard
   - Run Django management commands
   - Check file structure and permissions

3. **Test Database Connection**
   ```bash
   cd backend
   python manage.py dbshell
   ```

4. **Check Static Files**
   ```bash
   python manage.py collectstatic --dry-run
   ```

## 📊 Step 10: Performance and Monitoring

### 10.1 Performance Optimization

**Database Optimization:**
- Use connection pooling (already configured)
- Add database indexes for frequently queried fields
- Consider upgrading to paid PostgreSQL plan

**Static File Optimization:**
- Whitenoise compresses static files automatically
- Consider CDN for heavy traffic

**Frontend Optimization:**
- Vite automatically optimizes React build
- Code splitting is handled automatically

### 10.2 Monitoring

**Health Checks:**
- Render automatically monitors your service
- Set up custom health check endpoint if needed

**Logging:**
- View logs in Render dashboard
- Consider external logging service for production

## 💰 Step 11: Cost Considerations

### 11.1 Free Tier Limitations

**Web Service (Free):**
- Sleeps after 15 minutes of inactivity
- 750 hours per month limit
- Limited to 512MB RAM

**PostgreSQL (Free):**
- 1GB storage maximum
- 100 connections maximum
- No automatic backups

### 11.2 Upgrading for Production

**When to Upgrade:**
- Expecting consistent traffic
- Need 99.9% uptime
- Require database backups
- Need more than 1GB database storage

**Recommended Paid Plans:**
- **Web Service**: Starter ($7/month) or higher
- **PostgreSQL**: Starter ($7/month) or higher

## 🔄 Step 12: Continuous Deployment

### 12.1 Auto-Deploy Setup

With auto-deploy enabled:
1. Push code to your main branch
2. Render automatically builds and deploys
3. Monitor deployment in dashboard
4. Test the updated application

### 12.2 Manual Deployment

If you prefer manual control:
1. Disable auto-deploy in service settings
2. Use "Deploy latest commit" button
3. Monitor build and deployment progress

## 📝 Step 13: Environment Files Summary

### 13.1 Required Files

**Local Development** (`backend/.env`):
```env
SECRET_KEY=django-insecure-local-dev-key-change-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
OPENAI_API_KEY=your-openai-api-key-here
FRONTEND_URL=http://localhost:5174
ALLOWED_HOSTS=localhost,127.0.0.1,*
```

**Production** (Render Environment Variables):
```env
SECRET_KEY=your-super-secure-production-key-at-least-50-characters
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your-openai-api-key-here
FRONTEND_URL=https://logblog-app.onrender.com
ALLOWED_HOSTS=logblog-app.onrender.com,localhost,127.0.0.1
```

## 🎉 Congratulations!

Your LogBlog application should now be successfully deployed on Render! 

**Final Checklist:**
- ✅ Database created and connected
- ✅ Web service deployed and running
- ✅ Environment variables configured
- ✅ Django superuser created
- ✅ Frontend loading correctly
- ✅ API endpoints working
- ✅ User registration/login functional
- ✅ Blog posts can be created/viewed
- ✅ AI features working (if OpenAI key provided)

## 📞 Support and Resources

- **Render Documentation**: https://render.com/docs
- **Django Documentation**: https://docs.djangoproject.com/
- **React Documentation**: https://reactjs.org/docs/
- **Render Community**: https://community.render.com/

If you encounter issues, check the troubleshooting section above or reach out to the Render community for help!
