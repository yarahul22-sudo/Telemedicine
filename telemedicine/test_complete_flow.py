#!/usr/bin/env python
"""
Test the complete booking flow from find-doctor to booking form
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from django.test import Client
from users.models import CustomUser

print("\n" + "=" * 80)
print("TESTING COMPLETE BOOKING FLOW")
print("=" * 80)

client = Client()

# Setup user
user = CustomUser.objects.get(email='pshyam@telemedicine.com')
user.set_password('test123')
user.save()
client.force_login(user)

print(f"\n✓ Logged in as: {user.email} (Role: {user.role})")

# Test 1: Check find-doctor page
print("\n[Test 1] Accessing find-doctor page...")
response = client.get('/find-doctor/')
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    print(f"  ✓ Find Doctor page loads")
    content = response.content.decode('utf-8')
    if 'Book Appointment' in content and 'bookAppointment' in content:
        print(f"  ✓ Book Appointment button found in page")
else:
    print(f"  ✗ Error: {response.status_code}")

# Test 2: Try booking form with doctor_id=7
print("\n[Test 2] Accessing booking form (/book-appointment/?doctor_id=7)...")
response = client.get('/book-appointment/?doctor_id=7')
print(f"  Status: {response.status_code}")

if response.status_code == 200:
    print(f"  ✓ Booking form page loads!")
    
    content = response.content.decode('utf-8')
    
    # Check for form elements
    checks = {
        'Doctor name in page': 'dramlal' in content.lower(),
        'Booking form tag': 'id="bookingForm"' in content,
        'Appointment date field': 'appointment_date' in content,
        'Consultation type field': 'consultation_type' in content,
        'Notes field': 'id="notes"' in content,
        'Submit button': 'Book Appointment' in content,
    }
    
    print(f"\n  Form Elements Check:")
    all_present = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"    {status} {check_name}")
        if not result:
            all_present = False
    
    if all_present:
        print(f"\n  ✅ ALL FORM ELEMENTS PRESENT!")
        print(f"\n  The form IS displaying correctly.")
        print(f"\n  Possible issues:")
        print(f"    1. Browser cache - try Ctrl+Shift+Delete")
        print(f"    2. JavaScript not loading - check browser console (F12)")
        print(f"    3. Page taking time to load - wait a few seconds")
    else:
        print(f"\n  ❌ Some form elements missing")
        
elif response.status_code == 302:
    print(f"  ✗ Redirected (302)")
    print(f"  Location: {response.url}")
    print(f"  This means the page is redirecting before showing the form")
    
elif response.status_code == 404:
    print(f"  ✗ Page not found (404)")
    print(f"  The booking form template might not exist")
    
else:
    print(f"  ✗ Error: {response.status_code}")

# Test 3: Check all approved doctors
print("\n[Test 3] Checking approved doctors...")
from users.models import DoctorProfile

approved = DoctorProfile.objects.filter(is_approved=True)
print(f"  Approved doctors: {approved.count()}")

for i, doc in enumerate(approved[:3], 1):
    print(f"    {i}. {doc.user.email} (ID: {doc.id}) - {doc.get_specialization_display()}")

# Test 4: Try with different doctor_id
print("\n[Test 4] Testing with different doctor IDs...")
for doc_id in [1, 6, 7, 9]:
    response = client.get(f'/book-appointment/?doctor_id={doc_id}')
    status = "✓" if response.status_code == 200 else f"✗ {response.status_code}"
    print(f"  doctor_id={doc_id}: {status}")

print("\n" + "=" * 80)
print("FLOW TEST COMPLETE")
print("=" * 80 + "\n")
