from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Service, SubService
from .serializer import ServiceSerializer, ServiceCreateSerializer, SubServiceSerializer, SubServiceCreateSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def dashboard_services(request):
    """Get all services for dashboard"""
    services = Service.objects.filter(is_active=True).order_by('order', 'id')
    serializer = ServiceSerializer(services, many=True)
    return Response({
        "success": True,
        "data": serializer.data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_service(request):
    """Create a new service"""
    serializer = ServiceCreateSerializer(data=request.data)
    if serializer.is_valid():
        service = serializer.save()
        return Response({
            "success": True,
            "message": "Service created successfully",
            "data": ServiceSerializer(service).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        "success": False,
        "message": "Invalid data",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_service(request, service_id):
    """Get a specific service"""
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceSerializer(service)
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
    """Update a service"""
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceCreateSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            service = serializer.save()
            return Response({
                "success": True,
                "message": "Service updated successfully",
                "data": ServiceSerializer(service).data
            })
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
    """Create a new sub-service"""
    serializer = SubServiceCreateSerializer(data=request.data)
    if serializer.is_valid():
        sub_service = serializer.save()
        return Response({
            "success": True,
            "message": "Sub-service created successfully",
            "data": SubServiceSerializer(sub_service).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        "success": False,
        "message": "Invalid data",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = SubServiceSerializer(sub_services, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })
    except Service.DoesNotExist:
        return Response({
            "success": False,
            "message": "Service not found"
        }, status=status.HTTP_404_NOT_FOUND)

