from django.contrib import admin
from .models import PhoneOTP, ReservedSlot, Profile, Service, SubService, BookingSettings


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['phone', 'code', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['phone']


@admin.register(ReservedSlot)
class ReservedSlotAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_name', 'booking_date', 'booking_time', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__first_name', 'user__last_name', 'service_name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'country']
    list_filter = ['gender', 'country']
    search_fields = ['user__first_name', 'user__last_name']


class SubServiceInline(admin.TabularInline):
    model = SubService
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_ar', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title_en', 'title_ar']
    inlines = [SubServiceInline]
    ordering = ['order', 'id']


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'service', 'is_vib', 'is_active', 'order']
    list_filter = ['is_vib', 'is_active', 'service']
    search_fields = ['title_en', 'title_ar', 'service__title_en']
    ordering = ['service', 'order', 'id']


@admin.register(BookingSettings)
class BookingSettingsAdmin(admin.ModelAdmin):
    list_display = ['WORKING_HOURS_START', 'WORKING_HOURS_END', 'DEFAULT_RESERVATION_DURATION_MINUTES', 'OFF_DAYS', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['OFF_DAYS']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Working Hours', {
            'fields': ('WORKING_HOURS_START', 'WORKING_HOURS_END')
        }),
        ('Booking Settings', {
            'fields': ('DEFAULT_RESERVATION_DURATION_MINUTES', 'OFF_DAYS')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
