# Django App Deployment Guide for Hostinger

## Prerequisites
- Django app ready for deployment
- Hostinger hosting account
- Git repository with your code

## Files Created/Modified for Deployment

### 1. Production Configuration
- `backend/settings_production.py` - Production-specific settings
- Updated `backend/settings.py` with environment variable support

### 2. Deployment Files
- `Procfile` - Defines how to run the app
- `runtime.txt` - Specifies Python version
- `.gitignore` - Excludes unnecessary files from version control

### 3. Static Files Configuration
- WhiteNoise middleware for serving static files
- Proper static files settings for production

## Deployment Steps for Hostinger

### Step 1: Prepare Your Repository
1. Make sure all files are committed to git
2. Push to your GitHub repository

### Step 2: Hostinger Setup
1. Log into your Hostinger control panel
2. Go to "Advanced" → "Python App"
3. Create a new Python application

### Step 3: Configure the App
1. **App Name**: Choose a name for your app
2. **Python Version**: Select Python 3.13
3. **Startup File**: `backend.wsgi:application`
4. **Requirements**: Upload your `requirements.txt` file

### Step 4: Environment Variables
Set these environment variables in Hostinger:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
```

### Step 5: Database Configuration
For production, consider using a PostgreSQL database:
1. Create a PostgreSQL database in Hostinger
2. Update `DATABASES` setting in `settings_production.py`
3. Install `psycopg2-binary` in requirements.txt

### Step 6: Static Files
1. Run `python manage.py collectstatic` locally
2. Commit the staticfiles folder
3. Push to repository

### Step 7: Server Configuration
1. Update `ALLOWED_HOSTS` in settings with your server IP (72.60.209.172)
2. Configure server settings in Hostinger
3. Set up SSL certificate (optional for IP-based access)

## Local Testing Before Deployment

### 1. Test with Production Settings
```bash
python manage.py runserver --settings=backend.settings_production
```

### 2. Collect Static Files
```bash
python manage.py collectstatic
```

### 3. Run Migrations
```bash
python manage.py migrate
```

## Post-Deployment Checklist

- [ ] App is accessible via IP address (72.60.209.172)
- [ ] Static files are loading correctly
- [ ] Database connections work
- [ ] API endpoints respond correctly
- [ ] SSL certificate is active (optional)
- [ ] Environment variables are set

## Troubleshooting

### Common Issues:
1. **Static files not loading**: Check WhiteNoise configuration
2. **Database errors**: Verify database credentials
3. **CORS issues**: Check CORS settings
4. **Import errors**: Ensure all dependencies are in requirements.txt

### Logs:
Check application logs in Hostinger control panel for error details.

## Security Considerations

1. Change the SECRET_KEY for production
2. Set DEBUG=False
3. Use environment variables for sensitive data
4. Enable HTTPS
5. Configure proper CORS settings
6. Use a production database (PostgreSQL recommended)

## Performance Optimization

1. Enable WhiteNoise compression
2. Use CDN for static files
3. Configure database connection pooling
4. Set up caching (Redis recommended)
5. Optimize database queries

## Monitoring

1. Set up error tracking (Sentry recommended)
2. Monitor application performance
3. Set up log aggregation
4. Monitor database performance
