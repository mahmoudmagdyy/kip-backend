# 🔧 Render.com Media Files Fix

## ❌ **Problem**
The image `uploaded-image.png` returns 404 because:
- **Media files are not persisted** on Render.com
- **Media directory doesn't exist** on the server
- **Files get deleted** on each deployment

## ✅ **Quick Fix (Immediate)**

### **Update Build Command in Render.com:**
```bash
mkdir -p media/offers media/uploads && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
```

### **Update Start Command:**
```bash
daphne -b 0.0.0.0 -p $PORT backend.asgi:application
```

## 🚀 **Permanent Solutions**

### **Solution 1: Use Cloudinary (Recommended)**

#### **Step 1: Sign up for Cloudinary**
1. Go to [cloudinary.com](https://cloudinary.com)
2. Create a free account
3. Get your credentials from the dashboard

#### **Step 2: Update requirements.txt**
```
cloudinary==1.41.0
```

#### **Step 3: Update settings_production.py**
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

#### **Step 4: Update image upload views**
```python
import cloudinary.uploader

def upload_image(request):
    if request.FILES.get('image'):
        result = cloudinary.uploader.upload(request.FILES['image'])
        image_url = result['secure_url']
        # Save image_url to your model
```

#### **Step 5: Set environment variables in Render.com**
```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### **Solution 2: Use Static Files**

#### **Update settings_production.py**
```python
# Use static files for media in production
if not DEBUG:
    MEDIA_URL = '/static/media/'
    MEDIA_ROOT = BASE_DIR / 'staticfiles' / 'media'
```

#### **Update build command**
```bash
mkdir -p staticfiles/media && pip install -r requirements.txt && python manage.py migrate --settings=backend.settings_production && python manage.py collectstatic --noinput --settings=backend.settings_production
```

### **Solution 3: Use AWS S3**

#### **Install dependencies**
```bash
pip install boto3 django-storages
```

#### **Add to requirements.txt**
```
boto3==1.34.0
django-storages==1.14.2
```

#### **Update settings_production.py**
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

## 🧪 **Testing After Fix**

### **Test Image Upload**
```bash
curl -X POST "https://kip-backend.onrender.com/api/admin/offers/create-image/" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your-image.jpg"
```

### **Test Image Access**
```bash
curl "https://kip-backend.onrender.com/media/uploaded-image.png"
```

## 📋 **Environment Variables**

### **For Cloudinary:**
```bash
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### **For AWS S3:**
```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

## 🎯 **Recommended Steps**

1. **Immediate Fix**: Update build command to create media directories
2. **Long-term**: Implement Cloudinary for persistent storage
3. **Test**: Verify image upload and access works

## 🚀 **Ready to Deploy!**

Choose your solution:
- ✅ **Quick Fix** - Create media directories (temporary)
- ✅ **Cloudinary** - Persistent cloud storage (recommended)
- ✅ **AWS S3** - Professional cloud storage
- ✅ **Static Files** - Simple but files lost on deployment

**Your media files will work correctly after implementing any of these solutions!** 🎯
