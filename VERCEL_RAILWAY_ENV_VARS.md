# 🔧 Vercel + Railway Environment Variables Reference

## Railway Backend Variables

Copy these **exact variable names** to your Railway service Variables tab:

### 🔑 Core Django Settings
```bash
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=backend.settings
```

### 🗄️ Database Configuration
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
```
*Railway auto-populates this from your PostgreSQL service*

### 🤖 ML Configuration
```bash
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
```

### 🌐 Frontend & CORS
```bash
FRONTEND_URL=https://your-app-name.vercel.app
ALLOWED_HOSTS=your-backend-name.railway.app,your-app-name.vercel.app,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
```

### 📁 Static Files
```bash
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

---

## Vercel Frontend Variables

Copy these to your Vercel project Settings → Environment Variables:

### 🔗 API Configuration
```bash
VITE_API_URL=https://your-backend-name.railway.app
VITE_API_BASE_URL=https://your-backend-name.railway.app/api
```

### 📱 App Configuration
```bash
VITE_APP_NAME=AI Tutorial LogBlog
VITE_APP_DESCRIPTION=ML-powered tutorial generation platform
```

---

## 📝 How to Set Environment Variables

### Railway:
1. Go to your Railway project
2. Select your backend service
3. Click "Variables" tab
4. Click "New Variable"
5. Add name and value
6. Click "Add"

### Vercel:
1. Go to your Vercel project
2. Click "Settings"
3. Click "Environment Variables"
4. Add name and value
5. Select "Production" environment
6. Click "Save"

---

## 🎯 Example Configuration

If your services are named:
- **Railway**: `logblog-backend-production-abc123`
- **Vercel**: `logblog-frontend`

### Railway Variables:
```bash
SECRET_KEY=django-insecure-xyz123abc456def789ghi012jkl345mno678pqr901stu234vwx567yz
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
FRONTEND_URL=https://logblog-frontend.vercel.app
ALLOWED_HOSTS=logblog-backend-production-abc123.railway.app,logblog-frontend.vercel.app,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://logblog-frontend.vercel.app
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

### Vercel Variables:
```bash
VITE_API_URL=https://logblog-backend-production-abc123.railway.app
VITE_API_BASE_URL=https://logblog-backend-production-abc123.railway.app/api
VITE_APP_NAME=AI Tutorial LogBlog
```

---

## 🔍 How to Get Required Values

### 1. SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Railway Backend URL
1. Go to Railway project
2. Select your backend service
3. Click "Settings" → "Domains"
4. Copy the generated domain (e.g., `service-name.railway.app`)

### 3. Vercel Frontend URL
1. Go to Vercel project
2. Click "Domains" tab
3. Copy the generated domain (e.g., `your-app.vercel.app`)

### 4. Database URL
- Railway automatically provides this as `${{Postgres.DATABASE_URL}}`
- Don't change this variable - Railway manages it

---

## 🔄 Variable Dependencies

### Deployment Order:
1. **Deploy Railway backend** first
2. **Get Railway URL**
3. **Set Vercel variables** with Railway URL
4. **Deploy Vercel frontend**
5. **Update Railway variables** with Vercel URL
6. **Redeploy Railway** to apply CORS changes

### Critical Connections:
```
Railway CORS_ALLOWED_ORIGINS ← Vercel URL
Vercel VITE_API_URL ← Railway URL
```

---

## ⚠️ Important Notes

### Security:
- **Never commit** environment variables to repository
- **Use strong SECRET_KEY** (50+ characters)
- **Always set DEBUG=False** in production

### Common Mistakes:
- ❌ Wrong URL in `VITE_API_URL`
- ❌ Missing comma in `ALLOWED_HOSTS`
- ❌ Forgetting to update `CORS_ALLOWED_ORIGINS`
- ❌ Using external DATABASE_URL instead of `${{Postgres.DATABASE_URL}}`

### Variable Naming:
- **Railway**: Any name (Django convention)
- **Vercel**: Must start with `VITE_` for frontend access

---

## 📊 Variable Validation

### Check Railway Variables:
```bash
# In Railway service logs:
echo "SECRET_KEY length: ${#SECRET_KEY}"
echo "DEBUG: $DEBUG"
echo "DATABASE_URL: $DATABASE_URL"
```

### Check Vercel Variables:
```javascript
// In browser console:
console.log('API URL:', import.meta.env.VITE_API_URL);
console.log('App Name:', import.meta.env.VITE_APP_NAME);
```

---

## 🚨 Troubleshooting Variables

### Problem: "KeyError: 'SECRET_KEY'"
**Fix**: Add SECRET_KEY to Railway variables

### Problem: CORS errors
**Fix**: Update Railway CORS_ALLOWED_ORIGINS with exact Vercel URL

### Problem: Frontend can't reach backend
**Fix**: Update Vercel VITE_API_URL with exact Railway URL

### Problem: Database connection failed
**Fix**: Ensure DATABASE_URL uses `${{Postgres.DATABASE_URL}}`

### Problem: ML models not loading
**Fix**: Check USE_ML_GENERATOR=True and ML_MODEL_PATH

---

## 🔧 Quick Variable Check

### Before deployment, verify:
- [ ] SECRET_KEY is 50+ characters
- [ ] DEBUG=False
- [ ] DATABASE_URL uses Railway reference
- [ ] All URLs match actual service domains
- [ ] CORS_ALLOWED_ORIGINS includes Vercel URL
- [ ] VITE_API_URL points to Railway backend

---

## 🎯 Variable Template

### Railway Backend (.env template):
```bash
SECRET_KEY=your-50-character-secret-key-here
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

### Vercel Frontend (.env template):
```bash
VITE_API_URL=https://your-backend-name.railway.app
VITE_API_BASE_URL=https://your-backend-name.railway.app/api
VITE_APP_NAME=AI Tutorial LogBlog
```

---

*Replace `your-app-name` and `your-backend-name` with your actual service names!*
