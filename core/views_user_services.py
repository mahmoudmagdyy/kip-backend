from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Service, SubService
from .serializer import ServiceSerializer, ServiceCreateSerializer, SubServiceSerializer, SubServiceCreateSerializer
from django.conf import settings
import os
import uuid
import time


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def user_create_service(request):
    """Create a new service by user with image upload"""
    try:
        print(f"DEBUG: user_create_service called with FILES: {list(request.FILES.keys())}")
        print(f"DEBUG: user_create_service called with DATA: {request.data}")

        icon_url = None
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            print(f"DEBUG: Image file received: {uploaded_file.name}")

            # Generate unique filename
            file_extension = os.path.splitext(uploaded_file.name)[1]
            timestamp = int(time.time())
            unique_filename = f"user_service_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

            # Save file
            media_dir = settings.MEDIA_ROOT
            os.makedirs(media_dir, exist_ok=True)
            file_path = os.path.join(media_dir, unique_filename)

            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # ✅ Full URL (important!)
            icon_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{unique_filename}")
            print(f"DEBUG: Set icon_url to: {icon_url}")

        # Copy request data and include icon if uploaded
        service_data = request.data.copy()
        if icon_url:
            service_data['icon'] = icon_url

        serializer = ServiceCreateSerializer(data=service_data)
        if serializer.is_valid():
            service = serializer.save()
            return Response({
                "success": True,
                "message": "Service created successfully",
                "data": ServiceSerializer(service, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"DEBUG: Exception in user_create_service: {str(e)}")
        return Response({
            "success": False,
            "message": f"Error creating service: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def user_create_sub_service(request):
    """Create a new sub-service by user with image upload"""
    try:
        print(f"DEBUG: user_create_sub_service called with FILES: {list(request.FILES.keys())}")
        print(f"DEBUG: user_create_sub_service called with DATA: {request.data}")

        icon_url = None
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            print(f"DEBUG: Image file received: {uploaded_file.name}")

            # Generate unique filename
            file_extension = os.path.splitext(uploaded_file.name)[1]
            timestamp = int(time.time())
            unique_filename = f"user_subservice_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

            # Save file
            media_dir = settings.MEDIA_ROOT
            os.makedirs(media_dir, exist_ok=True)
            file_path = os.path.join(media_dir, unique_filename)

            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # ✅ Full URL (important!)
            icon_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{unique_filename}")
            print(f"DEBUG: Set icon_url to: {icon_url}")

        # Copy request data and include icon if uploaded
        sub_service_data = request.data.copy()
        if icon_url:
            sub_service_data['icon'] = icon_url

        serializer = SubServiceCreateSerializer(data=sub_service_data)
        if serializer.is_valid():
            sub_service = serializer.save()
            return Response({
                "success": True,
                "message": "Sub-service created successfully",
                "data": SubServiceSerializer(sub_service, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"DEBUG: Exception in user_create_sub_service: {str(e)}")
        return Response({
            "success": False,
            "message": f"Error creating sub-service: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def user_get_services(request):
    """Get all services for user"""
    try:
        services = Service.objects.filter(is_active=True).order_by('order', 'id')
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response({
            "success": True,
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving services: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def user_get_sub_services(request, service_id):
    """Get all sub-services for a specific service"""
    try:
        service = Service.objects.get(id=service_id)
        sub_services = service.sub_services.filter(is_active=True).order_by('order', 'id')
        serializer = SubServiceSerializer(sub_services, many=True, context={'request': request})
        return Response({
            "success": True,
            "data": serializer.data
        })
    except Service.DoesNotExist:
        return Response({
            "success": False,
            "message": "Service not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving sub-services: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
