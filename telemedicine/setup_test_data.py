#!/usr/bin/env python
"""
Setup script to create test data for booking form
"""
import os
import sys
import django
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from users.models import PatientProfile, DoctorProfile, CustomUser
from appointments.models import Disease

def setup_test_data():
    """Setup test patients and doctors"""
    
    print("=" * 60)
    print("SETTING UP TEST DATA")
    print("=" * 60)
    
    # Create test patient
    print("\n[1] Creating test patient...")
    patient, created = CustomUser.objects.get_or_create(
        email='testpatient@example.com',
        defaults={
            'username': 'testpatient',
            'first_name': 'Test',
            'last_name': 'Patient',
            'role': 'patient'
        }
    )
    patient.set_password('testpass123')
    patient.save()
    
    # Create patient profile if not exists
    PatientProfile.objects.get_or_create(user=patient)
    print(f"✓ Test Patient: {patient.email}")
    
    # Create test doctor
    print("\n[2] Creating test doctor...")
    doctor, created = CustomUser.objects.get_or_create(
        email='dr.nabish@example.com',
        defaults={
            'username': 'drnabish',
            'first_name': 'Nabish',
            'last_name': 'Ahmed',
            'role': 'doctor'
        }
    )
    doctor.set_password('doctorpass123')
    doctor.save()
    print(f"✓ Test Doctor: {doctor.email}")
    
    # Create doctor profile if not exists
    doctor_profile, created = DoctorProfile.objects.get_or_create(
        user=doctor,
        defaults={
            'specialization': 'neurology',
            'license_number': 'LIC123456',
            'experience_years': 10,
            'consultation_fee': 50,
            'available_days': 'Monday-Friday',
            'qualification': 'MD, Board Certified',
            'is_approved': True  # Automatically approve for testing
        }
    )
    print(f"✓ Doctor Profile: {doctor_profile.get_specialization_display()}")
    print(f"  - Is Approved: {doctor_profile.is_approved}")
    print(f"  - Doctor ID: {doctor_profile.id}")
    
    # Check diseases
    print("\n[3] Checking diseases...")
    disease_count = Disease.objects.count()
    print(f"Total diseases in database: {disease_count}")
    
    if disease_count == 0:
        print("⚠ No diseases found! Loading diseases...")
        os.system('python manage.py load_diseases')
        disease_count = Disease.objects.count()
        print(f"✓ Loaded {disease_count} diseases")
    
    print("\n" + "=" * 60)
    print("TEST DATA READY!")
    print("=" * 60)
    print(f"\nLogin credentials:")
    print(f"  Patient: testpatient@example.com / testpass123")
    print(f"  Doctor: dr.nabish@example.com / doctorpass123")
    print(f"\nBooking URL: /book-appointment/?doctor_id={doctor_profile.id}")
    print("=" * 60)

if __name__ == '__main__':
    setup_test_data()
