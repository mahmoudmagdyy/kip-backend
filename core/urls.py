from django.urls import path
from . import views_auth as auth
from . import views_booking as booking
from . import views_public as pub
from . import views_dashboard as dashboard
from . import views_booking_management as booking_mgmt
from . import views_admin_booking as admin_booking
from . import views_admin_users as admin_users
from . import views_admin_offers as admin_offers



urlpatterns = [
    path('check-phone/',auth.check_phone,name="check-phone"),
    path('send-otp/',auth.send_otp,name="send-otp"),
    path('verify-otp/',auth.verify_otp,name="verify-otp"),
    path('register/',auth.register,name="register"),
    path('register-without-otp/',auth.register_without_otp,name="register-without-otp"),
    path('user_info/',auth.current_user,name="register"),
    path('user_update_info/',auth.update_user,name="user_update_info"),
    path('login/',auth.login,name="login"),
    path('change-password/',auth.change_password,name="change-password"),
    path('reset-password/',auth.reset_password,name="reset-password"),
    path('reserved/',booking.reserved_slots,name="reserved-slots"),
    path('reserved/<int:slot_id>/',booking.reserved_slot_detail,name="reserved-slot-detail"),
    path('reservations/reserved_slots/', booking.reservations_reserved_slots, name="reservations-reserved-slots"),
    path('reservations/available_slots/', booking.available_time_slots, name="available-time-slots"),
    
    # Advanced Booking Management
    path('booking/settings/', booking_mgmt.booking_settings_management, name="booking-settings-management"),
    path('booking/smart-available-slots/', booking_mgmt.smart_available_slots, name="smart-available-slots"),
    path('booking/calendar/', booking_mgmt.booking_calendar, name="booking-calendar"),
    path('booking/create/', booking_mgmt.create_booking, name="create-booking"),
    path('user/delete/<str:pk>',auth.delete_user,name="deleteUser"),
    path('services/',pub.services,name="services"),
    path('offers/',pub.offers,name="offers"),
    path('booking-settings/',pub.booking_settings,name="booking_settings"),
    path('countries/',pub.countries,name="countries"),
    
    # Dashboard endpoints for services management
    path('dashboard/services/', dashboard.dashboard_services, name="dashboard-services"),
    path('dashboard/services/create/', dashboard.create_service, name="create-service"),
    path('dashboard/services/<int:service_id>/', dashboard.get_service, name="get-service"),
    path('dashboard/services/<int:service_id>/update/', dashboard.update_service, name="update-service"),
    path('dashboard/services/<int:service_id>/delete/', dashboard.delete_service, name="delete-service"),
    path('dashboard/services/<int:service_id>/sub-services/', dashboard.get_service_sub_services, name="get-service-sub-services"),
    path('dashboard/sub-services/create/', dashboard.create_sub_service, name="create-sub-service"),
    path('dashboard/sub-services/<int:sub_service_id>/', dashboard.get_sub_service, name="get-sub-service"),
    path('dashboard/sub-services/<int:sub_service_id>/update/', dashboard.update_sub_service, name="update-sub-service"),
    path('dashboard/sub-services/<int:sub_service_id>/delete/', dashboard.delete_sub_service, name="delete-sub-service"),

    # Admin Booking Management (NEW)
    path('admin/bookings/', admin_booking.admin_get_all_bookings, name="admin-get-all-bookings"),
    path('admin/bookings/stats/', admin_booking.admin_get_booking_stats, name="admin-get-booking-stats"),
    path('admin/bookings/<int:booking_id>/', admin_booking.admin_get_booking_details, name="admin-get-booking-details"),
    path('admin/bookings/<int:booking_id>/update/', admin_booking.admin_update_booking_status, name="admin-update-booking-status"),
    path('admin/bookings/<int:booking_id>/delete/', admin_booking.admin_delete_booking, name="admin-delete-booking"),
    path('admin/bookings/create/', admin_booking.admin_create_booking, name="admin-create-booking"),

    # Admin User Management (NEW)
    path('admin/users/', admin_users.admin_get_all_users, name="admin-get-all-users"),
    path('admin/users/stats/', admin_users.admin_get_user_stats, name="admin-get-user-stats"),
    path('admin/users/filter-options/', admin_users.admin_get_filter_options, name="admin-get-filter-options"),
    path('admin/users/<int:user_id>/', admin_users.admin_get_user_details, name="admin-get-user-details"),
    path('admin/users/<int:user_id>/update/', admin_users.admin_update_user, name="admin-update-user"),
    path('admin/users/<int:user_id>/delete/', admin_users.admin_delete_user, name="admin-delete-user"),
    path('admin/users/create/', admin_users.admin_create_user, name="admin-create-user"),

    # Admin Offer Management (NEW)
    path('admin/offers/', admin_offers.admin_offers_list, name="admin-get-all-offers"),
    path('admin/offers/stats/', admin_offers.admin_offers_stats, name="admin-get-offer-stats"),
    path('admin/offers/filter-options/', admin_offers.admin_offers_filter_options, name="admin-get-offer-filter-options"),
    path('admin/offers/<int:offer_id>/', admin_offers.admin_offer_detail, name="admin-get-offer-details"),
    path('admin/offers/<int:offer_id>/update/', admin_offers.admin_update_offer, name="admin-update-offer"),
    path('admin/offers/<int:offer_id>/delete/', admin_offers.admin_delete_offer, name="admin-delete-offer"),
    path('admin/offers/<int:offer_id>/toggle-status/', admin_offers.admin_toggle_offer_status, name="admin-toggle-offer-status"),
    path('admin/offers/<int:offer_id>/toggle-featured/', admin_offers.admin_toggle_offer_featured, name="admin-toggle-offer-featured"),
    path('admin/offers/<int:offer_id>/upload-image/', admin_offers.admin_upload_offer_image, name="admin-upload-offer-image"),
    path('admin/offers/<int:offer_id>/delete-image/', admin_offers.admin_delete_offer_image, name="admin-delete-offer-image"),
    path('admin/offers/create-image/', admin_offers.admin_create_offer_image, name="admin-create-offer-image"),
    path('admin/offers/create/', admin_offers.admin_create_offer, name="admin-create-offer"),
]
