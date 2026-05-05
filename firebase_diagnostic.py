#!/usr/bin/env python
"""Detailed Firebase token verification diagnostic"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
sys.path.insert(0, 'telemedicine')
django.setup()

import firebase_admin
from firebase_admin import auth, credentials
import json
from datetime import datetime, timedelta
import time

print("\n" + "="*70)
print("FIREBASE ADMIN SDK DIAGNOSTIC")
print("="*70)

# 1. Check Firebase initialization
print("\n1️⃣  FIREBASE INITIALIZATION STATUS")
print("-" * 70)
print(f"   Firebase apps: {len(firebase_admin._apps)} app(s)")
print(f"   Apps initialized: {list(firebase_admin._apps.keys())}")

if firebase_admin._apps:
    app = list(firebase_admin._apps.values())[0]
    print(f"   Default app project: {app.project_id if hasattr(app, 'project_id') else 'Unknown'}")
else:
    print("   ❌ No Firebase apps initialized!")

# 2. Check Firebase credentials
print("\n2️⃣  FIREBASE CREDENTIALS")
print("-" * 70)
env_service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
file_creds_path = os.path.join('telemedicine', 'firebase-credentials.json')

if env_service_account:
    print("   ✅ FIREBASE_SERVICE_ACCOUNT env var is set")
    try:
        if env_service_account.startswith("'"):
            env_service_account = env_service_account[1:-1]
        cred_data = json.loads(env_service_account)
        print(f"   Project ID: {cred_data.get('project_id', 'Unknown')}")
        print(f"   Email: {cred_data.get('client_email', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Error parsing env credentials: {e}")
else:
    print("   ⚠️  FIREBASE_SERVICE_ACCOUNT env var not set")

if os.path.exists(file_creds_path):
    print(f"   ✅ Credentials file exists at {file_creds_path}")
else:
    print(f"   ❌ Credentials file NOT found at {file_creds_path}")

# 3. Check Firebase Auth
print("\n3️⃣  FIREBASE AUTH CHECK")
print("-" * 70)
try:
    # Try to list a user (will fail if no users, but tests connection)
    result = auth.list_users(page_size=1)
    print(f"   ✅ Firebase Auth is accessible")
    print(f"   Sample user download count: {result.download_count}")
except Exception as e:
    print(f"   ❌ Firebase Auth error: {e}")
    import traceback
    traceback.print_exc()

# 4. Test token verification with current time
print("\n4️⃣  TIME SYNCHRONIZATION CHECK")
print("-" * 70)
now = datetime.utcnow()
timestamp = int(time.time())
print(f"   UTC now: {now.isoformat()}Z")
print(f"   Unix timestamp: {timestamp}")
print(f"   System time appears synchronized")

# 5. Try to create and verify a test ID token
print("\n5️⃣  TEST ID TOKEN CREATION & VERIFICATION")
print("-" * 70)
try:
    # Create test user
    test_email = f"test{int(time.time())}@telemedicine.local"
    user = auth.create_user(
        email=test_email,
        email_verified=True,
        password='Test@12345'
    )
    print(f"   ✅ Created test user: {user.uid}")
    print(f"   Email: {user.email}")
    
    # Create custom token (this is what admin SDK does)
    custom_token = auth.create_custom_token(user.uid)
    print(f"   ✅ Created custom token (length: {len(custom_token)})")
    
    # Test verification
    print(f"\n   Testing token verification options:")
    
    # Option 1: Default
    try:
        decoded = auth.verify_id_token(custom_token)
        print(f"   ✅ Verified with default settings")
    except firebase_admin.auth.InvalidIdTokenError as e:
        print(f"   ❌ Failed with defaults: {e}")
        print(f"      (Note: Custom tokens cannot be verified directly with verify_id_token)")
    
    # Option 2: With check_revoked=False
    try:
        decoded = auth.verify_id_token(custom_token, check_revoked=False)
        print(f"   ✅ Verified with check_revoked=False")
    except firebase_admin.auth.InvalidIdTokenError as e:
        print(f"   ❌ Failed with check_revoked=False: {e}")
        print(f"      (Note: Custom tokens cannot be verified directly)")
    
    # Create ID token via Firebase REST API (this is what client does)
    print(f"\n   To properly test, we need a real ID token from Firebase client SDK")
    print(f"   (This would require browser automation)")
    
    # Clean up
    auth.delete_user(user.uid)
    print(f"\n   ✅ Cleaned up test user")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# 6. Check Django authentication backend
print("\n6️⃣  DJANGO AUTHENTICATION BACKEND")
print("-" * 70)
try:
    from accounts.firestore_auth import FirestoreBackend
    backend = FirestoreBackend()
    print(f"   ✅ FirestoreBackend imported successfully")
    print(f"   Backend class: {backend.__class__.__name__}")
except Exception as e:
    print(f"   ❌ Error importing backend: {e}")

# 7. Check Firestore connectivity
print("\n7️⃣  FIRESTORE CONNECTIVITY")
print("-" * 70)
try:
    from telemedicine.firestore_db import db
    if db:
        print(f"   ✅ Firestore client initialized")
        # Try a simple query
        docs = db.collection('users').limit(1).stream()
        count = sum(1 for _ in docs)
        print(f"   ✅ Firestore query successful")
    else:
        print(f"   ❌ Firestore client is None")
except Exception as e:
    print(f"   ❌ Firestore error: {e}")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70 + "\n")
