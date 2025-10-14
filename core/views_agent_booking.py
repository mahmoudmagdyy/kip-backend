from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from .models import ReservedSlot, BookingSettings
from .serializer import ReservedSlotSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@api_view(['POST'])
@permission_classes([AllowAny])
def agent_create_booking(request):
    """
    Public endpoint for agents to create bookings.
    Creates user if not found, then creates booking.
    """
    try:
        # Get required fields
        required_fields = ['phone', 'service_name', 'booking_date', 'booking_time']
        for field in required_fields:
            if field not in request.data:
                return Response({
                    "success": False,
                    "message": f"Missing required field: {field}"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        phone = request.data['phone']
        service_name = request.data['service_name']
        booking_date_str = request.data['booking_date']
        booking_time_str = request.data['booking_time']
        
        # Parse booking date and time
        try:
            # Support multiple date formats
            date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y']
            booking_date = None
            for fmt in date_formats:
                try:
                    booking_date = datetime.strptime(booking_date_str, fmt).date()
                    break
                except ValueError:
                    continue
            
            if not booking_date:
                return Response({
                    "success": False,
                    "message": "Invalid date format. Use YYYY-MM-DD, DD/MM/YYYY, or MM/DD/YYYY"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Support multiple time formats
            time_formats = ['%H:%M', '%I:%M %p', '%I:%M%p', '%H:%M:%S']
            booking_time = None
            for fmt in time_formats:
                try:
                    booking_time = datetime.strptime(booking_time_str, fmt).time()
                    break
                except ValueError:
                    continue
            
            if not booking_time:
                return Response({
                    "success": False,
                    "message": "Invalid time format. Use HH:MM, HH:MM AM/PM, or HH:MM:SS"
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Error parsing date/time: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get booking settings
        settings = BookingSettings.objects.filter(is_active=True).first()
        if not settings:
            return Response({
                "success": False,
                "message": "No booking settings found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if date is an off day
        day_of_week = booking_date.weekday()
        off_days = settings.get_off_days_list()
        
        if day_of_week in off_days:
            return Response({
                "success": False,
                "message": "Booking not allowed on off days"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if time is within working hours
        if (booking_time.hour < settings.WORKING_HOURS_START or 
            booking_time.hour >= settings.WORKING_HOURS_END):
            return Response({
                "success": False,
                "message": "Booking time is outside working hours"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if time slot is already reserved
        existing_booking = ReservedSlot.objects.filter(
            booking_date=booking_date,
            booking_time=booking_time,
            status__in=['upcoming', 'completed']
        ).first()
        
        if existing_booking:
            return Response({
                "success": False,
                "message": "This time slot is already reserved"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            # Find or create user
            user, created = User.objects.get_or_create(
                username=phone,
                defaults={
                    'first_name': request.data.get('first_name', ''),
                    'last_name': request.data.get('last_name', ''),
                    'email': request.data.get('email', ''),
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            
            # Set password if user was created
            if created:
                user.set_password('password')
                user.save()
                
                # Create profile if it doesn't exist
                try:
                    from .models import Profile
                    Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            'gender': request.data.get('gender', ''),
                            'country': request.data.get('country', '')
                        }
                    )
                except:
                    pass  # Profile creation is optional
            
            # Create the booking
            booking = ReservedSlot.objects.create(
                user=user,
                service_name=service_name,
                booking_date=booking_date,
                booking_time=booking_time,
                duration_minutes=settings.DEFAULT_RESERVATION_DURATION_MINUTES,
                status=request.data.get('status', 'upcoming'),
                notes=request.data.get('notes', '')
            )
            
            # Send WebSocket notification for real-time dashboard updates
            try:
                channel_layer = get_channel_layer()
                if channel_layer:
                    # Create booking data with user details
                    booking_data = ReservedSlotSerializer(booking).data
                    
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
                    
                    # Send WebSocket notification
                    async_to_sync(channel_layer.group_send)(
                        'admin_bookings',
                        {
                            'type': 'booking_created',
                            'data': booking_data
                        }
                    )
            except Exception as e:
                print(f"Error sending WebSocket notification: {e}")
            
            return Response({
                "success": True,
                "message": "Booking created successfully",
                "user_created": created,
                "user_id": user.id,
                "booking_id": booking.id,
                "data": {
                    "booking": ReservedSlotSerializer(booking).data,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "phone": user.username,
                        "is_active": user.is_active,
                        "created": created
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error creating booking: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
