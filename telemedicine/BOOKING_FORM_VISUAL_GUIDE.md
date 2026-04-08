# Patient Booking Form - Visual Guide

## 📸 What You Should See

### **Step 1: Find Doctor Page (`/find-doctor/`)**

The page displays:
```
┌─────────────────────────────────────┐
│         Find a Doctor               │
│                                     │
│  Search: [Specialty dropdown ____]  │
│  Search: [Disease dropdown ______]  │
│                                     │
│  ─────────────────────────────────  │
│  Doctor Cards Grid:                 │
│                                     │
│  ┌──────────┐ ┌──────────┐         │
│  │ Dr. Name │ │ Dr. Name │         │
│  │ Specialty│ │ Specialty│         │
│  │ Rating ⭐ │ │ Rating ⭐ │         │
│  │[BOOK APP]│ │[BOOK APP]│         │
│  └──────────┘ └──────────┘         │
│                                     │
└─────────────────────────────────────┘
```

### **Step 2: Click "BOOK APPOINTMENT" Button**

When you click the button near a doctor's card:
- URL changes to: `/book-appointment/?doctor_id=123`
- Page loads with TWO sections

---

## 🔑 **BOOKING FORM PAGE - TWO COLUMN LAYOUT**

### **LEFT COLUMN** (Sticky - doesn't scroll)
```
┌───────────────────────────────────────┐
│  👨‍⚕️ Doctor Information                 │
├───────────────────────────────────────┤
│                                       │
│          Dr. Nabish Yadav            │
│          Neurology                   │
│                                       │
│  License: 2550                       │
│  Experience: 2 years                 │
│  Rating: ⭐ 5.0/5.0                   │
│  Fee: $0.00                          │
│  Available: Mon-Fri                  │
│  Qualification:                      │
│    [Doctor's credentials...]         │
│                                       │
│  Bio:                                │
│    [Doctor's biography...]           │
│                                       │
└───────────────────────────────────────┘
```

### **RIGHT COLUMN** (Main - scrollable)
```
┌───────────────────────────────────────┐
│  📅 Book Appointment                   │
├───────────────────────────────────────┤
│                                       │
│  ✓ Success/Error Messages Here       │
│                                       │
│  📅 Appointment Date *                │
│  ⊞ [Date/Time Picker ___]            │
│  Select within doctor hours           │
│                                       │
│  🏥 Disease/Condition                 │
│  ↓ [-- Select or leave blank --]    │
│     Headache                          │
│     Fever                             │
│     Back Pain                         │
│                                       │
│  💬 Consultation Type *               │
│  ↓ [-- Select Type --]               │
│     Video Call ✓                      │
│     Audio Call                        │
│     In Person                         │
│                                       │
│  📝 Symptoms/Notes *                  │
│  ⊞ [_____________________]            │
│  [_____________________]              │
│  [_____________________]              │
│  Describe symptoms...                 │
│                                       │
│  ┌─────────────┬──────────────┐      │
│  │✓ Book Appt  │ ← Back       │      │
│  └─────────────┴──────────────┘      │
│                                       │
│  [Loading spinner if submitting]     │
│                                       │
└───────────────────────────────────────┘
```

---

## 📋 Form Fields Explained

### **1. Appointment Date** ⚠️ REQUIRED
- **Type**: Date and Time picker
- **Min Date**: Tomorrow (auto-set)
- **Format**: Click to open calendar
- **Example**: 26/03/2026 2:30 PM
- **Why**: You must select when you want to meet the doctor

### **2. Disease/Condition** ✓ OPTIONAL
- **Type**: Dropdown menu
- **Options**: Lists all diseases from system
- **Default**: "-- Select or leave blank --"
- **Why**: Helps doctor see why you're visiting

### **3. Consultation Type** ⚠️ REQUIRED
- **Type**: Dropdown menu  
- **Options**:
  - Video Call (phone/video chat)
  - Audio Call (phone call only)
  - In Person (face-to-face)
- **Default**: None (must select)
- **Why**: Doctor needs to know meeting format

### **4. Symptoms/Notes** ⚠️ REQUIRED
- **Type**: Large text area (multiple lines)
- **Placeholder**: "Describe your symptoms..."
- **Why**: Doctor reads this to prepare for appointment
- **Example**: "I have had a severe headache for 3 days, with sensitivity to light"

---

## ✅ Form Validation

The form checks:

```
When you click "✓ Book Appointment":

✓ Check: Appointment date selected? 
  ✗ If NO → Shows: "Please fill in all required fields"
  ✓ If YES → Continue

✓ Check: Consultation type selected?
  ✗ If NO → Shows: "Please fill in all required fields"
  ✓ If YES → Continue

✓ Check: Symptoms/Notes filled?
  ✗ If NO → Shows: "Please fill in all required fields"
  ✓ If YES → Continue

All checks passed?
  → Shows loading spinner: "Booking appointment..."
  → Sends form to API: POST /api/appointments/appointments/book/
  → Waits for response...
```

---

## 🎯 Submission Flow

### **Step by Step:**

```
1️⃣  Patient fills form
    ↓
2️⃣  Patient clicks "✓ Book Appointment" button
    ↓
3️⃣  JavaScript validates form
    ✗ Error? → Shows red error message (stay on form)
    ✓ Valid? → Continue to step 4
    ↓
4️⃣  Loading spinner appears
    "Booking appointment..."
    ↓
5️⃣  Form data converts to JSON:
    {
      "doctor_id": 2,
      "appointment_date": "2026-03-26T14:30:00",
      "disease_id": 5,
      "notes": "I have a severe headache",
      "consultation_type": "video"
    }
    ↓
6️⃣  Sends to API: POST /api/appointments/appointments/book/
    ↓
7️⃣  Backend processes:
    - Checks patient exists ✓
    - Checks doctor exists ✓
    - Checks doctor approved ✓
    - Creates Appointment record ✓
    - Returns: 201 CREATED
    ↓
8️⃣  Success message appears:
    "✓ Appointment booked successfully!
     Redirecting to dashboard..."
    ↓
9️⃣  Wait 2 seconds...
    ↓
🔟  Redirects to: /dashboard/
    Dashboard now shows:
    - "📅 Upcoming Appointments: 1"
    - Shows appointment in upcoming section
```

---

## 📺 What Happens After Booking

### **Patient Sees:**

**On Dashboard (`/dashboard/`)**
```
┌─────────────────────────────────────┐
│  Welcome, John! 👋                  │
│                                     │
│  📅 Upcoming Appointments: 1         │
│  ✅ Completed Consultations: 0      │
│  💊 Active Prescriptions: 0         │
│  🔔 Notifications: 0                │
│                                     │
│  📅 Your Upcoming Appointments      │
│  ┌─────────────────────────────────┐│
│  │ Dr. Nabish Yadav                ││
│  │ Neurology                        ││
│  │ 📅 Mar 26, 2026 14:30           ││
│  │ Status: Scheduled ✓             ││
│  │ [Manage →]                      ││
│  └─────────────────────────────────┘│
│                                     │
└─────────────────────────────────────┘
```

**On My Appointments (`/my-appointments/`)**
```
┌─────────────────────────────────────┐
│  📅 My Appointments                  │
│                                     │
│  Tabs: 📅 Upcoming | ✅ Completed   │
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Dr. Nabish Yadav                ││
│  │ Headache                         ││
│  │                                  ││
│  │ 📅 Mar 26, 14:30                 ││
│  │ 🏥 Neurology                     ││
│  │ 💬 Video Call                    ││
│  │                                  ││
│  │ 🔄 Reschedule  ✕ Cancel        ││
│  └─────────────────────────────────┘│
│                                     │
└─────────────────────────────────────┘
```

### **Doctor Sees:**

**On Dashboard (`/dashboard/`)**
```
┌─────────────────────────────────────┐
│  📅 Upcoming Appointments: 1 ← NEW! │
│  ✅ Completed Consultations: 0      │
│  🔔 Notifications: 0                │
│                                     │
│  [📋 View Appointments →]           │
│                                     │
└─────────────────────────────────────┘
```

**On Doctor Appointments (`/doctor-appointments/`)**
```
┌─────────────────────────────────────┐
│  📅 My Appointments                  │
│                                     │
│  Tabs: 📅 Upcoming(1) | ✅ Completed│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 📋 John Patient                  ││
│  │ [Status: Scheduled]              ││
│  │                                  ││
│  │ 📅 Mar 26, 2026 14:30           ││
│  │ 🏥 Headache                      ││
│  │ 💬 Video Call                    ││
│  │                                  ││
│  │ 🔍 Patient Information:          ││
│  │ Email: john@example.com          ││
│  │ Allergies: Penicillin            ││
│  │ History: Previous headaches      ││
│  │ Current Conditions: Under stress ││
│  │                                  ││
│  │ 📝 Patient Notes:                ││
│  │ "Severe headache for 3 days..."  ││
│  │                                  ││
│  │ Buttons:                         ││
│  │ [✓ Mark Complete]                ││
│  │ [💊 Write Prescription]          ││
│  │ [📝 Add Notes]                   ││
│  │ [✕ Cancel]                       ││
│  └─────────────────────────────────┘│
│                                     │
└─────────────────────────────────────┘
```

---

## 🔍 Viewing Source Code

If form is not visible, check:

### **Open Browser Inspector (F12)**

```
Console Tab:
  Look for JavaScript errors
  Should see form loaded message

Network Tab:
  Look for: /book-appointment/ request
  Status should be: 200 OK
  
Elements Tab:
  Find: <form id="bookingForm">
  Should show form HTML
  All fields should be visible
```

### **Common Issues:**

| Issue | Solution |
|-------|----------|
| Form below fold | Scroll down on page |
| Form not visible | Hard refresh: Ctrl+Shift+Delete |
| Form fields missing | Check browser console for errors |
| Submit button disabled | Fill all required * fields first |
| Page shows blank | Check server is running |
| API error | Check doctor is approved by admin |

---

## ✨ Key Points

✅ **Form is always visible** when on `/book-appointment/?doctor_id=X`
✅ **Left side:** Doctor info (sticky, doesn't scroll)
✅ **Right side:** Booking form (scrolls)
✅ **Mobile:** Stacks vertically, form below doctor info
✅ **All fields required** unless marked optional
✅ **Submit sends to API** which creates appointment
✅ **Success redirects to dashboard** after 2 seconds
✅ **Doctor sees appointment** immediately in their dashboard
✅ **Both can manage** appointment after creation

---

## 🎓 Complete Example

### **Scenario: Patient Books Appointment**

```
1. Patient at /find-doctor/
2. Searches: "Neurology" 
3. Sees: "Dr. Nabish Yadav - 5.0★ - FREE"
4. Clicks: "Book Appointment"
5. Page loads: /book-appointment/?doctor_id=2

[LEFT]                          [RIGHT]
Doctor Info                     Booking Form
│                             │
Dr. Nabish Yadav              ├─ Appointment Date
Neurology                      ├─ Disease/Condition
License: 2550                  ├─ Consultation Type
Exp: 2 yrs                     ├─ Symptoms/Notes
Rating: 5.0/5                  └─ [Submit Button]
Fee: $0

6. Patient fills form:
   Date: Mar 26, 2026 14:30 ✓
   Disease: Headache ✓
   Type: Video Call ✓
   Notes: "Severe headache with light sensitivity" ✓

7. Clicks: "✓ Book Appointment"
8. Shows: "Booking appointment..." (loading)
9. Shows: "✓ Appointment booked!" (success)
10. Redirects to: /dashboard/
11. Dashboard shows: "📅 Upcoming Appointments: 1"

**MEANWHILE, DOCTOR:**
12. Doctor refreshes /dashboard/
13. Sees: "📅 Upcoming Appointments: 1 ← NEW"
14. Clicks: "📋 View Appointments"
15. Sees appointment in "Upcoming" tab
16. Can click: Mark Complete, Write Prescription, Add Notes
```

---

## 📞Summary

The booking form system works as follows:

1. ✅ Patient clicks "Book Appointment" on doctor card
2. ✅ Booking form page loads with two columns
3. ✅ Doctor info on left (sticky)
4. ✅ Booking form on right (scrollable)  
5. ✅ Patient fills form with required info
6. ✅ Patient clicks "✓ Book Appointment"
7. ✅ Form submits to API
8. ✅ Appointment appears in doctor dashboard
9. ✅ Doctor can manage appointment
10. ✅ Both can see prescription and notes

**Everything is working perfectly!**

Status: ✅ COMPLETE
