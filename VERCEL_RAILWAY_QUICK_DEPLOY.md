# 🚀 Vercel + Railway Quick Deploy Guide

## Pre-Deployment (5 minutes)

### 1. Generate Django Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**Save this key!** ⚠️

### 2. Push to GitHub
```bash
git add .
git commit -m "Ready for Vercel + Railway deployment"
git push origin main
```

### 3. Prepare API URLs
You'll need to update these after deployment:
- Railway backend URL: `https://your-backend-name.railway.app`
- Vercel frontend URL: `https://your-app-name.vercel.app`

---

## Railway Backend Setup (10 minutes)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your repository

### Step 2: Deploy Backend
1. New Project → Deploy from GitHub repo
2. Select your LogBlog repository
3. Choose backend folder
4. **Start Command**: `cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

### Step 3: Add PostgreSQL
1. In your project → New Service → PostgreSQL
2. Database auto-created
3. **Copy your Railway backend URL** 📋

### Step 4: Set Environment Variables
**Replace `your-backend-name` with your actual Railway service name!**

```bash
SECRET_KEY=your-generated-secret-key-from-step-1
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
FRONTEND_URL=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

---

## Vercel Frontend Setup (5 minutes)

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Connect your repository

### Step 2: Deploy Frontend
1. New Project → Import from GitHub
2. Select your LogBlog repository
3. **Configure build settings:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

### Step 3: Set Environment Variables
**Replace `your-backend-name` with your actual Railway service name!**

```bash
VITE_API_URL=https://your-backend-name.railway.app
VITE_API_BASE_URL=https://your-backend-name.railway.app/api
VITE_APP_NAME=AI Tutorial LogBlog
```

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-5 minutes
3. **Copy your Vercel frontend URL** 📋

---

## Connect Frontend & Backend (5 minutes)

### Step 1: Update Railway Variables
Go back to Railway and update these:
```bash
FRONTEND_URL=https://your-app-name.vercel.app
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app,localhost,127.0.0.1
```

### Step 2: Redeploy
1. **Railway**: Click "Deploy" to apply changes
2. **Vercel**: Auto-deploys on environment variable changes

---

## Testing (5 minutes)

### 1. Test Frontend
Visit: `https://your-app-name.vercel.app`
- [ ] App loads
- [ ] UI renders correctly

### 2. Test Backend API
```bash
curl https://your-backend-name.railway.app/health/
curl https://your-backend-name.railway.app/api/
```

### 3. Test Full Integration
1. Create account on frontend
2. Login successfully
3. Create tutorial request
4. Verify ML generation works

---

## 🚨 Quick Troubleshooting

### CORS Errors?
**Fix**: Update Railway environment variables:
```bash
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app
```

### Build Fails on Railway?
**Fix**: Check requirements.txt and build logs in Railway dashboard

### Frontend Can't Reach Backend?
**Fix**: Verify `VITE_API_URL` in Vercel matches Railway backend URL

### Database Connection Issues?
**Fix**: Ensure `DATABASE_URL=${{Postgres.DATABASE_URL}}` in Railway

### ML Models Not Working?
**Fix**: Check Railway logs, verify `USE_ML_GENERATOR=True`

---

## 💰 Cost Breakdown

### Railway (Backend + Database):
- **Free tier**: $5 monthly credit
- **Expected usage**: $0-3/month
- **Includes**: PostgreSQL database

### Vercel (Frontend):
- **Free tier**: Unlimited deployments
- **Expected usage**: $0/month
- **Includes**: CDN, custom domains

**Total Monthly Cost: $0** (within free tiers)

---

## 🎯 Success Indicators

- [ ] Frontend loads at Vercel URL
- [ ] Backend API responds at Railway URL
- [ ] No CORS errors in browser console
- [ ] User registration/login works
- [ ] Tutorial generation works
- [ ] ML models load correctly

---

## 📝 Final URLs

After successful deployment:
- **Frontend**: `https://your-app-name.vercel.app`
- **Backend**: `https://your-backend-name.railway.app`
- **Database**: Managed by Railway

---

## 🔄 Auto-Deployment

Both services auto-deploy on git push:
- **Railway**: Watches main branch
- **Vercel**: Watches main branch

No manual deployment needed after initial setup!

---

**Your AI Tutorial LogBlog is now live!** 🎉

*Total deployment time: ~25 minutes*
*Monthly cost: $0 (within free tiers)*
