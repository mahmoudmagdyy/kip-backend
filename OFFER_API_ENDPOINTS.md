# 🎯 Admin Offer Management API Endpoints

## Overview
This document describes the API endpoints for managing offers in the admin dashboard. These endpoints allow administrators to create, read, update, and delete offers with various discount types and validation rules.

## 🔐 Authentication
All endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## 📋 Endpoints

### 1. Get All Offers
**GET** `/api/admin/offers/`

**Query Parameters:**
- `search` (optional): Search in title and description
- `status` (optional): Filter by status (active, inactive, expired)
- `featured` (optional): Filter by featured status (true/false)
- `sort_by` (optional): Sort field (title, created_at, valid_from, valid_until)
- `limit` (optional): Number of results (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Example Request:**
```
GET /api/admin/offers/?search=summer&status=active&featured=true&sort_by=-created_at&limit=20&offset=0
```

**Response:**
```json
{
  "offers": [
    {
      "id": 1,
      "title": "Summer Special",
      "description": "Get 20% off on all services",
      "discount_type": "percentage",
      "discount_value": "20.00",
      "valid_from": "2025-06-01T00:00:00Z",
      "valid_until": "2025-08-31T23:59:59Z",
      "status": "active",
      "is_featured": true,
      "usage_limit": 100,
      "usage_count": 15,
      "created_by": 1,
      "created_by_name": "Admin User",
      "created_at": "2025-10-14T07:00:00Z",
      "updated_at": "2025-10-14T07:00:00Z",
      "is_valid": true,
      "remaining_uses": 85
    }
  ],
  "total_count": 1,
  "limit": 20,
  "offset": 0
}
```

### 2. Get Offer Statistics
**GET** `/api/admin/offers/stats/`

**Response:**
```json
{
  "total_offers": 25,
  "active_offers": 15,
  "inactive_offers": 5,
  "expired_offers": 5,
  "featured_offers": 3,
  "expiring_soon": 2
}
```

### 3. Get Filter Options
**GET** `/api/admin/offers/filter-options/`

**Response:**
```json
{
  "status_choices": ["active", "inactive", "expired"],
  "discount_types": ["percentage", "fixed"],
  "featured_options": [true, false]
}
```

### 4. Create New Offer
**POST** `/api/admin/offers/create/`

**Request Body:**
```json
{
  "title": "Black Friday Sale",
  "description": "Huge discounts on all services",
  "discount_type": "percentage",
  "discount_value": "30.00",
  "valid_from": "2025-11-24T00:00:00Z",
  "valid_until": "2025-11-30T23:59:59Z",
  "status": "active",
  "is_featured": true,
  "usage_limit": 500
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Black Friday Sale",
  "description": "Huge discounts on all services",
  "discount_type": "percentage",
  "discount_value": "30.00",
  "valid_from": "2025-11-24T00:00:00Z",
  "valid_until": "2025-11-30T23:59:59Z",
  "status": "active",
  "is_featured": true,
  "usage_limit": 500,
  "usage_count": 0,
  "created_by": 1,
  "created_by_name": "Admin User",
  "created_at": "2025-10-14T08:00:00Z",
  "updated_at": "2025-10-14T08:00:00Z",
  "is_valid": true,
  "remaining_uses": 500
}
```

### 5. Get Offer Details
**GET** `/api/admin/offers/{offer_id}/`

**Response:**
```json
{
  "id": 1,
  "title": "Summer Special",
  "description": "Get 20% off on all services",
  "discount_type": "percentage",
  "discount_value": "20.00",
  "valid_from": "2025-06-01T00:00:00Z",
  "valid_until": "2025-08-31T23:59:59Z",
  "status": "active",
  "is_featured": true,
  "usage_limit": 100,
  "usage_count": 15,
  "created_by": 1,
  "created_by_name": "Admin User",
  "created_at": "2025-10-14T07:00:00Z",
  "updated_at": "2025-10-14T07:00:00Z",
  "is_valid": true,
  "remaining_uses": 85
}
```

### 6. Update Offer
**PUT** `/api/admin/offers/{offer_id}/update/`

**Request Body:**
```json
{
  "title": "Updated Summer Special",
  "description": "Get 25% off on all services",
  "discount_value": "25.00",
  "valid_until": "2025-09-30T23:59:59Z"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Summer Special",
  "description": "Get 25% off on all services",
  "discount_type": "percentage",
  "discount_value": "25.00",
  "valid_from": "2025-06-01T00:00:00Z",
  "valid_until": "2025-09-30T23:59:59Z",
  "status": "active",
  "is_featured": true,
  "usage_limit": 100,
  "usage_count": 15,
  "created_by": 1,
  "created_by_name": "Admin User",
  "created_at": "2025-10-14T07:00:00Z",
  "updated_at": "2025-10-14T08:30:00Z",
  "is_valid": true,
  "remaining_uses": 85
}
```

### 7. Delete Offer
**DELETE** `/api/admin/offers/{offer_id}/delete/`

**Response:**
```json
{
  "message": "Offer deleted successfully"
}
```

### 8. Toggle Offer Status
**POST** `/api/admin/offers/{offer_id}/toggle-status/`

**Response:**
```json
{
  "id": 1,
  "title": "Summer Special",
  "description": "Get 20% off on all services",
  "discount_type": "percentage",
  "discount_value": "20.00",
  "valid_from": "2025-06-01T00:00:00Z",
  "valid_until": "2025-08-31T23:59:59Z",
  "status": "inactive",
  "is_featured": true,
  "usage_limit": 100,
  "usage_count": 15,
  "created_by": 1,
  "created_by_name": "Admin User",
  "created_at": "2025-10-14T07:00:00Z",
  "updated_at": "2025-10-14T08:30:00Z",
  "is_valid": false,
  "remaining_uses": 85
}
```

### 9. Toggle Featured Status
**POST** `/api/admin/offers/{offer_id}/toggle-featured/`

**Response:**
```json
{
  "id": 1,
  "title": "Summer Special",
  "description": "Get 20% off on all services",
  "discount_type": "percentage",
  "discount_value": "20.00",
  "valid_from": "2025-06-01T00:00:00Z",
  "valid_until": "2025-08-31T23:59:59Z",
  "status": "active",
  "is_featured": false,
  "usage_limit": 100,
  "usage_count": 15,
  "created_by": 1,
  "created_by_name": "Admin User",
  "created_at": "2025-10-14T07:00:00Z",
  "updated_at": "2025-10-14T08:30:00Z",
  "is_valid": true,
  "remaining_uses": 85
}
```

## 📊 Data Models

### Offer Model Fields
- `id`: Primary key
- `title`: Offer title (max 200 chars)
- `description`: Offer description
- `discount_type`: "percentage" or "fixed"
- `discount_value`: Decimal value (0-100 for percentage, any positive for fixed)
- `valid_from`: Start date/time
- `valid_until`: End date/time
- `status`: "active", "inactive", or "expired"
- `is_featured`: Boolean for featured offers
- `usage_limit`: Maximum uses (null = unlimited)
- `usage_count`: Current usage count
- `created_by`: User who created the offer
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Computed Fields
- `is_valid`: Boolean indicating if offer is currently valid
- `remaining_uses`: Number of uses remaining (null if unlimited)
- `created_by_name`: Full name of the creator

## 🔧 Validation Rules

### Discount Value Validation
- **Percentage**: Must be between 0 and 100
- **Fixed**: Must be positive

### Date Validation
- `valid_until` must be after `valid_from`

### Status Toggle
- Cannot toggle status for expired offers
- Active ↔ Inactive only

## 🚀 Usage Examples

### Create a Percentage Discount Offer
```bash
curl -X POST http://localhost:8000/api/admin/offers/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Year Sale",
    "description": "Start the year with 15% off",
    "discount_type": "percentage",
    "discount_value": "15.00",
    "valid_from": "2025-01-01T00:00:00Z",
    "valid_until": "2025-01-31T23:59:59Z",
    "status": "active",
    "is_featured": true,
    "usage_limit": 1000
  }'
```

### Create a Fixed Amount Discount
```bash
curl -X POST http://localhost:8000/api/admin/offers/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fixed Discount",
    "description": "Get $10 off your booking",
    "discount_type": "fixed",
    "discount_value": "10.00",
    "valid_from": "2025-10-15T00:00:00Z",
    "valid_until": "2025-12-31T23:59:59Z",
    "status": "active",
    "is_featured": false,
    "usage_limit": null
  }'
```

### Get Active Featured Offers
```bash
curl -X GET "http://localhost:8000/api/admin/offers/?status=active&featured=true" \
  -H "Authorization: Bearer <token>"
```

## 🎯 Dashboard Integration

These endpoints are designed to be used in an admin dashboard for:
- **Offer Management**: Create, edit, delete offers
- **Analytics**: View usage statistics and performance
- **Status Control**: Toggle active/inactive and featured status
- **Filtering**: Search and filter offers by various criteria
- **Pagination**: Handle large numbers of offers efficiently

## 🔒 Security Notes

- All endpoints require authentication
- Only authenticated users can manage offers
- Created offers are automatically assigned to the current user
- Soft validation prevents invalid discount values and date ranges
