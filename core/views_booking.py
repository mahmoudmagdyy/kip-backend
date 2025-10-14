from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from datetime import datetime, date, time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
        
        # Send WebSocket notification for real-time dashboard updates
        # Use the same approach as the admin endpoint
        try:
            channel_layer = get_channel_layer()
            print(f"DEBUG: Channel layer: {channel_layer}")
            
            if channel_layer:
                # Get user details for the notification (same as admin endpoint)
                from django.contrib.auth.models import User
                user = reserved_slot.user
                
                # Create booking data with user details
                booking_data = ReservedSlotSerializer(reserved_slot).data
                
                # Add user details
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.username,
                    "is_active": user.is_active,
                    "date_joined": user.date_joined.isoformat() if user.date_joined else None
                }
                
                # Add profile details if exists
                try:
                    profile = user.profile
                    user_data.update({
                        "gender": profile.gender,
                        "country": profile.country
                    })
                except:
                    user_data.update({
                        "gender": "",
                        "country": ""
                    })
                
                booking_data['user_details'] = user_data
                
                print(f"DEBUG: Sending WebSocket notification for booking {reserved_slot.id}")
                
                # Send WebSocket notification (same as admin endpoint)
                async_to_sync(channel_layer.group_send)(
                    'admin_bookings',
                    {
                        'type': 'booking_created',
                        'data': booking_data
                    }
                )
                print(f"DEBUG: WebSocket notification sent successfully")
            else:
                print("DEBUG: No channel layer available")
        except Exception as e:
            print(f"DEBUG: Error sending WebSocket notification: {e}")
        
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
        
        # Send WebSocket notification to admin dashboard
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        from django.contrib.auth.models import User
        
        channel_layer = get_channel_layer()
        if channel_layer:
            booking_data = ReservedSlotSerializer(slot).data
            
            # Add user details
            user = slot.user
            user_data = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.username,
                "is_active": user.is_active,
                "date_joined": user.date_joined.isoformat() if user.date_joined else None
            }
            
            # Add profile details if exists
            try:
                profile = user.profile
                user_data.update({
                    "gender": profile.gender,
                    "country": profile.country
                })
            except:
                user_data.update({
                    "gender": "",
                    "country": ""
                })
            
            booking_data['user_details'] = user_data
            
            async_to_sync(channel_layer.group_send)(
                'admin_bookings',
                {
                    'type': 'booking_updated',
                    'data': booking_data
                }
            )
        
        response_serializer = ReservedSlotSerializer(slot)
        return Response({"success": "Booking updated successfully", "data": response_serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        # Get booking data before cancellation for WebSocket notification
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        from django.contrib.auth.models import User
        
        booking_data = ReservedSlotSerializer(slot).data
        
        # Add user details
        user = slot.user
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.username,
            "is_active": user.is_active,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None
        }
        
        # Add profile details if exists
        try:
            profile = user.profile
            user_data.update({
                "gender": profile.gender,
                "country": profile.country
            })
        except:
            user_data.update({
                "gender": "",
                "country": ""
            })
        
        booking_data['user_details'] = user_data
        
        slot.status = 'cancelled'
        slot.save()
        
        # Send WebSocket notification to admin dashboard
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                'admin_bookings',
                {
                    'type': 'booking_updated',
                    'data': booking_data
                }
            )
        
        return Response({"success": "Booking cancelled successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def reservations_reserved_slots(request):
    """Get all reserved time slots from database - Public endpoint"""
    try:
        # Get query parameters
        date_filter = request.GET.get('date')
        service_filter = request.GET.get('service')
        status_filter = request.GET.get('status', 'upcoming')
        
        # Start with all reserved slots
        slots = ReservedSlot.objects.all()
        
        # Apply filters
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                slots = slots.filter(booking_date=filter_date)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid date format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if service_filter:
            slots = slots.filter(service_name__icontains=service_filter)
        
        if status_filter:
            slots = slots.filter(status=status_filter)
        
        # Order by date and time
        slots = slots.order_by('booking_date', 'booking_time')
        
        # Serialize the data
        serializer = ReservedSlotSerializer(slots, many=True)
        
        return Response({
            "success": True,
            "message": "Reserved slots retrieved successfully",
            "data": serializer.data,
            "total_count": slots.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving reserved slots: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def available_time_slots(request):
    """Get available time slots for a specific date"""
    try:
        # Get query parameters
        booking_date = request.GET.get('date')
        service_name = request.GET.get('service', '')
        
        if not booking_date:
            return Response({
                "success": False,
                "message": "Date parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            filter_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get reserved slots for the date
        reserved_slots = ReservedSlot.objects.filter(
            booking_date=filter_date,
            status='upcoming'
        )
        
        # Generate available time slots (9 AM to 5 PM, 1-hour slots)
        available_slots = []
        start_hour = 9
        end_hour = 17
        
        for hour in range(start_hour, end_hour):
            slot_time = time(hour, 0)
            
            # Check if this time slot is already reserved
            is_reserved = reserved_slots.filter(booking_time=slot_time).exists()
            
            if not is_reserved:
                available_slots.append({
                    "time": slot_time.strftime('%H:%M'),
                    "display_time": slot_time.strftime('%I:%M %p'),
                    "available": True
                })
            else:
                available_slots.append({
                    "time": slot_time.strftime('%H:%M'),
                    "display_time": slot_time.strftime('%I:%M %p'),
                    "available": False
                })
        
        return Response({
            "success": True,
            "message": "Available time slots retrieved successfully",
            "date": booking_date,
            "service": service_name,
            "available_slots": available_slots
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving available slots: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


