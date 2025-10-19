"""
Image proxy views for handling image uploads and serving
"""
import os
import uuid
import time
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_image_proxy(request):
    """
    Upload image and return a proxy URL that will serve the image
    """
    try:
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES['image']
        
        # Generate unique filename
        file_extension = os.path.splitext(uploaded_file.name)[1]
        timestamp = int(time.time())
        unique_filename = f"image_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

        # Save to a temporary location
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        file_path = os.path.join(temp_dir, unique_filename)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Return proxy URL
        proxy_url = f"/api/image-proxy/{unique_filename}"
        full_url = request.build_absolute_uri(proxy_url)

        return Response({
            "success": True,
            "image_url": full_url,
            "filename": unique_filename
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'OPTIONS'])
@permission_classes([AllowAny])
def serve_image_proxy(request, filename):
    """
    Serve image through proxy
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response['Access-Control-Allow-Headers'] = 'accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
        response['Access-Control-Max-Age'] = '86400'  # Cache for 24 hours
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
        
        if not os.path.exists(file_path):
            raise Http404("Image not found")
        
        with open(file_path, 'rb') as f:
            # Determine content type based on file extension
            file_extension = os.path.splitext(filename)[1].lower()
            content_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.bmp': 'image/bmp'
            }
            content_type = content_type_map.get(file_extension, 'image/jpeg')
            
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
            
            # Add CORS headers for maximum compatibility (Firebase, Flutter web, etc.)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
            response['Access-Control-Allow-Headers'] = 'accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
            response['Access-Control-Max-Age'] = '86400'  # Cache for 24 hours
            response['Access-Control-Allow-Credentials'] = 'true'
            
            return response
            
    except Exception as e:
        raise Http404("Image not found")


@api_view(['GET', 'OPTIONS'])
@permission_classes([AllowAny])
def test_image_cors(request):
    """
    Test endpoint to check CORS headers
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response['Access-Control-Allow-Headers'] = 'accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
        response['Access-Control-Max-Age'] = '86400'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    response = HttpResponse("CORS test successful - Firebase and all domains allowed")
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
    response['Access-Control-Allow-Headers'] = 'accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
    response['Access-Control-Max-Age'] = '86400'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Content-Type'] = 'text/plain'
    return response
