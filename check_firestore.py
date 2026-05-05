#!/usr/bin/env python
"""Check what's actually in Firestore appointments collection"""

import sys
import os

# Add telemedicine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'telemedicine'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')

import django
django.setup()

from telemedicine.firestore_db import db

# Check appointments collection
print("\n" + "="*80)
print("FIRESTORE APPOINTMENTS COLLECTION CHECK")
print("="*80)

appointments_ref = db.collection('appointments')
docs = appointments_ref.stream()

print(f"\nTotal documents in appointments collection: ", end="")

doc_list = list(docs)
print(len(doc_list))

if len(doc_list) == 0:
    print("❌ No appointments found in Firestore!")
else:
    print(f"\n✅ Found {len(doc_list)} appointments:\n")
    
    for i, doc in enumerate(doc_list, 1):
        data = doc.to_dict()
        print(f"{i}. Document ID: {doc.id}")
        print(f"   Patient ID: {data.get('patient_id', 'MISSING')}")
        print(f"   Patient Name: {data.get('patient_name', 'MISSING')}")
        print(f"   Doctor ID: {data.get('doctor_id', 'MISSING')}")
        print(f"   Doctor Name: {data.get('doctor_name', 'MISSING')}")
        print(f"   Status: {data.get('status', 'MISSING')}")
        print(f"   Appointment Date: {data.get('appointment_date', 'MISSING')}")
        print(f"   Notes: {data.get('notes', 'MISSING')[:50]}...")
        print()

# Now check for patient-specific appointments
patient_uid = "9gfdyHYwmuYYBD6Vb0eMWH7BCFB3"
print(f"\n{'='*80}")
print(f"CHECKING FOR PATIENT UID: {patient_uid}")
print("="*80)

patient_query = appointments_ref.where('patient_id', '==', patient_uid).stream()
patient_docs = list(patient_query)

print(f"\nAppointments for this patient: {len(patient_docs)}")

if patient_docs:
    for doc in patient_docs:
        print(f"  - Found appointment: {doc.to_dict().get('doctor_name', 'Unknown')}")
else:
    print("❌ No appointments found for this patient!")
    print("\nChecking for any 'scheduled' appointments...")
    scheduled_query = appointments_ref.where('status', '==', 'scheduled').stream()
    scheduled_docs = list(scheduled_query)
    print(f"Total 'scheduled' appointments: {len(scheduled_docs)}")
    
    if scheduled_docs:
        print("\nScheduled appointments by patient:")
        for doc in scheduled_docs:
            data = doc.to_dict()
            print(f"  - Patient ID: {data.get('patient_id')} - Doctor: {data.get('doctor_name')}")

print("\n" + "="*80)
