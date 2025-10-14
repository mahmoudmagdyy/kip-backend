# 🚀 Real-time Booking System - Postman Examples

## **📋 Complete API Testing Guide**

### **🔐 Authentication Endpoints**

#### **1. Admin Login**
```http
POST http://localhost:8000/api/login/
Content-Type: application/json

{
    "username": "9876543210",
    "password": "admin"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 4,
            "username": "9876543210",
            "email": "admin@example.com",
            "is_staff": true,
            "is_superuser": true
        }
    }
}
```

---

### **📊 Admin Dashboard Endpoints**

#### **2. Get All Bookings**
```http
GET http://localhost:8000/api/admin/bookings/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `date` - Filter by date (YYYY-MM-DD)
- `service` - Filter by service name
- `status` - Filter by status (upcoming, completed, cancelled)
- `limit` - Number of results (default: 50)
- `offset` - Pagination offset (default: 0)

**Example with filters:**
```http
GET http://localhost:8000/api/admin/bookings/?status=upcoming&limit=10&offset=0
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### **3. Get Booking Statistics**
```http
GET http://localhost:8000/api/admin/bookings/stats/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
    "success": true,
    "message": "Booking statistics retrieved successfully",
    "stats": {
        "total_bookings": 15,
        "upcoming_bookings": 8,
        "completed_bookings": 5,
        "cancelled_bookings": 2,
        "today_bookings": 3,
        "week_bookings": 12,
        "month_bookings": 15
    }
}
```

#### **4. Get Booking Details**
```http
GET http://localhost:8000/api/admin/bookings/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### **5. Update Booking Status**
```http
PUT http://localhost:8000/api/admin/bookings/1/update/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "status": "completed"
}
```

#### **6. Delete Booking**
```http
DELETE http://localhost:8000/api/admin/bookings/1/delete/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

### **👥 User Management Endpoints**

#### **7. Get All Users**
```http
GET http://localhost:8000/api/admin/users/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `search` - Search by username, first_name, last_name, or email
- `is_active` - Filter by active status (true/false)
- `is_staff` - Filter by staff status (true/false)
- `is_superuser` - Filter by superuser status (true/false)
- `gender` - Filter by gender (male/female)
- `country` - Filter by country
- `date_joined_from` - Users joined from this date (YYYY-MM-DD)
- `date_joined_to` - Users joined until this date (YYYY-MM-DD)
- `sort_by` - Sort field (id, username, first_name, last_name, email, date_joined, last_login, is_active, is_staff, is_superuser)
- `sort_order` - Sort direction (asc/desc)
- `limit` - Number of results (default: 50)
- `offset` - Pagination offset (default: 0)

**Example with filters:**
```http
GET http://localhost:8000/api/admin/users/?gender=male&country=Egypt&is_active=true&sort_by=date_joined&sort_order=desc&limit=10
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### **8. Get User Statistics**
```http
GET http://localhost:8000/api/admin/users/stats/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### **9. Get User Filter Options**
```http
GET http://localhost:8000/api/admin/users/filter-options/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### **10. Get User Details**
```http
GET http://localhost:8000/api/admin/users/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### **11. Create User**
```http
POST http://localhost:8000/api/admin/users/create/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "username": "5555555555",
    "email": "newuser@example.com",
    "password": "password123",
    "first_name": "New",
    "last_name": "User",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "gender": "male",
    "country": "Canada"
}
```

#### **12. Update User**
```http
PUT http://localhost:8000/api/admin/users/1/update/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "first_name": "Updated",
    "last_name": "Name",
    "is_staff": true,
    "gender": "female",
    "country": "USA"
}
```

#### **13. Delete User**
```http
DELETE http://localhost:8000/api/admin/users/1/delete/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

### **📅 Booking Management Endpoints**

#### **14. Get Available Time Slots**
```http
GET http://localhost:8000/api/booking/smart-available-slots/?date=2025-10-15
```

**Query Parameters:**
- `date` - Required: Booking date (YYYY-MM-DD)
- `service` - Optional: Service name filter

**Response:**
```json
{
    "success": true,
    "message": "Available time slots retrieved successfully",
    "date": "2025-10-15",
    "service": "",
    "working_hours": {
        "start": "09:00",
        "end": "17:00"
    },
    "duration_minutes": 60,
    "is_off_day": false,
    "available_slots": [
        {
            "time": "09:00",
            "display_time": "09:00 AM",
            "end_time": "10:00",
            "duration_minutes": 60,
            "available": true,
            "is_reserved": false
        },
        {
            "time": "10:00",
            "display_time": "10:00 AM",
            "end_time": "11:00",
            "duration_minutes": 60,
            "available": true,
            "is_reserved": false
        }
    ],
    "total_available_slots": 8
}
```

#### **15. Create Booking (Real-time)**
```http
POST http://localhost:8000/api/booking/create/
Content-Type: application/json

{
    "user_id": 1,
    "service_name": "Test Service",
    "booking_date": "2025-10-15",
    "booking_time": "10:00",
    "notes": "Test booking from Postman"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Booking created successfully",
    "data": {
        "id": 14,
        "service_name": "Test Service",
        "booking_date": "2025-10-15",
        "booking_time": "10:00",
        "duration_minutes": 60,
        "status": "upcoming",
        "created_at": "2025-10-13T06:15:30.123456+00:00"
    }
}
```

#### **16. Get Booking Calendar**
```http
GET http://localhost:8000/api/booking/calendar/?year=2025&month=10
```

**Query Parameters:**
- `year` - Required: Year (e.g., 2025)
- `month` - Required: Month (1-12)

#### **17. Get Booking Settings**
```http
GET http://localhost:8000/api/booking/settings/
```

#### **18. Update Booking Settings**
```http
POST http://localhost:8000/api/booking/settings/
Content-Type: application/json

{
    "WORKING_HOURS_START": 9,
    "WORKING_HOURS_END": 17,
    "DEFAULT_RESERVATION_DURATION_MINUTES": 60,
    "OFF_DAYS": "5,6",
    "is_active": true
}
```

---

### **🌐 Public Endpoints**

#### **19. Get Services**
```http
GET http://localhost:8000/api/services/
```

#### **20. Get Countries**
```http
GET http://localhost:8000/api/countries/
```

#### **21. Get Reserved Slots**
```http
GET http://localhost:8000/api/reservations/reserved_slots/
```

**Query Parameters:**
- `date` - Filter by date (YYYY-MM-DD)
- `service` - Filter by service name
- `status` - Filter by status (upcoming, completed, cancelled)

---

### **🔌 WebSocket Testing**

#### **22. WebSocket Connection**
**URL:** `ws://localhost:8000/ws/admin/bookings/`

**Connection Test (JavaScript):**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/admin/bookings/');

ws.onopen = function(event) {
    console.log('WebSocket connected');
    // Request current bookings
    ws.send(JSON.stringify({
        type: 'get_bookings'
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    switch(data.type) {
        case 'booking_created':
            console.log('New booking:', data.data);
            break;
        case 'booking_updated':
            console.log('Booking updated:', data.data);
            break;
        case 'booking_deleted':
            console.log('Booking deleted:', data.data);
            break;
        case 'bookings_data':
            console.log('Bookings data:', data.data);
            break;
    }
};

ws.onclose = function(event) {
    console.log('WebSocket disconnected');
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

---

### **🧪 Testing Real-time Features**

#### **Step 1: Open WebSocket Connection**
1. Use the JavaScript code above in browser console
2. Or use a WebSocket testing tool like Postman WebSocket

#### **Step 2: Create a Booking**
1. Use endpoint #15 to create a booking
2. Watch the WebSocket connection receive the real-time notification
3. The admin dashboard should update instantly

#### **Step 3: Test Multiple Connections**
1. Open multiple WebSocket connections
2. Create a booking from one connection
3. All other connections should receive the notification

---

### **📱 Frontend Integration Examples**

#### **JavaScript WebSocket Client:**
```javascript
class BookingWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 3000;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/admin/bookings/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (event) => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.requestBookings();
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = (event) => {
            console.log('WebSocket disconnected');
            this.handleReconnect();
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    handleMessage(data) {
        switch (data.type) {
            case 'booking_created':
                this.onBookingCreated(data.data);
                break;
            case 'booking_updated':
                this.onBookingUpdated(data.data);
                break;
            case 'booking_deleted':
                this.onBookingDeleted(data.data);
                break;
            case 'bookings_data':
                this.onBookingsData(data.data);
                break;
        }
    }

    onBookingCreated(bookingData) {
        console.log('New booking created:', bookingData);
        // Update UI here
        this.showNotification('New Booking!', 
            `${bookingData.user_details.first_name} ${bookingData.user_details.last_name} booked ${bookingData.service_name}`);
    }

    onBookingUpdated(bookingData) {
        console.log('Booking updated:', bookingData);
        // Update UI here
    }

    onBookingDeleted(bookingData) {
        console.log('Booking deleted:', bookingData);
        // Update UI here
    }

    onBookingsData(bookingsData) {
        console.log('Bookings data received:', bookingsData);
        // Update UI here
    }

    requestBookings() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                type: 'get_bookings'
            }));
        }
    }

    showNotification(title, message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.innerHTML = `
            <div class="notification-content">
                <h4>${title}</h4>
                <p>${message}</p>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Usage
const bookingWebSocket = new BookingWebSocket();
bookingWebSocket.connect();
```

---

### **🎯 Complete Testing Workflow**

#### **1. Authentication Test:**
```bash
# Login and get token
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "9876543210", "password": "admin"}'
```

#### **2. Get Bookings Test:**
```bash
# Get all bookings
curl -X GET http://localhost:8000/api/admin/bookings/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **3. Create Booking Test:**
```bash
# Create a booking (this will trigger WebSocket notification)
curl -X POST http://localhost:8000/api/booking/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "service_name": "Test Service",
    "booking_date": "2025-10-15",
    "booking_time": "12:00",
    "notes": "Test booking"
  }'
```

#### **4. WebSocket Test:**
```bash
# Test WebSocket connection
wscat -c ws://localhost:8000/ws/admin/bookings/
```

**Your real-time booking system is ready for testing with these comprehensive Postman examples! 🚀**
