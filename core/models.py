

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.phone} - verified={self.is_verified}"


class ReservedSlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserved_slots')
    service_name = models.CharField(max_length=100)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    status = models.CharField(max_length=20, choices=[
        ('upcoming', 'Upcoming'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], default='upcoming')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name} - {self.service_name} on {self.booking_date} at {self.booking_time}"



class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class Service(models.Model):
    title_ar = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    description_ar = models.TextField()
    description_en = models.TextField()
    icon = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title_en}"


class SubService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='sub_services')
    title_ar = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    description_ar = models.TextField()
    description_en = models.TextField()
    icon = models.URLField(max_length=500, blank=True, null=True)
    is_vib = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title_en} - {self.service.title_en}"


class BookingSettings(models.Model):
    WORKING_HOURS_START = models.IntegerField(default=9, help_text="Start hour (24-hour format)")
    WORKING_HOURS_END = models.IntegerField(default=17, help_text="End hour (24-hour format)")
    DEFAULT_RESERVATION_DURATION_MINUTES = models.IntegerField(default=60, help_text="Duration in minutes")
    OFF_DAYS = models.CharField(max_length=20, default="", blank=True, help_text="Comma-separated days (0=Monday, 6=Sunday)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking Settings"
        verbose_name_plural = "Booking Settings"

    def __str__(self):
        return f"Booking Settings - {self.WORKING_HOURS_START}:00 to {self.WORKING_HOURS_END}:00"

    def get_off_days_list(self):
        """Convert OFF_DAYS string to list of integers"""
        if not self.OFF_DAYS:
            return []
        return [int(day.strip()) for day in self.OFF_DAYS.split(',') if day.strip().isdigit()]


class Offer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='offers/', null=True, blank=True, help_text="Offer image")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage (0-100) or fixed amount")
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of uses (null = unlimited)")
    usage_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_offers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.discount_value}{'%' if self.discount_type == 'percentage' else ' USD'}"

    def is_valid(self):
        """Check if offer is currently valid"""
        now = timezone.now()
        return (
            self.status == 'active' and
            self.valid_from <= now <= self.valid_until and
            (self.usage_limit is None or self.usage_count < self.usage_limit)
        )

    def can_use(self):
        """Check if offer can be used"""
        return self.is_valid()

    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

