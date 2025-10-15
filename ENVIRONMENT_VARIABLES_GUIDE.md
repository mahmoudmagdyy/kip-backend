# 🔧 Environment Variables Guide for Render.com

## 📋 **Required Environment Variables**

You need to set these in your Render.com service:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=kip-backend.onrender.com
```

## 🔑 **How to Get Each Variable**

### **1. DEBUG=False**
- **What it is**: Django debug mode setting
- **How to get**: Just set this value (it's a setting, not a secret)
- **Value**: `False`

### **2. SECRET_KEY**
- **What it is**: Django secret key for security
- **How to get**: Generate a new one

#### **Option A: Generate Online**
1. Go to [djecrety.ir](https://djecrety.ir/)
2. Click "Generate Secret Key"
3. Copy the generated key

#### **Option B: Generate Locally**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### **Option C: Use Django's Built-in**
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Example SECRET_KEY**: `django-insecure-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz=`

### **3. DATABASE_URL**
- **What it is**: PostgreSQL database connection string
- **How to get**: From Render.com database service

#### **Step 1: Create Database in Render.com**
1. **Go to Render.com dashboard**
2. **Click "New +"**
3. **Select "PostgreSQL"**
4. **Choose plan** (Free tier available)
5. **Name it**: `kip-database`
6. **Click "Create Database"**

#### **Step 2: Get Database URL**
1. **Click on your database**
2. **Go to "Info" tab**
3. **Copy the "External Database URL"**
4. **It looks like**: `postgresql://user:password@host:port/database`

**Example DATABASE_URL**: `postgresql://kip_user:abc123def456@dpg-abc123def456-a.oregon-postgres.render.com/kip_database`

### **4. ALLOWED_HOSTS**
- **What it is**: Your Render.com domain
- **How to get**: From your Render.com service

#### **Step 1: Get Your Service URL**
1. **Go to your Render.com service**
2. **Look at the "URL" field**
3. **Copy the domain part** (without https://)

**Example ALLOWED_HOSTS**: `kip-backend.onrender.com`

## 🚀 **Step-by-Step Setup**

### **Step 1: Create Database**
1. **Go to Render.com dashboard**
2. **Click "New +" → "PostgreSQL"**
3. **Name**: `kip-database`
4. **Plan**: Free
5. **Click "Create Database"**
6. **Wait for it to be ready**

### **Step 2: Get Database URL**
1. **Click on your database**
2. **Go to "Info" tab**
3. **Copy "External Database URL"**

### **Step 3: Generate Secret Key**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Step 4: Set Environment Variables**
1. **Go to your Render.com service**
2. **Click "Environment" tab**
3. **Add each variable**:

```bash
DEBUG=False
SECRET_KEY=django-insecure-your-generated-key-here
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=kip-backend.onrender.com
```

## 🧪 **Test Your Setup**

### **Test Database Connection**
```bash
# Test if database is accessible
curl "https://kip-backend.onrender.com/api/services/"
```

### **Test Environment Variables**
```bash
# Test if DEBUG is working (should not show debug info)
curl "https://kip-backend.onrender.com/api/services/"
```

## 📋 **Complete Example**

Here's what your environment variables should look like:

```bash
DEBUG=False
SECRET_KEY=django-insecure-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz=
DATABASE_URL=postgresql://kip_user:abc123def456@dpg-abc123def456-a.oregon-postgres.render.com/kip_database
ALLOWED_HOSTS=kip-backend.onrender.com
```

## 🔧 **Troubleshooting**

### **If Database Connection Fails:**
1. **Check DATABASE_URL** is correct
2. **Verify database** is running in Render.com
3. **Check database credentials**

### **If SECRET_KEY is Invalid:**
1. **Generate a new one** using the commands above
2. **Make sure it's long enough** (at least 50 characters)
3. **Don't use spaces** in the key

### **If ALLOWED_HOSTS is Wrong:**
1. **Check your service URL** in Render.com
2. **Use only the domain** (without https://)
3. **Don't include trailing slash**

## 🚀 **Ready to Deploy!**

After setting all environment variables:
1. **Save the changes** in Render.com
2. **Trigger a new deployment**
3. **Wait for build to complete**
4. **Test your endpoints**

**Your environment variables are now properly configured!** 🎯
