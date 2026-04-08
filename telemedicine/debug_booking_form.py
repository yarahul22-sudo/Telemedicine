#!/usr/bin/env python
"""
Debug script to test booking form page access
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from django.test import Client
from django.conf import settings
from users.models import CustomUser, PatientProfile
from users.models import DoctorProfile
from appointments.models import Appointment, Disease

print("=" * 70)
print("BOOKING FORM DEBUG TEST")
print("=" * 70)

# Setup test client
client = Client()

# Step 1: Check user
print("\n[Step 1] Checking patient user...")
try:
    user = CustomUser.objects.get(email='pshyam@telemedicine.com')
    print(f"✓ User found: {user.email}")
    print(f"  Role: {user.role}")
    print(f"  Active: {user.is_active}")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Step 2: Check doctors
print("\n[Step 2] Checking doctors...")
approved_doctors = DoctorProfile.objects.filter(is_approved=True)
if approved_doctors.count() == 0:
    print("✗ No approved doctors found!")
    sys.exit(1)

doctor = approved_doctors.first()
print(f"✓ Found {approved_doctors.count()} approved doctors")
print(f"  Using: {doctor.user.email} (ID: {doctor.id})")

# Step 3: Test page WITHOUT login
print("\n[Step 3] Testing page access without login...")
response = client.get(f'/book-appointment/?doctor_id={doctor.id}')
print(f"  Status: {response.status_code}")
if response.status_code == 302:
    print(f"  ✓ Redirected to login (expected)")
    print(f"  Redirect location: {response.url}")
else:
    print(f"  Response: {response.status_code}")

# Step 4: Login manually and test
print("\n[Step 4] Logging in as patient...")

# Get user 
user = CustomUser.objects.get(email='pshyam@telemedicine.com')
user.set_password('pshyam123')
user.save()

# Use the test client's force_login method
client.force_login(user)
print(f"✓ Test client logged in as: {user.email}")

# Step 5: Test booking form page as patient
print("\n[Step 5] Testing booking form page access...")
url = f'/book-appointment/?doctor_id={doctor.id}'
print(f"  URL: {url}")

response = client.get(url)
print(f"  Status: {response.status_code}")

if response.status_code == 200:
    print(f"  ✓ Page loaded successfully!")
    
    # Check for form elements
    content = response.content.decode('utf-8')
    
    checks = {
        'bookingForm element': 'id="bookingForm"' in content,
        'appointment_date input': 'id="appointment_date"' in content,
        'consultation_type select': 'id="consultation_type"' in content,
        'notes textarea': 'id="notes"' in content,
        'Submit button': 'Book Appointment' in content,
        'Doctor name': doctor.user.get_full_name() in content,
    }
    
    print(f"\n  Form Elements:")
    all_found = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"    {status} {check_name}")
        if not result:
            all_found = False
    
    if all_found:
        print(f"\n  ✓ ALL FORM ELEMENTS PRESENT - FORM IS DISPLAYING!")
    else:
        print(f"\n  ✗ Some elements missing")
        print(f"\n  ===== RESPONSE CONTENT (First 1500 chars) =====")
        print(content[:1500])
        print(f"  ===== END RESPONSE =====")
        
elif response.status_code == 302:
    print(f"  ✗ Redirected (302)")
    print(f"  Location: {response.url}")
    
elif response.status_code == 403:
    print(f"  ✗ Forbidden (403)")
    
elif response.status_code == 404:
    print(f"  ✗ Not found (404)")
else:
    print(f"  ✗ Error: {response.status_code}")

# Step 6: Check template existence
print("\n[Step 6] Checking template file...")
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist

try:
    template = get_template('book-appointment.html')
    print(f"  ✓ Template loaded successfully")
except TemplateDoesNotExist:
    print(f"  ✗ Template not found")

print("\n" + "=" * 70)
print("DEBUG TEST COMPLETE")
print("=" * 70)
