# Agent Booking Endpoint Documentation

## 📋 **Overview**
The Agent Booking Endpoint is a **public endpoint** that allows agents to create bookings for users. It automatically creates users if they don't exist and creates bookings with real-time WebSocket notifications.

## 🔗 **Endpoint**
```
POST /api/agent/booking/create/
```

## 🔓 **Authentication**
- **No authentication required** (public endpoint)
- Perfect for agent systems and external integrations

## 📝 **Request Format**

### **Required Fields:**
- `phone` - User's phone number (used as username)
- `service_name` - Name of the service
- `booking_date` - Booking date (multiple formats supported)
- `booking_time` - Booking time (multiple formats supported)

### **Optional Fields:**
- `first_name` - User's first name
- `last_name` - User's last name
- `email` - User's email address
- `gender` - User's gender
- `country` - User's country
- `notes` - Booking notes
- `status` - Booking status (default: 'upcoming')

## 📅 **Date & Time Formats**

### **Supported Date Formats:**
- `YYYY-MM-DD` (e.g., "2025-10-20")
- `DD/MM/YYYY` (e.g., "20/10/2025")
- `MM/DD/YYYY` (e.g., "10/20/2025")
- `DD-MM-YYYY` (e.g., "20-10-2025")
- `MM-DD-YYYY` (e.g., "10-20-2025")

### **Supported Time Formats:**
- `HH:MM` (e.g., "14:00")
- `HH:MM AM/PM` (e.g., "2:00 PM")
- `HH:MMAM/PM` (e.g., "2:00PM")
- `HH:MM:SS` (e.g., "14:00:00")

## 🚀 **Example Requests**

### **Basic Request:**
```json
{
  "phone": "1234567890",
  "service_name": "Legal Consultation",
  "booking_date": "2025-10-20",
  "booking_time": "14:00"
}
```

### **Complete Request:**
```json
{
  "phone": "1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "gender": "male",
  "country": "USA",
  "service_name": "Legal Consultation",
  "booking_date": "2025-10-20",
  "booking_time": "14:00",
  "notes": "Agent created booking",
  "status": "upcoming"
}
```

## 📤 **Response Format**

### **Success Response:**
```json
{
  "success": true,
  "message": "Booking created successfully",
  "user_created": true,
  "user_id": 123,
  "booking_id": 456,
  "data": {
    "booking": {
      "id": 456,
      "service_name": "Legal Consultation",
      "booking_date": "2025-10-20",
      "booking_time": "14:00:00",
      "status": "upcoming",
      "notes": "Agent created booking",
      "created_at": "2025-10-14T12:00:00Z"
    },
    "user": {
      "id": 123,
      "username": "1234567890",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "phone": "1234567890",
      "is_active": true,
      "created": true
    }
  }
}
```

### **Error Response:**
```json
{
  "success": false,
  "message": "This time slot is already reserved"
}
```

## 🔧 **Features**

### **1. Automatic User Creation**
- Creates user if phone number doesn't exist
- Sets initial password to "password"
- Creates user profile with provided information

### **2. Booking Validation**
- Checks working hours (12 PM - 5 PM)
- Validates off days (Sundays)
- Prevents double booking
- Validates date/time formats

### **3. Real-time Notifications**
- Sends WebSocket notifications to admin dashboard
- Real-time updates for booking creation
- Includes user details in notifications

### **4. Transaction Safety**
- Uses database transactions
- Ensures data consistency
- Rollback on errors

## 🧪 **Testing Examples**

### **cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/agent/booking/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "service_name": "Legal Consultation",
    "booking_date": "2025-10-20",
    "booking_time": "14:00",
    "notes": "Agent created booking"
  }'
```

### **JavaScript Example:**
```javascript
const response = await fetch('http://localhost:8000/api/agent/booking/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone: '1234567890',
    first_name: 'John',
    last_name: 'Doe',
    email: 'john.doe@example.com',
    service_name: 'Legal Consultation',
    booking_date: '2025-10-20',
    booking_time: '14:00',
    notes: 'Agent created booking'
  })
});

const data = await response.json();
console.log(data);
```

## ⚠️ **Error Handling**

### **Common Error Messages:**
- `"Missing required field: phone"` - Missing required field
- `"Invalid date format"` - Unsupported date format
- `"Invalid time format"` - Unsupported time format
- `"Booking not allowed on off days"` - Booking on Sunday
- `"Booking time is outside working hours"` - Time outside 12-17
- `"This time slot is already reserved"` - Slot already taken
- `"No booking settings found"` - System configuration missing

## 🔄 **WebSocket Integration**

The endpoint automatically sends WebSocket notifications to the admin dashboard:

```javascript
// WebSocket message format
{
  "type": "booking_created",
  "data": {
    "id": 456,
    "service_name": "Legal Consultation",
    "booking_date": "2025-10-20",
    "booking_time": "14:00:00",
    "user_details": {
      "id": 123,
      "username": "1234567890",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    }
  }
}
```

## 🎯 **Use Cases**

1. **Agent Systems** - External booking systems
2. **Call Centers** - Phone-based booking creation
3. **Third-party Integrations** - External applications
4. **Mobile Apps** - Agent-assisted booking
5. **Web Portals** - External booking forms

## 🔒 **Security Notes**

- **Public endpoint** - No authentication required
- **Rate limiting** recommended for production
- **Input validation** on all fields
- **SQL injection protection** via Django ORM
- **XSS protection** via Django's built-in security

## 📊 **Performance**

- **Database transactions** for consistency
- **Efficient queries** with proper indexing
- **WebSocket notifications** for real-time updates
- **Error handling** with detailed messages
- **Support for high volume** booking creation

## 🚀 **Production Deployment**

1. **Rate limiting** - Implement rate limiting
2. **Monitoring** - Add logging and monitoring
3. **Validation** - Additional input validation
4. **Security** - Consider IP whitelisting
5. **Backup** - Ensure database backups

---

## 📞 **Support**

For questions or issues with the Agent Booking Endpoint, please contact the development team.
