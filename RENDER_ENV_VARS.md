# 🔧 Render Environment Variables Reference

## Required Environment Variables

Copy these **exact variable names** to your Render web service Environment tab:

### 🔑 Core Django Settings
```bash
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=backend.settings
```

### 🗄️ Database Configuration
```bash
DATABASE_URL=postgresql://user:pass@host:port/database
```
*Get this from your Render PostgreSQL service → Connect → Internal Database URL*

### 🤖 ML Configuration
```bash
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
```

### 🌐 Frontend & CORS
```bash
FRONTEND_URL=https://your-app-name.onrender.com
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
```

### 📁 Static Files
```bash
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

---

## 📝 How to Set Environment Variables in Render

### Method 1: Through Dashboard
1. Go to your web service
2. Click "Environment" tab
3. Click "Add Environment Variable"
4. Enter variable name and value
5. Click "Save Changes"

### Method 2: Through render.yaml (Optional)
```yaml
envVars:
  - key: SECRET_KEY
    generateValue: true
  - key: DEBUG
    value: "False"
  - key: USE_ML_GENERATOR
    value: "True"
```

---

## 🎯 Example Configuration

If your app name is `logblog-central`, your variables would be:

```bash
SECRET_KEY=django-insecure-xyz123abc456def789ghi012jkl345mno678pqr901stu234vwx567yz
DEBUG=False
DATABASE_URL=postgresql://logblog_user:securepass@dpg-abc123-a.oregon-postgres.render.com/logblog_db
USE_ML_GENERATOR=True
ML_MODEL_PATH=backend/ai_tutorial/models/
ML_DEVICE=cpu
FRONTEND_URL=https://logblog-central.onrender.com
ALLOWED_HOSTS=logblog-central.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://logblog-central.onrender.com
STATIC_URL=/static/
STATIC_ROOT=staticfiles/
```

---

## 🔍 How to Get Required Values

### 1. SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. DATABASE_URL
1. Go to your PostgreSQL service in Render
2. Click "Connect"
3. Copy "Internal Database URL"

### 3. Your App Name
- Check your web service URL
- Extract app name from: `https://your-app-name.onrender.com`

---

## ⚠️ Important Notes

### Security:
- **Never commit** environment variables to your repository
- **Use strong SECRET_KEY** (50+ characters)
- **Always set DEBUG=False** in production

### Common Mistakes:
- ❌ Using external DATABASE_URL instead of internal
- ❌ Wrong app name in FRONTEND_URL
- ❌ Missing comma in ALLOWED_HOSTS
- ❌ Forgetting to update CORS_ALLOWED_ORIGINS

### Testing Variables:
After setting variables, restart your service to apply changes:
1. Go to "Settings" → "Manual Deploy"
2. Click "Deploy Latest Commit"

---

## 📊 Variable Validation

### Check if variables are set correctly:
```bash
# In your Render shell (optional)
echo $SECRET_KEY
echo $DATABASE_URL
echo $USE_ML_GENERATOR
```

### Django settings validation:
```python
# This will be checked during deployment
from django.conf import settings
print(settings.SECRET_KEY)
print(settings.DEBUG)
print(settings.USE_ML_GENERATOR)
```

---

## 🚨 Troubleshooting Environment Variables

### Problem: App won't start
**Check**: All required variables are set with correct values

### Problem: Database connection failed
**Check**: DATABASE_URL is the internal URL from PostgreSQL service

### Problem: CORS errors
**Check**: FRONTEND_URL and CORS_ALLOWED_ORIGINS match your actual domain

### Problem: Static files not loading
**Check**: STATIC_URL and STATIC_ROOT are correctly set

### Problem: ML models not working
**Check**: USE_ML_GENERATOR=True and ML_MODEL_PATH is correct

---

*Copy these variables exactly as shown to your Render dashboard!*
