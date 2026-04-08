#!/usr/bin/env python
"""
Check and fix the pshyam@telemedicine.com user account
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from users.models import PatientProfile, DoctorProfile, CustomUser
from appointments.models import Disease

print("=" * 60)
print("CHECKING USER: pshyam@telemedicine.com")
print("=" * 60)

# Check if user exists
try:
    user = CustomUser.objects.get(email='pshyam@telemedicine.com')
    print(f"\n✓ User exists: {user.email}")
    print(f"  - Username: {user.username}")
    print(f"  - Full name: {user.get_full_name()}")
    print(f"  - Role: {user.role}")
    print(f"  - Is active: {user.is_active}")
    print(f"  - Is staff: {user.is_staff}")
    
    # Check if patient profile exists
    if user.role == 'patient':
        try:
            profile = PatientProfile.objects.get(user=user)
            print(f"  - Patient profile: EXISTS ✓")
        except PatientProfile.DoesNotExist:
            print(f"  - Patient profile: MISSING ✗ (Creating...)")
            PatientProfile.objects.create(user=user)
            print(f"  - Patient profile: CREATED ✓")
    
    # Check approved doctors
    print(f"\n✓ Checking approved doctors...")
    approved_doctors = DoctorProfile.objects.filter(is_approved=True)
    print(f"  Total approved doctors: {approved_doctors.count()}")
    
    if approved_doctors.count() == 0:
        print(f"  ⚠ WARNING: No approved doctors found!")
        print(f"  Need to have at least one approved doctor for booking")
        
        # Show all doctors
        all_doctors = DoctorProfile.objects.all()
        print(f"  Total doctors in system: {all_doctors.count()}")
        
        if all_doctors.count() > 0:
            print(f"\n  Approving first doctor...")
            doc = all_doctors.first()
            doc.is_approved = True
            doc.save()
            print(f"  ✓ Doctor approved: {doc.user.email}")
    else:
        print(f"\n  Approved doctors:")
        for doc in approved_doctors:
            print(f"    - {doc.user.email} ({doc.get_specialization_display()})")
    
    # Check diseases
    print(f"\n✓ Checking diseases...")
    diseases = Disease.objects.all()
    print(f"  Total diseases: {diseases.count()}")
    
    if diseases.count() == 0:
        print(f"  ⚠ Running load_diseases...")
        os.system('python manage.py load_diseases')
    
    # Test booking page
    print(f"\n" + "=" * 60)
    print(f"BOOKING URL (for pshyam@telemedicine.com):")
    print(f"=" * 60)
    
    if approved_doctors.count() > 0:
        doc = approved_doctors.first()
        print(f"\nhttp://127.0.0.1:8000/book-appointment/?doctor_id={doc.id}")
        print(f"\nDoctor: {doc.user.full_name} ({doc.get_specialization_display()})")
    else:
        print(f"Cannot provide URL - no approved doctors found")

except CustomUser.DoesNotExist:
    print(f"\n✗ User NOT found: pshyam@telemedicine.com")
    print(f"\nCreating account for pshyam@telemedicine.com...")
    
    user = CustomUser.objects.create_user(
        username='pshyam',
        email='pshyam@telemedicine.com',
        password='pshyam123',  # Default password
        first_name='Pshyam',
        last_name='User',
        role='patient'
    )
    
    # Create patient profile
    PatientProfile.objects.create(user=user)
    print(f"✓ User created successfully!")
    print(f"  Email: pshyam@telemedicine.com")
    print(f"  Password: pshyam123")
    print(f"  Role: Patient")
    
    # Check for approved doctors
    print(f"\n✓ Checking approved doctors...")
    approved_doctors = DoctorProfile.objects.filter(is_approved=True)
    
    if approved_doctors.count() == 0:
        print(f"  No approved doctors! Creating and approving one...")
        
        # Create a doctor
        doc_user = CustomUser.objects.create_user(
            username='drdemo',
            email='dr.demo@telemedicine.com',
            password='drdemo123',
            first_name='Demo',
            last_name='Doctor',
            role='doctor'
        )
        
        doc_profile = DoctorProfile.objects.create(
            user=doc_user,
            specialization='general_practice',
            license_number='LIC999999',
            experience_years=5,
            consultation_fee=30,
            available_days='Monday-Sunday',
            qualification='MD',
            is_approved=True
        )
        
        print(f"  ✓ Doctor created and approved")
        print(f"    Email: dr.demo@telemedicine.com")
        
        approved_doctors = DoctorProfile.objects.filter(is_approved=True)
    
    print(f"\n" + "=" * 60)
    print(f"READY TO BOOK APPOINTMENT!")
    print(f"=" * 60)
    print(f"\nLogin as: pshyam@telemedicine.com / pshyam123")
    print(f"\nThen visit:")
    
    doc = approved_doctors.first()
    print(f"http://127.0.0.1:8000/book-appointment/?doctor_id={doc.id}")
    
    print(f"\nDoctor: {doc.user.get_full_name()} ({doc.get_specialization_display()})")

print(f"\n" + "=" * 60)
