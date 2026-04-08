#!/usr/bin/env python
"""
List all users and their credentials from the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from users.models import CustomUser, PatientProfile, DoctorProfile
from django.db.models import Q

print("\n" + "=" * 80)
print("TELEMEDICINE SYSTEM - ALL USERS & CREDENTIALS")
print("=" * 80)

# Get all users
all_users = CustomUser.objects.all().order_by('role', 'email')

print(f"\n📊 TOTAL USERS: {all_users.count()}\n")

# Organize by role
patient_users = all_users.filter(role='patient')
doctor_users = all_users.filter(role='doctor')
admin_users = all_users.filter(is_superuser=True)

# Display Patients
print("\n" + "=" * 80)
print("👥 PATIENT ACCOUNTS ({} total)".format(patient_users.count()))
print("=" * 80)
print(f"{'Email':<35} {'Username':<20} {'Full Name':<30} {'Status':<12}")
print("-" * 80)

for user in patient_users:
    status = "✓ Active" if user.is_active else "✗ Inactive"
    print(f"{user.email:<35} {user.username:<20} {user.get_full_name():<30} {status:<12}")

# Display Doctors
print("\n" + "=" * 80)
print("👨‍⚕️ DOCTOR ACCOUNTS ({} total)".format(doctor_users.count()))
print("=" * 80)
print(f"{'Email':<35} {'Username':<20} {'Full Name':<25} {'Approved':<12} {'Specialty':<20}")
print("-" * 80)

for user in doctor_users:
    try:
        doc_profile = user.doctor_profile
        approved = "✓ Yes" if doc_profile.is_approved else "✗ No"
        specialty = doc_profile.get_specialization_display() if doc_profile.specialization else "N/A"
    except:
        approved = "N/A"
        specialty = "N/A"
    
    print(f"{user.email:<35} {user.username:<20} {user.get_full_name():<25} {approved:<12} {specialty:<20}")

# Display Admins
print("\n" + "=" * 80)
print("🔐 ADMIN ACCOUNTS ({} total)".format(admin_users.count()))
print("=" * 80)
print(f"{'Email':<35} {'Username':<20} {'Full Name':<30}")
print("-" * 80)

for user in admin_users:
    print(f"{user.email:<35} {user.username:<20} {user.get_full_name():<30}")

# Print detailed credentials table
print("\n\n" + "=" * 80)
print("🔑 DETAILED CREDENTIALS FOR LOGIN")
print("=" * 80)

print("\n📌 NOTE: Default passwords may have been changed. Use actual passwords you set.\n")

# Create a combined list
all_users_list = []

for user in patient_users:
    all_users_list.append({
        'role': 'Patient',
        'email': user.email,
        'username': user.username,
        'full_name': user.get_full_name(),
        'status': 'Active' if user.is_active else 'Inactive'
    })

for user in doctor_users:
    try:
        doc_profile = user.doctor_profile
        specialty = doc_profile.get_specialization_display() or 'N/A'
        approved = 'Approved' if doc_profile.is_approved else 'Pending'
    except:
        specialty = 'N/A'
        approved = 'N/A'
    
    all_users_list.append({
        'role': f'Doctor ({specialty})',
        'email': user.email,
        'username': user.username,
        'full_name': user.get_full_name(),
        'status': approved
    })

for user in admin_users:
    all_users_list.append({
        'role': 'Admin',
        'email': user.email,
        'username': user.username,
        'full_name': user.get_full_name(),
        'status': 'Active'
    })

# Print as table
print(f"{'#':<3} {'Email':<35} {'Username':<20} {'Role':<20} {'Full Name':<25} {'Status':<15}")
print("-" * 118)

for i, user_info in enumerate(all_users_list, 1):
    print(f"{i:<3} {user_info['email']:<35} {user_info['username']:<20} {user_info['role']:<20} {user_info['full_name']:<25} {user_info['status']:<15}")

# Test Login URLs
print("\n\n" + "=" * 80)
print("🔗 TEST LOGIN URLS")
print("=" * 80)
print("\nLogin page: http://127.0.0.1:8000/login/\n")

print("Quick test credentials:")
print("-" * 80)

# Sample a few users
if patient_users.exists():
    patient = patient_users.first()
    print(f"\n✓ Patient Test:")
    print(f"  Email: {patient.email}")
    print(f"  Username: {patient.username}")
    print(f"  Then visit: http://127.0.0.1:8000/book-appointment/?doctor_id=7")

if doctor_users.exists():
    doctor = doctor_users.first()
    print(f"\n✓ Doctor Test:")
    print(f"  Email: {doctor.email}")
    print(f"  Username: {doctor.username}")
    print(f"  Then visit: http://127.0.0.1:8000/doctor-appointments/")

if admin_users.exists():
    admin = admin_users.first()
    print(f"\n✓ Admin Test:")
    print(f"  Email: {admin.email}")
    print(f"  Username: {admin.username}")
    print(f"  Then visit: http://127.0.0.1:8000/admin/")

# Print database table stats
print("\n\n" + "=" * 80)
print("📈 DATABASE STATISTICS")
print("=" * 80)

from appointments.models import Appointment, Prescription, Disease

appointments_count = Appointment.objects.count()
prescriptions_count = Prescription.objects.count()
diseases_count = Disease.objects.count()

print(f"\n📅 Appointments: {appointments_count}")
print(f"💊 Prescriptions: {prescriptions_count}")
print(f"🏥 Diseases: {diseases_count}")

# Show appointment breakdown by status
print("\n  Appointment Status Breakdown:")
for status in ['scheduled', 'completed', 'cancelled']:
    count = Appointment.objects.filter(status=status).count()
    print(f"    - {status.capitalize()}: {count}")

print("\n" + "=" * 80)
print("✅ USER DATABASE EXPORT COMPLETE")
print("=" * 80 + "\n")
