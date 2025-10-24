from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PhoneOTP, ReservedSlot, Profile, Service, SubService, BookingSettings, Offer
from .utils import get_server_media_url



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
    
    def create(self, validated_data):
        """Create a new ReservedSlot instance"""
        from .models import ReservedSlot
        return ReservedSlot.objects.create(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length=8, required=True, write_only=True)
    new_password = serializers.CharField(min_length=8, required=True, write_only=True)


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title_ar', 'title_en', 'description_ar', 'description_en', 'icon', 'is_active', 'order']


# ---------------- SubService ----------------
class SubServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ['service', 'title_ar', 'title_en', 'description_ar', 'description_en', 'icon', 'is_vib', 'is_active', 'order']


class BookingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSettings
        fields = ['id', 'WORKING_HOURS_START', 'WORKING_HOURS_END', 'DEFAULT_RESERVATION_DURATION_MINUTES', 'OFF_DAYS', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
class SubServiceSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    
    class Meta:
        model = SubService
        fields = ['id', 'service', 'title_ar', 'title_en', 'description_ar', 'description_en',
                  'icon', 'is_vib', 'is_active', 'order']
    
    def get_icon(self, obj):
        request = self.context.get('request')
        if obj.icon:
            if obj.icon.startswith('http'):
                return obj.icon
            return get_server_media_url(request, obj.icon)
        return None

# ---------------- Service ----------------
class ServiceSerializer(serializers.ModelSerializer):
    sub_services = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'title_ar', 'title_en', 'description_ar', 'description_en',
                  'icon', 'is_active', 'order', 'sub_services']

    def get_icon(self, obj):
        request = self.context.get('request')
        if obj.icon:
            if obj.icon.startswith('http'):
                return obj.icon
            return get_server_media_url(request, obj.icon)
        return None

    def get_sub_services(self, obj):
        subs = obj.sub_services.filter(is_active=True).order_by('order', 'id')
        return SubServiceSerializer(subs, many=True, context=self.context).data
class OfferSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    is_valid = serializers.SerializerMethodField()
    remaining_uses = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'description', 'image', 'discount_type', 'discount_value', 
            'valid_from', 'valid_until', 'status', 'is_featured', 'usage_limit', 
            'usage_count', 'created_by', 'created_by_name', 'created_at', 'updated_at',
            'is_valid', 'remaining_uses'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'usage_count']
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
    
    def get_is_valid(self, obj):
        return obj.is_valid()
    
    def get_remaining_uses(self, obj):
        if obj.usage_limit is None:
            return None  # Unlimited
        return max(0, obj.usage_limit - obj.usage_count)


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'title', 'description', 'image', 'discount_type', 'discount_value', 
            'valid_from', 'valid_until', 'status', 'is_featured', 'usage_limit'
        ]
    
    def validate_discount_value(self, value):
        """Validate discount value based on type"""
        discount_type = self.initial_data.get('discount_type', 'percentage')
        if discount_type == 'percentage' and (value < 0 or value > 100):
            raise serializers.ValidationError("Percentage discount must be between 0 and 100")
        elif discount_type == 'fixed' and value < 0:
            raise serializers.ValidationError("Fixed discount must be positive")
        return value
    
    def validate(self, data):
        """Validate that valid_until is after valid_from"""
        if data['valid_until'] <= data['valid_from']:
            raise serializers.ValidationError("Valid until date must be after valid from date")
        return data


class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'title', 'description', 'image', 'discount_type', 'discount_value', 
            'valid_from', 'valid_until', 'status', 'is_featured', 'usage_limit'
        ]
    
    def validate_discount_value(self, value):
        """Validate discount value based on type"""
        discount_type = self.initial_data.get('discount_type', 'percentage')
        if discount_type == 'percentage' and (value < 0 or value > 100):
            raise serializers.ValidationError("Percentage discount must be between 0 and 100")
        elif discount_type == 'fixed' and value < 0:
            raise serializers.ValidationError("Fixed discount must be positive")
        return value
    
    def validate(self, data):
        """Validate that valid_until is after valid_from"""
        if data['valid_until'] <= data['valid_from']:
            raise serializers.ValidationError("Valid until date must be after valid from date")
        return data
