from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def services(request):
    return Response({
        "services": [
            {"id": 1, "title": "Cleaning", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.07%20PM.jpeg", "is_vib": True},
            {"id": 2, "title": "Plumbing", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.06%20PM(1).jpeg", "is_vib": False},
            {"id": 3, "title": "Electrical", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.06%20PM.jpeg", "is_vib": True},
            {"id": 1, "title": "Cleaning", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.05%20PM.jpeg", "is_vib": True},
            {"id": 2, "title": "Plumbing", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.05%20PM(1).jpeg", "is_vib": False},
            {"id": 3, "title": "Electrical", "image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.05.04%20PM(2).jpeg", "is_vib": True}
        ]
    })


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def offers(request):
    return Response({
        "offers": [
            {"image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.18.23%20PM(1).jpeg"},
            {"image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.18.23%20PM(2).jpeg"},
            {"image": "http://72.60.209.172:9090/WhatsApp%20Image%202025-10-06%20at%203.18.23%20PM.jpeg"}
        ]
    })


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


