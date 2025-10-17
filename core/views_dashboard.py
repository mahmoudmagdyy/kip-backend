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


@api_view(['PUT'])
@permission_classes([AllowAny])
@authentication_classes([])
def update_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        uploaded_file = request.FILES.get('image') or request.FILES.get('icon')
        service_data = request.data.copy()

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1]
            filename = f"service_{service_id}_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            service_data['icon'] = get_server_media_url(request, filename)

        serializer = ServiceCreateSerializer(service, data=service_data, partial=True)
        if serializer.is_valid():
            service = serializer.save()
            return Response({"success": True, "message": "Service updated successfully",
                             "data": ServiceSerializer(service, context={'request': request}).data})
        return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=400)
    except Service.DoesNotExist:
        return Response({"success": False, "message": "Service not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([])
def delete_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        service.delete()
        return Response({"success": True, "message": "Service deleted successfully"})
    except Service.DoesNotExist:
        return Response({"success": False, "message": "Service not found"}, status=404)



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
