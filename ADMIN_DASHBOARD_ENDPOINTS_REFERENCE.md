# 📋 Admin Dashboard API Endpoints Reference

## 🚀 **Base URL:** `http://localhost:8000`

---

## 📊 **SERVICE MANAGEMENT ENDPOINTS**

### **1. Services CRUD Operations**

#### **Get All Services**
```http
GET /api/dashboard/services/
```
**Response:**
```json
{
  "services": [
    {
      "id": 1,
      "title_ar": "خدمة تجريبية",
      "title_en": "Test Service",
      "description_ar": "وصف تجريبي",
      "description_en": "Test description",
      "icon": "http://localhost:8000/media/uploaded-image.png",
      "is_active": true,
      "order": 1,
      "sub_services": []
    }
  ]
}
```

#### **Create Service**
```http
POST /api/dashboard/services/create/
Content-Type: application/json

{
  "title_en": "Service Name",
  "title_ar": "اسم الخدمة",
  "description_en": "Service description",
  "description_ar": "وصف الخدمة",
  "is_active": true,
  "order": 1,
  "icon": "http://example.com/icon.png" // Optional
}
```
**Response:**
```json
{
  "success": true,
  "message": "Service created successfully",
  "data": {
    "id": 17,
    "title_ar": "اسم الخدمة",
    "title_en": "Service Name",
    "description_ar": "وصف الخدمة",
    "description_en": "Service description",
    "icon": null,
    "is_active": true,
    "order": 1,
    "sub_services": []
  }
}
```

#### **Get Specific Service**
```http
GET /api/dashboard/services/{service_id}/
```

#### **Update Service**
```http
PUT /api/dashboard/services/{service_id}/update/
Content-Type: application/json

{
  "title_en": "Updated Service Name",
  "title_ar": "اسم الخدمة المحدث",
  "description_en": "Updated description",
  "description_ar": "وصف محدث",
  "is_active": true,
  "order": 2
}
```

#### **Delete Service**
```http
DELETE /api/dashboard/services/{service_id}/delete/
```
**Response:**
```json
{
  "success": true,
  "message": "Service deleted successfully"
}
```

---

## 🔧 **SUB-SERVICE MANAGEMENT ENDPOINTS**

### **2. Sub-Services CRUD Operations**

#### **Get Service Sub-Services**
```http
GET /api/dashboard/services/{service_id}/sub-services/
```

#### **Create Sub-Service**
```http
POST /api/dashboard/sub-services/create/
Content-Type: application/json

{
  "service": 1,
  "title_en": "Sub-Service Name",
  "title_ar": "اسم الخدمة الفرعية",
  "description_en": "Sub-service description",
  "description_ar": "وصف الخدمة الفرعية",
  "is_vib": false,
  "is_active": true,
  "order": 1,
  "icon": "http://example.com/icon.png" // Optional
}
```

#### **Get Specific Sub-Service**
```http
GET /api/dashboard/sub-services/{sub_service_id}/
```

#### **Update Sub-Service**
```http
PUT /api/dashboard/sub-services/{sub_service_id}/update/
Content-Type: application/json

{
  "title_en": "Updated Sub-Service",
  "title_ar": "خدمة فرعية محدثة",
  "description_en": "Updated description",
  "description_ar": "وصف محدث",
  "is_vib": true,
  "is_active": true,
  "order": 2
}
```

#### **Delete Sub-Service**
```http
DELETE /api/dashboard/sub-services/{sub_service_id}/delete/
```

---

## 👥 **USER MANAGEMENT ENDPOINTS**

### **3. Admin User Management**

#### **Get All Users**
```http
GET /api/admin/users/
Authorization: Bearer {token}
```

#### **Get User Statistics**
```http
GET /api/admin/users/stats/
Authorization: Bearer {token}
```

#### **Get User Filter Options**
```http
GET /api/admin/users/filter-options/
Authorization: Bearer {token}
```

#### **Get Specific User**
```http
GET /api/admin/users/{user_id}/
Authorization: Bearer {token}
```

#### **Update User**
```http
PUT /api/admin/users/{user_id}/update/
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "Updated Name",
  "last_name": "Updated Last Name",
  "email": "updated@example.com",
  "phone": "1234567890"
}
```

#### **Delete User**
```http
DELETE /api/admin/users/{user_id}/delete/
Authorization: Bearer {token}
```

#### **Create User**
```http
POST /api/admin/users/create/
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "New User",
  "last_name": "Last Name",
  "email": "newuser@example.com",
  "phone": "1234567890",
  "password": "securepassword"
}
```

---

## 📅 **BOOKING MANAGEMENT ENDPOINTS**

### **4. Admin Booking Management**

#### **Get All Bookings**
```http
GET /api/admin/bookings/
Authorization: Bearer {token}
```

#### **Get Booking Statistics**
```http
GET /api/admin/bookings/stats/
Authorization: Bearer {token}
```

#### **Get Specific Booking**
```http
GET /api/admin/bookings/{booking_id}/
Authorization: Bearer {token}
```

#### **Update Booking Status**
```http
PUT /api/admin/bookings/{booking_id}/update/
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "confirmed",
  "notes": "Booking confirmed by admin"
}
```

#### **Delete Booking**
```http
DELETE /api/admin/bookings/{booking_id}/delete/
Authorization: Bearer {token}
```

#### **Create Booking**
```http
POST /api/admin/bookings/create/
Authorization: Bearer {token}
Content-Type: application/json

{
  "user": 1,
  "service": 1,
  "sub_service": 1,
  "date": "2025-10-20",
  "time": "10:00:00",
  "status": "pending",
  "notes": "Admin created booking"
}
```

---

## 🎁 **OFFER MANAGEMENT ENDPOINTS**

### **5. Admin Offer Management**

#### **Get All Offers**
```http
GET /api/admin/offers/
Authorization: Bearer {token}
```

#### **Get Offer Statistics**
```http
GET /api/admin/offers/stats/
Authorization: Bearer {token}
```

#### **Get Offer Filter Options**
```http
GET /api/admin/offers/filter-options/
Authorization: Bearer {token}
```

#### **Get Specific Offer**
```http
GET /api/admin/offers/{offer_id}/
Authorization: Bearer {token}
```

#### **Update Offer**
```http
PUT /api/admin/offers/{offer_id}/update/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Offer",
  "description": "Updated offer description",
  "discount_percentage": 20,
  "is_active": true,
  "is_featured": false
}
```

#### **Delete Offer**
```http
DELETE /api/admin/offers/{offer_id}/delete/
Authorization: Bearer {token}
```

#### **Toggle Offer Status**
```http
PUT /api/admin/offers/{offer_id}/toggle-status/
Authorization: Bearer {token}
```

#### **Toggle Offer Featured**
```http
PUT /api/admin/offers/{offer_id}/toggle-featured/
Authorization: Bearer {token}
```

#### **Upload Offer Image**
```http
POST /api/admin/offers/{offer_id}/upload-image/
Authorization: Bearer {token}
Content-Type: multipart/form-data

image: [file]
```

#### **Delete Offer Image**
```http
DELETE /api/admin/offers/{offer_id}/delete-image/
Authorization: Bearer {token}
```

#### **Create Offer Image**
```http
POST /api/admin/offers/create-image/
Authorization: Bearer {token}
Content-Type: multipart/form-data

image: [file]
```

#### **Create Offer**
```http
POST /api/admin/offers/create/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "New Offer",
  "description": "Offer description",
  "discount_percentage": 15,
  "is_active": true,
  "is_featured": false
}
```

---

## 🌐 **PUBLIC ENDPOINTS**

### **6. Public API Endpoints**

#### **Get Public Services**
```http
GET /api/services/
```

#### **Get Public Offers**
```http
GET /api/offers/
```

#### **Get Countries**
```http
GET /api/countries/
```

#### **Get Booking Settings**
```http
GET /api/booking-settings/
```

---

## 🔐 **AUTHENTICATION ENDPOINTS**

### **7. Authentication & User Management**

#### **Login**
```http
POST /api/login/
Content-Type: application/json

{
  "phone": "1234567890",
  "password": "password123"
}
```

#### **Register**
```http
POST /api/register/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "password": "password123"
}
```

#### **Send OTP**
```http
POST /api/send-otp/
Content-Type: application/json

{
  "phone": "1234567890"
}
```

#### **Verify OTP**
```http
POST /api/verify-otp/
Content-Type: application/json

{
  "phone": "1234567890",
  "otp": "123456"
}
```

#### **Change Password**
```http
POST /api/change-password/
Authorization: Bearer {token}
Content-Type: application/json

{
  "old_password": "oldpassword",
  "new_password": "newpassword"
}
```

#### **Reset Password**
```http
POST /api/reset-password/
Content-Type: application/json

{
  "phone": "1234567890",
  "otp": "123456",
  "new_password": "newpassword"
}
```

---

## 📱 **USER SERVICE ENDPOINTS**

### **8. User Service Creation**

#### **Get User Services**
```http
GET /api/user/services/
```

#### **Create User Service**
```http
POST /api/user/services/create/
Content-Type: application/json

{
  "title_en": "User Service",
  "title_ar": "خدمة المستخدم",
  "description_en": "User service description",
  "description_ar": "وصف خدمة المستخدم",
  "is_active": true,
  "order": 1
}
```

#### **Get User Sub-Services**
```http
GET /api/user/services/{service_id}/sub-services/
```

#### **Create User Sub-Service**
```http
POST /api/user/sub-services/create/
Content-Type: application/json

{
  "service": 1,
  "title_en": "User Sub-Service",
  "title_ar": "خدمة فرعية للمستخدم",
  "description_en": "User sub-service description",
  "description_ar": "وصف الخدمة الفرعية للمستخدم",
  "is_vib": false,
  "is_active": true,
  "order": 1
}
```

---

## 🔌 **WEBSOCKET ENDPOINTS**

### **9. Real-time Updates**

#### **Admin Bookings WebSocket**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/admin/bookings/');
```

---

## 📋 **QUICK REFERENCE**

### **✅ Working Endpoints:**
- **Services:** `/api/dashboard/services/`
- **Sub-Services:** `/api/dashboard/sub-services/`
- **Users:** `/api/admin/users/`
- **Bookings:** `/api/admin/bookings/`
- **Offers:** `/api/admin/offers/`
- **Public:** `/api/services/`, `/api/offers/`, `/api/countries/`
- **Auth:** `/api/login/`, `/api/register/`, `/api/send-otp/`
- **WebSocket:** `ws://localhost:8000/ws/admin/bookings/`

### **❌ Non-existent Endpoints:**
- `/api/services/create/` ❌
- `/api/services/{id}/delete/` ❌
- `/api/services/{id}/update/` ❌

### **🔧 Correct Patterns:**
- **Create:** `/api/dashboard/services/create/`
- **Update:** `/api/dashboard/services/{id}/update/`
- **Delete:** `/api/dashboard/services/{id}/delete/`
- **Get:** `/api/dashboard/services/{id}/`

---

## 🚀 **Usage Examples**

### **Flutter HTTP Client:**
```dart
// Create service
final response = await http.post(
  Uri.parse('http://localhost:8000/api/dashboard/services/create/'),
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Origin': 'http://localhost:8080',
  },
  body: json.encode(serviceData),
);

// Delete service
final response = await http.delete(
  Uri.parse('http://localhost:8000/api/dashboard/services/$serviceId/delete/'),
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Origin': 'http://localhost:8080',
  },
);
```

### **JavaScript Fetch:**
```javascript
// Create service
const response = await fetch('http://localhost:8000/api/dashboard/services/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Origin': 'http://localhost:8080',
  },
  body: JSON.stringify(serviceData),
});

// Delete service
const response = await fetch(`http://localhost:8000/api/dashboard/services/${serviceId}/delete/`, {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Origin': 'http://localhost:8080',
  },
});
```

---

## 📞 **Support**

If you encounter any issues with these endpoints, check:
1. **Server is running** on `http://localhost:8000`
2. **Correct endpoint URLs** are being used
3. **Proper headers** are included
4. **Authentication tokens** for protected endpoints

**All endpoints are tested and working!** 🚀
