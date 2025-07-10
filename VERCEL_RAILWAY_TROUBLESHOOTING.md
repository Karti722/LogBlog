# 🔧 Vercel + Railway Troubleshooting Guide

## 🚨 Common Deployment Issues & Solutions

### 1. CORS Errors

#### Problem: "CORS policy blocked the request"
**Symptoms:**
- Frontend loads but API calls fail
- Browser console shows CORS errors
- Network tab shows failed requests

**Solutions:**
1. **Check Railway CORS settings:**
   ```bash
   # In Railway variables:
   CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
   ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app,localhost,127.0.0.1
   ```

2. **Verify exact URLs:**
   - Copy exact Vercel URL from Vercel dashboard
   - No trailing slashes
   - Use https:// not http://

3. **Check Django CORS settings:**
   ```python
   # In settings.py - should already be configured
   CORS_ALLOWED_ORIGINS = [
       os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
   ]
   ```

---

### 2. API Connection Issues

#### Problem: Frontend can't reach backend
**Symptoms:**
- API calls return 404 or connection errors
- Network tab shows "failed to fetch"
- Console shows "Network Error"

**Solutions:**
1. **Check Vercel API URL:**
   ```bash
   # In Vercel environment variables:
   VITE_API_URL=https://your-backend-name.railway.app
   ```

2. **Verify Railway backend is running:**
   ```bash
   # Test Railway backend directly:
   curl https://your-backend-name.railway.app/health/
   ```

3. **Check frontend API configuration:**
   ```javascript
   // In your frontend code
   const API_BASE_URL = import.meta.env.VITE_API_URL;
   console.log('API URL:', API_BASE_URL); // Should show Railway URL
   ```

---

### 3. Railway Build Failures

#### Problem: "Build failed with exit code 1"
**Symptoms:**
- Railway deployment fails
- Build logs show dependency errors
- Python package installation fails

**Solutions:**
1. **Check requirements.txt:**
   ```txt
   # Ensure compatible versions
   Django==5.2.4
   torch==2.1.0
   scikit-learn==1.3.2
   # ... other packages
   ```

2. **Verify Python version:**
   ```bash
   # Railway uses Python 3.9+ by default
   # Check your local Python version matches
   python --version
   ```

3. **Check build logs:**
   - Go to Railway dashboard → Your service → Deployments
   - Click on failed deployment
   - Review build logs for specific errors

---

### 4. Database Connection Issues

#### Problem: "django.db.utils.OperationalError: could not connect to server"
**Symptoms:**
- Backend starts but database queries fail
- 500 errors on API endpoints
- Database migration failures

**Solutions:**
1. **Check DATABASE_URL:**
   ```bash
   # In Railway variables (should be exactly this):
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```

2. **Verify PostgreSQL service:**
   - Go to Railway dashboard
   - Check PostgreSQL service status
   - Ensure it's in "Running" state

3. **Check database migrations:**
   ```bash
   # In Railway build logs, look for:
   python manage.py migrate
   ```

---

### 5. Vercel Build Failures

#### Problem: "Build failed" on Vercel
**Symptoms:**
- Vercel deployment fails
- Build logs show npm/node errors
- Frontend doesn't deploy

**Solutions:**
1. **Check build settings:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

2. **Verify package.json:**
   ```json
   {
     "scripts": {
       "build": "vite build",
       "dev": "vite",
       "preview": "vite preview"
     }
   }
   ```

3. **Check Node.js version:**
   - Vercel uses Node.js 18.x by default
   - Ensure your local version is compatible

---

### 6. Environment Variable Issues

#### Problem: "Environment variable not found"
**Symptoms:**
- Apps can't access environment variables
- Configuration errors
- KeyError exceptions

**Solutions:**
1. **Railway variables not loading:**
   ```bash
   # Check Variables tab in Railway dashboard
   # Ensure all required variables are set
   # Redeploy after adding variables
   ```

2. **Vercel variables not loading:**
   ```bash
   # Check Environment Variables in Vercel Settings
   # Ensure variables start with VITE_ for frontend access
   # Redeploy after adding variables
   ```

3. **Variable naming issues:**
   ```bash
   # Railway: Use any name (Django convention)
   SECRET_KEY=value
   
   # Vercel: Must start with VITE_ for frontend
   VITE_API_URL=value
   ```

---

### 7. ML Model Issues

#### Problem: "No module named 'torch'" or ML errors
**Symptoms:**
- Backend starts but ML generation fails
- Import errors in logs
- Tutorial generation returns errors

**Solutions:**
1. **Check ML dependencies:**
   ```txt
   # In requirements.txt:
   torch==2.1.0
   torchvision==0.16.0
   scikit-learn==1.3.2
   transformers==4.35.2
   sentence-transformers==2.2.2
   ```

2. **Verify ML configuration:**
   ```bash
   # In Railway variables:
   USE_ML_GENERATOR=True
   ML_MODEL_PATH=backend/ai_tutorial/models/
   ML_DEVICE=cpu
   ```

3. **Check Railway resources:**
   - ML models need sufficient memory
   - Monitor Railway usage dashboard
   - Consider model optimization

---

## 🔍 Debugging Tools

### 1. Railway Debugging
```bash
# Check deployment logs:
Railway Dashboard → Your Service → Deployments → View Logs

# Check runtime logs:
Railway Dashboard → Your Service → Logs

# Check variables:
Railway Dashboard → Your Service → Variables
```

### 2. Vercel Debugging
```bash
# Check build logs:
Vercel Dashboard → Your Project → Deployments → View Logs

# Check runtime (functions):
Vercel Dashboard → Your Project → Functions

# Check variables:
Vercel Dashboard → Your Project → Settings → Environment Variables
```

### 3. Browser Debugging
```javascript
// Check frontend variables:
console.log('API URL:', import.meta.env.VITE_API_URL);

// Check API calls:
// Open Network tab in browser dev tools
// Look for failed requests
```

### 4. API Testing
```bash
# Test Railway backend:
curl https://your-backend-name.railway.app/health/
curl https://your-backend-name.railway.app/api/

# Test CORS:
curl -H "Origin: https://your-app-name.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://your-backend-name.railway.app/api/
```

---

## 🚀 Step-by-Step Debugging Process

### When Your App Doesn't Work:

1. **Check Service Status:**
   - Railway: Is backend service running?
   - Vercel: Is frontend deployed successfully?

2. **Verify URLs:**
   - Copy exact URLs from service dashboards
   - Ensure no typos in environment variables

3. **Test Backend Independently:**
   ```bash
   curl https://your-backend-name.railway.app/health/
   ```

4. **Test Frontend Independently:**
   - Visit Vercel URL directly
   - Check if frontend loads

5. **Check CORS Configuration:**
   - Verify CORS_ALLOWED_ORIGINS in Railway
   - Test with browser dev tools

6. **Monitor Logs:**
   - Railway: Check for backend errors
   - Vercel: Check for build errors
   - Browser: Check for console errors

---

## 🎯 Common Error Messages & Fixes

### "Failed to fetch"
**Fix:** Check VITE_API_URL in Vercel points to Railway backend

### "CORS policy blocked"
**Fix:** Add Vercel URL to CORS_ALLOWED_ORIGINS in Railway

### "Application error"
**Fix:** Check Railway logs for backend errors

### "Build failed"
**Fix:** Check requirements.txt or package.json for dependency issues

### "Database connection failed"
**Fix:** Ensure DATABASE_URL=${{Postgres.DATABASE_URL}} in Railway

### "Environment variable not found"
**Fix:** Add missing variables to respective service dashboards

---

## 💡 Pro Tips

### 1. Test URLs Manually
```bash
# Always test these URLs work:
https://your-backend-name.railway.app/health/
https://your-app-name.vercel.app
```

### 2. Use Browser Dev Tools
- Network tab for API call debugging
- Console for JavaScript errors
- Application tab for environment variables

### 3. Monitor Resource Usage
- Railway: Check usage doesn't exceed $5 credit
- Vercel: Monitor function execution time

### 4. Keep Logs Clean
- Remove debug prints from production
- Use proper logging levels
- Monitor error rates

---

## 📞 When to Contact Support

### Railway Support:
- Persistent build failures
- Database connectivity issues
- Billing questions
- Platform-specific problems

### Vercel Support:
- Build configuration issues
- Domain/DNS problems
- Function execution errors
- Performance issues

---

## ✅ Troubleshooting Checklist

Before contacting support:

### Railway Backend:
- [ ] All environment variables set correctly
- [ ] DATABASE_URL uses ${{Postgres.DATABASE_URL}}
- [ ] PostgreSQL service is running
- [ ] Build logs show no errors
- [ ] Health endpoint responds

### Vercel Frontend:
- [ ] Build settings configured correctly
- [ ] Environment variables set with VITE_ prefix
- [ ] Frontend loads without errors
- [ ] API calls reach Railway backend

### Integration:
- [ ] CORS_ALLOWED_ORIGINS includes Vercel URL
- [ ] VITE_API_URL points to Railway backend
- [ ] No CORS errors in browser console
- [ ] Authentication works end-to-end

---

## 🔄 Quick Fix Commands

### Redeploy Railway:
```bash
# In Railway dashboard:
Your Service → Deploy button
```

### Redeploy Vercel:
```bash
# In Vercel dashboard:
Your Project → Deployments → Redeploy
```

### Test Integration:
```bash
# Test full flow:
1. Visit Vercel URL
2. Open browser dev tools
3. Check Network tab for API calls
4. Verify no CORS errors
```

---

*Most issues are resolved by checking URLs and environment variables!*
