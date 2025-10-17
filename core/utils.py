"""
Utility functions for handling static file uploads in production
"""
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def save_media_to_static(file, filename):
    """
    Save uploaded file to static files directory in production
    """
    if settings.DEBUG:
        # In development, use default media handling
        return default_storage.save(f'media/{filename}', file)
    else:
        # In production, save to static files directory
        static_media_dir = os.path.join(settings.STATIC_ROOT, 'media')
        os.makedirs(static_media_dir, exist_ok=True)
        
        # Save file to static directory
        file_path = os.path.join(static_media_dir, filename)
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Return the static URL
        return f'/static/media/{filename}'


def get_media_url(file_path):
    """
    Get the correct media URL for both development and production
    """
    if settings.DEBUG:
        return f'/media/{file_path}'
    else:
        return f'/static/media/{file_path}'


def get_server_media_url(request, file_path):
    """
    Get the full server URL for media files
    """
    if hasattr(settings, 'SERVER_DOMAIN') and hasattr(settings, 'SERVER_PROTOCOL'):
        # Use server configuration for production
        return f"{settings.SERVER_PROTOCOL}://{settings.SERVER_DOMAIN}{settings.MEDIA_URL}{file_path}"
    else:
        # Fallback to request.build_absolute_uri
        return request.build_absolute_uri(f"{settings.MEDIA_URL}{file_path}")
