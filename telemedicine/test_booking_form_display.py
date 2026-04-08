#!/usr/bin/env python
"""
Test script to debug why the booking form isn't displaying
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from users.models import PatientProfile, DoctorProfile, CustomUser
from appointments.models import Disease

def test_booking_form():
    """Test if booking form displays correctly"""
    
    print("=" * 60)
    print("BOOKING FORM DISPLAY DIAGNOSTIC TEST")
    print("=" * 60)
    
    # Step 1: Check if test data exists
    print("\n[Step 1] Checking test data...")
    
    try:
        test_patient = CustomUser.objects.get(email='testpatient@example.com')
        print(f"✓ Test patient found: {test_patient.email} (Role: {test_patient.role})")
    except CustomUser.DoesNotExist:
        print("✗ Test patient NOT found. Creating...")
        test_patient = CustomUser.objects.create_user(
            username='testpatient',
            email='testpatient@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Patient',
            role='patient'
        )
        PatientProfile.objects.create(user=test_patient)
        print(f"✓ Test patient created")
    
    try:
        test_doctor = CustomUser.objects.get(email='dr.nabish@example.com')
        print(f"✓ Test doctor found: {test_doctor.email} (Role: {test_doctor.role})")
        
        doctor_profile = test_doctor.doctor_profile
        print(f"  - Is Approved: {doctor_profile.is_approved}")
        print(f"  - Specialization: {doctor_profile.get_specialization_display()}")
        print(f"  - ID: {doctor_profile.id}")
        
        if not doctor_profile.is_approved:
            print("  ⚠ Doctor is NOT approved - approving...")
            doctor_profile.is_approved = True
            doctor_profile.save()
            print("  ✓ Doctor approved")
            
    except CustomUser.DoesNotExist:
        print("✗ Test doctor NOT found. Please create one first.")
        return
    
    # Step 2: Check if diseases exist
    print("\n[Step 2] Checking disease data...")
    disease_count = Disease.objects.count()
    print(f"Total diseases in database: {disease_count}")
    if disease_count == 0:
        print("⚠ WARNING: No diseases found! Running load_diseases command first...")
        os.system('python manage.py load_diseases')
    
    # Step 3: Test the booking form page
    print("\n[Step 3] Testing booking form page...")
    client = Client()
    
    # 3a: Test without login (should redirect to login)
    print("\n  3a. Accessing without login...")
    response = client.get(f'/book-appointment/?doctor_id={doctor_profile.id}')
    print(f"     Status: {response.status_code}")
    if response.status_code == 302:
        print(f"     ✓ Redirects to login (expected)")
    else:
        print(f"     ✗ Response: {response.status_code} (should be 302)")
    
    # 3b: Test with patient login
    print("\n  3b. Logging in as patient and accessing booking form...")
    login_result = client.login(email='testpatient@example.com', password='testpass123')
    if not login_result:
        print("     ✗ Login failed!")
        return
    print("     ✓ Login successful")
    
    response = client.get(f'/book-appointment/?doctor_id={doctor_profile.id}')
    print(f"     Status: {response.status_code}")
    
    if response.status_code == 200:
        print("     ✓ Booking form page loads successfully!")
        
        # Check if form elements are in the HTML
        content = response.content.decode('utf-8')
        
        checks = [
            ('Doctor name in response', f'Dr. {test_doctor.get_full_name()}' in content),
            ('Booking form element', 'id="bookingForm"' in content),
            ('Appointment date input', 'id="appointment_date"' in content),
            ('Consultation type select', 'id="consultation_type"' in content),
            ('Notes textarea', 'id="notes"' in content),
            ('Submit button', 'Book Appointment' in content),
            ('CSRF token', 'csrfmiddlewaretoken' in content),
        ]
        
        print("\n     Form Elements Check:")
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"       {status} {check_name}")
        
        all_passed = all(result for _, result in checks)
        if all_passed:
            print("\n     ✓ ALL FORM ELEMENTS ARE PRESENT!")
        else:
            print("\n     ✗ Some form elements are missing!")
            
    elif response.status_code == 403:
        print("     ✗ Access forbidden (403)")
        print("     Check: Is user a patient? Is doctor approved?")
    elif response.status_code == 404:
        print("     ✗ Page not found (404)")
        print("     Check: Is the URL route registered?")
    elif response.status_code == 302:
        print("     ✗ Redirected (302)")
        print(f"     Redirect location: {response.url if hasattr(response, 'url') else 'Unknown'}")
    else:
        print(f"     ✗ Unexpected status: {response.status_code}")
    
    # Step 4: Test without doctor_id parameter
    print("\n[Step 4] Testing without doctor_id parameter...")
    response = client.get('/book-appointment/')
    print(f"  Status: {response.status_code}")
    if response.status_code == 302:
        print(f"  ✓ Redirects to find_doctor (expected)")
    
    # Step 5: Test with non-existent doctor
    print("\n[Step 5] Testing with non-existent doctor_id...")
    response = client.get('/book-appointment/?doctor_id=99999')
    print(f"  Status: {response.status_code}")
    if response.status_code == 302:
        print(f"  ✓ Redirects appropriately (expected)")
    
    # Step 6: Test as doctor (should be denied)
    print("\n[Step 6] Testing access as doctor (should be denied)...")
    client.logout()
    client.login(email='dr.nabish@example.com', password='testpass123')
    response = client.get(f'/book-appointment/?doctor_id={doctor_profile.id}')
    print(f"  Status: {response.status_code}")
    if response.status_code == 302:
        print(f"  ✓ Doctor denied access (expected)")
    else:
        print(f"  ✗ Doctor should be denied access")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_booking_form()
