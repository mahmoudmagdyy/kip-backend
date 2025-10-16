# Sub-Service Creation Debug Guide

## Issue Fixed
The problem was that sub-services were being created but not properly retrieved due to missing context parameters in serializers.

## Changes Made

### 1. Fixed ServiceSerializer
- **Before**: Had duplicate ServiceSerializer classes causing conflicts
- **After**: Single ServiceSerializer with proper icon handling and sub_services field

### 2. Added Context Parameters
- **Fixed**: `get_service_sub_services()` - Added `context={'request': request}`
- **Fixed**: `dashboard_services()` - Added `context={'request': request}`
- **Fixed**: `get_service()` - Added `context={'request': request}`

### 3. Enhanced ServiceSerializer
```python
class ServiceSerializer(serializers.ModelSerializer):
    sub_services = SubServiceSerializer(many=True, read_only=True)
    icon = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'title_ar', 'title_en', 'description_ar', 'description_en', 'icon', 'is_active', 'order', 'sub_services']
    
    def get_icon(self, obj):
        request = self.context.get('request')
        if obj.icon:
            if obj.icon.startswith('http'):
                return obj.icon
            return f"http://{request.get_host()}{obj.icon}"
        return None
```

## Testing Steps

### 1. Test Sub-Service Creation
```bash
curl -X POST http://your-api.com/api/dashboard/sub-services/create/ \
  -F "service=1" \
  -F "title_ar=خدمة فرعية للاختبار" \
  -F "title_en=Test Sub-Service" \
  -F "description_ar=وصف الخدمة الفرعية" \
  -F "description_en=Test sub-service description" \
  -F "is_active=true" \
  -F "is_vib=false" \
  -F "order=0" \
  -F "image=@/path/to/test_image.jpg"
```

**Expected Response (201 Created):**
```json
{
  "success": true,
  "message": "Sub-service created successfully",
  "data": {
    "id": 1,
    "service": 1,
    "title_ar": "خدمة فرعية للاختبار",
    "title_en": "Test Sub-Service",
    "description_ar": "وصف الخدمة الفرعية",
    "description_en": "Test sub-service description",
    "icon": "http://your-domain.com/media/subservice_1234567890_abc12345.jpg",
    "is_vib": false,
    "is_active": true,
    "order": 0
  }
}
```

### 2. Test Getting Sub-Services for a Service
```bash
curl -X GET http://your-api.com/api/dashboard/services/1/sub-services/
```

**Expected Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title_ar": "خدمة فرعية للاختبار",
      "title_en": "Test Sub-Service",
      "description_ar": "وصف الخدمة الفرعية",
      "description_en": "Test sub-service description",
      "icon": "http://your-domain.com/media/subservice_1234567890_abc12345.jpg",
      "is_vib": false,
      "is_active": true,
      "order": 0
    }
  ]
}
```

### 3. Test Getting Service with Sub-Services
```bash
curl -X GET http://your-api.com/api/dashboard/services/1/
```

**Expected Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title_ar": "خدمة التصميم",
    "title_en": "Design Service",
    "description_ar": "وصف الخدمة",
    "description_en": "Service description",
    "icon": "http://your-domain.com/media/service_1234567890_abc12345.jpg",
    "is_active": true,
    "order": 0,
    "sub_services": [
      {
        "id": 1,
        "title_ar": "خدمة فرعية للاختبار",
        "title_en": "Test Sub-Service",
        "description_ar": "وصف الخدمة الفرعية",
        "description_en": "Test sub-service description",
        "icon": "http://your-domain.com/media/subservice_1234567890_abc12345.jpg",
        "is_vib": false,
        "is_active": true,
        "order": 0
      }
    ]
  }
}
```

## Flutter Testing

### Test Sub-Service Creation
```dart
Future<void> testSubServiceCreation() async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('http://your-api.com/api/dashboard/sub-services/create/')
  );
  
  // Add form fields
  request.fields['service'] = '1'; // Replace with actual service ID
  request.fields['title_ar'] = 'خدمة فرعية للاختبار';
  request.fields['title_en'] = 'Test Sub-Service';
  request.fields['description_ar'] = 'وصف الخدمة الفرعية';
  request.fields['description_en'] = 'Test sub-service description';
  request.fields['is_active'] = 'true';
  request.fields['is_vib'] = 'false';
  request.fields['order'] = '0';
  
  // Add image file
  request.files.add(
    await http.MultipartFile.fromPath('image', imageFile.path)
  );
  
  // Send request
  var response = await request.send();
  var responseData = await http.Response.fromStream(response);
  
  print('Status: ${response.statusCode}');
  print('Response: ${responseData.body}');
  
  if (response.statusCode == 201) {
    print('✅ Sub-service created successfully!');
  } else {
    print('❌ Failed to create sub-service');
  }
}
```

### Test Getting Sub-Services
```dart
Future<void> testGetSubServices() async {
  try {
    final response = await http.get(
      Uri.parse('http://your-api.com/api/dashboard/services/1/sub-services/')
    );
    
    print('Status: ${response.statusCode}');
    print('Response: ${response.body}');
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['success'] == true) {
        final subServices = data['data'];
        print('✅ Found ${subServices.length} sub-services');
        for (var subService in subServices) {
          print('  - ${subService['title_en']} (ID: ${subService['id']})');
        }
      }
    }
  } catch (e) {
    print('❌ Error: $e');
  }
}
```

## Common Issues and Solutions

### Issue 1: Sub-services not showing in service response
**Cause**: Missing context parameter in ServiceSerializer
**Solution**: Ensure all endpoints pass `context={'request': request}` to serializers

### Issue 2: Icon URLs not working
**Cause**: Missing context parameter in SubServiceSerializer
**Solution**: Added `context={'request': request}` to all serializer calls

### Issue 3: Duplicate ServiceSerializer classes
**Cause**: Multiple ServiceSerializer definitions
**Solution**: Removed duplicate and kept the one with sub_services field

## Verification Checklist

- [ ] Sub-service creation returns 201 status
- [ ] Sub-service creation returns success: true
- [ ] Sub-service has valid ID in response
- [ ] Getting sub-services for service returns the created sub-service
- [ ] Getting service includes sub_services array with the created sub-service
- [ ] Icon URLs are properly formatted with full domain
- [ ] All serializers receive context parameter

## Debug Commands

### Check Database Directly
```python
# In Django shell
from core.models import Service, SubService

# Check if sub-service exists
sub_services = SubService.objects.all()
print(f"Total sub-services: {sub_services.count()}")

# Check sub-services for a specific service
service = Service.objects.get(id=1)
sub_services = service.sub_services.all()
print(f"Sub-services for service {service.title_en}: {sub_services.count()}")
for sub in sub_services:
    print(f"  - {sub.title_en} (ID: {sub.id})")
```

### Check API Responses
```bash
# Test all endpoints
curl -X GET http://your-api.com/api/dashboard/services/
curl -X GET http://your-api.com/api/dashboard/services/1/
curl -X GET http://your-api.com/api/dashboard/services/1/sub-services/
```

The issue should now be resolved! Sub-services will be properly stored and retrieved when you get the service again.
