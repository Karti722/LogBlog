# Vercel Deployment Guide for LogBlog Frontend

## Overview
This guide will help you deploy the LogBlog React frontend to Vercel, connecting it to your Railway backend.

## Prerequisites
- ✅ Railway backend deployed and working: `https://logblog-production.up.railway.app`
- ✅ GitHub repository with your code
- ✅ Vercel account (free tier works)

## Step 1: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)
1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

3. **Login to Vercel**:
   ```bash
   vercel login
   ```

4. **Deploy**:
   ```bash
   vercel --prod
   ```

### Option B: Using Vercel Dashboard
1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**:
   - Click "New Project"
   - Select your `LogBlog` repository
   - Choose the `frontend` folder as the root directory

3. **Configure Build Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Set Environment Variables**:
   - `REACT_APP_API_URL` = `https://logblog-production.up.railway.app`

5. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete

## Step 2: Configure Railway Backend

Update your Railway environment variables to allow the Vercel frontend:

1. **Go to Railway Dashboard**:
   - Open your LogBlog project
   - Click on the `web` service
   - Go to "Variables" tab

2. **Add/Update Variables**:
   ```
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ALLOWED_HOSTS=logblog-production.up.railway.app,your-vercel-app.vercel.app
   CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
   ```

3. **Redeploy**:
   - Click "Deploy" to apply changes

## Step 3: Test the Deployment

1. **Visit your Vercel URL**
2. **Test key features**:
   - ✅ Homepage loads
   - ✅ Blog posts display
   - ✅ AI tutorials work
   - ✅ Login/Register works
   - ✅ API calls to Railway backend work

## Step 4: Custom Domain (Optional)

1. **In Vercel Dashboard**:
   - Go to your project settings
   - Click "Domains"
   - Add your custom domain

2. **Update Railway CORS**:
   - Add your custom domain to `CORS_ALLOWED_ORIGINS`

## Environment Variables Reference

### Frontend (.env)
```
REACT_APP_API_URL=https://logblog-production.up.railway.app
REACT_APP_APP_NAME=LogBlog
REACT_APP_APP_VERSION=1.0.0
```

### Backend (Railway)
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
FRONTEND_URL=https://your-vercel-app.vercel.app
ALLOWED_HOSTS=logblog-production.up.railway.app,your-vercel-app.vercel.app
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

## Troubleshooting

### Common Issues:

1. **CORS Errors**:
   - Ensure your Vercel URL is in `CORS_ALLOWED_ORIGINS`
   - Check that Railway backend is accessible

2. **API Calls Failing**:
   - Verify `REACT_APP_API_URL` is correct
   - Check browser network tab for errors

3. **Build Failures**:
   - Ensure all dependencies are in `package.json`
   - Check build logs for specific errors

4. **404 on Refresh**:
   - Vercel should handle this with the `vercel.json` config
   - Check that routing is configured correctly

## Success Checklist

- [ ] Frontend deployed to Vercel
- [ ] Custom domain configured (if needed)
- [ ] Environment variables set
- [ ] Railway backend updated with CORS settings
- [ ] All API endpoints working
- [ ] Authentication working
- [ ] ML features working
- [ ] Responsive design working

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Check Railway backend logs
3. Test API endpoints directly
4. Verify environment variables

Your LogBlog application should now be fully deployed and working! 🎉
