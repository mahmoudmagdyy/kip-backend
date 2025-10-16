# Sub-Service Creation API Guide

## Overview
This guide explains how to create sub-services from the dashboard using the API endpoint with image upload functionality.

## API Endpoint
- **URL**: `/api/dashboard/sub-services/create/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Not required (AllowAny permission)

## Required Fields

### Form Data Fields
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
  "message": "Sub-service created successfully",
  "data": {
    "id": 1,
    "service": 1,
    "title_ar": "خدمة فرعية للتصميم",
    "title_en": "Design Sub-Service",
    "description_ar": "وصف الخدمة الفرعية بالعربية",
    "description_en": "Sub-service description in English",
    "icon": "http://your-domain.com/media/subservice_1234567890_abc12345.jpg",
    "is_vib": false,
    "is_active": true,
    "order": 0
  }
}
```

### Error Response (400 Bad Request)
```json
{
  "success": false,
  "message": "Invalid data",
  "errors": {
    "service": ["This field is required."],
    "title_ar": ["This field is required."],
    "title_en": ["This field is required."]
  }
}
```

### Error Response (500 Internal Server Error)
```json
{
  "success": false,
  "message": "Error creating sub-service: [error details]"
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

1. **Service Selection**: Must provide a valid parent service ID
2. **Image Selection**: Use `image_picker` package to select images from gallery
3. **Multipart Request**: Use `http.MultipartRequest` for file upload
4. **Form Validation**: Validate all required fields before submission
5. **Error Handling**: Handle network errors and API response errors
6. **Loading States**: Show loading indicators during API calls

### Example Usage

```dart
// Create sub-service with image
Future<void> createSubService() async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('http://your-api.com/api/dashboard/sub-services/create/')
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

### Using cURL
```bash
curl -X POST http://your-api.com/api/dashboard/sub-services/create/ \
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

### Using Postman
1. Set method to `POST`
2. Set URL to your API endpoint
3. Go to Body tab
4. Select `form-data`
5. Add all required fields as key-value pairs
6. For the image field, select `File` type and upload your image

## Key Differences from Service Creation

### Additional Fields
- **`service`**: Required parent service ID
- **`is_vib`**: Boolean field for VIB sub-service status

### Parent Service Requirement
- Sub-services must belong to an existing service
- The `service` field must contain a valid service ID
- Use the services endpoint to get available services first

## Getting Available Services

### Endpoint
- **URL**: `/api/dashboard/services/`
- **Method**: `GET`

### Response
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title_ar": "خدمة التصميم",
      "title_en": "Design Service",
      "description_ar": "وصف الخدمة",
      "description_en": "Service description",
      "icon": "http://domain.com/media/service_icon.jpg",
      "is_active": true,
      "order": 0
    }
  ]
}
```

## Common Issues and Solutions

### 1. Invalid Service ID
- **Issue**: Service field contains invalid or non-existent service ID
- **Solution**: Verify the service ID exists by calling the services endpoint first

### 2. Image Upload Fails
- **Issue**: Image not being sent or processed
- **Solution**: Ensure the field name is exactly `image` and file is properly attached

### 3. Validation Errors
- **Issue**: Required fields missing
- **Solution**: Validate all required fields before sending request

### 4. Network Errors
- **Issue**: Connection timeout or network issues
- **Solution**: Implement proper error handling and retry logic

## Related Endpoints

- `GET /api/dashboard/services/` - List all services (for parent selection)
- `GET /api/dashboard/sub-services/{id}/` - Get specific sub-service
- `PUT /api/dashboard/sub-services/{id}/update/` - Update sub-service
- `DELETE /api/dashboard/sub-services/{id}/delete/` - Delete sub-service
- `GET /api/dashboard/services/{id}/sub-services/` - Get sub-services for a service

## Flutter Example Files

1. **`flutter_subservice_creation_example.dart`** - Full-featured app with service selection
2. **`flutter_subservice_simple_test.dart`** - Simple test version for quick testing

Both examples include:
- Image picker functionality
- Form validation
- Error handling
- Loading states
- Complete API integration
