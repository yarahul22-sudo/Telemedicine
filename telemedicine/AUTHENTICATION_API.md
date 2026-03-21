# Telemedicine Authentication API

Complete user authentication system with role-based access control for Patient, Doctor, and Admin users.

## Features Implemented

### ? User Models
- **CustomUser Model** - Extended Django User model with role-based access
- **Role Types**: Patient, Doctor, Admin
- **Doctor-Specific Fields**: Specialization, License Number, Experience Years
- **Patient-Specific Fields**: Medical History
- **Common Fields**: Phone, Date of Birth, Profile Picture, Verification Status

### ? Authentication Endpoints
1. **POST /api/users/register/** - User Registration
2. **POST /api/users/login/** - User Login (Token-based)
3. **POST /api/users/logout/** - User Logout
4. **GET /api/users/profile/** - Get Current User Profile
5. **PUT/PATCH /api/users/profile/update/** - Update User Profile
6. **GET /api/users/role/** - Get User Role Information
7. **GET /api/users/doctors/** - List All Verified Doctors

### ? Security Features
- Token Authentication (Django REST Framework)
- Password Validation (minimum 8 characters)
- Password Confirmation Check
- Role-Based Access Control
- Phone Number Validation
- Doctor License Number Validation

## Installation & Setup

### 1. Install Dependencies
```bash
pip install django djangorestframework pillow
```

### 2. Update Settings
- Added `'rest_framework'` to INSTALLED_APPS
- Added `'rest_framework.authtoken'` to INSTALLED_APPS
- Added `'users'` to INSTALLED_APPS
- Added `AUTH_USER_MODEL = 'users.CustomUser'`

### 3. Run Migrations
```bash
python manage.py makemigrations users
python manage.py migrate
```

## API Usage Examples

### 1. User Registration (Patient)
```bash
POST http://127.0.0.1:8000/api/users/register/

{
    "username": "john_doe",
    "email": "john@patient.com",
    "password": "secure123456",
    "password_confirm": "secure123456",
    "first_name": "John",
    "last_name": "Doe",
    "role": "patient",
    "phone": "+1234567890"
}

Response:
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@patient.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "patient",
        "phone": "+1234567890",
        "is_verified": false
    },
    "token": "abcdef123456..."
}
```

### 2. User Registration (Doctor)
```bash
POST http://127.0.0.1:8000/api/users/register/

{
    "username": "dr_smith",
    "email": "smith@doctor.com",
    "password": "secure123456",
    "password_confirm": "secure123456",
    "first_name": "Dr",
    "last_name": "Smith",
    "role": "doctor",
    "phone": "+1987654321",
    "specialization": "Cardiology",
    "license_number": "LIC12345",
    "experience_years": 10
}
```

### 3. User Login
```bash
POST http://127.0.0.1:8000/api/users/login/

{
    "username": "john_doe",
    "password": "secure123456"
}

Response:
{
    "message": "Login successful",
    "user": { ... },
    "token": "abcdef123456..."
}
```

### 4. Get User Profile (Authenticated)
```bash
GET http://127.0.0.1:8000/api/users/profile/
Headers: Authorization: Token abcdef123456...

Response:
{
    "id": 1,
    "username": "john_doe",
    "email": "john@patient.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "patient",
    "phone": "+1234567890",
    "date_of_birth": null,
    "profile_picture": null,
    "specialization": "",
    "license_number": "",
    "experience_years": null,
    "medical_history": "",
    "is_verified": false,
    "created_at": "2026-03-21T12:00:00Z"
}
```

### 5. Update User Profile
```bash
PATCH http://127.0.0.1:8000/api/users/profile/update/
Headers: Authorization: Token abcdef123456...

{
    "date_of_birth": "1990-01-15",
    "phone": "+1234567890",
    "medical_history": "No known allergies"
}
```

### 6. Get User Role
```bash
GET http://127.0.0.1:8000/api/users/role/
Headers: Authorization: Token abcdef123456...

Response:
{
    "role": "patient",
    "is_doctor": false,
    "is_patient": true,
    "is_admin": false
}
```

### 7. List Verified Doctors
```bash
GET http://127.0.0.1:8000/api/users/doctors/
Headers: Authorization: Token abcdef123456...

Response: [
    {
        "id": 2,
        "username": "dr_smith",
        "email": "smith@doctor.com",
        "role": "doctor",
        "specialization": "Cardiology",
        "experience_years": 10,
        "is_verified": true
    },
    ...
]
```

### 8. User Logout
```bash
POST http://127.0.0.1:8000/api/users/logout/
Headers: Authorization: Token abcdef123456...

Response:
{
    "message": "Logout successful"
}
```

## Role-Based Access Control

### User Model Methods
```python
# Check user role
user.is_doctor()      # Returns True if user is a doctor
user.is_patient()     # Returns True if user is a patient
user.is_admin_user()  # Returns True if user is an admin
```

### Protected Endpoints
All endpoints except `/register/` and `/login/` require authentication:
- Use `Authorization: Token <token>` header
- Token is obtained from registration or login response

## Admin Interface

Access the admin panel at: http://127.0.0.1:8000/admin/

Features:
- View all users by role
- Filter by verification status
- Search by username, email, or phone
- Edit user information
- Manage user verification status

## File Structure

```
users/
+-- models.py          # CustomUser model definition
+-- views.py           # API endpoints
+-- serializers.py     # DRF serializers
+-- urls.py            # URL routing
+-- admin.py           # Admin configuration
+-- migrations/
    +-- 0001_initial.py
```

## Security Considerations

1. ? Passwords are hashed using Django's default password hashing
2. ? Token authentication uses REST Framework tokens
3. ? Phone numbers are validated with regex
4. ? Doctors must provide license number
5. ? Email is unique per user
6. ? Username is unique per user
7. ? Password must be at least 8 characters
8. ? Passwords must be confirmed during registration

## Future Enhancements

- [ ] Email verification for new users
- [ ] Password reset functionality
- [ ] Two-factor authentication
- [ ] OAuth2 integration
- [ ] User profile pictures upload
- [ ] Role-based permissions decorators
- [ ] API rate limiting
- [ ] Audit logging

## Testing

Run the test script:
```bash
python test_api.py
```

This will test:
- Patient registration
- Doctor registration
- User login
- Profile retrieval
- Role checking
- Doctor listing

