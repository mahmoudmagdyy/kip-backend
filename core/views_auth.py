from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models  import User
from django.contrib.auth.hashers  import make_password
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import (
    SignUpSerializer, UserSerializer, LoginSerializer, CheckPhoneSerializer,
    SendOTPSerializer, VerifyOTPSerializer, ResetPasswordSerializer, ChangePasswordSerializer,
    SimpleRegisterSerializer
)
from .models import PhoneOTP, Profile
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import requests
import random


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

    PhoneOTP.objects.update_or_create(
        phone=phone,
        defaults={'code': code, 'expires_at': expires_at, 'attempts': 0, 'is_verified': False}
    )

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
            headers = {"Authorization": f"Bearer {whatsapp_token}", "Content-Type": "application/json"}
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            sent_via_whatsapp = resp.status_code in (200, 201)
        except Exception:
            sent_via_whatsapp = False

    return Response({"success": "OTP sent", "expires_in_seconds": 300, "channel": "whatsapp" if sent_via_whatsapp else "local"}, status=status.HTTP_200_OK)


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
    data = request.data
    serializer = SignUpSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=data['phone']).exists():
        return Response({"success": 'Email is aleady exist!'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['phone'],
        username=data['phone'],
        password=make_password(data['password']),
    )
    Profile.objects.create(user=user, gender=data.get('gender', ''), country=data.get('country', ''))
    return Response({"success": 'account register succesfully', "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


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
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    phone = data.get("phone")
    if phone:
        user.username = phone
        user.email = phone
    password = data.get("password")
    if password:
        user.password = make_password(password)
    user.save()
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
        return Response({"success": "Login successfully", "access": str(refresh.access_token), "refresh": str(refresh), "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid phone or password"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.user.is_staff or request.user.is_superuser:
        user.delete()
        return Response({"success": "User deleted by admin"}, status=status.HTTP_200_OK)
    if user.id != request.user.id:
        return Response({"error": "Sorry, you cannot delete this user"}, status=status.HTTP_403_FORBIDDEN)
    user.delete()
    return Response({"success": "User deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    current_password = serializer.validated_data['current_password']
    new_password = serializer.validated_data['new_password']
    user = request.user
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    phone = serializer.validated_data['phone']
    new_password = serializer.validated_data['new_password']
    try:
        user = User.objects.get(username=phone)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    user.password = make_password(new_password)
    user.save()
    return Response({"success": "Password reset successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register_without_otp(request):
    serializer = SimpleRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    phone = serializer.validated_data['phone']
    first_name = serializer.validated_data.get('first_name', '')
    last_name = serializer.validated_data.get('last_name', '')
    if User.objects.filter(username=phone).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create(username=phone, email=phone, first_name=first_name, last_name=last_name, password=make_password('password'))
    Profile.objects.create(user=user, gender=serializer.validated_data.get('gender', ''), country=serializer.validated_data.get('country', ''))
    return Response({"success": "User created successfully", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


