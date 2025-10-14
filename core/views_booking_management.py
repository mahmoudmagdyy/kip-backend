from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ReservedSlot, BookingSettings
from .serializer import BookingSettingsSerializer


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([AllowAny])
def booking_settings_management(request):
    """Manage booking settings"""
    if request.method == 'GET':
        # Get current booking settings
        settings = BookingSettings.objects.filter(is_active=True).first()
        if not settings:
            # Create default settings if none exist
            settings = BookingSettings.objects.create()
        
        serializer = BookingSettingsSerializer(settings)
        return Response({
            "success": True,
            "data": serializer.data
        })
    
    elif request.method == 'POST':
        # Create new booking settings
        serializer = BookingSettingsSerializer(data=request.data)
        if serializer.is_valid():
            # Deactivate old settings
            BookingSettings.objects.filter(is_active=True).update(is_active=False)
            # Create new settings
            settings = serializer.save(is_active=True)
            return Response({
                "success": True,
                "message": "Booking settings created successfully",
                "data": BookingSettingsSerializer(settings).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        # Update existing booking settings
        settings = BookingSettings.objects.filter(is_active=True).first()
        if not settings:
            return Response({
                "success": False,
                "message": "No active booking settings found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookingSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            settings = serializer.save()
            return Response({
                "success": True,
                "message": "Booking settings updated successfully",
                "data": BookingSettingsSerializer(settings).data
            })
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def smart_available_slots(request):
    """Get available time slots based on booking settings"""
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
        
        # Get booking settings
        settings = BookingSettings.objects.filter(is_active=True).first()
        if not settings:
            return Response({
                "success": False,
                "message": "No booking settings found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the date is an off day
        day_of_week = filter_date.weekday()  # 0=Monday, 6=Sunday
        off_days = settings.get_off_days_list()
        
        if day_of_week in off_days:
            return Response({
                "success": True,
                "message": "This day is an off day",
                "date": booking_date,
                "is_off_day": True,
                "available_slots": []
            })
        
        # Get reserved slots for the date
        reserved_slots = ReservedSlot.objects.filter(
            booking_date=filter_date,
            status='upcoming'
        )
        
        # Generate available time slots based on settings
        available_slots = []
        start_hour = settings.WORKING_HOURS_START
        end_hour = settings.WORKING_HOURS_END
        duration_minutes = settings.DEFAULT_RESERVATION_DURATION_MINUTES
        
        # Create time slots based on duration
        current_time = time(start_hour, 0)
        end_time = time(end_hour, 0)
        
        while current_time < end_time:
            # Check if this time slot is available
            slot_end_time = (datetime.combine(date.today(), current_time) + 
                           timedelta(minutes=duration_minutes)).time()
            
            # Check if slot would go beyond working hours
            if slot_end_time > end_time:
                break
            
            # Check if this time slot is already reserved
            is_reserved = reserved_slots.filter(booking_time=current_time).exists()
            
            available_slots.append({
                "time": current_time.strftime('%H:%M'),
                "display_time": current_time.strftime('%I:%M %p'),
                "end_time": slot_end_time.strftime('%H:%M'),
                "duration_minutes": duration_minutes,
                "available": not is_reserved,
                "is_reserved": is_reserved
            })
            
            # Move to next slot
            current_time = (datetime.combine(date.today(), current_time) + 
                          timedelta(minutes=duration_minutes)).time()
        
        # Filter to return only available slots
        available_only_slots = [slot for slot in available_slots if slot['available']]
        
        return Response({
            "success": True,
            "message": "Available time slots retrieved successfully",
            "date": booking_date,
            "service": service_name,
            "working_hours": {
                "start": f"{start_hour:02d}:00",
                "end": f"{end_hour:02d}:00"
            },
            "duration_minutes": duration_minutes,
            "is_off_day": False,
            "available_slots": available_only_slots,
            "total_available_slots": len(available_only_slots)
        })
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving available slots: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def booking_calendar(request):
    """Get booking calendar for a month"""
    try:
        # Get query parameters
        year = request.GET.get('year', datetime.now().year)
        month = request.GET.get('month', datetime.now().month)
        
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({
                "success": False,
                "message": "Invalid year or month"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get booking settings
        settings = BookingSettings.objects.filter(is_active=True).first()
        if not settings:
            return Response({
                "success": False,
                "message": "No booking settings found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get all reserved slots for the month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        reserved_slots = ReservedSlot.objects.filter(
            booking_date__gte=start_date,
            booking_date__lt=end_date,
            status='upcoming'
        )
        
        # Create calendar data
        calendar_data = []
        current_date = start_date
        
        while current_date < end_date:
            day_of_week = current_date.weekday()
            off_days = settings.get_off_days_list()
            
            # Count reserved slots for this day
            day_reservations = reserved_slots.filter(booking_date=current_date)
            
            calendar_data.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "day": current_date.day,
                "day_name": current_date.strftime('%A'),
                "is_off_day": day_of_week in off_days,
                "reserved_count": day_reservations.count(),
                "is_weekend": day_of_week >= 5,
                "is_today": current_date == date.today()
            })
            
            current_date += timedelta(days=1)
        
        return Response({
            "success": True,
            "message": "Booking calendar retrieved successfully",
            "year": year,
            "month": month,
            "calendar": calendar_data,
            "working_hours": {
                "start": f"{settings.WORKING_HOURS_START:02d}:00",
                "end": f"{settings.WORKING_HOURS_END:02d}:00"
            },
            "off_days": off_days
        })
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving calendar: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_booking(request):
    """Create a new booking with validation"""
    try:
        # Get booking settings
        settings = BookingSettings.objects.filter(is_active=True).first()
        if not settings:
            return Response({
                "success": False,
                "message": "No booking settings found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validate required fields
        required_fields = ['service_name', 'booking_date', 'booking_time', 'user_id']
        for field in required_fields:
            if field not in request.data:
                return Response({
                    "success": False,
                    "message": f"Missing required field: {field}"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse booking date and time
        try:
            booking_date = datetime.strptime(request.data['booking_date'], '%Y-%m-%d').date()
            booking_time = datetime.strptime(request.data['booking_time'], '%H:%M').time()
        except ValueError:
            return Response({
                "success": False,
                "message": "Invalid date or time format"
            }, status=status.HTTP_400_BAD_REQUEST)
        
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
            status='upcoming'
        ).exists()
        
        if existing_booking:
            return Response({
                "success": False,
                "message": "This time slot is already reserved"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the booking
        booking = ReservedSlot.objects.create(
            user_id=request.data['user_id'],
            service_name=request.data['service_name'],
            booking_date=booking_date,
            booking_time=booking_time,
            duration_minutes=settings.DEFAULT_RESERVATION_DURATION_MINUTES,
            status='upcoming',
            notes=request.data.get('notes', '')
        )
        
        # Send WebSocket notification to admin dashboard
        channel_layer = get_channel_layer()
        if channel_layer:
            from .serializer import ReservedSlotSerializer
            from django.contrib.auth.models import User
            
            # Get user details for the notification
            user = User.objects.get(id=booking.user_id)
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
            
            async_to_sync(channel_layer.group_send)(
                'admin_bookings',
                {
                    'type': 'booking_created',
                    'data': booking_data
                }
            )
        
        return Response({
            "success": True,
            "message": "Booking created successfully",
            "data": {
                "id": booking.id,
                "service_name": booking.service_name,
                "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
                "booking_time": booking.booking_time.strftime('%H:%M'),
                "duration_minutes": booking.duration_minutes,
                "status": booking.status,
                "created_at": booking.created_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error creating booking: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
