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


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def dashboard_services(request):
    """Get all services for dashboard"""
    services = Service.objects.filter(is_active=True).order_by('order', 'id')
    serializer = ServiceSerializer(services, many=True, context={'request': request})
    return Response({
        "success": True,
        "data": serializer.data
    })



@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_service(request):
    """Create a new service with optional image upload"""
    try:
        print(f"DEBUG: create_service called with FILES: {list(request.FILES.keys())}")
        print(f"DEBUG: create_service called with DATA: {request.data}")

        icon_url = None
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            print(f"DEBUG: Image file received: {uploaded_file.name}")

            # Generate unique filename
            file_extension = os.path.splitext(uploaded_file.name)[1]
            timestamp = int(time.time())
            unique_filename = f"service_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

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
        print(f"DEBUG: Exception in create_service: {str(e)}")
        return Response({
            "success": False,
            "message": f"Error creating service: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_service(request, service_id):
    """Get a specific service"""
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceSerializer(service, context={'request': request})
        return Response({
            "success": True,
            "data": serializer.data
        })
    except Service.DoesNotExist:
        return Response({
            "success": False,
            "message": "Service not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([AllowAny])
@authentication_classes([])
def update_service(request, service_id):
    """Update a service with optional image upload"""
    try:
        print(f"DEBUG: update_service called for service_id: {service_id}")
        print(f"DEBUG: update_service called with FILES: {list(request.FILES.keys())}")
        print(f"DEBUG: update_service called with DATA: {request.data}")
        
        service = Service.objects.get(id=service_id)
        print(f"DEBUG: Found service with current icon: {service.icon}")
        
        # Handle file upload if present
        icon_url = None
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            print(f"DEBUG: Image file received: {uploaded_file.name}")
            
            # Generate unique filename
            file_extension = os.path.splitext(uploaded_file.name)[1]
            timestamp = int(time.time())
            unique_filename = f"service_{service_id}_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"
            print(f"DEBUG: Generated unique filename: {unique_filename}")
            
            # Save to media directory
            media_dir = settings.MEDIA_ROOT
            os.makedirs(media_dir, exist_ok=True)
            
            # Save file to media directory
            file_path = os.path.join(media_dir, unique_filename)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Set the icon URL
            icon_url = f'/media/{unique_filename}'
            print(f"DEBUG: Set icon_url to: {icon_url}")
        else:
            print("DEBUG: No image file found in request")
        
        # Prepare data for serializer
        service_data = request.data.copy()
        if icon_url:
            service_data['icon'] = icon_url
            print(f"DEBUG: Updated service_data with icon: {service_data}")
        
        serializer = ServiceCreateSerializer(service, data=service_data, partial=True)
        if serializer.is_valid():
            service = serializer.save()
            print(f"DEBUG: Service updated with icon: {service.icon}")
            return Response({
                "success": True,
                "message": "Service updated successfully",
                "data": ServiceSerializer(service).data
            })
        print(f"DEBUG: Serializer errors: {serializer.errors}")
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Service.DoesNotExist:
        return Response({
            "success": False,
            "message": "Service not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"DEBUG: Exception in update_service: {str(e)}")
        return Response({
            "success": False,
            "message": f"Error updating service: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([])
def delete_service(request, service_id):
    """Delete a service"""
    try:
        service = Service.objects.get(id=service_id)
        service.delete()
        return Response({
            "success": True,
            "message": "Service deleted successfully"
        })
    except Service.DoesNotExist:
        return Response({
            "success": False,
            "message": "Service not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_sub_service(request):
    """Create a new sub-service with optional image upload"""
    try:
        print(f"DEBUG: create_sub_service called with FILES: {list(request.FILES.keys())}")
        print(f"DEBUG: create_sub_service called with DATA: {request.data}")

        icon_url = None
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            print(f"DEBUG: Image file received: {uploaded_file.name}")

            # Generate unique filename
            file_extension = os.path.splitext(uploaded_file.name)[1]
            timestamp = int(time.time())
            unique_filename = f"subservice_{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"

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
        print(f"DEBUG: Exception in create_sub_service: {str(e)}")
        return Response({
            "success": False,
            "message": f"Error creating sub-service: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_sub_service(request, sub_service_id):
    """Get a specific sub-service"""
    try:
        sub_service = SubService.objects.get(id=sub_service_id)
        serializer = SubServiceSerializer(sub_service)
        return Response({
            "success": True,
            "data": serializer.data
        })
    except SubService.DoesNotExist:
        return Response({
            "success": False,
            "message": "Sub-service not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([AllowAny])
@authentication_classes([])
def update_sub_service(request, sub_service_id):
    """Update a sub-service"""
    try:
        sub_service = SubService.objects.get(id=sub_service_id)
        serializer = SubServiceCreateSerializer(sub_service, data=request.data, partial=True)
        if serializer.is_valid():
            sub_service = serializer.save()
            return Response({
                "success": True,
                "message": "Sub-service updated successfully",
                "data": SubServiceSerializer(sub_service).data
            })
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except SubService.DoesNotExist:
        return Response({
            "success": False,
            "message": "Sub-service not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([])
def delete_sub_service(request, sub_service_id):
    """Delete a sub-service"""
    try:
        sub_service = SubService.objects.get(id=sub_service_id)
        sub_service.delete()
        return Response({
            "success": True,
            "message": "Sub-service deleted successfully"
        })
    except SubService.DoesNotExist:
        return Response({
            "success": False,
            "message": "Sub-service not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_service_sub_services(request, service_id):
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

