# New Features Documentation

## Overview
This update adds powerful features to connect patients with appropriate doctors based on medical specialization and disease conditions. Patients can now quickly find doctors, and doctors can view their assigned patients with complete medical information.

---

## ✨ New Features

### 1. **Patient Quick Action - Find Doctor**

#### Access Path
- URL: `/find-doctor/`
- Dashboard Button: "🏥 Find Doctor" (shown in quick actions after login)

#### Features
- **Search by Specialty**: Filter doctors by their medical specialization
  - Cardiology
  - Neurology
  - Orthopedics
  - Dermatology (Skin)
  - Gynecology
  - Psychiatry
  - Pediatrics
  - General Practitioner

- **Search by Disease**: Find doctors based on patient's condition
  - Input disease name (e.g., "Skin Disease", "Heart Problem")
  - System automatically recommends doctors with appropriate specialization
  - System maps diseases to required specialist automatically

- **Get Recommendations**: View personalized doctor suggestions
  - Based on current medical conditions in patient profile
  - Shows doctors sorted by rating and experience
  - Available doctors only (is_available = True)

#### Doctor Display Information
For each doctor, patients can see:
- Full name and specialization
- Years of professional experience
- Rating (1-5 stars)
- Consultation fee
- Professional qualifications
- Professional biography
- Availability status
- Clinic address and phone number

#### Booking an Appointment
- Click "Book Appointment" button on any doctor's card
- Redirects to appointment booking page
- Doctor information is pre-selected

---

### 2. **Doctor Dashboard - View Assigned Patients**

#### Access Path
- URL: `/doctor-patients/`
- Available only to users with doctor role

#### Features
- **Patient List**: Display all patients who have booked appointments
- **Patient Cards** show:
  - Patient name and email
  - Disease/condition being treated
  - Current health status
  - Appointment date and time
  - Appointment status (Scheduled/Completed/Cancelled/No Show)
  - Patient's consultation notes

#### Detailed Patient View
- Click "View Full Details" button to open detailed modal with:
  - Personal Information
  - Current medical conditions
  - Complete medical history
  - Known allergies
  - Consultation notes from the appointment

#### Filtering and Sorting
- Patients are filtered by appointment status (scheduled/completed)
- Can view full patient medical profile
- Status indicators with color coding:
  - Blue: Scheduled
  - Green: Completed
  - Red: Cancelled
  - Gray: No Show

---

### 3. **Appointment System** (Backend)

#### Models Created
1. **Disease Model**
   - Disease name (unique)
   - Description
   - Recommended specialization
   - 15 pre-loaded common diseases

2. **Appointment Model**
   - Links patient with doctor
   - Tracks disease/condition
   - Appointment date and time
   - Status tracking
   - Consultation type (Video/Audio/In-Person)
   - Patient notes/concerns
   - Timestamps

#### Available Diseases
Pre-loaded diseases include:
- Heart Disease, Hypertension
- Diabetes
- Skin Disease, Acne, Psoriasis
- Headache, Migraine
- Back Pain, Joint Pain
- Anxiety Disorder, Depression
- Childhood Illness
- Cold and Flu, Cough

---

## 🔌 API Endpoints

### Appointment API (Base URL: `/api/appointments/`)

#### 1. Search Doctors by Specialty
```
GET /doctors/search/?specialty=dermatology
GET /doctors/search/?disease=Skin%20Disease
```
**Response**: List of available doctors with full details

#### 2. Get All Diseases
```
GET /diseases/
```
**Response**: List of all diseases with specialization recommendations

#### 3. Get Recommended Doctors
```
GET /doctors/recommended/
```
**Auth Required**: Patient only
**Response**: Doctors recommended based on patient's current diseases

#### 4. Book Appointment
```
POST /appointments/book/
```
**Auth Required**: Patient only
**Body**:
```json
{
  "doctor_id": 1,
  "appointment_date": "2026-03-25T10:30:00Z",
  "disease_id": 2,
  "notes": "Patient complaints about skin condition"
}
```

#### 5. Get My Appointments
```
GET /appointments/my/
```
**Auth Required**: Patient only
**Response**: List of patient's appointments

#### 6. Get Doctor's Patients
```
GET /doctor/patients/
```
**Auth Required**: Doctor only
**Response**: List of patients assigned to this doctor

---

## 📊 Database Changes

### New Tables Created
1. `appointments_disease` - Disease catalog
2. `appointments_appointment` - Appointment bookings

### Modified Tables
1. `users_patientprofile` - Added field:
   - `current_diseases` (TextField) - Patient's current health conditions

---

## 🚀 How to Use

### For Patients:
1. Log in to dashboard
2. Click "🏥 Find Doctor" button in Quick Actions
3. Choose search method:
   - By specialty (e.g., Dermatology for skin issues)
   - By disease name (e.g., "Acne")
   - Get recommendations based on profile
4. View doctors matching criteria
5. Click "Book Appointment" on desired doctor
6. Complete appointment booking with:
   - Appointment date/time
   - Disease/condition
   - Any symptoms or notes

### For Doctors:
1. Log in to dashboard
2. Go to `/doctor-patients/` or find link in navigation
3. View all patient assignments
4. Click on patient for detailed medical information including:
   - Medical history
   - Current conditions
   - Allergies
   - Consultation notes
5. Manage appointment statuses

---

## 🔒 Security & Permissions

- Patient features protected: `IsAuthenticated` + `IsPatient` permission
- Doctor features protected: `IsAuthenticated` + `IsDoctor` permission
- Database queries optimized with `select_related()` for performance
- CSRF protection on all forms
- Authentication via token or session

---

## 📝 Management Commands

### Load Initial Diseases
```bash
python manage.py load_diseases
```
This command:
- Creates 15 common diseases
- Maps each disease to appropriate medical specialization
- Skips existing diseases (safe to run multiple times)

---

## 🎨 Templates Created

1. **find-doctor.html** - Patient doctor search interface
2. **doctor-patients.html** - Doctor patient management dashboard

Both templates include:
- Responsive design
- Bootstrap-style CSS
- Interactive JavaScript for API calls
- Modal windows for detailed views
- Status indicators with color coding
- Loading states

---

## 📱 Features Summary

| Feature | Patient | Doctor | Guest |
|---------|---------|--------|-------|
| Find Doctor | ✅ | ❌ | ❌ |
| Search by Specialty | ✅ | ❌ | ❌ |
| Search by Disease | ✅ | ❌ | ❌ |
| Book Appointment | ✅ | ❌ | ❌ |
| View My Appointments | ✅ | ❌ | ❌ |
| View Assigned Patients | ❌ | ✅ | ❌ |
| Patient Medical Info | ❌ | ✅ | ❌ |

---

## 🔧 Technical Details

### Dependencies Used
- Django REST Framework
- Django ORM
- JavaScript Fetch API
- HTML5/CSS3

### Performance Optimizations
- Database queries use `select_related()` for efficiency
- Indexes on commonly filtered fields (specialization, is_available, status)
- Pagination-ready API design

### Code Structure
```
appointments/
├── models.py (Disease, Appointment models)
├── views.py (API views for appointments)
├── serializers.py (DRF serializers)
├── urls.py (Appointment endpoints)
├── admin.py (Admin interface)
└── management/commands/
    └── load_diseases.py (Data management)

templates/
├── find-doctor.html (Patient interface)
└── doctor-patients.html (Doctor interface)
```

---

## 🐛 Troubleshooting

### Diseases not showing?
- Run: `python manage.py load_diseases`

### API returns 401 Unauthorized?
- Ensure user is authenticated
- Check user role matches endpoint requirements

### Appointments not showing?
- Verify appointment dates are in future
- Check status filter in query

---

## 📞 Support

For issues or feature requests related to:
- Doctor discovery: Check `/find-doctor/` page
- Patient management: Check `/doctor-patients/` page
- API errors: Check response status codes and error messages

---

## Version
- **Feature Version**: 1.0
- **Release Date**: March 24, 2026
- **Status**: Production Ready

---

## Future Enhancements
- Video/Audio consultation integration
- Real-time appointment scheduling
- Email notifications
- Review and rating system
- Payment integration
- Prescription management
