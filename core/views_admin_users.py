from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile
from .serializer import UserSerializer
from datetime import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_all_users(request):
    """
    Admin endpoint to get all users with filtering and pagination.
    Only accessible by staff/superuser.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get query parameters
        search = request.GET.get('search')
        is_active = request.GET.get('is_active')
        is_staff = request.GET.get('is_staff')
        is_superuser = request.GET.get('is_superuser')
        gender = request.GET.get('gender')
        country = request.GET.get('country')
        date_joined_from = request.GET.get('date_joined_from')
        date_joined_to = request.GET.get('date_joined_to')
        last_login_from = request.GET.get('last_login_from')
        last_login_to = request.GET.get('last_login_to')
        has_profile = request.GET.get('has_profile')
        sort_by = request.GET.get('sort_by', 'date_joined')
        sort_order = request.GET.get('sort_order', 'desc')
        limit = int(request.GET.get('limit', 50))
        offset = int(request.GET.get('offset', 0))
        
        # Start with all users
        users = User.objects.all()
        
        # Apply filters
        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if is_active is not None:
            users = users.filter(is_active=is_active.lower() == 'true')
        
        if is_staff is not None:
            users = users.filter(is_staff=is_staff.lower() == 'true')
        
        if is_superuser is not None:
            users = users.filter(is_superuser=is_superuser.lower() == 'true')
        
        if gender:
            users = users.filter(profile__gender=gender)
        
        if country:
            users = users.filter(profile__country__icontains=country)
        
        if date_joined_from:
            try:
                from_date = datetime.strptime(date_joined_from, '%Y-%m-%d').date()
                users = users.filter(date_joined__date__gte=from_date)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid date_joined_from format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if date_joined_to:
            try:
                to_date = datetime.strptime(date_joined_to, '%Y-%m-%d').date()
                users = users.filter(date_joined__date__lte=to_date)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid date_joined_to format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if last_login_from:
            try:
                from_date = datetime.strptime(last_login_from, '%Y-%m-%d').date()
                users = users.filter(last_login__date__gte=from_date)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid last_login_from format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if last_login_to:
            try:
                to_date = datetime.strptime(last_login_to, '%Y-%m-%d').date()
                users = users.filter(last_login__date__lte=to_date)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid last_login_to format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if has_profile is not None:
            if has_profile.lower() == 'true':
                users = users.filter(profile__isnull=False)
            else:
                users = users.filter(profile__isnull=True)
        
        # Apply sorting
        sort_field = sort_by
        if sort_order == 'desc':
            sort_field = f'-{sort_by}'
        
        # Validate sort field
        valid_sort_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']
        if sort_by not in valid_sort_fields:
            sort_field = '-date_joined'
        
        users = users.order_by(sort_field)
        
        # Apply pagination
        total_count = users.count()
        users = users[offset:offset + limit]
        
        # Serialize the data with profile details
        users_data = []
        for user in users:
            user_dict = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.username,  # Phone is stored as username
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
                "profile": {}
            }
            
            # Add profile details if exists
            try:
                profile = user.profile
                user_dict["profile"] = {
                    "gender": profile.gender,
                    "country": profile.country
                }
            except:
                user_dict["profile"] = {
                    "gender": "",
                    "country": ""
                }
            
            users_data.append(user_dict)
        
        return Response({
            "success": True,
            "message": "Users retrieved successfully",
            "data": users_data,
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
            "message": f"Error retrieving users: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_user_details(request, user_id):
    """
    Admin endpoint to get detailed information about a specific user.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.username,  # Phone is stored as username
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
            "profile": {}
        }
        
        # Add profile details if exists
        try:
            profile = user.profile
            user_data["profile"] = {
                "gender": profile.gender,
                "country": profile.country
            }
        except:
            user_data["profile"] = {
                "gender": "",
                "country": ""
            }
        
        return Response({
            "success": True,
            "message": "User details retrieved successfully",
            "data": user_data
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            "success": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving user details: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_user(request):
    """
    Admin endpoint to create a new user.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get data from request
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        is_active = request.data.get('is_active', True)
        is_staff = request.data.get('is_staff', False)
        is_superuser = request.data.get('is_superuser', False)
        gender = request.data.get('gender', '')
        country = request.data.get('country', '')
        
        # Validate required fields
        if not username or not email or not password:
            return Response({
                "success": False,
                "message": "Username, email, and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "User with this username already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({
                "success": False,
                "message": "User with this email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        
        # Create profile
        Profile.objects.create(
            user=user,
            gender=gender,
            country=country
        )
        
        return Response({
            "success": True,
            "message": "User created successfully",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.username,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "date_joined": user.date_joined,
                "profile": {
                    "gender": gender,
                    "country": country
                }
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error creating user: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def admin_update_user(request, user_id):
    """
    Admin endpoint to update user information.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Update user fields
        if 'username' in request.data:
            new_username = request.data['username']
            if new_username != user.username and User.objects.filter(username=new_username).exists():
                return Response({
                    "success": False,
                    "message": "Username already exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            user.username = new_username
        
        if 'email' in request.data:
            new_email = request.data['email']
            if new_email != user.email and User.objects.filter(email=new_email).exists():
                return Response({
                    "success": False,
                    "message": "Email already exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email
        
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        
        if 'password' in request.data:
            user.set_password(request.data['password'])
        
        if 'is_active' in request.data:
            user.is_active = request.data['is_active']
        
        if 'is_staff' in request.data:
            user.is_staff = request.data['is_staff']
        
        if 'is_superuser' in request.data:
            user.is_superuser = request.data['is_superuser']
        
        user.save()
        
        # Update profile if exists
        try:
            profile = user.profile
            if 'gender' in request.data:
                profile.gender = request.data['gender']
            if 'country' in request.data:
                profile.country = request.data['country']
            profile.save()
        except:
            # Create profile if doesn't exist
            Profile.objects.create(
                user=user,
                gender=request.data.get('gender', ''),
                country=request.data.get('country', '')
            )
        
        return Response({
            "success": True,
            "message": "User updated successfully",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.username,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "date_joined": user.date_joined,
                "last_login": user.last_login
            }
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            "success": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error updating user: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_user(request, user_id):
    """
    Admin endpoint to delete a user.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent admin from deleting themselves
        if user.id == request.user.id:
            return Response({
                "success": False,
                "message": "Cannot delete your own account"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete user (this will also delete the profile due to CASCADE)
        user.delete()
        
        return Response({
            "success": True,
            "message": "User deleted successfully"
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            "success": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error deleting user: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_user_stats(request):
    """
    Admin endpoint to get user statistics.
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
        
        users = User.objects.all()
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                users = users.filter(date_joined__gte=start_date_obj)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid start_date format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                users = users.filter(date_joined__lte=end_date_obj)
            except ValueError:
                return Response({
                    "success": False,
                    "message": "Invalid end_date format. Use YYYY-MM-DD"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate statistics
        total_users = users.count()
        active_users = users.filter(is_active=True).count()
        inactive_users = users.filter(is_active=False).count()
        staff_users = users.filter(is_staff=True).count()
        superusers = users.filter(is_superuser=True).count()
        
        # Get today's registrations
        from datetime import date
        today = date.today()
        today_registrations = users.filter(date_joined__date=today).count()
        
        # Get this week's registrations
        from datetime import timedelta
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_registrations = users.filter(
            date_joined__date__gte=week_start,
            date_joined__date__lte=week_end
        ).count()
        
        # Get this month's registrations
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            month_end = today.replace(month=today.month + 1, day=1)
        
        month_registrations = users.filter(
            date_joined__date__gte=month_start,
            date_joined__date__lt=month_end
        ).count()
        
        return Response({
            "success": True,
            "message": "User statistics retrieved successfully",
            "stats": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "staff_users": staff_users,
                "superusers": superusers,
                "today_registrations": today_registrations,
                "week_registrations": week_registrations,
                "month_registrations": month_registrations
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving user statistics: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_filter_options(request):
    """
    Admin endpoint to get available filter options for users.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({
            "success": False,
            "message": "Access denied. Admin privileges required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get unique countries
        countries = Profile.objects.values_list('country', flat=True).distinct().exclude(country='').order_by('country')
        
        # Get unique genders
        genders = Profile.objects.values_list('gender', flat=True).distinct().exclude(gender='').order_by('gender')
        
        # Get date ranges
        from django.db.models import Min, Max
        date_range = User.objects.aggregate(
            earliest_joined=Min('date_joined'),
            latest_joined=Max('date_joined'),
            earliest_login=Min('last_login'),
            latest_login=Max('last_login')
        )
        
        return Response({
            "success": True,
            "message": "Filter options retrieved successfully",
            "filter_options": {
                "countries": list(countries),
                "genders": list(genders),
                "date_ranges": {
                    "earliest_joined": date_range['earliest_joined'],
                    "latest_joined": date_range['latest_joined'],
                    "earliest_login": date_range['earliest_login'],
                    "latest_login": date_range['latest_login']
                },
                "sort_options": [
                    {"value": "id", "label": "ID"},
                    {"value": "username", "label": "Username"},
                    {"value": "first_name", "label": "First Name"},
                    {"value": "last_name", "label": "Last Name"},
                    {"value": "email", "label": "Email"},
                    {"value": "date_joined", "label": "Date Joined"},
                    {"value": "last_login", "label": "Last Login"},
                    {"value": "is_active", "label": "Active Status"},
                    {"value": "is_staff", "label": "Staff Status"},
                    {"value": "is_superuser", "label": "Superuser Status"}
                ],
                "sort_orders": [
                    {"value": "asc", "label": "Ascending"},
                    {"value": "desc", "label": "Descending"}
                ]
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving filter options: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
