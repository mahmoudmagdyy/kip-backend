from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
from .models import Service, SubService
from .serializer import ServiceSerializer, ServiceCreateSerializer, SubServiceSerializer, SubServiceCreateSerializer
from .utils import get_server_media_url
import os
import uuid
import time

# ------------------- Service Views -------------------


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def dashboard_services(request):
    """Return all active services with their sub-services"""
    services = Service.objects.filter(is_active=True).order_by('order', 'id')
    serializer = ServiceSerializer(services, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_service(request):
    try:
        uploaded_file = request.FILES.get('image') or request.FILES.get('icon')
        service_data = request.data.copy()

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1]
            filename = f"service_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            service_data['icon'] = get_server_media_url(request, filename)

        serializer = ServiceCreateSerializer(data=service_data)
        if serializer.is_valid():
            service = serializer.save()
            return Response({"success": True, "message": "Service created successfully",
                             "data": ServiceSerializer(service, context={'request': request}).data}, status=201)
        return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "message": f"Error creating service: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceSerializer(service, context={'request': request})
        return Response({"success": True, "data": serializer.data})
    except Service.DoesNotExist:
        return Response({"success": False, "message": "Service not found"}, status=404)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# @authentication_classes([])
# def update_service(request, service_id):
#     try:
#         service = Service.objects.get(id=service_id)
#         uploaded_file = request.FILES.get('image') or request.FILES.get('icon')
#         service_data = request.data.copy()

#         if uploaded_file:
#             ext = os.path.splitext(uploaded_file.name)[1]
#             filename = f"service_{service_id}_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
#             os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
#             path = os.path.join(settings.MEDIA_ROOT, filename)
#             with open(path, 'wb') as f:
#                 for chunk in uploaded_file.chunks():
#                     f.write(chunk)
#             service_data['icon'] = get_server_media_url(request, filename)

#         serializer = ServiceCreateSerializer(service, data=service_data, partial=True)
#         if serializer.is_valid():
#             service = serializer.save()

#             return Response({"success": True, "message": "Service updated successfully",
#                              "data": ServiceSerializer(service, context={'request': request}).data})
#         return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=400)
#     except Service.DoesNotExist:
#         return Response({"success": False, "message": "Service not found"}, status=404)


# @api_view(['DELETE'])
# @permission_classes([AllowAny])
# @authentication_classes([])
# def delete_service(request, service_id):
#     try:
#         service = Service.objects.get(id=service_id)
#         service.delete()
#         return Response({"success": True, "message": "Service deleted successfully"})
#     except Service.DoesNotExist:
#         return Response({"success": False, "message": "Service not found"}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Add authentication
@authentication_classes([JWTAuthentication])
def update_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        uploaded_file = request.FILES.get('image') or request.FILES.get('icon')
        service_data = request.data.copy()

        # Store old icon path for cleanup
        old_icon_path = None
        if service.icon:
            old_icon_path = service.icon

        if uploaded_file:
            # Validate file type
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in allowed_extensions:
                return Response({
                    "success": False, 
                    "message": "Invalid file type. Allowed: JPG, PNG, GIF, WEBP"
                }, status=400)

            # Validate file size (5MB limit)
            if uploaded_file.size > 5 * 1024 * 1024:
                return Response({
                    "success": False, 
                    "message": "File too large. Maximum size: 5MB"
                }, status=400)

            filename = f"service_{service_id}_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            path = os.path.join(settings.MEDIA_ROOT, filename)
            
            with open(path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            # Fix URL construction to avoid duplication
            if hasattr(settings, 'SERVER_DOMAIN') and hasattr(settings, 'SERVER_PROTOCOL'):
                # Check if SERVER_DOMAIN already includes protocol
                if settings.SERVER_DOMAIN.startswith(('http://', 'https://')):
                    service_data['icon'] = f"{settings.SERVER_DOMAIN}{settings.MEDIA_URL}{filename}"
                else:
                    service_data['icon'] = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_DOMAIN}{settings.MEDIA_URL}{filename}"
            else:
                service_data['icon'] = request.build_absolute_uri(f"{settings.MEDIA_URL}{filename}")

        serializer = ServiceCreateSerializer(service, data=service_data, partial=True)
        if serializer.is_valid():
            service = serializer.save()
            
            # Clean up old file if it exists and is different from new one
            if old_icon_path and old_icon_path != service.icon:
                try:
                    # Extract filename from URL
                    old_filename = old_icon_path.split('/')[-1]
                    old_file_path = os.path.join(settings.MEDIA_ROOT, old_filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                except Exception as e:
                    # Log error but don't fail the update
                    print(f"Error cleaning up old file: {e}")
            
            return Response({
                "success": True, 
                "message": "Service updated successfully",
                "data": ServiceSerializer(service, context={'request': request}).data
            })
        
        return Response({
            "success": False, 
            "message": "Invalid data", 
            "errors": serializer.errors
        }, status=400)
        
    except Service.DoesNotExist:
        return Response({
            "success": False, 
            "message": "Service not found"
        }, status=404)
    except Exception as e:
        return Response({
            "success": False, 
            "message": f"Update failed: {str(e)}"
        }, status=500)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Add authentication
@authentication_classes([JWTAuthentication])
def delete_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        
        # Store icon path for cleanup
        icon_path = service.icon
        
        # Delete associated sub-services first
        sub_services = service.sub_services.all()
        for sub_service in sub_services:
            # Clean up sub-service icon if exists
            if sub_service.icon:
                try:
                    sub_filename = sub_service.icon.split('/')[-1]
                    sub_file_path = os.path.join(settings.MEDIA_ROOT, sub_filename)
                    if os.path.exists(sub_file_path):
                        os.remove(sub_file_path)
                except Exception as e:
                    print(f"Error cleaning up sub-service file: {e}")
        
        # Delete the service (this will cascade delete sub-services)
        service.delete()
        
        # Clean up service icon file
        if icon_path:
            try:
                filename = icon_path.split('/')[-1]
                file_path = os.path.join(settings.MEDIA_ROOT, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up service file: {e}")
        
        return Response({
            "success": True, 
            "message": "Service and associated sub-services deleted successfully"
        })
        
    except Service.DoesNotExist:
        return Response({
            "success": False, 
            "message": "Service not found"
        }, status=404)
    except Exception as e:
        return Response({
            "success": False, 
            "message": f"Delete failed: {str(e)}"
        }, status=500)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_sub_service(request):
    try:
        uploaded_file = request.FILES.get('image') or request.FILES.get('icon')
        sub_service_data = request.data.copy()

        service_id = sub_service_data.get('service')
        if not service_id:
            return Response({"success": False, "message": "'service' field is required"}, status=400)

        # Validate service exists
        try:
            service_instance = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"success": False, "message": "Service not found"}, status=404)

        sub_service_data['service'] = service_instance.id

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1]
            filename = f"subservice_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            sub_service_data['icon'] = get_server_media_url(request, filename)

        serializer = SubServiceCreateSerializer(data=sub_service_data)
        if serializer.is_valid():
            sub_service = serializer.save()
            return Response({"success": True, "message": "Sub-service created successfully",
                             "data": SubServiceSerializer(sub_service, context={'request': request}).data}, status=201)
        return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=400)
    except Exception as e:
        return Response({"success": False, "message": f"Error creating sub-service: {str(e)}"}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_sub_service(request, sub_service_id):
    try:
        sub_service = SubService.objects.get(id=sub_service_id)
        serializer = SubServiceSerializer(sub_service, context={'request': request})
        return Response({"success": True, "data": serializer.data})
    except SubService.DoesNotExist:
        return Response({"success": False, "message": "Sub-service not found"}, status=404)


@api_view(['PUT'])
@permission_classes([AllowAny])
@authentication_classes([])
def update_sub_service(request, sub_service_id):
    try:
        sub_service = SubService.objects.get(id=sub_service_id)
        uploaded_file = request.FILES.get('image') or request.FILES.get('icon')
        sub_service_data = request.data.copy()

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1]
            filename = f"subservice_{sub_service_id}_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            sub_service_data['icon'] = get_server_media_url(request, filename)

        serializer = SubServiceCreateSerializer(sub_service, data=sub_service_data, partial=True)
        if serializer.is_valid():
            sub_service = serializer.save()
            return Response({"success": True, "message": "Sub-service updated successfully",
                             "data": SubServiceSerializer(sub_service, context={'request': request}).data})
        return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=400)
    except SubService.DoesNotExist:
        return Response({"success": False, "message": "Sub-service not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([])
def delete_sub_service(request, sub_service_id):
    try:
        sub_service = SubService.objects.get(id=sub_service_id)
        sub_service.delete()
        return Response({"success": True, "message": "Sub-service deleted successfully"})
    except SubService.DoesNotExist:
        return Response({"success": False, "message": "Sub-service not found"}, status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_service_sub_services(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        sub_services = service.sub_services.filter(is_active=True).order_by('order', 'id')
        serializer = SubServiceSerializer(sub_services, many=True, context={'request': request})
        return Response({"success": True, "data": serializer.data})
    except Service.DoesNotExist:
        return Response({"success": False, "message": "Service not found"}, status=404)
