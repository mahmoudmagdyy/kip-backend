from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Service
from .serializer import ServiceSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def services(request):
    # Get services from database
    services = Service.objects.filter(is_active=True).order_by('order', 'id')
    serializer = ServiceSerializer(services, many=True)
    return Response({
        "services": serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def offers(request):
    """Get all active offers for mobile app"""
    try:
        from .models import Offer
        from django.utils import timezone
        
        # Get active offers that are currently valid
        now = timezone.now()
        offers = Offer.objects.filter(
            status='active',
            valid_from__lte=now,
            valid_until__gte=now
        ).order_by('-is_featured', '-created_at')
        
        # Build response with image URLs
        offers_data = []
        for offer in offers:
            offer_data = {
                "id": offer.id,
                "title": offer.title,
                "description": offer.description,
                "discount_type": offer.discount_type,
                "discount_value": str(offer.discount_value),
                "valid_from": offer.valid_from.isoformat() if offer.valid_from else None,
                "valid_until": offer.valid_until.isoformat() if offer.valid_until else None,
                "is_featured": offer.is_featured,
                "image": None
            }
            
            # Add image URL if available
            if offer.image_url:
                # Build absolute URL for the image
                offer_data["image"] = request.build_absolute_uri(offer.image_url)
            elif offer.image:
                # Fallback to Django's image field
                offer_data["image"] = request.build_absolute_uri(offer.image.url)
            
            offers_data.append(offer_data)
        
        return Response({
            "success": True,
            "offers": offers_data
        })
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error retrieving offers: {str(e)}",
            "offers": []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def booking_settings(request):
    return Response([
        {"id": 2, "name": "WORKING_HOURS_START", "value": 12},
        {"id": 3, "name": "WORKING_HOURS_END", "value": 17},
        {"id": 5, "name": "DEFAULT_RESERVATION_DURATION_MINUTES", "value": 1},
        {"id": 6, "name": "OFF_DAYS", "value": "s"}
    ])


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
    return Response(data)