# Patient Appointment Booking & Doctor Dashboard Guide

## 📋 Complete Flow Overview

### **PATIENT SIDE:**
1. Patient navigates to `/find-doctor/`
2. Patient searches for a doctor by specialty or disease
3. Patient sees list of approved doctors
4. Patient clicks "Book Appointment" → Redirected to `/book-appointment/?doctor_id=X`
5. **BOOKING FORM PAGE APPEARS** with:
   - ✅ Doctor information (left side) - sticky/fixed
   - ✅ Booking form (right side) - with all required fields
6. Patient fills the form:
   - 📅 Appointment Date & Time
   - 🏥 Disease/Condition (optional)
   - 💬 Consultation Type (Video, Audio, In-Person)
   - 📝 Symptoms/Notes
7. Patient clicks "✓ Book Appointment" button
8. Form submits to → `POST /api/appointments/appointments/book/`
9. ✅ Success message appears
10. 🔄 Redirects to `/dashboard/` after 2 seconds

---

### **DOCTOR SIDE:**
Once appointment is created:

1. Doctor logs in to `/dashboard/`
   - ✅ Dashboard shows **"📅 Upcoming Appointments"** count
   - ✅ Shows next appointment details
   - ✅ Quick action button: **"📋 View Appointments"**

2. Doctor clicks **"📋 View Appointments"** → `/doctor-appointments/`
   - ✅ Appointment appears in **"📅 Upcoming"** tab
   - ✅ Shows patient information:
     - Patient name & ID
     - Medical history
     - Allergies
     - Current conditions
     - Patient's symptoms/notes from booking
   
3. Doctor can perform actions:
   - ✅ **"✓ Mark Complete"** - End consultation
   - ✅ **"💊 Write Prescription"** - Add medications
   - ✅ **"📝 Add Notes"** - Document consultation
   - ✅ **"✕ Cancel"** - Cancel if needed

---

## 🔑 Key URLs

| Page/Action | URL | Who | Purpose |
|-----------|-----|-----|---------|
| Find Doctors | `/find-doctor/` | Patient | Search & select doctor |
| **Book Appointment Form** | `/book-appointment/?doctor_id=X` | Patient | **FILL FORM & SUBMIT** |
| My Appointments | `/my-appointments/` | Patient | Manage own appointments |
| Doctor Appointments | `/doctor-appointments/` | Doctor | View & manage appointments |
| Doctor Patients List | `/doctor-patients/` | Doctor | View all patients |
| Dashboard | `/dashboard/` | Both | See overview stats |

---

## 📝 Booking Form Fields

When patient clicks "Book Appointment", the form has these fields:

### **Required Fields:**
1. **Appointment Date** ⚠️ 
   - Type: DateTime picker
   - Minimum: Tomorrow (automatically set)
   - Format: YYYY-MM-DD HH:MM
   - Example: 2026-03-26 14:30

2. **Consultation Type** ⚠️
   - Video Call (default)
   - Audio Call
   - In Person
   - Required

3. **Symptoms/Notes** ⚠️
   - Textarea with placeholder
   - Detailed description of symptoms
   - Helps doctor prepare

### **Optional Fields:**
4. **Disease/Condition**
   - Dropdown menu
   - Select from available diseases
   - Not required

---

## ✅ Form Submission Flow

```
Patient Clicks "Book Appointment" Button
                    ↓
JavaScript validates required fields
                    ↓
Converts datetime-local to ISO format
                    ↓
Creates JSON payload with:
  - doctor_id: From URL parameter
  - appointment_date: ISO datetime string
  - consultation_type: Selected type
  - notes: Symptoms/notes text
  - disease_id: Optional
                    ↓
POST to /api/appointments/appointments/book/
                    ↓
Backend creates Appointment record
                    ↓
Links Patient → Doctor via Appointment
                    ↓
Sets status: 'scheduled'
                    ↓
Returns appointment details
                    ↓
Shows success message
                    ↓
Redirects to /dashboard/ after 2 seconds
```

---

## 🏥 Doctor Sees Appointment

### **In Doctor's Dashboard (`/dashboard/`):**
```
Stat Cards will show:
  • 📅 Upcoming Appointments: 1 (just booked)
  • ✅ Completed Consultations: 0
  • Quick Action: "📋 View Appointments"
```

### **In Doctor Appointments Page (`/doctor-appointments/`):**
```
📅 Upcoming Tab will display:
┌─────────────────────────────────┐
│ Patient Name                     │
│ [status: Scheduled]              │
├─────────────────────────────────┤
│ 📅 Date & Time: Mar 26, 14:30   │
│ 🏥 Condition: Headache           │
│ 💬 Type: Video Call              │
├─────────────────────────────────┤
│ 🔍 Patient Information:          │
│ • Email: patient@example.com     │
│ • Medical History: ...           │
│ • Allergies: None known          │
│ • Current Conditions: ...        │
├─────────────────────────────────┤
│ 📝 Patient Notes:                │
│ Experiencing severe headaches... │
├─────────────────────────────────┤
│ Buttons:                         │
│ ✓ Mark Complete                  │
│ 💊 Write Prescription            │
│ 📝 Add Notes                     │
│ ✕ Cancel                         │
└─────────────────────────────────┘
```

---

## 🔄 What Happens After Patient Submits

### **Immediately After:**
1. ✅ Appointment saved to database
2. ✅ Links patient & doctor together
3. ✅ Sets appointment status to **'scheduled'**
4. ✅ Stores date, time, consultation type, notes

### **Doctor Can See:**
- ✅ In Dashboard → Upcoming count increases
- ✅ In `/doctor-appointments/` → Appointment appears in Upcoming tab
- ✅ Via API → `/api/appointments/doctor/patients/`

### **Patient Can See:**
- ✅ In Dashboard → Upcoming appointment appears
- ✅ In `/my-appointments/` → Can reschedule or cancel

---

## 🧪 Testing the Complete Flow

### **Test Data Created:**
```
Patient Account:
  Email: testpatient@example.com
  Role: Patient

Doctor Account:
  Email: dr.nabish@example.com
  Role: Doctor (Approved)
  Specialization: Neurology
```

### **To Test:**

1. **Login as Patient**
   - Email: testpatient@example.com
   - Go to `/find-doctor/`
   - Search for Neurology

2. **Click Doctor Name** → Doctor Info Page
   - Shows Dr. Nabish Yadav
   - Click "Book Appointment"

3. **Fill Booking Form**
   - Date: Select tomorrow 2:00 PM
   - Disease: Select any disease
   - Type: Choose "Video Call"
   - Notes: "I have a headache"
   - Click "✓ Book Appointment"

4. **See Success**
   - ✅ "Appointment booked successfully!"
   - 🔄 Redirects to Dashboard after 2 seconds
   - Shows appointment in "Upcoming Appointments"

5. **Doctor Logs In**
   - Email: dr.nabish@example.com
   - Go to `/dashboard/`
   - Should see: "📅 Upcoming Appointments: 1"
   - Click "📋 View Appointments"
   - Should see patient appointment in Upcoming tab
   - Can click buttons to manage

---

## 🐛 Troubleshooting

### **Form Not Visible**
- ✅ Scroll right (especially on mobile)
- ✅ Check browser zoom (100%)
- ✅ Refresh page (Ctrl+F5)
- ✅ Check browser console for errors (F12)

### **Form Submission Fails**
- ❌ Check all required fields are filled
- ❌ Check date is set to future date
- ❌ Check internet connection
- ❌ Look for CSRF token error in console

### **Appointment Not Appearing**
- ❌ Verify doctor is "approved" in admin
- ❌ Verify appointment date is in future
- ❌ Refresh doctor's page
- ❌ Check appointment status is "scheduled"

### **Check API Response**
```
Browser Console (F12):
- Look for successful POST to /api/appointments/appointments/book/
- Response should be 201 Created
- Should show appointment details in response
```

---

## 📱 Responsive Design

### **Desktop (1200px+)**
- Doctor card (left) - Sticky
- Form (right) - Scrollable
- Two column layout

### **Tablet (768px - 1199px)**
- May stack to single column
- Both visible when scrolling

### **Mobile (<768px)**
- Single column layout
- Doctor info first, then form
- Scroll down to see booking form

---

## 🎯 Expected Behavior Checklist

- [x] Patient can access `/find-doctor/`
- [x] Patient can search and find doctors
- [x] Patient can click "Book Appointment"
- [x] Patient sees `/book-appointment/?doctor_id=X` page
- [x] **Doctor information displays** (left side)
- [x] **Booking form displays** (right side)
- [x] **All form fields visible** (Date, Type, Disease, Notes)
- [x] **Submit button clickable** and styled
- [x] Form validates on submit (required fields)
- [x] **API call succeeds** (POST to /api/appointments/appointments/book/)
- [x] Success message appears
- [x] Redirects to `/dashboard/`
- [x] Doctor sees appointment in `/doctor-appointments/`
- [x] Appointment shows in "Upcoming" tab
- [x] Doctor can click "Mark Complete"
- [x] Doctor can click "Write Prescription"
- [x] Doctor can click "Add Notes"

---

## 📊 Database Schema

### **Appointment Table:**
```
Appointment Record:
├─ id: Auto increment
├─ patient: FK → PatientProfile
├─ doctor: FK → DoctorProfile
├─ disease: FK → Disease (nullable)
├─ appointment_date: DateTime (patient selected)
├─ consultation_type: Char (video/audio/in_person)
├─ notes: Text (patient's symptoms)
├─ status: Char (scheduled/completed/cancelled)
├─ created_at: DateTime (auto)
└─ updated_at: DateTime (auto)
```

### **Status Flow:**
```
Patient Books
     ↓
'scheduled' (Waiting for doctor)
     ↓
Doctor Actions:
├─ Mark Complete → 'completed'
├─ Cancel → 'cancelled'
└─ Wait/Reschedule → stays 'scheduled'
```

---

## 🔐 Security Features

- ✅ CSRF token protection on form
- ✅ User authentication required
- ✅ Patient can only book with approved doctors
- ✅ Doctor can only see own appointments
- ✅ Appointment validation before creation
- ✅ Proper error handling and messages

---

## 📞 Support

If the form is not visible:
1. **Check browser console** → F12 → Console tab
2. **Look for JavaScript errors**
3. **Check Network tab** → See if page loaded correctly
4. **Try hard refresh** → Ctrl+Shift+Delete (Clear cache) then Ctrl+F5
5. **Check browser compatibility** → Works in Chrome, Firefox, Edge

---

## ✨ Summary

The appointment booking system is **fully functional** with:

✅ Patient booking form with all fields
✅ Real-time submission via API  
✅ Appointment appears in doctor dashboard
✅ Doctor can manage appointments
✅ Full patient information visible to doctor
✅ Prescription and notes support
✅ Responsive design for all devices
✅ Complete error handling
✅ Success/failure messages

**The form is there and ready to use!**

Generated: March 24, 2026
Status: ✅ COMPLETE AND TESTED
