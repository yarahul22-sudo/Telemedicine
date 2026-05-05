# Telemedicine API - Auto-Generated Documentation

**Generated:** 2026-05-05 04:20:24

**Base URL:** `https://api.telemedicine.moscow/v1`

**Total Endpoints:** 48

## Table of Contents

- [Admin](#admin)
- [Appointments](#appointments)
- [Authentication](#authentication)
- [Doctors](#doctors)
- [Medical Records](#medical-records)
- [Patients](#patients)
- [Payments](#payments)
- [Prescriptions](#prescriptions)
- [Users](#users)
- [Video Calls](#video-calls)

---

## Admin

### 🟦 `GET` /admin/dashboard

**Description:** Admin dashboard

**URL:** `https://api.telemedicine.moscow/v1/admin/dashboard`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /admin/doctors/pending

**Description:** Pending approvals

**URL:** `https://api.telemedicine.moscow/v1/admin/doctors/pending`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /admin/doctors/{application_id}/approve

**Description:** Approve doctor

**URL:** `https://api.telemedicine.moscow/v1/admin/doctors/{application_id}/approve`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `application_id` (string, required)


### 🟩 `POST` /admin/doctors/{application_id}/reject

**Description:** Reject doctor

**URL:** `https://api.telemedicine.moscow/v1/admin/doctors/{application_id}/reject`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `application_id` (string, required)


### 🟦 `GET` /admin/payments/report

**Description:** Payment report

**URL:** `https://api.telemedicine.moscow/v1/admin/payments/report`

**Authentication:** Bearer Token (Required)


## Appointments

### 🟩 `POST` /appointments/book

**Description:** Book appointment

**URL:** `https://api.telemedicine.moscow/v1/appointments/book`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /appointments

**Description:** List appointments

**URL:** `https://api.telemedicine.moscow/v1/appointments`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /appointments/{appointment_id}

**Description:** Get appointment

**URL:** `https://api.telemedicine.moscow/v1/appointments/{appointment_id}`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `appointment_id` (string, required)


### 🟨 `PUT` /appointments/{appointment_id}/reschedule

**Description:** Reschedule appointment

**URL:** `https://api.telemedicine.moscow/v1/appointments/{appointment_id}/reschedule`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `appointment_id` (string, required)


### 🟥 `DELETE` /appointments/{appointment_id}

**Description:** Cancel appointment

**URL:** `https://api.telemedicine.moscow/v1/appointments/{appointment_id}`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `appointment_id` (string, required)


### 🟩 `POST` /appointments/{appointment_id}/complete

**Description:** Complete appointment

**URL:** `https://api.telemedicine.moscow/v1/appointments/{appointment_id}/complete`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `appointment_id` (string, required)


## Authentication

### 🟩 `POST` /auth/register

**Description:** Register new user

**URL:** `https://api.telemedicine.moscow/v1/auth/register`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/login

**Description:** Login user

**URL:** `https://api.telemedicine.moscow/v1/auth/login`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/logout

**Description:** Logout user

**URL:** `https://api.telemedicine.moscow/v1/auth/logout`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/refresh-token

**Description:** Refresh access token

**URL:** `https://api.telemedicine.moscow/v1/auth/refresh-token`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/verify-email

**Description:** Verify email

**URL:** `https://api.telemedicine.moscow/v1/auth/verify-email`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/password-reset

**Description:** Request password reset

**URL:** `https://api.telemedicine.moscow/v1/auth/password-reset`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/password-reset-confirm

**Description:** Confirm password reset

**URL:** `https://api.telemedicine.moscow/v1/auth/password-reset-confirm`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /auth/2fa/enable

**Description:** Enable 2FA

**URL:** `https://api.telemedicine.moscow/v1/auth/2fa/enable`

**Authentication:** Bearer Token (Required)


## Doctors

### 🟦 `GET` /doctors

**Description:** List doctors

**URL:** `https://api.telemedicine.moscow/v1/doctors`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /doctors/{doctor_id}

**Description:** Get doctor details

**URL:** `https://api.telemedicine.moscow/v1/doctors/{doctor_id}`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `doctor_id` (string, required)


### 🟦 `GET` /doctors/{doctor_id}/availability

**Description:** Get availability

**URL:** `https://api.telemedicine.moscow/v1/doctors/{doctor_id}/availability`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `doctor_id` (string, required)


### 🟦 `GET` /doctors/{doctor_id}/reviews

**Description:** Get reviews

**URL:** `https://api.telemedicine.moscow/v1/doctors/{doctor_id}/reviews`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `doctor_id` (string, required)


### 🟩 `POST` /doctors/register

**Description:** Register as doctor

**URL:** `https://api.telemedicine.moscow/v1/doctors/register`

**Authentication:** Bearer Token (Required)


### 🟨 `PUT` /doctors/profile

**Description:** Update doctor profile

**URL:** `https://api.telemedicine.moscow/v1/doctors/profile`

**Authentication:** Bearer Token (Required)


## Medical Records

### 🟩 `POST` /medical-records/upload

**Description:** Upload medical record

**URL:** `https://api.telemedicine.moscow/v1/medical-records/upload`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /medical-records

**Description:** List medical records

**URL:** `https://api.telemedicine.moscow/v1/medical-records`

**Authentication:** Bearer Token (Required)


### 🟥 `DELETE` /medical-records/{record_id}

**Description:** Delete record

**URL:** `https://api.telemedicine.moscow/v1/medical-records/{record_id}`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `record_id` (string, required)


## Patients

### 🟦 `GET` /patients/profile

**Description:** Get patient profile

**URL:** `https://api.telemedicine.moscow/v1/patients/profile`

**Authentication:** Bearer Token (Required)


### 🟨 `PUT` /patients/profile

**Description:** Update patient profile

**URL:** `https://api.telemedicine.moscow/v1/patients/profile`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /patients/medical-records

**Description:** Get medical records

**URL:** `https://api.telemedicine.moscow/v1/patients/medical-records`

**Authentication:** Bearer Token (Required)


## Payments

### 🟩 `POST` /payments/process

**Description:** Process payment

**URL:** `https://api.telemedicine.moscow/v1/payments/process`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /payments/history

**Description:** Payment history

**URL:** `https://api.telemedicine.moscow/v1/payments/history`

**Authentication:** Bearer Token (Required)


### 🟩 `POST` /payments/refund

**Description:** Request refund

**URL:** `https://api.telemedicine.moscow/v1/payments/refund`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /payments/invoices/{invoice_id}

**Description:** Get invoice

**URL:** `https://api.telemedicine.moscow/v1/payments/invoices/{invoice_id}`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `invoice_id` (string, required)


## Prescriptions

### 🟩 `POST` /prescriptions/create

**Description:** Create prescription

**URL:** `https://api.telemedicine.moscow/v1/prescriptions/create`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /prescriptions

**Description:** List prescriptions

**URL:** `https://api.telemedicine.moscow/v1/prescriptions`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /prescriptions/{prescription_id}

**Description:** Get prescription

**URL:** `https://api.telemedicine.moscow/v1/prescriptions/{prescription_id}`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `prescription_id` (string, required)


### 🟩 `POST` /prescriptions/{prescription_id}/download

**Description:** Download prescription

**URL:** `https://api.telemedicine.moscow/v1/prescriptions/{prescription_id}/download`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `prescription_id` (string, required)


## Users

### 🟦 `GET` /users/profile

**Description:** Get user profile

**URL:** `https://api.telemedicine.moscow/v1/users/profile`

**Authentication:** Bearer Token (Required)


### 🟨 `PUT` /users/profile

**Description:** Update user profile

**URL:** `https://api.telemedicine.moscow/v1/users/profile`

**Authentication:** Bearer Token (Required)


### 🟨 `PUT` /users/password

**Description:** Change password

**URL:** `https://api.telemedicine.moscow/v1/users/password`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /users/preferences

**Description:** Get preferences

**URL:** `https://api.telemedicine.moscow/v1/users/preferences`

**Authentication:** Bearer Token (Required)


### 🟨 `PUT` /users/preferences

**Description:** Update preferences

**URL:** `https://api.telemedicine.moscow/v1/users/preferences`

**Authentication:** Bearer Token (Required)


## Video Calls

### 🟩 `POST` /video-calls/initialize

**Description:** Initialize video call

**URL:** `https://api.telemedicine.moscow/v1/video-calls/initialize`

**Authentication:** Bearer Token (Required)


### 🟦 `GET` /video-calls/{call_session_id}/stats

**Description:** Get call stats

**URL:** `https://api.telemedicine.moscow/v1/video-calls/{call_session_id}/stats`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `call_session_id` (string, required)


### 🟩 `POST` /video-calls/{call_session_id}/end

**Description:** End call

**URL:** `https://api.telemedicine.moscow/v1/video-calls/{call_session_id}/end`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `call_session_id` (string, required)


### 🟩 `POST` /video-calls/{call_session_id}/record

**Description:** Record call

**URL:** `https://api.telemedicine.moscow/v1/video-calls/{call_session_id}/record`

**Authentication:** Bearer Token (Required)

**Path Parameters:**

- `call_session_id` (string, required)


