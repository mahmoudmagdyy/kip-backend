"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Server is running'})

def debug_info(request):
    import sys
    import django
    from django.conf import settings
    return JsonResponse({
        'status': 'ok',
        'django_version': django.get_version(),
        'python_version': sys.version,
        'settings_module': settings.SETTINGS_MODULE,
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'installed_apps': settings.INSTALLED_APPS,
    })

urlpatterns = [
    path('', health_check, name='health_check'),
    path('health/', health_check, name='health_check_alt'),
    path('debug/', debug_info, name='debug_info'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('dashboard/', TemplateView.as_view(template_name='admin_dashboard.html'), name='admin_dashboard'),
    path('test/', TemplateView.as_view(template_name='test_realtime.html'), name='test_realtime'),
    path('test-image-upload/', TemplateView.as_view(template_name='test_image_upload.html'), name='test_image_upload'),
]

# Serve static and media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serve media files in production
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    # Also serve static files in production
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
