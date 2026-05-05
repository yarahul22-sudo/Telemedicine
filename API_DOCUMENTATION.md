# **TELEMEDICINE PLATFORM - API DOCUMENTATION**
## **RESTful API Reference**

**API Version:** 1.0  
**Base URL:** `https://api.telemedicine.moscow/v1`  
**Authentication:** OAuth 2.0 + JWT Tokens  
**Response Format:** JSON  
**Timezone:** MSK (Moscow Standard Time, UTC+3)

---

## **TABLE OF CONTENTS**
1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Doctors](#doctors)
4. [Patients](#patients)
5. [Appointments](#appointments)
6. [Video Calls](#video-calls)
7. [Prescriptions](#prescriptions)
8. [Medical Records](#medical-records)
9. [Payments](#payments)
10. [Admin](#admin)
11. [Error Codes](#error-codes)
12. [Rate Limiting](#rate-limiting)

---

## **AUTHENTICATION** {#authentication}

### **Base Authentication Info**
- **Type:** OAuth 2.0 + JWT
- **Bearer Token:** Required in all requests (except login/register)
- **Header:** `Authorization: Bearer <access_token>`
- **Token Expiry:** 24 hours
- **Refresh Token Expiry:** 30 days

---

### **POST /auth/register**
Register a new user account

**Request:**
```json
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "user_type": "patient|doctor|admin",
  "first_name": "Ivan",
  "last_name": "Petrov",
  "phone": "+7-916-XXX-XXXX",
  "date_of_birth": "1980-05-15"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": "USR-20260505-001",
    "email": "user@example.com",
    "user_type": "patient",
    "created_at": "2026-05-05T10:30:00Z",
    "verification_token": "ver_xxxxxxxxxxxxx"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "INVALID_EMAIL",
  "message": "Email format is invalid"
}
```

---

### **POST /auth/login**
Authenticate user and get access token

**Request:**
```json
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "ref_xxxxxxxxxxxxx",
    "expires_in": 86400,
    "user": {
      "user_id": "USR-20260505-001",
      "email": "user@example.com",
      "first_name": "Ivan",
      "user_type": "patient",
      "verified": true
    }
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "INVALID_CREDENTIALS",
  "message": "Email or password is incorrect"
}
```

---

### **POST /auth/refresh-token**
Refresh access token using refresh token

**Request:**
```json
POST /auth/refresh-token
Content-Type: application/json

{
  "refresh_token": "ref_xxxxxxxxxxxxx"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400
  }
}
```

---

### **POST /auth/logout**
Logout user and invalidate tokens

**Request:**
```json
POST /auth/logout
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### **POST /auth/verify-email**
Verify email address with token

**Request:**
```json
POST /auth/verify-email
Content-Type: application/json

{
  "token": "ver_xxxxxxxxxxxxx"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

---

### **POST /auth/password-reset**
Request password reset

**Request:**
```json
POST /auth/password-reset
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset link sent to email"
}
```

---

### **POST /auth/password-reset-confirm**
Confirm password reset with token

**Request:**
```json
POST /auth/password-reset-confirm
Content-Type: application/json

{
  "token": "reset_xxxxxxxxxxxxx",
  "new_password": "NewSecurePassword456!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset successful"
}
```

---

### **POST /auth/2fa/enable**
Enable two-factor authentication

**Request:**
```json
POST /auth/2fa/enable
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "method": "sms|authenticator_app"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "qr_code": "data:image/png;base64,...",
    "backup_codes": [
      "XXXX-XXXX-XXXX",
      "YYYY-YYYY-YYYY"
    ]
  }
}
```

---

## **USER MANAGEMENT** {#user-management}

### **GET /users/profile**
Get current user's profile

**Request:**
```
GET /users/profile
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": "USR-20260505-001",
    "email": "user@example.com",
    "first_name": "Ivan",
    "last_name": "Petrov",
    "phone": "+7-916-123-4567",
    "date_of_birth": "1980-05-15",
    "user_type": "patient",
    "created_at": "2026-05-05T10:30:00Z",
    "profile_photo_url": "https://cdn.telemedicine.moscow/photos/user123.jpg",
    "verified": true
  }
}
```

---

### **PUT /users/profile**
Update current user's profile

**Request:**
```json
PUT /users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Ivan",
  "last_name": "Petrov",
  "phone": "+7-916-123-4567",
  "profile_photo": "base64_encoded_image_or_file"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user_id": "USR-20260505-001",
    "first_name": "Ivan",
    "profile_photo_url": "https://cdn.telemedicine.moscow/photos/user123_updated.jpg"
  }
}
```

---

### **PUT /users/password**
Change password

**Request:**
```json
PUT /users/password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword456!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

### **GET /users/preferences**
Get user notification preferences

**Request:**
```
GET /users/preferences
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "email_notifications": true,
    "sms_notifications": true,
    "in_app_notifications": true,
    "marketing_emails": false,
    "appointment_reminders": "24_hours_before",
    "notification_frequency": "immediate",
    "quiet_hours_enabled": false,
    "quiet_hours_start": "22:00",
    "quiet_hours_end": "08:00"
  }
}
```

---

### **PUT /users/preferences**
Update notification preferences

**Request:**
```json
PUT /users/preferences
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email_notifications": true,
  "sms_notifications": false,
  "in_app_notifications": true,
  "marketing_emails": false,
  "appointment_reminders": "1_hour_before",
  "quiet_hours_enabled": true,
  "quiet_hours_start": "22:00",
  "quiet_hours_end": "08:00"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Preferences updated successfully"
}
```

---

## **DOCTORS** {#doctors}

### **GET /doctors**
Get list of all doctors with filters

**Request:**
```
GET /doctors?specialization=cardiology&min_rating=4&availability=today&limit=20&offset=0
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `specialization` (string): Filter by specialty (cardiology, dermatology, etc.)
- `min_rating` (number): Minimum rating (1-5)
- `availability` (string): today, tomorrow, this_week, custom_date
- `available_date` (string): YYYY-MM-DD (if availability=custom_date)
- `search` (string): Search by doctor name
- `limit` (number): Results per page (default: 20, max: 100)
- `offset` (number): Pagination offset (default: 0)
- `sort_by` (string): rating, experience, availability

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "doctor_id": "DOC-20260101-001",
      "first_name": "Ivan",
      "last_name": "Petrov",
      "specialization": ["Cardiology", "Internal Medicine"],
      "experience_years": 15,
      "bio": "Experienced cardiologist with 15 years in clinical practice",
      "profile_photo_url": "https://cdn.telemedicine.moscow/doctors/doc001.jpg",
      "rating": 4.8,
      "review_count": 87,
      "consultation_fee": 500,
      "available_slots": ["14:00", "14:30", "15:00"],
      "languages": ["Russian", "English"],
      "hospital": "City Hospital #1",
      "response_time_minutes": 30,
      "is_favorite": false
    }
  ],
  "pagination": {
    "total": 450,
    "limit": 20,
    "offset": 0,
    "pages": 23
  }
}
```

---

### **GET /doctors/{doctor_id}**
Get detailed information about a specific doctor

**Request:**
```
GET /doctors/DOC-20260101-001
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "doctor_id": "DOC-20260101-001",
    "first_name": "Ivan",
    "last_name": "Petrov",
    "email": "dr.petrov@hospital.com",
    "phone": "+7-916-555-1234",
    "specialization": ["Cardiology", "Internal Medicine"],
    "experience_years": 15,
    "education": [
      {
        "degree": "MD",
        "school": "Moscow Medical University",
        "year": 1998
      },
      {
        "degree": "Board Certification",
        "specialty": "Cardiology",
        "year": 2005
      }
    ],
    "bio": "Experienced cardiologist with 15 years in clinical practice",
    "profile_photo_url": "https://cdn.telemedicine.moscow/doctors/doc001.jpg",
    "rating": 4.8,
    "review_count": 87,
    "consultation_fee": 500,
    "working_hours": {
      "monday": "09:00-17:00",
      "tuesday": "09:00-17:00",
      "wednesday": "OFF",
      "thursday": "09:00-17:00",
      "friday": "09:00-17:00",
      "saturday": "10:00-14:00",
      "sunday": "OFF"
    },
    "available_dates": [
      {
        "date": "2026-05-05",
        "slots": ["14:00", "14:30", "15:00", "15:30"]
      },
      {
        "date": "2026-05-06",
        "slots": ["09:00", "09:30", "10:00"]
      }
    ],
    "languages": ["Russian", "English"],
    "hospital": "City Hospital #1",
    "response_time_minutes": 30,
    "accepted_insurance": ["Sberbank Insurance", "VTB Insurance"],
    "top_reviews": [
      {
        "reviewer_name": "Anonymous",
        "rating": 5,
        "comment": "Dr. Petrov was very professional and thorough",
        "created_at": "2026-04-28T15:30:00Z"
      }
    ]
  }
}
```

---

### **GET /doctors/{doctor_id}/availability**
Get doctor's availability for specific date range

**Request:**
```
GET /doctors/DOC-20260101-001/availability?start_date=2026-05-05&end_date=2026-05-12
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "doctor_id": "DOC-20260101-001",
    "doctor_name": "Dr. Ivan Petrov",
    "availability": [
      {
        "date": "2026-05-05",
        "day_of_week": "Monday",
        "slots": [
          {
            "time": "14:00",
            "available": true,
            "duration_minutes": 30
          },
          {
            "time": "14:30",
            "available": true,
            "duration_minutes": 30
          },
          {
            "time": "15:00",
            "available": false,
            "duration_minutes": 30,
            "reason": "Already booked"
          }
        ]
      }
    ]
  }
}
```

---

### **POST /doctors/register**
Register as a doctor (Admin verification required)

**Request:**
```json
POST /doctors/register
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "specialization": ["Cardiology", "Internal Medicine"],
  "experience_years": 15,
  "bio": "Experienced cardiologist...",
  "medical_license_number": "LIC-123456",
  "medical_degree": "MD",
  "degree_university": "Moscow Medical University",
  "degree_year": 1998,
  "certifications": [
    {
      "name": "Board Certification - Cardiology",
      "year": 2005
    }
  ],
  "hospital_affiliation": "City Hospital #1",
  "consultation_fee": 500,
  "languages": ["Russian", "English"],
  "working_hours": {
    "monday": "09:00-17:00",
    "tuesday": "09:00-17:00",
    "wednesday": "OFF",
    "thursday": "09:00-17:00",
    "friday": "09:00-17:00",
    "saturday": "10:00-14:00",
    "sunday": "OFF"
  },
  "documents": [
    {
      "type": "medical_license",
      "file": "base64_encoded_file"
    },
    {
      "type": "degree_certificate",
      "file": "base64_encoded_file"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Doctor profile submitted for approval",
  "data": {
    "doctor_id": "DOC-20260505-001",
    "status": "pending_approval",
    "submitted_at": "2026-05-05T10:30:00Z",
    "message": "Your application will be reviewed within 24-48 hours"
  }
}
```

---

### **PUT /doctors/profile**
Update doctor's profile (by doctor)

**Request:**
```json
PUT /doctors/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "bio": "Updated bio...",
  "consultation_fee": 550,
  "working_hours": {
    "monday": "10:00-18:00",
    "tuesday": "10:00-18:00"
  },
  "specialization": ["Cardiology", "Internal Medicine", "Hypertension"]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

---

### **GET /doctors/{doctor_id}/reviews**
Get all reviews for a doctor

**Request:**
```
GET /doctors/DOC-20260101-001/reviews?limit=20&offset=0&sort_by=recent
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "doctor_id": "DOC-20260101-001",
    "average_rating": 4.8,
    "total_reviews": 87,
    "reviews": [
      {
        "review_id": "REV-20260504-001",
        "patient_name": "Anonymous",
        "rating": 5,
        "title": "Excellent doctor",
        "comment": "Dr. Petrov was very professional and thorough. Highly recommended!",
        "consultation_date": "2026-04-28",
        "helpful_count": 12,
        "doctor_response": {
          "response": "Thank you for your kind words!",
          "responded_at": "2026-04-29T10:00:00Z"
        },
        "created_at": "2026-04-28T15:30:00Z"
      }
    ]
  }
}
```

---

## **PATIENTS** {#patients}

### **GET /patients/profile**
Get current patient's profile

**Request:**
```
GET /patients/profile
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "patient_id": "PAT-20260505-001",
    "user_id": "USR-20260505-001",
    "first_name": "Ivan",
    "last_name": "Sokolov",
    "email": "ivan@example.com",
    "phone": "+7-916-123-4567",
    "date_of_birth": "1972-03-15",
    "age": 54,
    "gender": "male",
    "blood_type": "O+",
    "height_cm": 180,
    "weight_kg": 85,
    "bmi": 26.2,
    "profile_photo_url": "https://cdn.telemedicine.moscow/patients/pat001.jpg",
    "chronic_diseases": [
      {
        "disease": "Hypertension",
        "diagnosed_year": 2010,
        "status": "controlled"
      },
      {
        "disease": "Type 2 Diabetes",
        "diagnosed_year": 2015,
        "status": "controlled"
      }
    ],
    "allergies": [
      {
        "allergen": "Penicillin",
        "reaction": "Rash",
        "severity": "moderate"
      },
      {
        "allergen": "NSAIDs",
        "reaction": "Stomach upset",
        "severity": "mild"
      }
    ],
    "current_medications": [
      {
        "medication_name": "Atorvastatin",
        "dosage": "20mg",
        "frequency": "once daily",
        "since_date": "2026-05-05"
      }
    ],
    "emergency_contact": {
      "name": "Maria Sokolova",
      "relationship": "Wife",
      "phone": "+7-916-987-6543"
    }
  }
}
```

---

### **PUT /patients/profile**
Update patient's health information

**Request:**
```json
PUT /patients/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "weight_kg": 82,
  "height_cm": 180,
  "blood_type": "O+",
  "gender": "male",
  "chronic_diseases": [
    {
      "disease": "Hypertension",
      "diagnosed_year": 2010
    },
    {
      "disease": "Type 2 Diabetes",
      "diagnosed_year": 2015
    }
  ],
  "allergies": [
    {
      "allergen": "Penicillin",
      "reaction": "Rash"
    }
  ],
  "emergency_contact": {
    "name": "Maria Sokolova",
    "relationship": "Wife",
    "phone": "+7-916-987-6543"
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

---

### **GET /patients/medical-records**
Get patient's medical records and history

**Request:**
```
GET /patients/medical-records?limit=50&offset=0
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "patient_id": "PAT-20260505-001",
    "medical_records": [
      {
        "record_id": "REC-20260505-001",
        "record_type": "consultation_notes",
        "consultation_id": "APT-20260505-001",
        "doctor_id": "DOC-20260101-001",
        "doctor_name": "Dr. Ivan Petrov",
        "date": "2026-05-05T14:00:00Z",
        "diagnosis": "Hypertension Management",
        "notes": "Patient presented with slightly elevated BP...",
        "created_at": "2026-05-05T14:30:00Z"
      },
      {
        "record_id": "REC-20260420-001",
        "record_type": "lab_results",
        "test_name": "Blood Test",
        "test_date": "2026-04-20",
        "results": {
          "cholesterol": "245 mg/dL",
          "triglycerides": "180 mg/dL",
          "blood_glucose": "145 mg/dL"
        },
        "created_at": "2026-04-20T16:00:00Z"
      }
    ]
  }
}
```

---

## **APPOINTMENTS** {#appointments}

### **POST /appointments/book**
Create a new appointment

**Request:**
```json
POST /appointments/book
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "doctor_id": "DOC-20260101-001",
  "appointment_date": "2026-05-05",
  "appointment_time": "14:00",
  "consultation_type": "video|text",
  "reason_for_visit": "Hypertension management",
  "payment_method": "credit_card|yandex_kassa|sberbank"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Appointment booked successfully",
  "data": {
    "appointment_id": "APT-20260505-001",
    "doctor_id": "DOC-20260101-001",
    "doctor_name": "Dr. Ivan Petrov",
    "patient_id": "PAT-20260505-001",
    "appointment_date": "2026-05-05",
    "appointment_time": "14:00",
    "end_time": "14:30",
    "consultation_type": "video",
    "status": "confirmed",
    "consultation_fee": 500,
    "confirmation_number": "CONF-202605-001234",
    "created_at": "2026-05-05T10:30:00Z",
    "reminder_sent": true
  }
}
```

---

### **GET /appointments**
Get list of user's appointments

**Request:**
```
GET /appointments?status=upcoming|completed|cancelled&limit=20&offset=0
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` (string): upcoming, completed, cancelled, all
- `date_from` (string): YYYY-MM-DD
- `date_to` (string): YYYY-MM-DD
- `limit` (number): Results per page
- `offset` (number): Pagination offset

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "appointment_id": "APT-20260505-001",
      "doctor_id": "DOC-20260101-001",
      "doctor_name": "Dr. Ivan Petrov",
      "doctor_photo": "https://cdn.telemedicine.moscow/doctors/doc001.jpg",
      "specialization": "Cardiology",
      "appointment_date": "2026-05-05",
      "appointment_time": "14:00",
      "duration_minutes": 30,
      "consultation_type": "video",
      "status": "confirmed",
      "reason_for_visit": "Hypertension management",
      "consultation_fee": 500,
      "confirmation_number": "CONF-202605-001234",
      "created_at": "2026-05-05T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 45,
    "limit": 20,
    "offset": 0,
    "pages": 3
  }
}
```

---

### **GET /appointments/{appointment_id}**
Get detailed information about a specific appointment

**Request:**
```
GET /appointments/APT-20260505-001
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "appointment_id": "APT-20260505-001",
    "doctor_id": "DOC-20260101-001",
    "doctor_name": "Dr. Ivan Petrov",
    "doctor_email": "dr.petrov@hospital.com",
    "doctor_phone": "+7-916-555-1234",
    "patient_id": "PAT-20260505-001",
    "patient_name": "Ivan Sokolov",
    "appointment_date": "2026-05-05",
    "appointment_time": "14:00",
    "end_time": "14:30",
    "duration_minutes": 30,
    "consultation_type": "video",
    "status": "confirmed",
    "reason_for_visit": "Hypertension management",
    "consultation_fee": 500,
    "payment_status": "paid",
    "confirmation_number": "CONF-202605-001234",
    "video_call_link": "https://telemedicine.moscow/call/APT-20260505-001",
    "video_call_password": "XYZABC123",
    "reminder_sent": true,
    "created_at": "2026-05-05T10:30:00Z",
    "updated_at": "2026-05-05T10:35:00Z"
  }
}
```

---

### **PUT /appointments/{appointment_id}/reschedule**
Request to reschedule an appointment

**Request:**
```json
PUT /appointments/APT-20260505-001/reschedule
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "new_date": "2026-05-06",
  "new_time": "15:00",
  "reason": "Schedule conflict"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Reschedule request sent to doctor",
  "data": {
    "appointment_id": "APT-20260505-001",
    "status": "reschedule_requested",
    "original_date": "2026-05-05",
    "requested_date": "2026-05-06",
    "requested_time": "15:00"
  }
}
```

---

### **DELETE /appointments/{appointment_id}**
Cancel an appointment

**Request:**
```json
DELETE /appointments/APT-20260505-001
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "reason": "Cannot attend",
  "notify_doctor": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Appointment cancelled successfully",
  "data": {
    "appointment_id": "APT-20260505-001",
    "status": "cancelled",
    "cancellation_date": "2026-05-05T10:45:00Z",
    "refund_status": "processed",
    "refund_amount": 500
  }
}
```

---

### **POST /appointments/{appointment_id}/complete**
Mark appointment as completed (Doctor only)

**Request:**
```json
POST /appointments/APT-20260505-001/complete
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "consultation_notes": "Patient has elevated BP, started on medication",
  "diagnosis": "Hypertension",
  "duration_actual_minutes": 28
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Appointment marked as completed",
  "data": {
    "appointment_id": "APT-20260505-001",
    "status": "completed",
    "completed_at": "2026-05-05T14:28:00Z"
  }
}
```

---

## **VIDEO CALLS** {#video-calls}

### **POST /video-calls/initialize**
Initialize a video call session

**Request:**
```json
POST /video-calls/initialize
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "appointment_id": "APT-20260505-001",
  "user_type": "patient|doctor"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "call_session_id": "CALL-202605-001",
    "appointment_id": "APT-20260505-001",
    "ice_servers": [
      {
        "urls": "stun:stun.telemedicine.moscow:3478"
      },
      {
        "urls": "turn:turn.telemedicine.moscow:3478",
        "username": "user123",
        "credential": "pass123"
      }
    ],
    "signaling_url": "wss://signaling.telemedicine.moscow",
    "room_id": "ROOM-APT-20260505-001",
    "video_codec": "VP9",
    "audio_codec": "Opus",
    "call_started_at": "2026-05-05T14:00:00Z"
  }
}
```

---

### **GET /video-calls/{call_session_id}/stats**
Get real-time video call statistics

**Request:**
```
GET /video-calls/CALL-202605-001/stats
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "call_session_id": "CALL-202605-001",
    "duration_seconds": 125,
    "video_quality": {
      "resolution": "720p",
      "frame_rate": 30,
      "codec": "VP9"
    },
    "audio_quality": {
      "codec": "Opus",
      "sample_rate": 48000
    },
    "network_stats": {
      "bandwidth_download_mbps": 8.2,
      "bandwidth_upload_mbps": 5.1,
      "latency_ms": 42,
      "packet_loss_percent": 0.1,
      "jitter_ms": 5
    },
    "connection_quality": "excellent"
  }
}
```

---

### **POST /video-calls/{call_session_id}/end**
End a video call session

**Request:**
```json
POST /video-calls/CALL-202605-001/end
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "actual_duration_seconds": 1680,
  "quality_rating": 5
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Call ended successfully",
  "data": {
    "call_session_id": "CALL-202605-001",
    "duration_seconds": 1680,
    "ended_at": "2026-05-05T14:28:00Z"
  }
}
```

---

### **POST /video-calls/{call_session_id}/record**
Start recording a call (with consent)

**Request:**
```json
POST /video-calls/CALL-202605-001/record
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "record_type": "video|audio_only",
  "consent_confirmed": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Recording started",
  "data": {
    "recording_id": "REC-20260505-001",
    "call_session_id": "CALL-202605-001",
    "started_at": "2026-05-05T14:00:30Z",
    "record_type": "video"
  }
}
```

---

## **PRESCRIPTIONS** {#prescriptions}

### **POST /prescriptions/create**
Create a new prescription (Doctor only)

**Request:**
```json
POST /prescriptions/create
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "appointment_id": "APT-20260505-001",
  "patient_id": "PAT-20260505-001",
  "medicines": [
    {
      "medicine_id": "MED-001",
      "medicine_name": "Atorvastatin",
      "strength": "20mg",
      "quantity": 30,
      "form": "tablet",
      "dosage": "1 tablet",
      "frequency": "once daily",
      "duration_days": 30,
      "special_instructions": "Take with food"
    },
    {
      "medicine_id": "MED-002",
      "medicine_name": "Lisinopril",
      "strength": "10mg",
      "quantity": 60,
      "form": "tablet",
      "dosage": "1 tablet",
      "frequency": "twice daily",
      "duration_days": 30,
      "special_instructions": "Take morning and evening"
    }
  ],
  "diagnosis": "Hypertension, Hyperlipidemia",
  "notes": "Patient has elevated BP and cholesterol. Started on statin and ACE inhibitor.",
  "allergies_to_avoid": ["Penicillin"]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Prescription created and sent to patient",
  "data": {
    "prescription_id": "PRE-20260505-001",
    "appointment_id": "APT-20260505-001",
    "patient_id": "PAT-20260505-001",
    "doctor_id": "DOC-20260101-001",
    "created_at": "2026-05-05T14:30:00Z",
    "expires_at": "2026-08-03T14:30:00Z",
    "pdf_url": "https://cdn.telemedicine.moscow/prescriptions/PRE-20260505-001.pdf",
    "patient_notified": true
  }
}
```

---

### **GET /prescriptions**
Get patient's prescriptions

**Request:**
```
GET /prescriptions?status=active|expired|all&limit=20&offset=0
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "prescription_id": "PRE-20260505-001",
      "doctor_name": "Dr. Ivan Petrov",
      "date_issued": "2026-05-05",
      "expires_at": "2026-08-03",
      "status": "active",
      "medicines": [
        {
          "medicine_name": "Atorvastatin",
          "strength": "20mg",
          "dosage": "1 tablet",
          "frequency": "once daily",
          "duration_days": 30,
          "special_instructions": "Take with food"
        }
      ],
      "diagnosis": "Hypertension, Hyperlipidemia",
      "pdf_url": "https://cdn.telemedicine.moscow/prescriptions/PRE-20260505-001.pdf"
    }
  ]
}
```

---

### **GET /prescriptions/{prescription_id}**
Get detailed prescription information

**Request:**
```
GET /prescriptions/PRE-20260505-001
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "prescription_id": "PRE-20260505-001",
    "doctor_id": "DOC-20260101-001",
    "doctor_name": "Dr. Ivan Petrov",
    "patient_id": "PAT-20260505-001",
    "patient_name": "Ivan Sokolov",
    "date_issued": "2026-05-05",
    "expires_at": "2026-08-03",
    "status": "active",
    "diagnosis": "Hypertension, Hyperlipidemia",
    "medicines": [
      {
        "medicine_name": "Atorvastatin",
        "strength": "20mg",
        "quantity": 30,
        "form": "tablet",
        "dosage": "1 tablet",
        "frequency": "once daily",
        "duration_days": 30,
        "special_instructions": "Take with food",
        "contraindications": [],
        "side_effects": ["Muscle pain", "Headache"]
      }
    ],
    "pdf_url": "https://cdn.telemedicine.moscow/prescriptions/PRE-20260505-001.pdf",
    "download_count": 2
  }
}
```

---

### **POST /prescriptions/{prescription_id}/download**
Download prescription as PDF

**Request:**
```
POST /prescriptions/PRE-20260505-001/download
Authorization: Bearer <access_token>
```

**Response (200 OK - PDF File):**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="prescription_PRE-20260505-001.pdf"

[PDF Binary Data]
```

---

## **MEDICAL RECORDS** {#medical-records}

### **POST /medical-records/upload**
Upload medical document or test results

**Request:**
```
POST /medical-records/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

- document_type: lab_report|medical_image|hospital_discharge|other
- document_title: "Blood Test Results"
- document_date: 2026-05-01
- description: "Lipid panel and glucose test"
- file: [binary file data]
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Document uploaded successfully",
  "data": {
    "record_id": "REC-20260505-002",
    "document_type": "lab_report",
    "document_title": "Blood Test Results",
    "document_date": "2026-05-01",
    "file_url": "https://cdn.telemedicine.moscow/records/REC-20260505-002.pdf",
    "uploaded_at": "2026-05-05T10:30:00Z",
    "file_size_kb": 245
  }
}
```

---

### **GET /medical-records**
Get all medical records

**Request:**
```
GET /medical-records?document_type=all&limit=50&offset=0
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "record_id": "REC-20260505-002",
      "document_type": "lab_report",
      "document_title": "Blood Test Results",
      "document_date": "2026-05-01",
      "file_url": "https://cdn.telemedicine.moscow/records/REC-20260505-002.pdf",
      "uploaded_at": "2026-05-05T10:30:00Z",
      "uploaded_by": "self"
    }
  ]
}
```

---

### **DELETE /medical-records/{record_id}**
Delete a medical record

**Request:**
```
DELETE /medical-records/REC-20260505-002
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Record deleted successfully"
}
```

---

## **PAYMENTS** {#payments}

### **POST /payments/process**
Process a payment for consultation

**Request:**
```json
POST /payments/process
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "appointment_id": "APT-20260505-001",
  "amount": 500,
  "currency": "RUB",
  "payment_method": "credit_card",
  "card_token": "tok_visa_xxxxxxxxxxxxx",
  "idempotency_key": "unique-key-12345"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Payment processed successfully",
  "data": {
    "transaction_id": "TXN-20260505-001",
    "appointment_id": "APT-20260505-001",
    "amount": 500,
    "currency": "RUB",
    "status": "succeeded",
    "payment_method": "credit_card",
    "card_last_four": "1234",
    "processed_at": "2026-05-05T10:30:00Z",
    "receipt_url": "https://telemedicine.moscow/receipts/TXN-20260505-001"
  }
}
```

---

### **GET /payments/history**
Get payment history

**Request:**
```
GET /payments/history?limit=50&offset=0&status=succeeded|failed|all
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "transaction_id": "TXN-20260505-001",
      "appointment_id": "APT-20260505-001",
      "amount": 500,
      "currency": "RUB",
      "status": "succeeded",
      "payment_method": "credit_card",
      "card_last_four": "1234",
      "processed_at": "2026-05-05T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 45,
    "limit": 50,
    "offset": 0
  }
}
```

---

### **POST /payments/refund**
Request refund for a consultation

**Request:**
```json
POST /payments/refund
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "transaction_id": "TXN-20260505-001",
  "appointment_id": "APT-20260505-001",
  "reason": "Doctor no-show",
  "amount": 500
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Refund processed successfully",
  "data": {
    "refund_id": "REF-20260505-001",
    "transaction_id": "TXN-20260505-001",
    "amount": 500,
    "status": "processed",
    "processed_at": "2026-05-05T11:00:00Z",
    "expected_in_account": "2026-05-09"
  }
}
```

---

### **GET /payments/invoices/{invoice_id}**
Get invoice for a consultation

**Request:**
```
GET /payments/invoices/INV-20260505-001
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "invoice_id": "INV-20260505-001",
    "appointment_id": "APT-20260505-001",
    "doctor_name": "Dr. Ivan Petrov",
    "patient_name": "Ivan Sokolov",
    "service_date": "2026-05-05",
    "description": "Medical Consultation - Cardiology",
    "amount": 500,
    "currency": "RUB",
    "vat_percent": 20,
    "vat_amount": 100,
    "total": 600,
    "payment_status": "paid",
    "invoice_date": "2026-05-05",
    "due_date": "2026-05-05",
    "pdf_url": "https://cdn.telemedicine.moscow/invoices/INV-20260505-001.pdf"
  }
}
```

---

## **ADMIN** {#admin}

### **GET /admin/dashboard**
Get admin dashboard metrics

**Request:**
```
GET /admin/dashboard
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "users": {
      "total_patients": 87532,
      "new_today": 145,
      "active_7_days": 45231,
      "churn_rate": 0.8
    },
    "doctors": {
      "total_doctors": 652,
      "active_doctors": 612,
      "pending_approval": 23,
      "new_today": 5
    },
    "appointments": {
      "total_today": 234,
      "completed_today": 198,
      "no_shows_today": 5,
      "cancellations_today": 3,
      "completion_rate": 96.2
    },
    "revenue": {
      "total_month": 2340000,
      "platform_revenue": 468000,
      "doctor_payouts": 1872000,
      "growth_vs_month": 15.3
    },
    "system": {
      "uptime_percent": 99.7,
      "avg_response_time_ms": 145,
      "active_users": 12345,
      "database_size_gb": 45.2
    }
  }
}
```

---

### **GET /admin/doctors/pending**
Get pending doctor approvals

**Request:**
```
GET /admin/doctors/pending?limit=50&offset=0
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "application_id": "APP-20260505-001",
      "doctor_name": "Dr. Mikhail Korolyov",
      "specialization": "Orthopedics",
      "experience_years": 20,
      "hospital": "City Hospital #3",
      "documents_verified": 5,
      "documents_pending": 0,
      "applied_at": "2026-05-05T10:30:00Z",
      "status": "ready_for_review",
      "actions": ["approve", "reject", "request_info"]
    }
  ]
}
```

---

### **POST /admin/doctors/{application_id}/approve**
Approve a doctor registration

**Request:**
```json
POST /admin/doctors/APP-20260505-001/approve
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "notes": "All documents verified and valid"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Doctor approved successfully",
  "data": {
    "doctor_id": "DOC-20260505-001",
    "doctor_name": "Dr. Mikhail Korolyov",
    "status": "active",
    "approved_at": "2026-05-05T11:00:00Z",
    "welcome_email_sent": true
  }
}
```

---

### **POST /admin/doctors/{application_id}/reject**
Reject a doctor registration

**Request:**
```json
POST /admin/doctors/APP-20260505-001/reject
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "reason": "Medical license invalid",
  "details": "License expired on 2025-12-31"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Application rejected",
  "data": {
    "application_id": "APP-20260505-001",
    "status": "rejected",
    "rejection_email_sent": true
  }
}
```

---

### **GET /admin/payments/report**
Get payment and revenue report

**Request:**
```
GET /admin/payments/report?start_date=2026-05-01&end_date=2026-05-31&group_by=daily|doctor
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "period": "2026-05-01 to 2026-05-31",
    "total_revenue": 2340000,
    "platform_revenue": 468000,
    "doctor_payouts": 1872000,
    "refunds": 45670,
    "daily_breakdown": [
      {
        "date": "2026-05-05",
        "consultations": 234,
        "revenue": 156000,
        "platform_share": 31200,
        "refunds": 2500
      }
    ]
  }
}
```

---

## **ERROR CODES** {#error-codes}

### **Common Error Responses**

**400 Bad Request:**
```json
{
  "success": false,
  "error": "INVALID_REQUEST",
  "message": "Request validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

**401 Unauthorized:**
```json
{
  "success": false,
  "error": "UNAUTHORIZED",
  "message": "Invalid or expired token"
}
```

**403 Forbidden:**
```json
{
  "success": false,
  "error": "FORBIDDEN",
  "message": "You don't have permission to access this resource"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": "NOT_FOUND",
  "message": "Resource not found"
}
```

**409 Conflict:**
```json
{
  "success": false,
  "error": "CONFLICT",
  "message": "Resource already exists"
}
```

**429 Too Many Requests:**
```json
{
  "success": false,
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Retry after 60 seconds",
  "retry_after_seconds": 60
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "error": "INTERNAL_SERVER_ERROR",
  "message": "An unexpected error occurred"
}
```

### **Error Code Reference**

| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| INVALID_EMAIL | 400 | Email format is invalid |
| PASSWORD_WEAK | 400 | Password doesn't meet requirements |
| EMAIL_EXISTS | 409 | Email already registered |
| USER_NOT_FOUND | 404 | User account doesn't exist |
| INVALID_CREDENTIALS | 401 | Email or password incorrect |
| TOKEN_EXPIRED | 401 | Token has expired |
| INSUFFICIENT_PERMISSIONS | 403 | User lacks required permissions |
| APPOINTMENT_CONFLICT | 409 | Time slot already booked |
| DOCTOR_NOT_AVAILABLE | 400 | Doctor not available at requested time |
| PAYMENT_FAILED | 400 | Payment processing failed |
| REFUND_NOT_ALLOWED | 400 | Refund window has passed |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| SERVER_ERROR | 500 | Internal server error |

---

## **RATE LIMITING** {#rate-limiting}

### **Rate Limit Configuration**

**Public Endpoints (Not Authenticated):**
- 100 requests per hour per IP

**Authenticated Endpoints:**
- 1000 requests per hour per user

**Sensitive Operations:**
- Login attempts: 5 per 15 minutes per IP
- Password reset: 3 per 24 hours per email
- Payment: 10 per hour per user

### **Rate Limit Headers**

All responses include rate limit information:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1620000000
X-RateLimit-Retry-After: 60
```

---

## **PAGINATION**

### **Pagination Parameters**

All list endpoints support pagination:

```
GET /resource?limit=20&offset=0
```

- `limit`: Number of items per page (max: 100, default: 20)
- `offset`: Number of items to skip (default: 0)

### **Pagination Response**

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 450,
    "limit": 20,
    "offset": 0,
    "pages": 23,
    "has_next": true,
    "has_previous": false,
    "next_offset": 20,
    "prev_offset": null
  }
}
```

---

## **SORTING**

### **Sort Parameters**

Some endpoints support custom sorting:

```
GET /resource?sort_by=field&sort_order=asc|desc
```

**Supported sort fields by endpoint:**
- `/doctors`: rating, experience, availability, name
- `/appointments`: date, status, created_at
- `/prescriptions`: date_issued, expires_at
- `/payments`: amount, processed_at, status

---

## **FILTERING**

### **Common Filter Examples**

```
# Filter by status
GET /appointments?status=upcoming

# Filter by date range
GET /prescriptions?date_from=2026-05-01&date_to=2026-05-31

# Filter by specialization
GET /doctors?specialization=cardiology

# Filter by rating
GET /doctors?min_rating=4&max_rating=5

# Combine filters
GET /doctors?specialization=cardiology&min_rating=4&availability=today
```

---

## **API EXAMPLES**

### **Example 1: Complete Appointment Booking Flow**

**Step 1: Search for doctors**
```bash
curl -X GET https://api.telemedicine.moscow/v1/doctors \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"specialization":"cardiology", "availability":"today"}'
```

**Step 2: Book appointment**
```bash
curl -X POST https://api.telemedicine.moscow/v1/appointments/book \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": "DOC-20260101-001",
    "appointment_date": "2026-05-05",
    "appointment_time": "14:00",
    "consultation_type": "video",
    "payment_method": "credit_card"
  }'
```

**Step 3: Process payment**
```bash
curl -X POST https://api.telemedicine.moscow/v1/payments/process \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "APT-20260505-001",
    "amount": 500,
    "currency": "RUB",
    "payment_method": "credit_card",
    "card_token": "tok_visa_xxxxxxxxxxxxx"
  }'
```

---

### **Example 2: Doctor Completing Appointment**

**Step 1: Get appointment details**
```bash
curl -X GET https://api.telemedicine.moscow/v1/appointments/APT-20260505-001 \
  -H "Authorization: Bearer <doctor_token>" \
  -H "Content-Type: application/json"
```

**Step 2: Create prescription**
```bash
curl -X POST https://api.telemedicine.moscow/v1/prescriptions/create \
  -H "Authorization: Bearer <doctor_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "APT-20260505-001",
    "patient_id": "PAT-20260505-001",
    "medicines": [
      {
        "medicine_name": "Atorvastatin",
        "strength": "20mg",
        "dosage": "1 tablet",
        "frequency": "once daily",
        "duration_days": 30
      }
    ],
    "diagnosis": "Hypertension"
  }'
```

**Step 3: Complete appointment**
```bash
curl -X POST https://api.telemedicine.moscow/v1/appointments/APT-20260505-001/complete \
  -H "Authorization: Bearer <doctor_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "consultation_notes": "Patient has elevated BP, started on medication",
    "diagnosis": "Hypertension",
    "duration_actual_minutes": 28
  }'
```

---

## **WEBHOOKS** (Future Implementation)

### **Webhook Events**

Supported webhook events (implementation in progress):

- `appointment.created`
- `appointment.updated`
- `appointment.completed`
- `appointment.cancelled`
- `payment.succeeded`
- `payment.failed`
- `doctor.approved`
- `doctor.rejected`
- `prescription.created`
- `video_call.started`
- `video_call.ended`

### **Webhook Payload Example**

```json
{
  "event": "appointment.completed",
  "timestamp": "2026-05-05T14:30:00Z",
  "data": {
    "appointment_id": "APT-20260505-001",
    "status": "completed",
    "doctor_id": "DOC-20260101-001",
    "patient_id": "PAT-20260505-001"
  }
}
```

---

## **SDK AVAILABILITY**

### **Available SDKs**

- **Python SDK**: `pip install telemedicine-sdk`
- **JavaScript SDK**: `npm install telemedicine-sdk`
- **Java SDK**: In development

### **Python Example**

```python
from telemedicine_sdk import Client

client = Client(api_key="your_api_key")

# Book appointment
appointment = client.appointments.book(
    doctor_id="DOC-20260101-001",
    date="2026-05-05",
    time="14:00"
)

# Process payment
payment = client.payments.process(
    appointment_id=appointment.id,
    amount=500,
    method="credit_card"
)
```

---

**API Version:** 1.0  
**Last Updated:** May 5, 2026  
**Support Email:** api-support@telemedicine.moscow  
**Documentation:** https://docs.telemedicine.moscow
