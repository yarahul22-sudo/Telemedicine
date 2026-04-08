# 🔧 BOOKING FORM - QUICK TEST GUIDE

## ✅ What Was Fixed
- ✓ Added `testserver` to ALLOWED_HOSTS (needed for testing)
- ✓ Created test patient & doctor accounts
- ✓ Verified all 15 diseases are loaded
- ✓ Django server is now running

## 📋 Test Credentials

**Patient Account:**
- Email: `testpatient@example.com`
- Password: `testpass123`

**Doctor Account:**
- Email: `dr.nabish@example.com`
- Password: `doctorpass123`

---

## 🧪 How to Test the Booking Form

### **Step 1: Login as Patient**
1. Open: http://127.0.0.1:8000/login/
2. Enter email: `testpatient@example.com`
3. Enter password: `testpass123`
4. Click Login

### **Step 2: Access Booking Form**
1. Go to: http://127.0.0.1:8000/find-doctor/
2. You should see doctors list
3. Find "Dr. Nabish Ahmed" (Neurology specialist)
4. Click "Book Appointment" button

**OR directly access:**
```
http://127.0.0.1:8000/book-appointment/?doctor_id=6
```

### **Step 3: Check If Form Displays**
When you access the booking page, you should see:

**Left Side (Doctor Info - Sticky):**
- 👨‍⚕️ Doctor name: Dr. Nabish Ahmed
- Specialty: Neurology
- License number
- Experience, rating, fee
- Available days
- Qualification & bio

**Right Side (Booking Form - Scrollable):**
- 📅 Appointment Date (date/time picker)
- 🏥 Disease/Condition (dropdown - 15 options)
- 💬 Consultation Type (Video/Audio/In-Person)
- 📝 Symptoms/Notes (text area)
- ✓ Book Appointment (button)
- ← Back (button)

### **Step 4: Fill & Submit Form**
1. Select appointment date/time (must be tomorrow or later)
2. Select disease (optional)
3. Select consultation type (required)
4. Enter symptoms/notes (required)
5. Click "✓ Book Appointment"
6. You should see: "✓ Appointment booked successfully! Redirecting..."
7. Redirected to dashboard

### **Step 5: Verify Doctor Sees Appointment**
1. Login as doctor: `dr.nabish@example.com` / `doctorpass123`
2. Go to: http://127.0.0.1:8000/doctor-appointments/
3. Click "Upcoming" tab
4. You should see the appointment you just booked
5. Should show patient info, date, disease, consultation type, symptoms

---

## ✨ What Should Display

### **Booking Form Page Layout:**
```
┌─────────────────────────────────────────────────────┐
│                    Telemedicine                      │
│                Dashboard | Appointments | Logout     │
└─────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────────────────────┐
│   DOCTOR     │  │   BOOKING FORM               │
│   INFO       │  │                              │
│   (Sticky)   │  │  📅 Appointment Date   [  ]   │
│              │  │  🏥 Disease/Condition [ ▼ ]  │
│ Dr. Nabish   │  │  💬 Consultation Type [ ▼ ]  │
│ Neurology    │  │  📝 Symptoms/Notes   [     ]  │
│ License: ... │  │                              │
│ Experience:  │  │  [✓ Book] [← Back]          │
│ 10 years     │  │                              │
│ Rating: ⭐5  │  │  ✓ Loading spinner shown    │
│ Fee: $50     │  │    during submission         │
│ Available:   │  │                              │
│ Mon-Fri      │  =  [Success/Error Message]    │
│ Qualif: MD   │  │                              │
│              │  │ [Form fields with labels]    │
│ Bio: ...     │  │                              │
└──────────────┘  └──────────────────────────────┘
```

---

## ❓ Troubleshooting

### **Form Not Displaying?**
- [ ] Are you logged in as patient?
- [ ] Is the doctor ID valid (6)?
- [ ] Check browser console (F12 → Console tab) for errors
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Refresh page (Ctrl+F5)

### **"Doctor not approved" Error?**
- Doctor is automatically marked as approved
- Check if you're using correct doctor ID (6)

### **Nothing appears on right side?**
- Scroll down/right on the page
- Check if browser width is narrow (may stack vertically on mobile)
- Hit F12 and check responsive design mode

### **Form fields missing?**
- Hard refresh: Ctrl+Shift+Delete
- Make sure JavaSc ript is enabled
- Check browser console for errors

---

## 🔍 Form Fields Checklist

When form loads, you should see ALL of these:

- [ ] Appointment Date field (says "Select a date and time...")
- [ ] Disease/Condition field (dropdown with 15+ options)
- [ ] Consultation Type field (Video Call, Audio Call, In Person)
- [ ] Symptoms/Notes field (large text area)
- [ ] "✓ Book Appointment" button (blue)
- [ ] "← Back" button (gray)

---

## 📊 API Endpoint Being Used

The form submits to:
```
POST /api/appointments/appointments/book/
```

**Expected Success Response:**
- Status: 201 Created
- Message: "Appointment booked successfully"
- Redirect: To `/dashboard/`

---

## 🎯 What Happens After Booking

1. **Patient Dashboard:**
   - "Upcoming Appointments" shows 1
   - Appointment appears in My Appointments page

2. **Doctor Dashboard:**
   - Goes to `/doctor-appointments/`
   - Appears in "Upcoming" tab immediately
   - Shows full patient information
   - Can mark complete, write prescription, add notes

---

## 📝 Notes

- Server is running at: http://127.0.0.1:8000/
- ALLOWED_HOSTS has been updated to support testing
- Test data is loaded and ready
- All 15 diseases are available in dropdown
- Doctor account is pre-approved

**Now test the booking form and let me know what you see!**

