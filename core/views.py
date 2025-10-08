from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models  import User
from django.contrib.auth.hashers  import make_password
from rest_framework import status
from .serializer import SignUpSerializer,UserSerializer,LoginSerializer,CheckPhoneSerializer,SendOTPSerializer,VerifyOTPSerializer,ResetPasswordSerializer,ReservedSlotSerializer,CreateReservedSlotSerializer,ChangePasswordSerializer,SimpleRegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from .models import PhoneOTP, ReservedSlot, Profile
import random
from django.conf import settings
import requests



# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def check_phone(request):
    serializer = CheckPhoneSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone = serializer.validated_data['phone']
    exists = User.objects.filter(username=phone).exists()
    return Response({"exists": exists}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def send_otp(request):
    serializer = SendOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone = serializer.validated_data['phone']
    code = f"{random.randint(100000, 999999)}"
    expires_at = timezone.now() + timedelta(minutes=5)

    otp_obj, _ = PhoneOTP.objects.update_or_create(
        phone=phone,
        defaults={
            'code': code,
            'expires_at': expires_at,
            'attempts': 0,
            'is_verified': False,
        }
    )

    # Send via WhatsApp Cloud API if configured
    sent_via_whatsapp = False
    whatsapp_token = getattr(settings, 'WHATSAPP_TOKEN', None)
    whatsapp_phone_id = getattr(settings, 'WHATSAPP_PHONE_ID', None)
    if whatsapp_token and whatsapp_phone_id:
        try:
            url = f"https://graph.facebook.com/v20.0/{whatsapp_phone_id}/messages"
            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "text",
                "text": {"body": f"Your verification code is {code}. It expires in 5 minutes."}
            }
            headers = {
                "Authorization": f"Bearer {whatsapp_token}",
                "Content-Type": "application/json"
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            sent_via_whatsapp = resp.status_code in (200, 201)
        except Exception:
            sent_via_whatsapp = False

    return Response({
        "success": "OTP sent",
        "expires_in_seconds": 300,
        "channel": "whatsapp" if sent_via_whatsapp else "local"
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone = serializer.validated_data['phone']
    code = serializer.validated_data['code']

    otp_obj = PhoneOTP.objects.filter(phone=phone).first()
    if not otp_obj:
        return Response({"error": "OTP not requested for this phone"}, status=status.HTTP_400_BAD_REQUEST)
    if otp_obj.is_verified:
        return Response({"success": "Already verified"}, status=status.HTTP_200_OK)
    if otp_obj.is_expired():
        return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
    # Accept either the actual code or the master override code "0000"
    if otp_obj.code != code and code != "000000":
        otp_obj.attempts += 1
        otp_obj.save(update_fields=['attempts'])
        return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

    otp_obj.is_verified = True
    otp_obj.save(update_fields=['is_verified'])
    return Response({"success": "Phone verified"}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    data=request.data
    user=SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['phone']).exists():
            user=User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['phone'],
                username=data['phone'],
                password=make_password(data['password']),
                )
            # create profile with optional gender and country
            Profile.objects.create(
                user=user,
                gender=data.get('gender',''),
                country=data.get('country','')
            )
            return Response({"success": 'account register succesfully', "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success":'Email is aleady exist!'},status=status.HTTP_400_BAD_REQUEST)
    else:
            return Response(user.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    # expected fields: first_name, last_name, phone, optional password
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    phone = data.get("phone")
    if phone:
        user.username = phone
        user.email = phone  # keep email aligned if you previously used phone as email
    password = data.get("password")
    if password:
        user.password = make_password(password)

    user.save()
    # update profile fields if provided
    profile, _ = Profile.objects.get_or_create(user=user)
    if 'gender' in data:
        profile.gender = data['gender']
    if 'country' in data:
        profile.country = data['country']
    profile.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone = serializer.validated_data['phone']
    password = serializer.validated_data['password']
    user = authenticate(username=phone, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": "Login successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({"error": "Invalid phone or password"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    user = get_object_or_404(User, id=pk)

    # Admins can delete anyone
    if request.user.is_staff or request.user.is_superuser:
        user.delete()
        return Response({"success": "User deleted by admin"}, status=status.HTTP_200_OK)

    # Normal users can only delete themselves
    if user.id != request.user.id:
        return Response(
            {"error": "Sorry, you cannot delete this user"},
            status=status.HTTP_403_FORBIDDEN
        )

    user.delete()
    return Response({"success": "User deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def services(request):
    # Public services list: image and title only
    return Response({
        "services": [
            {"id": 1, "title": "Cleaning", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.07%20PM.jpeg", "is_vib": True},
            {"id": 2, "title": "Plumbing", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.06%20PM(1).jpeg", "is_vib": False},
            {"id": 3, "title": "Electrical", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.06%20PM.jpeg", "is_vib": True},
        {"id": 1, "title": "Cleaning", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.05%20PM.jpeg", "is_vib": True},
            {"id": 2, "title": "Plumbing", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.05%20PM(1).jpeg", "is_vib": False},
            {"id": 3, "title": "Electrical", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.04%20PM(2).jpeg", "is_vib": True}
        ]
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register_without_otp(request):
    """Create a user with default password 'password' without OTP verification.
    Body: {"phone": "...", "first_name": "...", "last_name": "..."}
    """
    serializer = SimpleRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone = serializer.validated_data['phone']
    first_name = serializer.validated_data.get('first_name', '')
    last_name = serializer.validated_data.get('last_name', '')

    if User.objects.filter(username=phone).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=phone,
        email=phone,
        first_name=first_name,
        last_name=last_name,
        password=make_password('password')
    )
    Profile.objects.create(
        user=user,
        gender=serializer.validated_data.get('gender',''),
        country=serializer.validated_data.get('country','')
    )

    return Response({
        "success": "User created successfully",
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def offers(request):
    # Public offers list: images only (stubbed). Replace with DB-backed data later.
    return Response({
        "offers": [
            {"image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.18.23%20PM(1).jpeg"},
            {"image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.18.23%20PM(2).jpeg"},
            {"image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.18.23%20PM.jpeg"}
        ]
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def booking_settings(request):
    # Static booking settings; replace with DB-driven values if needed later
    return Response([
        {"id": 2, "name": "WORKING_HOURS_START", "value": 12},
        {"id": 3, "name": "WORKING_HOURS_END", "value": 17},
        {"id": 5, "name": "DEFAULT_RESERVATION_DURATION_MINUTES", "value": 1},
        {"id": 6, "name": "OFF_DAYS", "value": "s"}
    ], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def countries(request):
    data = [
        {"code": "EG", "name": "Egypt"},
        {"code": "SA", "name": "Saudi Arabia"},
        {"code": "AE", "name": "United Arab Emirates"},
        {"code": "QA", "name": "Qatar"},
        {"code": "KW", "name": "Kuwait"},
        {"code": "JO", "name": "Jordan"},
        {"code": "LB", "name": "Lebanon"},
        {"code": "MA", "name": "Morocco"},
        {"code": "TN", "name": "Tunisia"},
        {"code": "DZ", "name": "Algeria"},
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change password for the authenticated user.
    Body: {"current_password": "...", "new_password": "..."}
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    current_password = serializer.validated_data['current_password']
    new_password = serializer.validated_data['new_password']

    user = request.user
    # Verify current password
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password
    user.set_password(new_password)
    user.save()

    return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def reset_password(request):
    """
    Reset password endpoint for forgotten passwords.
    Expected body: {"phone": "phone_number", "new_password": "new_password"}
    """
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone = serializer.validated_data['phone']
    new_password = serializer.validated_data['new_password']

    # Check if user exists
    try:
        user = User.objects.get(username=phone)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Reset the password
    user.password = make_password(new_password)
    user.save()

    return Response({
        "success": "Password reset successfully"
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reserved_slots(request):
    """
    GET: Retrieve user's reserved slots
    POST: Create a new reserved slot/booking
    """
    if request.method == 'GET':
        # Get all reserved slots for the authenticated user
        slots = ReservedSlot.objects.filter(user=request.user)
        serializer = ReservedSlotSerializer(slots, many=True)
        return Response({
            "success": "Reserved slots retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create a new reserved slot
        serializer = CreateReservedSlotSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get booking details
        booking_date = serializer.validated_data['booking_date']
        booking_time = serializer.validated_data['booking_time']
        duration = 60  # Default duration in minutes
        
        # Create the reserved slot
        reserved_slot = ReservedSlot.objects.create(
            user=request.user,
            service_name=serializer.validated_data['service_name'],
            booking_date=booking_date,
            booking_time=booking_time,
            duration_minutes=duration,
            status=serializer.validated_data.get('status', 'upcoming'),
            notes=serializer.validated_data.get('notes', '')
        )
        
        response_serializer = ReservedSlotSerializer(reserved_slot)
        return Response({
            "success": "Booking created successfully",
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reserved_slot_detail(request, slot_id):
    """
    PUT: Update a reserved slot
    DELETE: Cancel a reserved slot
    """
    try:
        slot = ReservedSlot.objects.get(id=slot_id, user=request.user)
    except ReservedSlot.DoesNotExist:
        return Response({
            "error": "Reserved slot not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        # Update the reserved slot
        serializer = CreateReservedSlotSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Update fields if provided
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
        return Response({
            "success": "Booking updated successfully",
            "data": response_serializer.data
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        # Cancel the reserved slot
        slot.status = 'cancelled'
        slot.save()
        
        return Response({
            "success": "Booking cancelled successfully"
        }, status=status.HTTP_200_OK)
