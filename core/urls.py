from django.urls import path
from . import views_auth as auth
from . import views_booking as booking
from . import views_public as pub



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
    path('user/delete/<str:pk>',auth.delete_user,name="deleteUser"),
    path('services/',pub.services,name="services"),
    path('offers/',pub.offers,name="offers"),
    path('booking-settings/',pub.booking_settings,name="booking_settings"),
    path('countries/',pub.countries,name="countries"),
]
