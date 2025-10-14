from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from datetime import datetime, date, time
from .models import ReservedSlot, BookingSettings
from .serializer import ReservedSlotSerializer, CreateReservedSlotSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_all_bookings(request):
    """
    Admin endpoint to get all bookings with filtering and pagination.
    Only accessible by staff/superuser.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get query parameters
        date_filter = request.GET.get('date')
        service_filter = request.GET.get('service')
        status_filter = request.GET.get('status')
        user_filter = request.GET.get('user_id')
        phone_filter = request.GET.get('phone')
        limit = int(request.GET.get('limit', 50))
        offset = int(request.GET.get('offset', 0))
        
        # Start with all bookings
        bookings = ReservedSlot.objects.all()
        
        # Apply filters
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                bookings = bookings.filter(booking_date=filter_date)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid date format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if service_filter:
            bookings = bookings.filter(service_name__icontains=service_filter)
        
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        if user_filter:
            bookings = bookings.filter(user_id=user_filter)
        
        if phone_filter:
            bookings = bookings.filter(user__username__icontains=phone_filter)
        
        # Order by date and time (newest first)
        bookings = bookings.order_by('-booking_date', '-booking_time')
        
        # Apply pagination
        total_count = bookings.count()
        bookings = bookings[offset:offset + limit]
        
        # Serialize the data with user details
        bookings_data = []
        for booking in bookings:
            booking_dict = ReservedSlotSerializer(booking).data
            
            # Add user details
            user = booking.user
            user_data = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.username,  # Phone is stored as username
                "is_active": user.is_active,
                "date_joined": user.date_joined
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
            
            booking_dict['user_details'] = user_data
            bookings_data.append(booking_dict)
        
        return Response({
            "success": True,
            "message": "Bookings retrieved successfully",
            "data": bookings_data,
            "pagination": {
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_count
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving bookings: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_booking_stats(request):
    """
    Admin endpoint to get booking statistics.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        bookings = ReservedSlot.objects.all()
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                bookings = bookings.filter(booking_date__gte=start_date_obj)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid start_date format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                bookings = bookings.filter(booking_date__lte=end_date_obj)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid end_date format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate statistics
        total_bookings = bookings.count()
        upcoming_bookings = bookings.filter(status='upcoming').count()
        cancelled_bookings = bookings.filter(status='cancelled').count()
        completed_bookings = bookings.filter(status='completed').count()
        
        # Get today's bookings
        today = date.today()
        today_bookings = bookings.filter(booking_date=today).count()
        
        # Get this week's bookings
        from datetime import timedelta
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_bookings = bookings.filter(
            booking_date__gte=week_start,
            booking_date__lte=week_end
        ).count()
        
        # Get this month's bookings
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            month_end = today.replace(month=today.month + 1, day=1)
        
        month_bookings = bookings.filter(
            booking_date__gte=month_start,
            booking_date__lt=month_end
        ).count()
        
        # Get popular services
        from django.db.models import Count
        popular_services = bookings.values('service_name').annotate(
            count=Count('service_name')
        ).order_by('-count')[:5]
        
        return Response({
            "success": True,
            "message": "Booking statistics retrieved successfully",
            "stats": {
                "total_bookings": total_bookings,
                "upcoming_bookings": upcoming_bookings,
                "cancelled_bookings": cancelled_bookings,
                "completed_bookings": completed_bookings,
                "today_bookings": today_bookings,
                "week_bookings": week_bookings,
                "month_bookings": month_bookings,
                "popular_services": list(popular_services)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving booking statistics: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def admin_update_booking_status(request, booking_id):
    """
    Admin endpoint to update booking status.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = ReservedSlot.objects.get(id=booking_id)
        
        new_status = request.data.get('status')
        if new_status not in ['upcoming', 'cancelled', 'completed']:
            return Response({
                "success": False,
                "message": "Invalid status. Must be 'upcoming', 'cancelled', or 'completed'"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = new_status
        booking.save()
        
        # Send WebSocket notification to admin dashboard
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        from django.contrib.auth.models import User
        
        channel_layer = get_channel_layer()
        if channel_layer:
            booking_data = ReservedSlotSerializer(booking).data
            
            # Add user details
            user = booking.user
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
        
        return Response({
            "success": True,
            "message": f"Booking status updated to {new_status}",
            "data": ReservedSlotSerializer(booking).data
        }, status=status.HTTP_200_OK)
        
    except ReservedSlot.DoesNotExist:
        return Response({
            "success": False,
            "message": "Booking not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error updating booking: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_booking(request, booking_id):
    """
    Admin endpoint to delete a booking.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = ReservedSlot.objects.get(id=booking_id)
        
        # Get booking data before deletion for WebSocket notification
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        from django.contrib.auth.models import User
        
        booking_data = ReservedSlotSerializer(booking).data
        
        # Add user details
        user = booking.user
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
        
        # Delete the booking
        booking.delete()
        
        # Send WebSocket notification to admin dashboard
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                'admin_bookings',
                {
                    'type': 'booking_deleted',
                    'data': booking_data
                }
            )
        
        return Response({
            "success": True,
            "message": "Booking deleted successfully"
        }, status=status.HTTP_200_OK)
        
    except ReservedSlot.DoesNotExist:
        return Response({
            "success": False,
            "message": "Booking not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error deleting booking: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_booking_details(request, booking_id):
    """
    Admin endpoint to get detailed information about a specific booking.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = ReservedSlot.objects.get(id=booking_id)
        
        # Get user details
        user = booking.user
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "date_joined": user.date_joined
        }
        
        # Get profile details if exists
        try:
            profile = user.profile
            user_data.update({
                "gender": profile.gender,
                "country": profile.country
            })
        except:
            pass
        
        booking_data = ReservedSlotSerializer(booking).data
        booking_data['user_details'] = user_data
        
        return Response({
            "success": True,
            "message": "Booking details retrieved successfully",
            "data": booking_data
        }, status=status.HTTP_200_OK)
        
    except ReservedSlot.DoesNotExist:
        return Response({
            "success": False,
            "message": "Booking not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving booking details: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_booking(request):
    """
    Admin endpoint to create a booking on behalf of a user.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        serializer = CreateReservedSlotSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Invalid booking data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the booking with user_id
        booking = serializer.save(user_id=request.data.get('user_id'))
        
        # Send WebSocket notification to admin dashboard
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        if channel_layer:
            # Get user details for the notification
            user = booking.user
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
            "data": ReservedSlotSerializer(booking).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error creating booking: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
