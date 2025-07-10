# 🚀 Render Deployment Quick Checklist

## Pre-Deployment (5 minutes)

### 1. Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**Save this key!** ⚠️

### 2. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 3. Verify Files Present
- [ ] `render.yaml` ✅
- [ ] `build.sh` ✅
- [ ] `backend/requirements.txt` ✅
- [ ] `frontend/package.json` ✅

---

## Render Setup (10 minutes)

### Step 1: Create PostgreSQL Database
1. New → PostgreSQL
2. Name: `logblog-database`
3. Database: `logblog_db`
4. User: `logblog_user`
5. **Copy Internal Database URL** 📋

### Step 2: Create Web Service
1. New → Web Service
2. Connect GitHub repo
3. Name: `logblog-app` (or your choice)
4. Build Command: `./build.sh`
5. Start Command: `cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

### Step 3: Set Environment Variables
**Replace `your-app-name` with your actual app name!**

```bash
SECRET_KEY=your-generated-secret-key-from-step-1
DEBUG=False
DATABASE_URL=your-postgresql-internal-url-from-step-1
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
FRONTEND_URL=https://your-app-name.onrender.com
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
```

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes
3. Monitor build logs

---

## Post-Deployment Testing (5 minutes)

### 1. Check App Status
Visit: `https://your-app-name.onrender.com`

### 2. Test Health Check
```bash
curl https://your-app-name.onrender.com/health/
```

### 3. Test Tutorial Generation
1. Create account on deployed app
2. Submit tutorial request
3. Verify ML generation works

---

## Quick Troubleshooting

### Build Fails?
- Check build logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Ensure `build.sh` has correct permissions

### Database Connection Issues?
- Verify `DATABASE_URL` is correct
- Check PostgreSQL service is running
- Ensure database and web service in same region

### Static Files Not Loading?
- Check `STATIC_URL` and `STATIC_ROOT` settings
- Verify `build.sh` copies frontend files
- Check WhiteNoise configuration

### ML Models Not Working?
- Check `ML_MODEL_PATH` is correct
- Verify models are in repository
- Check build logs for model training errors

---

## 🎯 Success Indicators

- [ ] App loads at your Render URL
- [ ] Health check returns 200
- [ ] User registration works
- [ ] Tutorial generation works
- [ ] Static files load correctly

---

**Your AI Tutorial LogBlog is now live on Render!** 🎉

*For detailed troubleshooting, see the full deployment guide.*
