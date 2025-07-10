# 🔧 Render Deployment Troubleshooting Guide

## 🚨 Common Deployment Issues & Solutions

### 1. Build Failures

#### Problem: "Build failed with exit code 1"
**Symptoms:**
- Build stops during dependency installation
- Python package installation errors
- ML model training failures

**Solutions:**
```bash
# Check requirements.txt for incompatible versions
# Verify Python version compatibility (3.8+)
# Check build logs for specific error messages

# Common fixes:
pip install --upgrade pip
pip install setuptools wheel
```

**Fix Steps:**
1. Go to Render dashboard → Your service → Logs
2. Find the exact error message
3. Update `requirements.txt` if needed
4. Push changes and redeploy

#### Problem: "Permission denied" during build
**Solutions:**
```bash
# Make build.sh executable
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push origin main
```

---

### 2. Database Connection Issues

#### Problem: "django.db.utils.OperationalError: could not connect to server"
**Symptoms:**
- App starts but can't connect to database
- 500 errors when accessing database

**Solutions:**
1. **Check DATABASE_URL:**
   ```bash
   # Must be INTERNAL database URL, not external
   # Format: postgresql://user:pass@internal-host:5432/dbname
   ```

2. **Verify PostgreSQL service:**
   - Go to PostgreSQL service in Render
   - Check status is "Available"
   - Ensure same region as web service

3. **Fix DATABASE_URL:**
   - Copy from PostgreSQL service → Connect → Internal Database URL
   - Update environment variable in web service

#### Problem: "relation does not exist"
**Solution:**
```bash
# Migrations not run properly
# Check build.sh includes: python manage.py migrate
# Verify migrations are in your repository
```

---

### 3. Static Files Not Loading

#### Problem: CSS/JS files return 404
**Symptoms:**
- App loads but no styling
- Missing JavaScript functionality
- Static files not found

**Solutions:**
1. **Check build.sh:**
   ```bash
   # Must include these commands:
   cd ../frontend
   npm install
   npm run build
   mkdir -p ../backend/staticfiles
   cp -r dist/* ../backend/staticfiles/
   ```

2. **Verify Django settings:**
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   ```

3. **Check WhiteNoise configuration:**
   ```python
   # In settings.py MIDDLEWARE
   'whitenoise.middleware.WhiteNoiseMiddleware',
   ```

---

### 4. ML Model Issues

#### Problem: "No module named 'torch'" or ML import errors
**Solutions:**
1. **Check requirements.txt:**
   ```txt
   torch==2.1.0
   torchvision==0.16.0
   scikit-learn==1.3.2
   transformers==4.35.2
   sentence-transformers==2.2.2
   ```

2. **Verify ML_DEVICE setting:**
   ```bash
   ML_DEVICE=cpu  # Always use CPU on Render
   ```

#### Problem: "ML models not found"
**Solutions:**
1. **Check ML_MODEL_PATH:**
   ```bash
   ML_MODEL_PATH=backend/ai_tutorial/models/
   ```

2. **Verify model training in build.sh:**
   ```bash
   python manage.py train_ml_models --force
   ```

---

### 5. Environment Variable Issues

#### Problem: "KeyError: 'SECRET_KEY'"
**Solutions:**
1. Go to web service → Environment
2. Add missing environment variables
3. Restart service

#### Problem: "DEBUG should be False"
**Solutions:**
```bash
# Ensure DEBUG=False (not True)
DEBUG=False
```

---

### 6. CORS and Frontend Issues

#### Problem: "CORS policy blocked"
**Symptoms:**
- Frontend can't make API calls
- Browser console shows CORS errors

**Solutions:**
1. **Check CORS_ALLOWED_ORIGINS:**
   ```bash
   CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
   ```

2. **Verify FRONTEND_URL:**
   ```bash
   FRONTEND_URL=https://your-app-name.onrender.com
   ```

3. **Check ALLOWED_HOSTS:**
   ```bash
   ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
   ```

---

### 7. Memory and Resource Issues

#### Problem: "Application error" or crashes
**Symptoms:**
- App starts but crashes under load
- Memory limit exceeded

**Solutions:**
1. **Optimize ML models:**
   ```python
   # Use smaller models
   # Implement model caching
   # Lazy loading of models
   ```

2. **Monitor resource usage:**
   - Check Render dashboard → Metrics
   - Consider upgrading plan if needed

---

## 🔍 Debugging Tools

### 1. Check Build Logs
```bash
# In Render dashboard:
Your Service → Logs → Build Logs
```

### 2. Check Runtime Logs
```bash
# In Render dashboard:
Your Service → Logs → Runtime Logs
```

### 3. Environment Variables Check
```bash
# In Render dashboard:
Your Service → Environment
# Verify all variables are set correctly
```

### 4. Service Status
```bash
# Check service health:
curl https://your-app-name.onrender.com/health/
```

---

## 🚀 Step-by-Step Debugging Process

### When Your App Won't Start:

1. **Check Build Logs:**
   - Look for red error messages
   - Identify failed commands

2. **Verify Environment Variables:**
   - All required variables set?
   - Correct values?

3. **Test Database Connection:**
   - PostgreSQL service running?
   - Correct DATABASE_URL?

4. **Check Static Files:**
   - Build script copying files?
   - WhiteNoise configured?

5. **Verify Dependencies:**
   - All packages in requirements.txt?
   - Compatible versions?

---

## 🎯 Common Error Messages & Fixes

### "Error: Could not find a version that satisfies the requirement"
**Fix:** Update requirements.txt with compatible package versions

### "ModuleNotFoundError: No module named 'X'"
**Fix:** Add missing package to requirements.txt

### "Application error (H10)"
**Fix:** Check web service start command and environment variables

### "Database connection failed"
**Fix:** Use internal DATABASE_URL, not external

### "Static files not found"
**Fix:** Check build.sh copies frontend files to staticfiles/

---

## 💡 Pro Tips

### 1. Test Locally First
```bash
# Before deploying, test locally:
python manage.py runserver
npm run build
```

### 2. Use Same Dependencies
```bash
# Keep local and production dependencies identical
pip freeze > requirements.txt
```

### 3. Monitor Resource Usage
- Check Render dashboard regularly
- Monitor database storage (100MB limit on free tier)
- Watch for memory usage spikes

### 4. Keep Logs Clean
- Remove debug prints from production code
- Use proper logging levels
- Monitor error rates

---

## 📞 When to Contact Support

Contact Render support if:
- Service won't start despite following all steps
- Database connectivity issues persist
- Billing or account issues
- Platform-specific problems

**Render Support:** https://render.com/support

---

## ✅ Final Verification Checklist

Before contacting support, verify:

- [ ] All environment variables are set correctly
- [ ] DATABASE_URL is the internal URL
- [ ] Build.sh is executable and complete
- [ ] Requirements.txt has all dependencies
- [ ] GitHub repository is up to date
- [ ] PostgreSQL service is running
- [ ] Domain names match in all configurations

---

*Most deployment issues are resolved by checking environment variables and build logs!*
