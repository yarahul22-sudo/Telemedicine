#!/usr/bin/env python
"""Check and create test users in Firebase"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
sys.path.insert(0, 'telemedicine')
django.setup()

import firebase_admin
from firebase_admin import auth, firestore

print("\n" + "="*70)
print("FIREBASE USER MANAGEMENT")
print("="*70)

# Check if test user exists
test_email = "bsaladek@gmail.com"
test_password = "Test@12345"

print(f"\n1️⃣  CHECKING FOR EXISTING USER: {test_email}")
print("-" * 70)

try:
    user = auth.get_user_by_email(test_email)
    print(f"   ✅ User found in Firebase Auth")
    print(f"      UID: {user.uid}")
    print(f"      Email: {user.email}")
    print(f"      Email verified: {user.email_verified}")
except auth.UserNotFoundError:
    print(f"   ❌ User NOT found in Firebase Auth")
    print(f"\n2️⃣  CREATING NEW USER")
    print("-" * 70)
    try:
        user = auth.create_user(
            email=test_email,
            email_verified=True,
            password=test_password
        )
        print(f"   ✅ User created successfully")
        print(f"      UID: {user.uid}")
        print(f"      Email: {user.email}")
    except Exception as e:
        print(f"   ❌ Error creating user: {e}")
        sys.exit(1)

# Check if user exists in Firestore
print(f"\n3️⃣  CHECKING FIRESTORE")
print("-" * 70)

db = firestore.client()
users_ref = db.collection('users')

try:
    user_doc = users_ref.document(user.uid).get()
    if user_doc.exists:
        print(f"   ✅ User found in Firestore")
        print(f"      Data: {user_doc.to_dict()}")
    else:
        print(f"   ❌ User NOT in Firestore, creating...")
        
        user_data = {
            'uid': user.uid,
            'email': test_email,
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'patient',
            'created_at': firestore.SERVER_TIMESTAMP,
        }
        
        users_ref.document(user.uid).set(user_data)
        print(f"   ✅ User created in Firestore")
        
except Exception as e:
    print(f"   ❌ Firestore error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("COMPLETE - User should now be able to log in")
print("="*70 + "\n")
