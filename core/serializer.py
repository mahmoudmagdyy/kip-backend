from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PhoneOTP, ReservedSlot, Profile



class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=False, required=True)
    last_name = serializers.CharField(allow_blank=False, required=True)
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True, write_only=True)
    gender = serializers.ChoiceField(choices=[('male','male'),('female','female'),('other','other')], required=False)
    country = serializers.CharField(required=False, allow_blank=True)
        
class CheckPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)

class SimpleRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=[('male','male'),('female','female'),('other','other')], required=False)
    country = serializers.CharField(required=False, allow_blank=True)
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)
    password = serializers.CharField( allow_blank=False, required=True, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'gender', 'country']

    def get_phone(self, obj):
        return obj.username

    def get_gender(self, obj):
        if hasattr(obj, 'profile') and obj.profile.gender:
            return obj.profile.gender
        return ''

    def get_country(self, obj):
        if hasattr(obj, 'profile') and obj.profile.country:
            return obj.profile.country
        return ''


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)
    code = serializers.CharField(min_length=4, max_length=6, allow_blank=False, required=True)

class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=8, allow_blank=False, required=True)
    new_password = serializers.CharField(min_length=8, allow_blank=False, required=True, write_only=True)

class ReservedSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedSlot
        fields = ['id', 'service_name', 'booking_date', 'booking_time', 'duration_minutes', 'status', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']

class CreateReservedSlotSerializer(serializers.Serializer):
    service_name = serializers.CharField(max_length=100, required=True)
    booking_date = serializers.CharField(required=True)
    booking_time = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[
        ('upcoming', 'Upcoming'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], default='upcoming', required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_booking_date(self, value):
        """Parse date from format 'Oct 31, 2025'"""
        try:
            from datetime import datetime
            parsed_date = datetime.strptime(value.strip(), '%b %d, %Y').date()
            return parsed_date
        except ValueError:
            raise serializers.ValidationError("Date must be in format 'Oct 31, 2025'")
    
    def validate_booking_time(self, value):
        """Parse time from format '01:00 PM'"""
        try:
            from datetime import datetime
            parsed_time = datetime.strptime(value.strip(), '%I:%M %p').time()
            return parsed_time
        except ValueError:
            raise serializers.ValidationError("Time must be in format '01:00 PM'")


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length=8, required=True, write_only=True)
    new_password = serializers.CharField(min_length=8, required=True, write_only=True)
