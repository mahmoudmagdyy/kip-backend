# 📁 Media Files Configuration for Render.com

## ❌ **Problem**
The uploaded image `uploaded-image.png` returns 404 because:
1. **Media files are not persisted** on Render.com (they get deleted on each deployment)
2. **Media directory doesn't exist** on the server
3. **File permissions** may be incorrect

## ✅ **Solutions**

### **Solution 1: Use Cloud Storage (Recommended)**

#### **Option A: AWS S3**
1. **Install boto3**:
   ```bash
   pip install boto3 django-storages
   ```

2. **Add to requirements.txt**:
   ```
   boto3==1.34.0
   django-storages==1.14.2
   ```

3. **Update settings_production.py**:
   ```python
   # AWS S3 Configuration
   AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
   AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
   
   # Media files
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
   ```

#### **Option B: Cloudinary**
1. **Install cloudinary**:
   ```bash
   pip install cloudinary
   ```

2. **Add to requirements.txt**:
   ```
   cloudinary==1.41.0
   ```

3. **Update settings_production.py**:
   ```python
   import cloudinary
   import cloudinary.uploader
   import cloudinary.api
   
   cloudinary.config(
       cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
       api_key=os.environ.get('CLOUDINARY_API_KEY'),
       api_secret=os.environ.get('CLOUDINARY_API_SECRET')
   )
   ```

### **Solution 2: Create Media Directory on Server**

#### **Update deploy.sh**:
```bash
#!/bin/bash

echo "🚀 Starting deployment preparation..."

# Create media directory
echo "📁 Creating media directory..."
mkdir -p media
mkdir -p media/offers
mkdir -p media/uploads

# Set permissions
echo "🔐 Setting permissions..."
chmod 755 media
chmod 755 media/offers
chmod 755 media/uploads

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=backend.settings_production

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.settings_production

echo "✅ Deployment preparation completed!"
```

#### **Update build command in Render.com**:
```bash
mkdir -p media/offers media/uploads && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
```

### **Solution 3: Use Static Files for Images**

#### **Update settings_production.py**:
```python
# Use static files for media in production
if not DEBUG:
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = BASE_DIR / 'staticfiles' / 'media'
```

#### **Update build command**:
```bash
mkdir -p staticfiles/media && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
```

## 🚀 **Recommended Implementation**

### **Step 1: Use Cloudinary (Easiest)**

1. **Sign up for Cloudinary** (free tier available)
2. **Get your credentials** from Cloudinary dashboard
3. **Update requirements.txt**:
   ```
   cloudinary==1.41.0
   ```

4. **Update settings_production.py**:
   ```python
   import cloudinary
   import cloudinary.uploader
   import cloudinary.api
   
   # Cloudinary configuration
   cloudinary.config(
       cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
       api_key=os.environ.get('CLOUDINARY_API_KEY'),
       api_secret=os.environ.get('CLOUDINARY_API_SECRET')
   )
   ```

5. **Update your image upload views**:
   ```python
   import cloudinary.uploader
   
   def upload_image(request):
       if request.FILES.get('image'):
           result = cloudinary.uploader.upload(request.FILES['image'])
           image_url = result['secure_url']
           # Save image_url to your model
   ```

6. **Set environment variables in Render.com**:
   ```bash
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

### **Step 2: Alternative - Use Static Files**

1. **Update build command in Render.com**:
   ```bash
   mkdir -p staticfiles/media && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
   ```

2. **Update settings_production.py**:
   ```python
   # Use static files for media in production
   if not DEBUG:
       MEDIA_URL = '/static/media/'
       MEDIA_ROOT = BASE_DIR / 'staticfiles' / 'media'
   ```

## 🧪 **Testing After Configuration**

### **Test Image Upload**:
```bash
curl -X POST "https://kip-backend.onrender.com/api/admin/offers/create-image/" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your-image.jpg"
```

### **Test Image Access**:
```bash
curl "https://kip-backend.onrender.com/media/uploaded-image.png"
```

## 📋 **Environment Variables for Cloudinary**

Set these in your Render.com service:
```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

## 🎯 **Quick Fix (Temporary)**

If you need a quick fix, update your build command in Render.com:
```bash
mkdir -p media && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
```

**Note**: This is temporary as files will be lost on each deployment.

## 🚀 **Ready to Deploy!**

Choose your preferred solution:
- ✅ **Cloudinary** (Recommended) - Persistent, reliable
- ✅ **Static Files** - Simple, but files lost on deployment
- ✅ **AWS S3** - Professional, scalable

**Your media files will work correctly after implementing any of these solutions!** 🎯
