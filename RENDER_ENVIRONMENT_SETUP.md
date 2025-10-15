# 🔧 How to Set Environment Variables in Render.com

## 📍 **Step-by-Step Guide**

### **Step 1: Go to Your Service**
1. **Open Render.com dashboard**
2. **Click on your service** (kip-backend)
3. **You'll see your service dashboard**

### **Step 2: Find Environment Tab**
1. **Look for tabs** at the top of your service page
2. **Click on "Environment"** tab
3. **You'll see a list of environment variables**

### **Step 3: Add Environment Variables**
1. **Click "Add Environment Variable"** button
2. **Add each variable one by one:**

#### **Variable 1: DEBUG**
- **Key**: `DEBUG`
- **Value**: `False`
- **Click "Save"**

#### **Variable 2: SECRET_KEY**
- **Key**: `SECRET_KEY`
- **Value**: `django-insecure-your-generated-key-here`
- **Click "Save"**

#### **Variable 3: DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: `postgresql://user:password@host:port/database`
- **Click "Save"**

#### **Variable 4: ALLOWED_HOSTS**
- **Key**: `ALLOWED_HOSTS`
- **Value**: `kip-backend.onrender.com`
- **Click "Save"**

## 🖼️ **Visual Guide**

### **What You'll See:**
```
Service Dashboard
├── Overview
├── Environment  ← Click this tab
├── Settings
└── Logs
```

### **Environment Variables Page:**
```
Environment Variables
├── Add Environment Variable
├── DEBUG = False
├── SECRET_KEY = django-insecure-...
├── DATABASE_URL = postgresql://...
└── ALLOWED_HOSTS = kip-backend.onrender.com
```

## 🔑 **How to Get Each Value**

### **1. DEBUG**
- **Value**: `False` (always this for production)

### **2. SECRET_KEY**
**Generate a Django secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**Or use online generator**: [djecrety.ir](https://djecrety.ir/)

### **3. DATABASE_URL**
**Create PostgreSQL database:**
1. **Render.com dashboard** → **"New +"** → **"PostgreSQL"**
2. **Name**: `kip-database`
3. **Plan**: Free
4. **Create Database**
5. **Click on database** → **"Info" tab** → **Copy "External Database URL"**

### **4. ALLOWED_HOSTS**
**Get your service URL:**
1. **Go to your service**
2. **Look at "URL" field**
3. **Copy the domain** (without https://)

## 📋 **Complete Example**

Your environment variables should look like this:

```
DEBUG = False
SECRET_KEY = django-insecure-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz=
DATABASE_URL = postgresql://kip_user:abc123def456@dpg-abc123def456-a.oregon-postgres.render.com/kip_database
ALLOWED_HOSTS = kip-backend.onrender.com
```

## 🚀 **After Setting Variables**

1. **Save all variables**
2. **Go to "Settings" tab**
3. **Update build command** (if needed)
4. **Click "Manual Deploy"**
5. **Wait for deployment to complete**

## 🔧 **Troubleshooting**

### **If You Can't Find Environment Tab:**
1. **Make sure you're in your service** (not dashboard)
2. **Look for tabs** at the top
3. **Click on "Environment"**

### **If Variables Don't Save:**
1. **Check for typos** in variable names
2. **Make sure values are correct**
3. **Try refreshing the page**

### **If Deployment Fails:**
1. **Check the logs** in Render.com
2. **Verify all variables** are set correctly
3. **Make sure build command** is correct

## 🎯 **Quick Checklist**

- [ ] **Go to your service** in Render.com
- [ ] **Click "Environment" tab**
- [ ] **Add DEBUG = False**
- [ ] **Add SECRET_KEY = your-generated-key**
- [ ] **Add DATABASE_URL = your-database-url**
- [ ] **Add ALLOWED_HOSTS = your-domain**
- [ ] **Save all variables**
- [ ] **Redeploy your service**

**Your environment variables are now set!** 🎯
