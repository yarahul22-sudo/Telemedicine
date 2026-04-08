#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
sys.path.insert(0, '/c/Users/raybi/OneDrive/Desktop/Telemedicine/telemedicine')
django.setup()

from appointments.models import Appointment, Disease
from users.models import PatientProfile, DoctorProfile
from datetime import datetime, timedelta

# Get a patient and a dermatologist
patient = PatientProfile.objects.first()
doctor = DoctorProfile.objects.filter(specialization='dermatology').first()
disease = Disease.objects.filter(name__icontains='skin').first()

if patient and doctor:
    # Create test appointment
    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        disease=disease,
        appointment_date=datetime.now() + timedelta(days=2),
        notes='Test appointment for demo',
        consultation_type='video',
        status='scheduled'
    )
    print(f"✓ Created appointment: {patient.user.get_full_name()} -> Dr. {doctor.user.get_full_name()}")
    print(f"  Disease: {disease.name if disease else 'Not specified'}")
else:
    print("Patient or Doctor not found")
    if not patient:
        print("No patients found")
    if not doctor:
        print("No dermatologists found")
