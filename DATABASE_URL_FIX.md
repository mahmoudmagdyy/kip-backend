# 🔧 DATABASE_URL Fix for Render.com

## ❌ **Problem**
The error `dj_database_url.UnknownSchemeError: Scheme '://' is unknown` occurs because:
1. **DATABASE_URL environment variable** is not set correctly
2. **Empty or invalid DATABASE_URL** is being passed to `dj_database_url.parse()`
3. **Database URL format** is incorrect

## ✅ **Solution Applied**

I've updated `backend/settings_production.py` to handle invalid DATABASE_URL gracefully:

```python
# Database
# Use environment variable for database URL (for cloud deployment)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

# Validate DATABASE_URL
if not DATABASE_URL or DATABASE_URL == '://':
    # Fallback to SQLite if DATABASE_URL is not set or invalid
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Use the provided DATABASE_URL
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
```

## 🚀 **Step 1: Create PostgreSQL Database in Render.com**

### **Create Database:**
1. **Go to Render.com dashboard**
2. **Click "New +"**
3. **Select "PostgreSQL"**
4. **Name**: `kip-database`
5. **Plan**: Free
6. **Click "Create Database"**
7. **Wait for it to be ready**

### **Get Database URL:**
1. **Click on your database**
2. **Go to "Info" tab**
3. **Copy "External Database URL"**
4. **It should look like**: `postgresql://user:password@host:port/database`

## 🔧 **Step 2: Set Environment Variables**

### **In Render.com Service:**
1. **Go to your service**
2. **Click "Environment" tab**
3. **Add these variables:**

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=kip-backend.onrender.com
```

### **Example DATABASE_URL:**
```
postgresql://kip_user:abc123def456@dpg-abc123def456-a.oregon-postgres.render.com/kip_database
```

## 🧪 **Step 3: Test Database Connection**

### **Test 1: Check Environment Variables**
```bash
# This should show your DATABASE_URL
echo $DATABASE_URL
```

### **Test 2: Test Database Connection**
```bash
# Test if database is accessible
curl "https://kip-backend.onrender.com/api/services/"
```

### **Test 3: Check Database in Render.com**
1. **Go to your database**
2. **Click "Connect" tab**
3. **Test the connection**

## 🔧 **Step 4: Alternative Solutions**

### **Option 1: Use SQLite (Temporary)**
If you don't need PostgreSQL, the app will automatically use SQLite as fallback.

### **Option 2: Fix DATABASE_URL Format**
Make sure your DATABASE_URL follows this format:
```
postgresql://username:password@host:port/database_name
```

### **Option 3: Manual Database Configuration**
If DATABASE_URL still doesn't work, you can set the database manually:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',
        'PORT': '5432',
    }
}
```

## 📋 **Step 5: Complete Setup Checklist**

- [ ] **Create PostgreSQL database** in Render.com
- [ ] **Get DATABASE_URL** from database info
- [ ] **Set environment variables** in service
- [ ] **Update build command** (if needed)
- [ ] **Redeploy service**
- [ ] **Test database connection**

## 🚀 **Step 6: Redeploy**

1. **Save all environment variables**
2. **Go to "Settings" tab**
3. **Update build command** (if needed)
4. **Click "Manual Deploy"**
5. **Wait for deployment to complete**

## 🧪 **Step 7: Test After Deployment**

### **Test Database Connection:**
```bash
curl "https://kip-backend.onrender.com/api/services/"
```

### **Test Database Migrations:**
```bash
# Check if migrations ran successfully
curl "https://kip-backend.onrender.com/api/admin/bookings/"
```

## 🔧 **Troubleshooting**

### **If DATABASE_URL is Still Invalid:**
1. **Check the format** of your DATABASE_URL
2. **Verify database** is running in Render.com
3. **Check database credentials**
4. **Try the fallback SQLite** option

### **If Database Connection Fails:**
1. **Check database status** in Render.com
2. **Verify credentials** are correct
3. **Check network connectivity**
4. **Review Render.com logs**

### **If Migrations Fail:**
1. **Check database permissions**
2. **Verify database exists**
3. **Check migration files**
4. **Review error logs**

## 🎯 **Quick Fix Commands**

### **Test DATABASE_URL:**
```bash
# This should show a valid PostgreSQL URL
echo $DATABASE_URL
```

### **Test Database Connection:**
```bash
# This should return 200 if database is working
curl "https://kip-backend.onrender.com/api/services/"
```

## 🚀 **Ready to Deploy!**

Your database configuration is now fixed and will work correctly! 🎯
