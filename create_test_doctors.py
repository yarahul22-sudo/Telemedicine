#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, r'c:\Users\raybi\OneDrive\Desktop\Telemedicine\telemedicine')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from users.models import CustomUser, DoctorProfile

# Create test doctors
doctors_data = [
    {
        'email': 'dermatologist@example.com',
        'username': 'dermatologist',
        'first_name': 'Dr. Rachel',
        'last_name': 'Nelson',
        'specialization': 'dermatology',
        'license_number': 'DL12345',
        'experience_years': 8,
        'qualification': 'MD, Dermatology Specialist',
        'consultation_fee': 50.00,
        'bio': 'Experienced dermatologist specializing in skin conditions, acne, and psoriasis',
        'rating': 4.8,
    },
    {
        'email': 'cardiologist@example.com',
        'username': 'cardiologist',
        'first_name': 'Dr. Michael',
        'last_name': 'Chen',
        'specialization': 'cardiology',
        'license_number': 'CL67890',
        'experience_years': 12,
        'qualification': 'MD, MS in Cardiology',
        'consultation_fee': 75.00,
        'bio': 'Board-certified cardiologist with 12 years of experience in heart disease treatment',
        'rating': 4.9,
    },
    {
        'email': 'neurologist@example.com',
        'username': 'neurologist',
        'first_name': 'Dr. Sarah',
        'last_name': 'Kumar',
        'specialization': 'neurology',
        'license_number': 'NL24680',
        'experience_years': 10,
        'qualification': 'MD, Neurology Specialist',
        'consultation_fee': 60.00,
        'bio': 'Neurologist specializing in migraines, headaches, and neurological disorders',
        'rating': 4.7,
    },
]

for doctor_data in doctors_data:
    try:
        # Check if user already exists
        if CustomUser.objects.filter(email=doctor_data['email']).exists():
            print(f"Doctor {doctor_data['email']} already exists")
            continue
        
        # Create user
        user = CustomUser.objects.create_user(
            email=doctor_data['email'],
            username=doctor_data['username'],
            password='testpass123',
            first_name=doctor_data['first_name'],
            last_name=doctor_data['last_name'],
            role='doctor'
        )
        
        # Create doctor profile
        profile_data = {k: v for k, v in doctor_data.items() if k not in ['email', 'username', 'first_name', 'last_name']}
        doctor_profile = DoctorProfile.objects.create(
            user=user,
            **profile_data
        )
        
        print(f"✓ Created doctor: {user.get_full_name()} ({doctor_data['specialization']})")
    except Exception as e:
        print(f"✗ Error creating doctor {doctor_data['email']}: {e}")

print("\n✓ All test doctors created successfully!")
