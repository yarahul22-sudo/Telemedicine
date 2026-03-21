# Quick Start Guide - Telemedicine Authentication

## Project Structure Created

```
users/
+-- models.py        - CustomUser model with role-based access (Patient/Doctor/Admin)
+-- views.py         - 7 API endpoints for authentication
+-- serializers.py   - DRF serializers for data validation
+-- urls.py          - URL routing for all endpoints
+-- admin.py         - Admin interface configuration
+-- migrations/
    +-- 0001_initial.py - Database migrations
```

## 7 API Endpoints Created

1. POST /api/users/register/         ? User registration
2. POST /api/users/login/            ? User login (returns token)
3. POST /api/users/logout/           ? User logout
4. GET  /api/users/profile/          ? Get current user profile
5. PUT  /api/users/profile/update/   ? Update user profile
6. GET  /api/users/role/             ? Get user role info
7. GET  /api/users/doctors/          ? List verified doctors

## Features Implemented

? User Registration with role selection (Patient/Doctor/Admin)
? Secure Login with token-based authentication
? Password validation and confirmation
? Role-based access control with helper methods
? Doctor-specific fields (specialization, license, experience)
? Patient-specific fields (medical history)
? Phone number validation
? User profile management
? Django admin interface with custom filters
? Token authentication for protected endpoints

## Database Setup Done

? Created CustomUser model extending Django User
? Added 'rest_framework.authtoken' to settings
? Updated AUTH_USER_MODEL to 'users.CustomUser'
? Ran migrations - database ready to use

## Testing the API

Using curl or Postman:

1. Register a Patient:
   curl -X POST http://127.0.0.1:8000/api/users/register/ \
   -H "Content-Type: application/json" \
   -d '{
     "username": "john_doe",
     "email": "john@example.com",
     "password": "secure123456",
     "password_confirm": "secure123456",
     "first_name": "John",
     "last_name": "Doe",
     "role": "patient"
   }'

2. Login:
   curl -X POST http://127.0.0.1:8000/api/users/login/ \
   -H "Content-Type: application/json" \
   -d '{
     "username": "john_doe",
     "password": "secure123456"
   }'

3. Get Profile (use token from login response):
   curl -X GET http://127.0.0.1:8000/api/users/profile/ \
   -H "Authorization: Token <your-token-here>"

## Admin Panel Access

URL: http://127.0.0.1:8000/admin/

Features:
- View all users filtered by role
- Filter by verification status
- Search by username, email, or phone
- Edit user information
- Manage user verification status

## Security Features

? Passwords hashed with Django's default hasher
? Token authentication (DRF tokens)
? Phone validation with regex pattern
? Doctor license number validation
? Email uniqueness enforced
? Username uniqueness enforced
? Password minimum length 8 characters
? Password confirmation required during registration

## User Role Methods

In Python code, use these methods on user objects:

user.is_doctor()      # Check if user is doctor
user.is_patient()     # Check if user is patient
user.is_admin_user()  # Check if user is admin

Example:
if request.user.is_doctor():
    # Show doctor-specific content

## Configuration Changes Made to settings.py

Added to INSTALLED_APPS:
- 'rest_framework.authtoken'

Added at end of file:
- AUTH_USER_MODEL = 'users.CustomUser'

## Next Steps

1. Create frontend pages for registration/login
2. Add email verification for new users
3. Add password reset functionality
4. Create appointment booking system
5. Add doctor availability management
6. Create prescription management

## Files to Reference

- AUTHENTICATION_API.md - Full API documentation with examples
- test_api.py - Script to test all endpoints
- update_settings.py - Script that updated Django settings

