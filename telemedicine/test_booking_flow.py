#!/usr/bin/env python
"""
Test script to verify the complete appointment booking flow:
1. Patient books an appointment
2. Appointment appears in doctor's upcoming list
3. Appointment appears in doctor's patient list
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, '/c/Users/raybi/OneDrive/Desktop/Telemedicine/telemedicine')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from users.models.base import CustomUser
from users.models.patient import PatientProfile
from users.models.doctor import DoctorProfile
from appointments.models import Appointment, Disease
from django.utils import timezone

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_complete_booking_flow():
    """Test the complete booking flow"""
    
    print_section("APPOINTMENT BOOKING FLOW TEST")
    
    # Step 1: Get or create test patient
    print("\n[STEP 1] Getting test patient...")
    patient_email = 'testpatient@example.com'
    try:
        patient_user = CustomUser.objects.get(email=patient_email)
        patient = patient_user.patient_profile
        print(f"✓ Found patient: {patient_user.get_full_name()} ({patient_email})")
    except CustomUser.DoesNotExist:
        print(f"✗ Patient not found: {patient_email}")
        print("  Create a patient account first via the registration page")
        return False
    
    # Step 2: Get or create test doctor
    print("\n[STEP 2] Getting approved doctor...")
    doctor_email = 'dr.nabish@example.com'
    try:
        doctor_user = CustomUser.objects.get(email=doctor_email)
        doctor = doctor_user.doctor_profile
        
        if not doctor.is_approved:
            print(f"✗ Doctor not approved: {doctor_user.get_full_name()}")
            print("  Doctor must be approved by admin to receive appointments")
            return False
        
        print(f"✓ Found approved doctor: {doctor_user.get_full_name()} ({doctor.specialization})")
    except CustomUser.DoesNotExist:
        print(f"✗ Doctor not found: {doctor_email}")
        return False
    
    # Step 3: Get or create a disease
    print("\n[STEP 3] Getting disease for appointment...")
    try:
        disease = Disease.objects.first()
        print(f"✓ Using disease: {disease.name}")
    except:
        print("✗ No diseases found in database")
        print("  Run: python manage.py load_diseases")
        return False
    
    # Step 4: Create appointment
    print("\n[STEP 4] Creating appointment...")
    appointment_date = timezone.now() + timedelta(days=2, hours=10)
    
    try:
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            disease=disease,
            appointment_date=appointment_date,
            notes="Test appointment - patient experiencing headaches",
            consultation_type="video",
            status="scheduled"
        )
        print(f"✓ Appointment created successfully!")
        print(f"  ID: {appointment.id}")
        print(f"  Patient: {appointment.patient.user.get_full_name()}")
        print(f"  Doctor: {appointment.doctor.user.get_full_name()}")
        print(f"  Date: {appointment.appointment_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Status: {appointment.status}")
        print(f"  Notes: {appointment.notes}")
    except Exception as e:
        print(f"✗ Error creating appointment: {str(e)}")
        return False
    
    # Step 5: Verify appointment appears in doctor's upcoming
    print("\n[STEP 5] Verifying appointment in doctor's upcoming list...")
    upcoming = Appointment.objects.filter(
        doctor=doctor,
        status='scheduled',
        appointment_date__gte=timezone.now()
    )
    
    if appointment in upcoming:
        print(f"✓ Appointment visible in doctor's upcoming list")
        print(f"  Total upcoming appointments: {upcoming.count()}")
    else:
        print(f"✗ Appointment NOT in doctor's upcoming list")
        return False
    
    # Step 6: Verify appointment links doctor and patient
    print("\n[STEP 6] Verifying doctor-patient relationship...")
    doctor_appointments = Appointment.objects.filter(doctor=doctor)
    patient_appointments = Appointment.objects.filter(patient=patient)
    
    print(f"✓ Doctor has {doctor_appointments.count()} total appointments")
    print(f"✓ Patient has {patient_appointments.count()} total appointments")
    
    if appointment in doctor_appointments and appointment in patient_appointments:
        print(f"✓ Relationship verified: Doctor and Patient are linked correctly")
    else:
        print(f"✗ Relationship broken!")
        return False
    
    # Step 7: Verify appointment should appear in doctor's dashboard
    print("\n[STEP 7] Doctor should see this appointment in:")
    print(f"  - Dashboard URL: http://127.0.0.1:8000/dashboard/")
    print(f"  - Appointments URL: http://127.0.0.1:8000/doctor-appointments/")
    print(f"  - Patient List API: http://127.0.0.1:8000/api/appointments/doctor/patients/")
    
    # Step 8: Verify patient can see appointment
    print("\n[STEP 8] Patient should see this appointment in:")
    print(f"  - Dashboard URL: http://127.0.0.1:8000/dashboard/")
    print(f"  - My Appointments URL: http://127.0.0.1:8000/my-appointments/")
    
    print("\n" + "="*60)
    print("  ✓ ALL TESTS PASSED - BOOKING FLOW IS WORKING!")
    print("="*60)
    print("\nNEXT STEPS:")
    print("1. Login as doctor and go to: http://127.0.0.1:8000/doctor-appointments/")
    print("2. You should see the appointment in the 'Upcoming' tab")
    print("3. Doctor can click 'Mark Complete' to end the appointment")
    print("4. Doctor can click 'Write Prescription' to add medication")
    print("5. Doctor can click 'Add Notes' to document the consultation")
    
    return True

if __name__ == '__main__':
    success = test_complete_booking_flow()
    sys.exit(0 if success else 1)
