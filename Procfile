# Procfile for Heroku/Render deployment
web: daphne -b 0.0.0.0 -p $PORT backend.asgi:application
worker: python manage.py migrate && python manage.py collectstatic --noinput