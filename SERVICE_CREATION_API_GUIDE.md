# Service Creation API Guide

## Overview
This guide explains how to create services from the dashboard using the API endpoint with image upload functionality.

## API Endpoint
- **URL**: `/api/dashboard/services/create/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Not required (AllowAny permission)

## Required Fields

### Form Data Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title_ar` | String | Yes | Service title in Arabic |
| `title_en` | String | Yes | Service title in English |
| `description_ar` | String | Yes | Service description in Arabic |
| `description_en` | String | Yes | Service description in English |
| `image` | File | Yes | Service icon/image file |
| `is_active` | Boolean | No | Service active status (default: true) |
| `order` | Integer | No | Display order (default: 0) |

### File Requirements
- **Field Name**: `image`
- **Accepted Formats**: JPG, PNG, GIF, etc.
- **Max Size**: Recommended 1MB or less
- **Dimensions**: Recommended 512x512 or similar square format

## API Response

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
    "icon": "http://your-domain.com/media/service_1234567890_abc12345.jpg",
    "is_active": true,
    "order": 0,
    "sub_services": []
  }
}
```

### Error Response (400 Bad Request)
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

### Error Response (500 Internal Server Error)
```json
{
  "success": false,
  "message": "Error creating service: [error details]"
}
```

## Flutter Implementation

### Required Dependencies
Add these to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  image_picker: ^1.0.4
  path: ^1.8.3
```

### Key Implementation Points

1. **Image Selection**: Use `image_picker` package to select images from gallery
2. **Multipart Request**: Use `http.MultipartRequest` for file upload
3. **Form Validation**: Validate all required fields before submission
4. **Error Handling**: Handle network errors and API response errors
5. **Loading States**: Show loading indicators during API calls

### Example Usage

```dart
// Create service with image
Future<void> createService() async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('http://your-api.com/api/dashboard/services/create/')
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

## Testing the API

### Using cURL
```bash
curl -X POST http://your-api.com/api/dashboard/services/create/ \
  -F "title_ar=خدمة التصميم" \
  -F "title_en=Design Service" \
  -F "description_ar=وصف الخدمة بالعربية" \
  -F "description_en=Service description in English" \
  -F "is_active=true" \
  -F "order=0" \
  -F "image=@/path/to/your/image.jpg"
```

### Using Postman
1. Set method to `POST`
2. Set URL to your API endpoint
3. Go to Body tab
4. Select `form-data`
5. Add all required fields as key-value pairs
6. For the image field, select `File` type and upload your image

## Common Issues and Solutions

### 1. Image Upload Fails
- **Issue**: Image not being sent or processed
- **Solution**: Ensure the field name is exactly `image` and file is properly attached

### 2. Validation Errors
- **Issue**: Required fields missing
- **Solution**: Validate all required fields before sending request

### 3. Network Errors
- **Issue**: Connection timeout or network issues
- **Solution**: Implement proper error handling and retry logic

### 4. File Size Issues
- **Issue**: Image too large
- **Solution**: Compress image before upload or implement file size validation

## Security Considerations

1. **File Validation**: The API should validate file types and sizes
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Authentication**: Consider adding authentication for production use
4. **CORS**: Ensure proper CORS configuration for web clients

## Related Endpoints

- `GET /api/dashboard/services/` - List all services
- `GET /api/dashboard/services/{id}/` - Get specific service
- `PUT /api/dashboard/services/{id}/update/` - Update service
- `DELETE /api/dashboard/services/{id}/delete/` - Delete service
