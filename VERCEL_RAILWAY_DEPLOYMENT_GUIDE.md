# 🚀 Complete Vercel + Railway Deployment Guide for AI Tutorial LogBlog

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Architecture](#deployment-architecture)
3. [Step 1: Railway Backend Setup](#step-1-railway-backend-setup)
4. [Step 2: Vercel Frontend Setup](#step-2-vercel-frontend-setup)
5. [Environment Variables Configuration](#environment-variables-configuration)
6. [Database Setup](#database-setup)
7. [Domain Configuration](#domain-configuration)
8. [Post-Deployment Testing](#post-deployment-testing)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

---

## 🛠️ Prerequisites

### Required Accounts:
- ✅ **Railway Account** (Free $5 monthly credit)
- ✅ **Vercel Account** (Free tier available)
- ✅ **GitHub Account** with your repository
- ✅ **Git** installed locally

### Repository Requirements:
- ✅ Your LogBlog project pushed to GitHub
- ✅ Separate frontend and backend folders
- ✅ All dependencies in requirements.txt and package.json

---

## 🏗️ Deployment Architecture

```
Frontend (React) → Vercel (Free)
    ↓ API Calls
Backend (Django) → Railway (Free $5 credit)
    ↓ Database
PostgreSQL → Railway (Included)
```

**Benefits:**
- ✅ **Completely free** to start
- ✅ **Excellent performance** for React apps
- ✅ **ML models** work well on Railway
- ✅ **PostgreSQL** included
- ✅ **Easy scaling** later

---

## 🔧 Step 1: Railway Backend Setup

### 1.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your repository

### 1.2 Deploy Django Backend
1. **Click "New Project"**
2. **Select "Deploy from GitHub repo"**
3. **Choose your LogBlog repository**
4. **Select backend folder** (if prompted)
5. **Configure deployment:**
   ```
   Name: logblog-backend
   Start Command: cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
   ```

### 1.3 Add PostgreSQL Database
1. **In your Railway project**
2. **Click "New Service"**
3. **Select "PostgreSQL"**
4. **Database will be created automatically**
5. **Copy connection details** (we'll use these in environment variables)

### 1.4 Configure Environment Variables
In Railway dashboard → Your service → Variables tab:

```bash
# Django Configuration
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=backend.settings

# Database (Railway will auto-populate these)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# ML Configuration
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu

# Frontend & CORS (update after Vercel deployment)
FRONTEND_URL=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

### 1.5 Deploy Backend
1. **Click "Deploy"**
2. **Wait for build to complete** (5-10 minutes)
3. **Note your Railway backend URL** (e.g., `https://your-backend-name.railway.app`)

---

## ⚛️ Step 2: Vercel Frontend Setup

### 2.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Connect your repository

### 2.2 Deploy React Frontend
1. **Click "New Project"**
2. **Import your GitHub repository**
3. **Configure build settings:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

### 2.3 Configure Environment Variables
In Vercel dashboard → Your project → Settings → Environment Variables:

```bash
# API Configuration
VITE_API_URL=https://your-backend-name.railway.app
VITE_API_BASE_URL=https://your-backend-name.railway.app/api

# App Configuration
VITE_APP_NAME=AI Tutorial LogBlog
VITE_APP_DESCRIPTION=ML-powered tutorial generation platform
```

### 2.4 Update Frontend API Configuration
Update your frontend API configuration file:

```javascript
// src/services/api.js or similar
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 2.5 Deploy Frontend
1. **Click "Deploy"**
2. **Wait for build to complete** (2-5 minutes)
3. **Note your Vercel frontend URL** (e.g., `https://your-app-name.vercel.app`)

---

## 🔗 Step 3: Connect Frontend and Backend

### 3.1 Update Railway Environment Variables
Go back to Railway and update these variables:

```bash
FRONTEND_URL=https://your-app-name.vercel.app
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app,localhost,127.0.0.1
```

### 3.2 Update Vercel Environment Variables
Ensure your Vercel environment variables point to your Railway backend:

```bash
VITE_API_URL=https://your-backend-name.railway.app
```

### 3.3 Redeploy Both Services
1. **Railway**: Click "Deploy" to apply new environment variables
2. **Vercel**: Will auto-deploy on environment variable changes

---

## 🔑 Environment Variables Configuration

### Railway Backend Variables:
```bash
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
FRONTEND_URL=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

### Vercel Frontend Variables:
```bash
VITE_API_URL=https://your-backend-name.railway.app
VITE_API_BASE_URL=https://your-backend-name.railway.app/api
VITE_APP_NAME=AI Tutorial LogBlog
```

---

## 🗄️ Database Setup

### PostgreSQL on Railway:
- **Automatically created** with your project
- **Connection string** auto-populated in `DATABASE_URL`
- **Free tier includes**: 100MB storage, shared CPU
- **Access via**: Railway dashboard → PostgreSQL service

### Database Configuration:
```python
# Django settings.py (already configured)
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

---

## 🌐 Domain Configuration

### Default Domains:
- **Frontend**: `https://your-app-name.vercel.app`
- **Backend**: `https://your-backend-name.railway.app`

### Custom Domains (Optional):
1. **Vercel**: Project Settings → Domains → Add custom domain
2. **Railway**: Service Settings → Domains → Add custom domain
3. **Update environment variables** with new domains

---

## 🧪 Post-Deployment Testing

### 1. Test Frontend
Visit: `https://your-app-name.vercel.app`
- [ ] App loads successfully
- [ ] UI renders correctly
- [ ] Navigation works

### 2. Test Backend API
```bash
# Health check
curl https://your-backend-name.railway.app/health/

# API endpoints
curl https://your-backend-name.railway.app/api/
```

### 3. Test Full Integration
1. **Create account** on frontend
2. **Login successfully**
3. **Create tutorial request**
4. **Verify ML generation** works
5. **Check database** persistence

### 4. Test CORS
Open browser console and verify:
- [ ] No CORS errors
- [ ] API calls successful
- [ ] Authentication works

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. CORS Errors
**Problem**: Frontend can't make API calls
**Solution**:
```bash
# In Railway, verify CORS settings:
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app
```

#### 2. Database Connection Issues
**Problem**: Backend can't connect to PostgreSQL
**Solution**:
```bash
# Check Railway PostgreSQL service is running
# Verify DATABASE_URL is set to: ${{Postgres.DATABASE_URL}}
```

#### 3. Build Failures
**Problem**: Railway build fails
**Solution**:
```bash
# Check requirements.txt
# Verify Python dependencies
# Check build logs in Railway dashboard
```

#### 4. Environment Variables Not Loading
**Problem**: App can't find environment variables
**Solution**:
```bash
# Railway: Check Variables tab
# Vercel: Check Environment Variables in Settings
# Ensure variable names match exactly
```

#### 5. ML Models Not Working
**Problem**: ML tutorial generation fails
**Solution**:
```bash
# Check ML_MODEL_PATH=backend/ai_tutorial/models/
# Verify USE_ML_GENERATOR=True
# Check Railway logs for model loading errors
```

---

## 📊 Cost Monitoring

### Railway Usage:
- **Free tier**: $5 monthly credit
- **Monitor usage**: Railway dashboard → Project → Usage
- **Typical usage**: $0-3/month for small apps

### Vercel Usage:
- **Free tier**: Unlimited static deployments
- **Monitor usage**: Vercel dashboard → Usage
- **Typical usage**: $0/month for frontend

---

## 🔄 Continuous Deployment

### Automatic Deployments:
- **Railway**: Auto-deploys on git push to main branch
- **Vercel**: Auto-deploys on git push to main branch

### Manual Deployments:
- **Railway**: Dashboard → Deploy button
- **Vercel**: Dashboard → Deployments → Redeploy

---

## 🚀 Scaling and Optimization

### Performance Tips:
1. **Enable caching** in Django
2. **Optimize ML models** for CPU usage
3. **Use CDN** for static assets
4. **Implement database** indexing

### When to Scale:
- **Railway**: Upgrade when exceeding $5 credit
- **Vercel**: Pro plan for team features
- **Database**: Upgrade when approaching 100MB limit

---

## 📞 Support Resources

### Documentation:
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)

### Community:
- [Railway Discord](https://discord.gg/railway)
- [Vercel Discord](https://discord.gg/vercel)
- [Django Community](https://www.djangoproject.com/community/)

---

## ✅ Deployment Checklist

### Pre-Deployment:
- [ ] Code pushed to GitHub
- [ ] Environment variables prepared
- [ ] Dependencies updated
- [ ] Local testing completed

### Railway Setup:
- [ ] PostgreSQL service created
- [ ] Backend deployed successfully
- [ ] Environment variables configured
- [ ] Database migrations run

### Vercel Setup:
- [ ] Frontend deployed successfully
- [ ] Environment variables configured
- [ ] Build settings correct
- [ ] Domain configured

### Integration:
- [ ] CORS configured correctly
- [ ] API endpoints accessible
- [ ] Frontend-backend communication works
- [ ] Authentication functional

### Testing:
- [ ] User registration/login works
- [ ] Tutorial generation works
- [ ] ML models loading correctly
- [ ] Database persistence works

---

## 🎉 Success!

Your AI Tutorial LogBlog is now deployed with:
- ✅ **React frontend** on Vercel (free)
- ✅ **Django backend** on Railway (free $5 credit)
- ✅ **PostgreSQL database** on Railway
- ✅ **ML-based tutorial generation**
- ✅ **Production-ready configuration**

**Frontend URL**: `https://your-app-name.vercel.app`
**Backend URL**: `https://your-backend-name.railway.app`

---

*Last updated: July 2025*
*This deployment should cost $0/month within Railway's free tier!*
