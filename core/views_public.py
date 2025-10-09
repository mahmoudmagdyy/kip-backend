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
      "title_ar": "الخدمات القانونية وقطاع الشركات",
      "title_en": "Legal Services & Corporate Sector",
      "description_ar": "خدمات قانونية شاملة للشركات والأفراد، تشمل الاستشارات والتوثيق والتأسيس.",
      "description_en": "Comprehensive legal services for companies and individuals, including consultancy, documentation, and incorporation.",
      "icon": "https://www.svgrepo.com/svg/505182/legal-service",  
      "sub_services": [
        {
          "id": 101,
          "title_ar": "الاستشارات القانونية",
          "title_en": "Legal Consultations",
          "description_ar": "تقديم استشارات قانونية مهنية في القضايا المدنية والجنائية.",
          "description_en": "Providing professional legal advice in civil and criminal matters.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 102,
          "title_ar": "التمثيل والاستشارات أمام الجهات المختصة",
          "title_en": "Representation & Advisory before Authorities",
          "description_ar": "تمثيل قانوني أمام الجهات الحكومية والهيئات المختصة.",
          "description_en": "Legal representation before governmental bodies and competent authorities.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 103,
          "title_ar": "إعداد وصياغة المستندات والعقود القانونية",
          "title_en": "Drafting Legal Documents & Contracts",
          "description_ar": "صياغة ومراجعة العقود والمستندات القانونية بشكل دقيق.",
          "description_en": "Drafting and reviewing legal agreements and documents with precision.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 104,
          "title_ar": "عقود التأسيس واتفاقيات الشراكة",
          "title_en": "Foundation Contracts & Partnership Agreements",
          "description_ar": "إعداد عقود التأسيس واتفاقيات الشراكة بين الأطراف.",
          "description_en": "Preparing formation contracts and partnership agreements.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 105,
          "title_ar": "أنشطة قانونية واستشارات عامة",
          "title_en": "General Legal Activities & Consultations",
          "description_ar": "تقديم أعمال قانونية متنوعة واستشارات عامة.",
          "description_en": "Providing diverse legal tasks and general consultations.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 106,
          "title_ar": "تأسيس الشركات وخدمات الشركات (التراخيص، السجل، الحوكمة)",
          "title_en": "Company Formation & Corporate Services (Licensing, Registry, Governance)",
          "description_ar": "تأسيس الشركات، استخراج التراخيص، التسجيل، وتنظيم الحوكمة.",
          "description_en": "Incorporation, licensing, registry, and governance setup for companies.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 107,
          "title_ar": "مستشارون قانونيون",
          "title_en": "Legal Consultants",
          "description_ar": "مستشارون يقدمون حلول قانونية مخصصة وفق حاجة العميل.",
          "description_en": "Consultants offering tailored legal solutions based on client needs.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        }
      ]
    },
    {
      "id": 2,
      "title_ar": "خدمات الملكية الفكرية",
      "title_en": "Intellectual Property Services",
      "description_ar": "خدمات لحماية الأفكار والإبداعات عبر تسجيل براءات الاختراع والعلامات التجارية.",
      "description_en": "Services to protect ideas and creativity via patent and trademark registration.",
      "icon": "https://www.svgrepo.com/svg/425985/globe-language",
      "sub_services": [
        {
          "id": 201,
          "title_ar": "وكيل براءات/ملكية صناعية",
          "title_en": "Patent / Industrial Property Agent",
          "description_ar": "تسجيل براءات الاختراع وحماية الحقوق الصناعية.",
          "description_en": "Registering patents and securing industrial property rights.",
          "icon": "https://www.svgrepo.com/svg/425985/globe-language",
          "is_vib": false
        },
        {
          "id": 202,
          "title_ar": "وكيل تسجيل العلامات التجارية",
          "title_en": "Trademark Registration Agent",
          "description_ar": "تسجيل العلامات التجارية محلياً ودولياً.",
          "description_en": "Register trademarks locally and internationally.",
          "icon": "https://www.svgrepo.com/svg/425985/globe-language",
          "is_vib": false
        },
        {
          "id": 203,
          "title_ar": "وكيل تسجيل حقوق الملكية الفكرية",
          "title_en": "Intellectual Property Rights Agent",
          "description_ar": "إدارة حقوق التأليف والنشر وحقوق الملكية الفكرية.",
          "description_en": "Managing copyrights and intellectual property rights.",
          "icon": "https://www.svgrepo.com/svg/425985/globe-language",
          "is_vib": false
        },
        {
          "id": 204,
          "title_ar": "وكالة تحصيل حقوق النشر الدولية",
          "title_en": "International Copyright Collection Agency",
          "description_ar": "جمع حقوق النشر الدولية لصالح المؤلفين.",
          "description_en": "Collecting international copyright royalties for authors.",
          "icon": "https://www.svgrepo.com/svg/425985/globe-language",
          "is_vib": false
        },
        {
          "id": 205,
          "title_ar": "خدمات النشر/حقوق النشر الدولية",
          "title_en": "Publishing & International Copyright Services",
          "description_ar": "دعم عملية النشر مع حقوق النشر الدولية.",
          "description_en": "Support for publishing with international copyright protections.",
          "icon": "https://www.svgrepo.com/svg/425985/globe-language",
          "is_vib": false
        }
      ]
    },
    {
      "id": 3,
      "title_ar": "خدمات الترجمة والاتصال",
      "title_en": "Translation & Communication Services",
      "description_ar": "خدمات ترجمة متعددة الأنواع بالإضافة إلى التواصل والعلاقات العامة.",
      "description_en": "Various translation services plus communication and public relations.",
      "icon": "https://www.svgrepo.com/svg/455407/language-translation",
      "sub_services": [
        {
          "id": 301,
          "title_ar": "أنشطة الترجمة التحريرية والشفوية",
          "title_en": "Written & Oral Translation Activities",
          "description_ar": "ترجمة نصية وشفوية لنطاق واسع من المحتوى.",
          "description_en": "Textual and oral translation across a wide range of content.",
          "icon": "https://www.svgrepo.com/svg/455407/language-translation",
          "is_vib": false
        },
        {
          "id": 302,
          "title_ar": "خدمات الترجمة العامة والمتخصصة",
          "title_en": "General & Specialized Translation Services",
          "description_ar": "ترجمة في المجالات العامة والتخصصية بدقة.",
          "description_en": "Translation in general and specialized domains with accuracy.",
          "icon": "https://www.svgrepo.com/svg/455407/language-translation",
          "is_vib": false
        },
        {
          "id": 303,
          "title_ar": "الترجمة القانونية",
          "title_en": "Legal Translation",
          "description_ar": "ترجمة المستندات القانونية والعقود بمهنية.",
          "description_en": "Translating legal documents and contracts with professionalism.",
          "icon": "https://www.svgrepo.com/svg/455407/language-translation",
          "is_vib": false
        },
        {
          "id": 304,
          "title_ar": "الترجمة الفورية",
          "title_en": "Interpretation",
          "description_ar": "خدمات التفسير الفوري للمؤتمرات والاجتماعات.",
          "description_en": "Real-time interpretation services for conferences and meetings.",
          "icon": "https://www.svgrepo.com/svg/455407/language-translation",
          "is_vib": false
        },
        {
          "id": 305,
          "title_ar": "خدمات العلاقات العامة (PR)",
          "title_en": "Public Relations (PR) Services",
          "description_ar": "إدارة الصورة العامة والتواصل الإعلامي.",
          "description_en": "Managing public image and media communications.",
          "icon": "https://www.svgrepo.com/svg/455407/language-translation",
          "is_vib": false
        },
        {
          "id": 306,
          "title_ar": "خدمات المؤلف/الكتّاب",
          "title_en": "Author Services",
          "description_ar": "دعم المؤلفين في النشر والتنسيق وحقوقهم.",
          "description_en": "Supporting authors in publishing, formatting, and their rights.",
          "icon": "https://www.svgrepo.com/svg/455407/language-translation",
          "is_vib": false
        }
      ]
    },
    {
      "id": 4,
      "title_ar": "الدعم الإداري وقطاع الأعمال",
      "title_en": "Administrative Support & Business Sector",
      "description_ar": "خدمات إدارية ودعم للأعمال تشمل التنظيم والمشورة.",
      "description_en": "Administrative and business support services including organization and consulting.",
      "icon": "https://www.svgrepo.com/svg/505182/legal-service",
      "sub_services": [
        {
          "id": 401,
          "title_ar": "الخدمات الإدارية لرجال الأعمال",
          "title_en": "Administrative Services for Businessmen",
          "description_ar": "تنسيق وإدارة الأعمال الإدارية لرواد الأعمال.",
          "description_en": "Coordination and management of administrative tasks for entrepreneurs.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 402,
          "title_ar": "خدمات رجال الأعمال",
          "title_en": "Businessmen Services",
          "description_ar": "خدمات مخصصة لدعم أنشطة رجال الأعمال.",
          "description_en": "Tailored services to support businessmen’s operations.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 403,
          "title_ar": "الاستشارات التجارية",
          "title_en": "Business Consulting",
          "description_ar": "تقديم استشارات وخطط تجارية احترافية.",
          "description_en": "Providing professional business consulting and strategies.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 404,
          "title_ar": "التجارة العامة",
          "title_en": "General Trading",
          "description_ar": "التعامل في سلع متنوعة وشبكات التوزيع.",
          "description_en": "Dealing in diverse goods and distribution networks.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 405,
          "title_ar": "مركز خدمة توافق لأصحاب العمل والعمال",
          "title_en": "Tawafoq Services Center for Employers & Employees",
          "description_ar": "مركز يقدم تسوية النزاعات وخدمات توافق بين الأطراف.",
          "description_en": "Center offering dispute resolution and harmony services between parties.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        }
      ]
    },
    {
      "id": 5,
      "title_ar": "التحصيل المالي وخدمات الديون",
      "title_en": "Financial Collection & Debt Services",
      "description_ar": "إدارة تحصيل المبالغ المستحقة وخدمات الديون.",
      "description_en": "Management of collection of owed amounts and debt services.",
      "icon": "https://www.svgrepo.com/svg/505182/legal-service",
      "sub_services": [
        {
          "id": 501,
          "title_ar": "تحصيل الديون",
          "title_en": "Debt Collection",
          "description_ar": "تحصيل الديون نيابة عن العملاء للأفراد والشركات.",
          "description_en": "Collecting debts on behalf of clients for individuals and companies.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 502,
          "title_ar": "وكالة/مكتب تحصيل الديون",
          "title_en": "Debt Collection Office/Agency",
          "description_ar": "مكتب متخصص في إدارة عمليات التحصيل.",
          "description_en": "An agency specialized in handling debt collection operations.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 503,
          "title_ar": "تحصيل المدفوعات للمطالبات",
          "title_en": "Payment Collection for Claims",
          "description_ar": "تحصيل المدفوعات المتعلقة بالمطالبات القانونية.",
          "description_en": "Collecting payments related to legal claims.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 504,
          "title_ar": "توريد المدفوعات للعملاء",
          "title_en": "Remittance to Clients",
          "description_ar": "إرسال المبالغ المحصلة إلى العملاء.",
          "description_en": "Remitting collected amounts back to clients.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        }
      ]
    },
    {
      "id": 6,
      "title_ar": "مجالات القضايا والخدمات القانونية",
      "title_en": "Fields of Cases & Legal Services",
      "description_ar": "تخصص في أنواع القضايا القانونية مع تقديم حلول متخصصة.",
      "description_en": "Specialization in various legal case types with tailored solutions.",
      "icon": "https://www.svgrepo.com/svg/505182/legal-service",
      "sub_services": [
        {
          "id": 601,
          "title_ar": "القضايا العقارية",
          "title_en": "Real Estate Cases",
          "description_ar": "القضايا المتعلّقة بالعقارات وحقوق الملكية.",
          "description_en": "Disputes related to real estate and property rights.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 602,
          "title_ar": "نزاعات الملكية والإيجار والبيع العقاري",
          "title_en": "Property, Rent & Real Estate Sale Disputes",
          "description_ar": "نزاعات متعلقة بالملكية، الإيجار، أو البيع العقاري.",
          "description_en": "Disputes related to ownership, rent, or real estate sale.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 603,
          "title_ar": "عقود التطوير والمشاريع العقارية",
          "title_en": "Development & Real Estate Project Contracts",
          "description_ar": "صياغة ومراجعة عقود المشاريع العقارية.",
          "description_en": "Drafting and reviewing real estate development project contracts.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 604,
          "title_ar": "قضايا العقود والاتفاقيات وصياغة العقود ومراجعتها",
          "title_en": "Contract & Agreement Cases, Drafting & Reviewing",
          "description_ar": "القضايا المتعلقة بالعقود وأعمال التصميم والمراجعة.",
          "description_en": "Cases related to contracts and drafting & reviewing tasks.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 605,
          "title_ar": "تسوية النزاعات التعاقدية والتحكيم",
          "title_en": "Contractual Dispute Settlement & Arbitration",
          "description_ar": "تسوية النزاعات عبر الاتفاق أو اللجوء للتحكيم.",
          "description_en": "Settling disputes by agreement or resorting to arbitration.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 606,
          "title_ar": "القضايا المدنية",
          "title_en": "Civil Cases",
          "description_ar": "القضايا المدنية بين الأفراد أو الكيانات القانونية.",
          "description_en": "Civil cases between individuals or legal entities.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 607,
          "title_ar": "التعويضات والمطالبات المالية",
          "title_en": "Compensations & Financial Claims",
          "description_ar": "المطالبة بالتعويضات المالية عبر المسار القانوني.",
          "description_en": "Seeking financial compensation through legal means.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 608,
          "title_ar": "المنازعات بين الأفراد والشركات",
          "title_en": "Disputes Between Individuals & Companies",
          "description_ar": "النزاعات القانونية بين الأفراد والشركات.",
          "description_en": "Legal disputes between individuals and corporate entities.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 609,
          "title_ar": "القضايا العمالية (عقود العمل، نزاعات الأجور، الإجازات، الفصل)",
          "title_en": "Labor Cases (Contracts, Wage Disputes, Leave, Termination)",
          "description_ar": "القضايا العمالية كالعقود، الأجور، الفصل والإجازات.",
          "description_en": "Labor cases such as contracts, wage disputes, termination and leave.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 610,
          "title_ar": "القضايا الجزائية والدفاع في القضايا الجنائية",
          "title_en": "Criminal Cases & Defense",
          "description_ar": "القضايا الجنائية وتقديم الدفاع القانوني.",
          "description_en": "Criminal cases and providing legal defense.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 611,
          "title_ar": "تقديم الشكاوى ومتابعة الإجراءات القضائية",
          "title_en": "Filing Complaints & Following Legal Procedures",
          "description_ar": "تقديم الشكاوى ومتابعة جميع الإجراءات القانونية.",
          "description_en": "Filing complaints and tracking all legal procedures.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 612,
          "title_ar": "قانون الأسرة (الطلاق، النفقة، الحضانة)",
          "title_en": "Family Law (Divorce, Alimony, Custody)",
          "description_ar": "قضايا الأسرة كَ الطلاق، النفقة، الحضانة، وغيرها.",
          "description_en": "Family law matters like divorce, alimony, custody, etc.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        },
        {
          "id": 613,
          "title_ar": "تسويات ودية واستشارات أسرية",
          "title_en": "Amicable Settlements & Family Consultations",
          "description_ar": "تسوية النزاعات العائلية ودعم الاستشارات الأسرية.",
          "description_en": "Resolving family disputes amicably and providing consultations.",
          "icon": "https://www.svgrepo.com/svg/505182/legal-service",
          "is_vib": false
        }
      ]
    }
  ]
}

        
    )




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


