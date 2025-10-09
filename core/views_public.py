from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def services(request):
    return Response({
        "services": [
            {
                "id": 1,
                "title": "قضايا قانونية",
                "image": "https://images.pexels.com/photos/374074/pexels-photo-374074.jpeg",
                "is_vib": True,
                "sub_services": [
                    {
                        "id": 101,
                        "title": "استشارات قانونية",
                        "description": "استشارة قانونية شاملة حول القضايا المدنية والجنائية.",
                        "image": "https://images.pexels.com/photos/442761/pexels-photo-442761.jpeg",
                        "is_vib": True
                    },
                    {
                        "id": 102,
                        "title": "صياغة العقود",
                        "description": "صياغة ومراجعة العقود التجارية والعقارية.",
                        "image": "https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg",
                        "is_vib": False
                    }
                ]
            },
              {
                "id": 2,
                "title": "قضايا قانونية",
                "image": "https://images.pexels.com/photos/374074/pexels-photo-374074.jpeg",
                "is_vib": False,
                "sub_services": [
                    {
                        "id": 301,
                        "title": "استشارات قانونية",
                        "description": "استشارة قانونية شاملة حول القضايا المدنية والجنائية.",
                        "image": "https://images.pexels.com/photos/442761/pexels-photo-442761.jpeg",
                        "is_vib": False
                    },
                    {
                        "id": 302,
                        "title": "صياغة العقود",
                        "description": "صياغة ومراجعة العقود التجارية والعقارية.",
                        "image": "https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg",
                        "is_vib": False
                    }
                ]
            },
              {
                "id": 3,
                "title": "قضايا قانونية",
                "image": "https://images.pexels.com/photos/374074/pexels-photo-374074.jpeg",
                "is_vib": True,
                "sub_services": [
                    {
                        "id": 200,
                        "title": "استشارات قانونية",
                        "description": "استشارة قانونية شاملة حول القضايا المدنية والجنائية.",
                        "image": "https://images.pexels.com/photos/442761/pexels-photo-442761.jpeg",
                        "is_vib": False
                    },
                    {
                        "id": 201,
                        "title": "صياغة العقود",
                        "description": "صياغة ومراجعة العقود التجارية والعقارية.",
                        "image": "https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg",
                        "is_vib": False
                    }
                ]
            },
          
        ]
    })



@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def offers(request):
    return Response({
        "offers": [
            {"image": "https://images.pexels.com/photos/374074/pexels-photo-374074.jpeg?_gl=1*1mgn3hc*_ga*MTE1NDQ1ODM0LjE3NTk0OTA2NzM.*_ga_8JE65Q40S6*czE3NTk5NDQ3ODQkbzIkZzAkdDE3NTk5NDQ3ODQkajYwJGwwJGgw"},
            {"image": "https://images.pexels.com/photos/374074/pexels-photo-374074.jpeg?_gl=1*1mgn3hc*_ga*MTE1NDQ1ODM0LjE3NTk0OTA2NzM.*_ga_8JE65Q40S6*czE3NTk5NDQ3ODQkbzIkZzAkdDE3NTk5NDQ3ODQkajYwJGwwJGgw"},
            {"image": "https://images.pexels.com/photos/374074/pexels-photo-374074.jpeg?_gl=1*1mgn3hc*_ga*MTE1NDQ1ODM0LjE3NTk0OTA2NzM.*_ga_8JE65Q40S6*czE3NTk5NDQ3ODQkbzIkZzAkdDE3NTk5NDQ3ODQkajYwJGwwJGgw"}
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


