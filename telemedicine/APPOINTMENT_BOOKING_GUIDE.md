# Telemedicine Platform - Testing & Verification Guide

## ✅ System Status

### Appointment Booking System - FIXED ✅
- **URL:** `/book-appointment/?doctor_id=<ID>`
- **Form:** Collects appointment details with validation
- **API Endpoint:** `/api/appointments/appointments/book/`
- **Database:** Appointments now being created correctly

### Admin Management - WORKING ✅
- **URL:** `/admin-doctors/` - List all doctors
- **URL:** `/admin-doctor/<ID>/` - View specific doctor + patients
- **Shows:** All patients assigned to each doctor with their diseases

### Doctor Dashboard - WORKING ✅
- **URL:** `/doctor-patients/` - View only for approved doctors
- **Data:** API endpoint retrieves all patients

---

## 🧪 Testing Workflow

### Step 1: Create Test Appointment (DONE)
- Test appointment created in database
- Patient: Ram Dam
- Doctor: Dr. Rachel Nelson (Dermatologist)
- Disease: Skin Condition
- Status: Scheduled

### Step 2: Verify Admin Can See Patient
1. **Login as Admin:**
   - URL: `http://localhost:8000/admin/`
   - Username: `admin`
   - Password: `Admin123456`

2. **Navigate to Manage Doctors:**
   - Click "Manage Doctors" from dashboard or go to `/admin-doctors/`
   - Find "Dr. Rachel Nelson"
   - Click "View Profile"

3. **Expected Result:**
   - Shows doctor details
   - Shows section: "👥 Assigned Patients (1)"
   - Patient "Ram Dam" should appear with:
     - Email, phone, DOB
     - Disease: Skin disease
     - Appointment count: 1

### Step 3: Verify Doctor Can See Patients
1. **Login as Doctor:**
   - Email: (use existing doctor account)
   - Password: (same as registration)

2. **Go to Doctor Dashboard:**
   - URL: `/doctor-patients/`
   - Should show patient list with diseases

### Step 4: Patient Books Real Appointment
1. **Login as Patient:**
   - Use patient account

2. **Find Doctor:**
   - Go to `/find-doctor/`
   - Search by specialty or disease
   - Find dermatologist

3. **Book Appointment:**
   - Click "Book Appointment"
   - Should redirect to `/book-appointment/?doctor_id=X`
   - Fill form:
     - Select future date/time
     - Select disease (e.g., "Skin Condition")
     - Select consultation type (Video, Audio, or In-Person)
     - Enter symptoms/notes
   - Click "Book Appointment"
   - Should redirect to dashboard with success message

4. **Verify in Admin:**
   - Go to Admin > Manage Doctors > Dr. Specific Doctor
   - Should see the new patient with appointment details

---

## 📊 Database Verification

### Check Appointments
```bash
cd telemedicine
..\venv\Scripts\python.exe manage.py shell -c "from appointments.models import Appointment; print(f'Total: {Appointment.objects.count()}')"
```

### Check Doctor-Patient Relationships
```bash
..\venv\Scripts\python.exe manage.py shell -c "from appointments.models import Appointment; from users.models import DoctorProfile; doctor = DoctorProfile.objects.filter(specialization='dermatology').first(); apps = Appointment.objects.filter(doctor=doctor); print(f'Dermatologist appointments: {apps.count()}')"
```

---

## 🔧 Key Components

### 1. Booking Form (`/book-appointment/?doctor_id=<ID>`)
- ✅ Displays doctor information
- ✅ Form validation
- ✅ DateTime-local input with minimum date set
- ✅ Disease selection
- ✅ Consultation type selection
- ✅ Symptoms/notes textarea
- ✅ JavaScript logging (open DevTools to see)

### 2. API Endpoint (`/api/appointments/appointments/book/`)
- ✅ Receives POST requests
- ✅ Validates doctor approval status
- ✅ Creates appointment in database
- ✅ Captures consultation_type field
- ✅ Returns success/error response

### 3. Admin Views
- ✅ `/admin-doctors/` - Doctor list with stats
- ✅ `/admin-doctor/<ID>/` - Doctor details + assigned patients
- ✅ Shows patient diseases and medical history
- ✅ Displays allergy warnings

### 4. Doctor Views
- ✅ `/doctor-patients/` - List of assigned patients
- ✅ API endpoint for fetching patient data
- ✅ Approval check before viewing

---

## 🐛 Debugging Tips

### If Appointments Not Showing:

1. **Check DevTools Console** (`F12 > Console`)
   - Should see form data and API response logs
   - Check for fetch errors

2. **Check Django Console**
   - Should see confirmation of API endpoint hit
   - Check for validation errors

3. **Check Database Directly**
   - Run shell command to verify appointment exists
   - Check appointment status is 'scheduled'

### Common Issues:

| Issue | Solution |
|-------|----------|
| "Appointment showing 0 patients" | Check appointment status in DB is 'scheduled' or 'completed' |
| "Doctor not appearing in search" | Check `is_approved=True` in admin or database |
| "Booking form gives 404" | Ensure URL format is `/appointments/book/?doctor_id=2` |
| "Form not submitting" | Open DevTools, check console for errors, check network tab |

---

## 📝 Next Steps (Optional)

1. Add notification system for doctors when new appointments are booked
2. Add appointment status updates (completed, cancelled, no-show)
3. Add appointment reminders
4. Add review/rating system for doctors
5. Add prescription management system

---

## 📞 Support Commands

### Run Server
```bash
cd telemedicine
..\venv\Scripts\python.exe manage.py runserver
```

### Access Admin
- URL: `http://localhost:8000/admin/`
- Username: `admin`
- Password: `Admin123456`

### Check All Appointments
```bash
..\venv\Scripts\python.exe manage.py shell -c "from appointments.models import Appointment; [print(f'{a.patient.user.get_full_name()} -> {a.doctor.user.get_full_name()} | {a.status}') for a in Appointment.objects.all()]"
```

