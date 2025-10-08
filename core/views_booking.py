from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from .models import ReservedSlot
from .serializer import ReservedSlotSerializer, CreateReservedSlotSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reserved_slots(request):
    if request.method == 'GET':
        slots = ReservedSlot.objects.filter(user=request.user)
        serializer = ReservedSlotSerializer(slots, many=True)
        return Response({"success": "Reserved slots retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CreateReservedSlotSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        reserved_slot = ReservedSlot.objects.create(
            user=request.user,
            service_name=serializer.validated_data['service_name'],
            booking_date=serializer.validated_data['booking_date'],
            booking_time=serializer.validated_data['booking_time'],
            duration_minutes=60,
            status=serializer.validated_data.get('status', 'upcoming'),
            notes=serializer.validated_data.get('notes', '')
        )
        response_serializer = ReservedSlotSerializer(reserved_slot)
        return Response({"success": "Booking created successfully", "data": response_serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reserved_slot_detail(request, slot_id):
    try:
        slot = ReservedSlot.objects.get(id=slot_id, user=request.user)
    except ReservedSlot.DoesNotExist:
        return Response({"error": "Reserved slot not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = CreateReservedSlotSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'service_name' in serializer.validated_data:
            slot.service_name = serializer.validated_data['service_name']
        if 'booking_date' in serializer.validated_data:
            slot.booking_date = serializer.validated_data['booking_date']
        if 'booking_time' in serializer.validated_data:
            slot.booking_time = serializer.validated_data['booking_time']
        if 'status' in serializer.validated_data:
            slot.status = serializer.validated_data['status']
        if 'notes' in serializer.validated_data:
            slot.notes = serializer.validated_data['notes']
        slot.save()
        response_serializer = ReservedSlotSerializer(slot)
        return Response({"success": "Booking updated successfully", "data": response_serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        slot.status = 'cancelled'
        slot.save()
        return Response({"success": "Booking cancelled successfully"}, status=status.HTTP_200_OK)


