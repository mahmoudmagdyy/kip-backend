# User Service Creation API Guide

## Overview
This guide explains how users can create services and sub-services using the public API endpoints with image upload functionality.

## API Endpoints

### Service Creation
- **URL**: `/api/user/services/create/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Not required (AllowAny permission)

### Sub-Service Creation
- **URL**: `/api/user/sub-services/create/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Not required (AllowAny permission)

### Get Services
- **URL**: `/api/user/services/`
- **Method**: `GET`
- **Authentication**: Not required

### Get Sub-Services
- **URL**: `/api/user/services/{service_id}/sub-services/`
- **Method**: `GET`
- **Authentication**: Not required

## Service Creation

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title_ar` | String | Yes | Service title in Arabic |
| `title_en` | String | Yes | Service title in English |
| `description_ar` | String | Yes | Service description in Arabic |
| `description_en` | String | Yes | Service description in English |
| `image` | File | Yes | Service icon/image file |
| `is_active` | Boolean | No | Service active status (default: true) |
| `order` | Integer | No | Display order (default: 0) |

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Service created successfully",
  "data": {
    "id": 1,
    "title_ar": "خدمة التصميم",
    "title_en": "Design Service",
    "description_ar": "وصف الخدمة بالعربية",
    "description_en": "Service description in English",
    "icon": "http://your-domain.com/media/user_service_1234567890_abc12345.jpg",
    "is_active": true,
    "order": 0,
    "sub_services": []
  }
}
```

## Sub-Service Creation

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `service` | Integer | Yes | Parent service ID |
| `title_ar` | String | Yes | Sub-service title in Arabic |
| `title_en` | String | Yes | Sub-service title in English |
| `description_ar` | String | Yes | Sub-service description in Arabic |
| `description_en` | String | Yes | Sub-service description in English |
| `image` | File | Yes | Sub-service icon/image file |
| `is_active` | Boolean | No | Sub-service active status (default: true) |
| `is_vib` | Boolean | No | VIB sub-service status (default: false) |
| `order` | Integer | No | Display order (default: 0) |

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Sub-service created successfully",
  "data": {
    "id": 1,
    "service": 1,
    "title_ar": "خدمة فرعية للتصميم",
    "title_en": "Design Sub-Service",
    "description_ar": "وصف الخدمة الفرعية بالعربية",
    "description_en": "Sub-service description in English",
    "icon": "http://your-domain.com/media/user_subservice_1234567890_abc12345.jpg",
    "is_vib": false,
    "is_active": true,
    "order": 0
  }
}
```

## Flutter Implementation

### Required Dependencies
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  image_picker: ^1.0.4
  path: ^1.8.3
```

### Service Creation Example
```dart
Future<void> createService() async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('http://your-api.com/api/user/services/create/')
  );
  
  // Add form fields
  request.fields['title_ar'] = 'خدمة التصميم';
  request.fields['title_en'] = 'Design Service';
  request.fields['description_ar'] = 'وصف الخدمة';
  request.fields['description_en'] = 'Service description';
  request.fields['is_active'] = 'true';
  request.fields['order'] = '0';
  
  // Add image file
  request.files.add(
    await http.MultipartFile.fromPath('image', imageFile.path)
  );
  
  // Send request
  var response = await request.send();
  var responseData = await http.Response.fromStream(response);
  
  if (response.statusCode == 201) {
    print('Service created successfully!');
  } else {
    print('Error: ${responseData.body}');
  }
}
```

### Sub-Service Creation Example
```dart
Future<void> createSubService() async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('http://your-api.com/api/user/sub-services/create/')
  );
  
  // Add form fields
  request.fields['service'] = '1'; // Parent service ID
  request.fields['title_ar'] = 'خدمة فرعية للتصميم';
  request.fields['title_en'] = 'Design Sub-Service';
  request.fields['description_ar'] = 'وصف الخدمة الفرعية';
  request.fields['description_en'] = 'Sub-service description';
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
  
  if (response.statusCode == 201) {
    print('Sub-service created successfully!');
  } else {
    print('Error: ${responseData.body}');
  }
}
```

## Testing the API

### Service Creation (cURL)
```bash
curl -X POST http://your-api.com/api/user/services/create/ \
  -F "title_ar=خدمة التصميم" \
  -F "title_en=Design Service" \
  -F "description_ar=وصف الخدمة بالعربية" \
  -F "description_en=Service description in English" \
  -F "is_active=true" \
  -F "order=0" \
  -F "image=@/path/to/your/image.jpg"
```

### Sub-Service Creation (cURL)
```bash
curl -X POST http://your-api.com/api/user/sub-services/create/ \
  -F "service=1" \
  -F "title_ar=خدمة فرعية للتصميم" \
  -F "title_en=Design Sub-Service" \
  -F "description_ar=وصف الخدمة الفرعية بالعربية" \
  -F "description_en=Sub-service description in English" \
  -F "is_active=true" \
  -F "is_vib=false" \
  -F "order=0" \
  -F "image=@/path/to/your/image.jpg"
```

## Key Differences from Dashboard Endpoints

### User Endpoints vs Dashboard Endpoints

| Feature | User Endpoints | Dashboard Endpoints |
|---------|----------------|-------------------|
| URL Prefix | `/api/user/` | `/api/dashboard/` |
| Authentication | Not required | Not required |
| File Prefix | `user_service_` / `user_subservice_` | `service_` / `subservice_` |
| Functionality | Same | Same |
| Response Format | Same | Same |

### File Naming Convention
- **User Services**: `user_service_{timestamp}_{uuid}.{ext}`
- **User Sub-Services**: `user_subservice_{timestamp}_{uuid}.{ext}`
- **Dashboard Services**: `service_{timestamp}_{uuid}.{ext}`
- **Dashboard Sub-Services**: `subservice_{timestamp}_{uuid}.{ext}`

## Error Handling

### Common Error Responses

#### Validation Error (400 Bad Request)
```json
{
  "success": false,
  "message": "Invalid data",
  "errors": {
    "title_ar": ["This field is required."],
    "title_en": ["This field is required."]
  }
}
```

#### Server Error (500 Internal Server Error)
```json
{
  "success": false,
  "message": "Error creating service: [error details]"
}
```

## Flutter Example Files

1. **`flutter_user_service_creation_example.dart`** - Full-featured user service creation
2. **`flutter_user_subservice_creation_example.dart`** - Full-featured user sub-service creation

Both examples include:
- Image picker functionality
- Form validation
- Error handling
- Loading states
- Complete API integration

## Related Endpoints

- `GET /api/user/services/` - List all services
- `GET /api/user/services/{id}/sub-services/` - Get sub-services for a service
- `POST /api/user/services/create/` - Create service
- `POST /api/user/sub-services/create/` - Create sub-service

## Security Considerations

1. **Public Access**: These endpoints are publicly accessible (no authentication required)
2. **File Validation**: The API validates file types and sizes
3. **Rate Limiting**: Consider implementing rate limiting for production use
4. **CORS**: Ensure proper CORS configuration for web clients
