# 📮 Complete Postman Collection Guide

## 🎯 Overview
This guide explains how to use the complete Postman collection for the KIP booking system. The collection includes all API endpoints organized into logical sections.

## 📦 Collection Structure

### 🔐 Authentication Section
- **Check Phone** - Verify if phone number exists
- **Send OTP** - Send verification code to phone
- **Verify OTP** - Verify the OTP code
- **Register User** - Create new user account
- **Register Without OTP** - Quick registration
- **Login** - Authenticate user (auto-saves JWT token)
- **Get Current User Info** - Get logged-in user details
- **Update User Info** - Update user profile
- **Change Password** - Change user password
- **Reset Password** - Reset password via phone

### 📅 Bookings Section
- **Get User Bookings** - List user's bookings
- **Get Booking Details** - Get specific booking info
- **Update Booking** - Modify existing booking
- **Cancel Booking** - Delete/cancel booking
- **Get Available Time Slots** - Check available times
- **Create Booking** - Make new booking (auto-saves booking ID)

### 👥 Admin - Users Section
- **Get All Users** - List all users with filtering
- **Get User Statistics** - User analytics
- **Get User Filter Options** - Available filter choices
- **Get User Details** - Specific user information
- **Update User** - Modify user details
- **Delete User** - Remove user account
- **Create User** - Add new user (admin only)

### 📋 Admin - Bookings Section
- **Get All Bookings** - List all bookings with filtering
- **Get Booking Statistics** - Booking analytics
- **Get Booking Details** - Specific booking info
- **Update Booking Status** - Change booking status
- **Delete Booking** - Remove booking
- **Create Booking (Admin)** - Admin-created booking

### 🎯 Admin - Offers Section
- **Get All Offers** - List all offers with filtering
- **Get Offer Statistics** - Offer analytics
- **Get Offer Filter Options** - Available filter choices
- **Create Offer** - Create new offer (auto-saves offer ID)
- **Get Offer Details** - Specific offer information
- **Update Offer** - Modify offer details
- **Toggle Offer Status** - Activate/deactivate offer
- **Toggle Offer Featured** - Mark/unmark as featured
- **Delete Offer** - Remove offer

### 🛠️ Services Section
- **Get All Services** - List available services
- **Get Countries** - List supported countries
- **Get Booking Settings** - System booking configuration

### 📊 Dashboard - Services Management
- **Get Dashboard Services** - Admin service management
- **Create Service** - Add new service
- **Get Service Details** - Specific service info
- **Update Service** - Modify service
- **Delete Service** - Remove service
- **Get Service Sub-Services** - Service sub-categories
- **Create Sub-Service** - Add sub-category
- **Get Sub-Service Details** - Sub-service info
- **Update Sub-Service** - Modify sub-service
- **Delete Sub-Service** - Remove sub-service

### 🔌 WebSocket Testing Section
- **WebSocket Connection Test** - Basic WebSocket testing
- **WebSocket Connection Test (Advanced)** - Advanced testing
- **Mobile Simulator** - Simulate mobile app
- **Real-time Dashboard** - Live dashboard testing

## 🚀 Getting Started

### 1. Import the Collection
1. Open Postman
2. Click "Import" button
3. Select `Complete_API_Collection.postman_collection.json`
4. The collection will be imported with all endpoints

### 2. Set Up Environment Variables
The collection uses these variables:
- `base_url`: `http://localhost:8000/api` (default)
- `jwt_token`: Auto-populated after login
- `user_id`: Auto-populated from login response
- `booking_id`: Auto-populated when creating bookings
- `offer_id`: Auto-populated when creating offers

### 3. Start the Server
Make sure your Django server is running:
```bash
python3 manage.py runserver
```

### 4. Authentication Flow
1. **Register a new user** or **Login** with existing credentials
2. The JWT token will be automatically saved
3. All subsequent requests will use the saved token

## 📋 Usage Examples

### Complete User Registration Flow
1. **Check Phone** → Verify phone availability
2. **Send OTP** → Get verification code
3. **Verify OTP** → Confirm phone number
4. **Register User** → Create account
5. **Login** → Get JWT token (auto-saved)

### Complete Booking Flow
1. **Get Available Time Slots** → Check available times
2. **Create Booking** → Make reservation (ID auto-saved)
3. **Get User Bookings** → View all bookings
4. **Update Booking** → Modify if needed
5. **Cancel Booking** → Delete if needed

### Complete Admin Offer Management
1. **Get All Offers** → View existing offers
2. **Get Offer Statistics** → Check analytics
3. **Create Offer** → Add new offer (ID auto-saved)
4. **Update Offer** → Modify offer details
5. **Toggle Offer Status** → Activate/deactivate
6. **Toggle Offer Featured** → Mark as featured
7. **Delete Offer** → Remove offer

## 🔧 Advanced Features

### Auto-Variable Population
The collection automatically saves important IDs:
- **JWT Token**: Saved after successful login
- **User ID**: Extracted from login response
- **Booking ID**: Saved when creating bookings
- **Offer ID**: Saved when creating offers

### Pre-request Scripts
- Automatically sets base URL if not configured
- Handles common authentication scenarios

### Test Scripts
- Auto-saves JWT token from login response
- Auto-saves IDs from creation responses
- Provides helpful error messages

### Global Error Handling
- **401**: Authentication required
- **403**: Access forbidden
- **404**: Resource not found
- **500+**: Server errors

## 🎯 Testing Scenarios

### 1. User Registration & Booking
```
1. Check Phone → Send OTP → Verify OTP → Register → Login
2. Get Available Time Slots → Create Booking
3. Get User Bookings → Update Booking → Cancel Booking
```

### 2. Admin User Management
```
1. Login as admin → Get All Users → Get User Statistics
2. Create User → Get User Details → Update User → Delete User
```

### 3. Admin Booking Management
```
1. Get All Bookings → Get Booking Statistics
2. Create Booking (Admin) → Update Booking Status → Delete Booking
```

### 4. Admin Offer Management
```
1. Get All Offers → Get Offer Statistics → Create Offer
2. Update Offer → Toggle Status → Toggle Featured → Delete Offer
```

### 5. Services Management
```
1. Get All Services → Create Service → Update Service → Delete Service
2. Create Sub-Service → Update Sub-Service → Delete Sub-Service
```

## 🔌 WebSocket Testing

### Real-time Testing
1. Open **WebSocket Connection Test** in browser
2. Open **Mobile Simulator** in another tab
3. Create booking in simulator
4. Watch real-time updates in connection test

### WebSocket URLs
- **Connection Test**: `http://localhost:8000/static/websocket_simple_test.html`
- **Advanced Test**: `http://localhost:8000/static/websocket_connection_test.html`
- **Mobile Simulator**: `http://localhost:8000/static/mobile_simulator.html`
- **Real-time Dashboard**: `http://localhost:8000/static/test_dashboard.html`

## 📊 Collection Features

### Organized Structure
- **Logical grouping** by functionality
- **Clear naming** for easy navigation
- **Descriptive requests** with examples

### Auto-Authentication
- **JWT token** automatically included in requests
- **Token refresh** handling
- **Error detection** for auth issues

### Smart Variables
- **Auto-population** of IDs from responses
- **Environment management** for different setups
- **Dynamic URLs** based on saved IDs

### Comprehensive Coverage
- **All CRUD operations** for each resource
- **Admin and user endpoints** separated
- **WebSocket testing** included
- **Real-time features** demonstrated

## 🚨 Important Notes

### Authentication
- **Login first** before testing protected endpoints
- **JWT token** expires after 24 hours (default)
- **Re-login** if you get 401 errors

### Server Requirements
- **Django server** must be running on port 8000
- **Database migrations** applied
- **WebSocket server** (daphne) for real-time features

### Testing Order
1. **Start with authentication** (register/login)
2. **Test basic operations** (CRUD)
3. **Test admin features** (if admin user)
4. **Test WebSocket** features
5. **Test real-time** scenarios

## 🎉 Success Indicators

### Authentication Success
- **200 response** from login
- **JWT token** saved in variables
- **User ID** populated

### Booking Success
- **201 response** from booking creation
- **Booking ID** saved in variables
- **Real-time updates** in WebSocket

### Admin Success
- **Statistics endpoints** return data
- **CRUD operations** work correctly
- **Filtering and pagination** functional

## 🔧 Troubleshooting

### Common Issues
1. **401 Unauthorized**: Login first or check JWT token
2. **404 Not Found**: Check server is running and URL is correct
3. **500 Server Error**: Check Django logs for detailed error
4. **WebSocket 404**: Use daphne server instead of runserver

### Debug Steps
1. **Check server status**: `curl http://localhost:8000/api/services/`
2. **Verify authentication**: Test login endpoint
3. **Check variables**: Ensure JWT token is set
4. **Review logs**: Check Django console for errors

This comprehensive Postman collection provides complete testing coverage for your KIP booking system! 🚀
