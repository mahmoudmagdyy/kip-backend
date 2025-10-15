#!/usr/bin/env python3
"""
Quick fix script for media files on Render.com
This script creates the media directory and sets proper permissions
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_production')
django.setup()

def create_media_directories():
    """Create media directories and set permissions"""
    print("📁 Creating media directories...")
    
    # Get the base directory
    BASE_DIR = Path(__file__).resolve().parent
    
    # Create media directories
    media_dirs = [
        BASE_DIR / 'media',
        BASE_DIR / 'media' / 'offers',
        BASE_DIR / 'media' / 'uploads',
        BASE_DIR / 'media' / 'users',
    ]
    
    for media_dir in media_dirs:
        media_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {media_dir}")
        
        # Set permissions (755)
        os.chmod(media_dir, 0o755)
        print(f"🔐 Set permissions: {media_dir}")
    
    print("✅ Media directories created successfully!")

if __name__ == "__main__":
    create_media_directories()
