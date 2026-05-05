#!/usr/bin/env python
"""Test Firebase token verification"""
import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
sys.path.insert(0, 'telemedicine')
django.setup()

import firebase_admin
from firebase_admin import credentials, auth
from datetime import datetime

print("=" * 60)
print("FIREBASE TOKEN VERIFICATION TEST")
print("=" * 60)

# Check Firebase initialization
print(f"\n📊 Firebase Status:")
print(f"   Firebase Apps: {firebase_admin._apps}")
print(f"   Number of apps: {len(firebase_admin._apps)}")

if firebase_admin._apps:
    print("   ✅ Firebase is initialized")
else:
    print("   ❌ Firebase is NOT initialized")
    print("\n   Attempting to initialize...")
    from telemedicine.firebase_setup import initialize_firebase
    result = initialize_firebase()
    print(f"   Result: {result}")

# Check system time
print(f"\n⏰ System Time Check:")
print(f"   Current time: {datetime.utcnow().isoformat()}Z")
print(f"   Unix timestamp: {int(time.time())}")

# Try to create and verify a test user
print(f"\n🔐 Firebase User Operations:")
try:
    # First, check if test user exists and delete it
    test_email = "firebasetest@telemedicine.local"
    try:
        user = auth.get_user_by_email(test_email)
        print(f"   Found existing test user: {user.uid}")
        auth.delete_user(user.uid)
        print(f"   ✅ Deleted existing test user")
    except auth.UserNotFoundError:
        print(f"   No existing test user found (OK)")
    
    # Create a new test user
    user = auth.create_user(
        email=test_email,
        email_verified=True,
        password='Test@12345'
    )
    print(f"   ✅ Created test user: {user.uid}")
    
    # Generate token for the test user
    custom_token = auth.create_custom_token(user.uid)
    print(f"   ✅ Generated custom token (length: {len(custom_token)})")
    
    # Verify the token
    print(f"\n   Attempting to verify token...")
    try:
        decoded = auth.verify_id_token(custom_token, check_revoked=False)
        print(f"   ✅ Token verification SUCCEEDED")
        print(f"      UID: {decoded['uid']}")
        print(f"      Email: {decoded.get('email', 'N/A')}")
    except firebase_admin.auth.InvalidIdTokenError as e:
        print(f"   ❌ Token verification FAILED: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error during verification: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    auth.delete_user(user.uid)
    print(f"   ✅ Cleaned up test user")
    
except Exception as e:
    print(f"   ❌ Error during test: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
