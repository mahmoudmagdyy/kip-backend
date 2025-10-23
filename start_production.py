#!/usr/bin/env python
"""
Production startup script with error handling
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_production')

def main():
    try:
        # Initialize Django
        django.setup()
        print("✅ Django initialized successfully")
        
        # Run migrations
        print("Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--settings=backend.settings_production'])
        
        # Collect static files
        print("Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--settings=backend.settings_production'])
        
        print("✅ Production setup completed successfully")
        
        # Start the server
        import subprocess
        import os
        
        port = os.environ.get('PORT', '8000')
        print(f"Starting server on port {port}...")
        
        # Use daphne to start the ASGI server
        subprocess.run([
            'daphne', 
            '-b', '0.0.0.0', 
            '-p', port, 
            'backend.asgi:application'
        ])
        
    except Exception as e:
        print(f"❌ Error starting production server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
