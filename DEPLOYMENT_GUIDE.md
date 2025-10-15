# 🚀 KIP Backend Deployment Guide

This guide will help you deploy the KIP Backend to various cloud platforms.

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database
- Redis server
- Domain name (optional)

## 🛠️ Deployment Options

### 1. Render.com Deployment

#### Step 1: Prepare Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### Step 2: Create Render Service
1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure the following:

**Build Command:**
```bash
pip install -r requirements_production.txt && python manage.py collectstatic --noinput --settings=backend.settings_production
```

**Start Command:**
```bash
daphne -b 0.0.0.0 -p $PORT backend.asgi:application
```

**Environment Variables:**
```
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://redis-host:6379
ALLOWED_HOSTS=your-app.onrender.com
```

#### Step 3: Add Redis Service
1. Create a Redis service in Render
2. Use the Redis URL in your environment variables

### 2. Heroku Deployment

#### Step 1: Install Heroku CLI
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Create Heroku App
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev
```

#### Step 3: Configure Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
```

#### Step 4: Deploy
```bash
# Deploy to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate --settings=backend.settings_production

# Create superuser
heroku run python manage.py shell --settings=backend.settings_production
```

### 3. Railway Deployment

#### Step 1: Connect Repository
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will auto-detect Django

#### Step 2: Configure Environment
```bash
# Set environment variables in Railway dashboard
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://redis-host:6379
```

#### Step 3: Deploy
Railway will automatically deploy when you push to your repository.

### 4. Docker Deployment

#### Step 1: Build and Run
```bash
# Build Docker image
docker build -t kip-backend .

# Run with Docker Compose
docker-compose up -d
```

#### Step 2: Run Migrations
```bash
docker-compose exec web python manage.py migrate --settings=backend.settings_production
```

## 🔧 Environment Variables

Create a `.env` file or set these in your deployment platform:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/database_name

# Redis
REDIS_URL=redis://localhost:6379

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## 📊 Database Setup

### PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE kip_db;

-- Create user
CREATE USER kip_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE kip_db TO kip_user;
```

### Run Migrations
```bash
python manage.py migrate --settings=backend.settings_production
```

## 🔄 Redis Setup

### Local Redis
```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
```

### Cloud Redis
- **Redis Cloud**: https://redis.com/redis-enterprise-cloud/
- **AWS ElastiCache**: https://aws.amazon.com/elasticache/
- **DigitalOcean Redis**: https://www.digitalocean.com/products/managed-databases

## 🌐 Domain Configuration

### 1. Custom Domain Setup
1. Point your domain to your deployment platform
2. Update `ALLOWED_HOSTS` in environment variables
3. Configure SSL certificates

### 2. CORS Configuration
Update `CORS_ALLOWED_ORIGINS` with your frontend domain:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com",
]
```

## 🔒 Security Configuration

### 1. SSL/HTTPS
- Enable SSL in your deployment platform
- Set `SECURE_SSL_REDIRECT=True` in production
- Configure `SESSION_COOKIE_SECURE=True`
- Set `CSRF_COOKIE_SECURE=True`

### 2. Environment Variables
- Never commit `.env` files
- Use strong secret keys
- Rotate keys regularly

### 3. Database Security
- Use strong database passwords
- Enable SSL for database connections
- Regular backups

## 📈 Monitoring and Logging

### 1. Sentry Integration
```bash
# Install Sentry
pip install sentry-sdk

# Add to settings
SENTRY_DSN=your-sentry-dsn-here
```

### 2. Health Checks
Add a health check endpoint:
```python
# In urls.py
path('health/', views.health_check, name='health_check'),
```

### 3. Logging
Logs are automatically configured in production settings.

## 🚀 Deployment Checklist

### Before Deployment
- [ ] All tests pass
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Static files collected
- [ ] Security settings configured

### After Deployment
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Health check endpoint working
- [ ] WebSocket connections working
- [ ] API endpoints responding
- [ ] Static files serving correctly

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
python manage.py dbshell --settings=backend.settings_production
```

#### 2. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput --settings=backend.settings_production

# Check static files directory
ls -la staticfiles/
```

#### 3. WebSocket Not Working
```bash
# Check Redis connection
redis-cli ping

# Check channel layers
python manage.py shell --settings=backend.settings_production
```

#### 4. CORS Issues
```bash
# Check CORS settings
python manage.py shell --settings=backend.settings_production
```

## 📞 Support

If you encounter issues during deployment:

1. Check the logs in your deployment platform
2. Verify environment variables
3. Test database and Redis connections
4. Check the health check endpoint

## 🎯 Production URLs

After successful deployment, your API will be available at:

- **API Base**: `https://your-domain.com/api/`
- **Admin**: `https://your-domain.com/admin/`
- **WebSocket**: `wss://your-domain.com/ws/admin/bookings/`
- **Health Check**: `https://your-domain.com/health/`

## 📚 API Documentation

- **Agent Booking**: `POST /api/agent/booking/create/`
- **Admin Bookings**: `GET /api/admin/bookings/`
- **User Authentication**: `POST /api/login/`
- **Services**: `GET /api/services/`
- **Offers**: `GET /api/offers/`

---

**🎉 Congratulations! Your KIP Backend is now ready for production!**