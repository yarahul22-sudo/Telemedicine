#!/usr/bin/env python
"""
Video Call Connection Testing Script
Run this to verify Twilio connection and appointments setup
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from telemedicine.firestore_db import db
from appointments.models import Appointment
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import json

User = get_user_model()

def check_twilio_credentials():
    """Verify Twilio credentials are configured"""
    print("\n" + "="*60)
    print("1. CHECKING TWILIO CREDENTIALS")
    print("="*60)
    
    required = ['TWILIO_ACCOUNT_SID', 'TWILIO_API_KEY', 'TWILIO_API_SECRET']
    all_set = True
    
    for var in required:
        value = getattr(settings, var, None)
        if value:
            # Show only first and last chars for security
            masked = value[0] + '*' * (len(value) - 2) + value[-1] if len(value) > 2 else '*'
            print(f"✓ {var}: {masked}")
        else:
            print(f"✗ {var}: NOT SET")
            all_set = False
    
    return all_set

def check_firestore_connection():
    """Verify Firestore connection"""
    print("\n" + "="*60)
    print("2. CHECKING FIRESTORE CONNECTION")
    print("="*60)
    
    try:
        # Try to access collections
        collections = db.collections()
        count = 0
        for col in collections:
            count += 1
            if count <= 5:
                print(f"✓ Found collection: {col.id}")
        print(f"✓ Total collections: {count}")
        return True
    except Exception as e:
        print(f"✗ Firestore connection error: {e}")
        return False

def check_appointments():
    """Check for test appointments in Firestore"""
    print("\n" + "="*60)
    print("3. CHECKING APPOINTMENTS IN FIRESTORE")
    print("="*60)
    
    try:
        docs = db.collection('appointments').limit(3).stream()
        count = 0
        for doc in docs:
            count += 1
            data = doc.to_dict()
            print(f"\nAppointment {count}: {doc.id}")
            print(f"  Patient ID: {data.get('patient_id')}")
            print(f"  Doctor ID: {data.get('doctor_id')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Date: {data.get('appointment_date')}")
        
        if count == 0:
            print("⚠ No appointments found in Firestore")
            return False
        
        print(f"\n✓ Found {count} appointment(s)")
        return True
    except Exception as e:
        print(f"✗ Error checking appointments: {e}")
        return False

def generate_test_token(appointment_id):
    """Generate a test Twilio token"""
    print("\n" + "="*60)
    print("4. GENERATING TEST TOKEN")
    print("="*60)
    
    try:
        # Get appointment
        doc = db.collection('appointments').document(appointment_id).get()
        if not doc.exists:
            print(f"✗ Appointment {appointment_id} not found")
            return False
        
        data = doc.to_dict()
        room_name = f"appointment_{appointment_id}"
        identity = f"test_user_{appointment_id}"
        
        print(f"Appointment ID: {appointment_id}")
        print(f"Room Name: {room_name}")
        print(f"Identity: {identity}")
        
        # Generate token
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity=identity,
            ttl=3600
        )
        
        video_grant = VideoGrant(room=room_name)
        token.add_grant(video_grant)
        
        jwt_token = token.to_jwt()
        print(f"\n✓ Token generated successfully")
        print(f"Token length: {len(jwt_token)} chars")
        print(f"Token preview: {jwt_token[:50]}...")
        
        return {
            'token': jwt_token,
            'room_name': room_name,
            'identity': identity,
            'appointment_id': appointment_id
        }
    except Exception as e:
        print(f"✗ Token generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_permissions(user_email):
    """Test if user can access appointments"""
    print("\n" + "="*60)
    print("5. TESTING USER PERMISSIONS")
    print("="*60)
    
    try:
        user = User.objects.get(email=user_email)
        print(f"User: {user.email}")
        print(f"UID: {user.uid}")
        print(f"Role: {user.role}")
        print(f"Is Doctor: {user.is_doctor()}")
        print(f"Is Patient: {user.is_patient()}")
        
        # Check Firestore user doc
        user_doc = db.collection('users').document(user.uid).get()
        if user_doc.exists:
            print(f"✓ User found in Firestore")
        else:
            print(f"⚠ User not found in Firestore")
        
        return True
    except User.DoesNotExist:
        print(f"✗ User {user_email} not found")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "VIDEO CALL CONNECTION TEST" + " "*17 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        'Twilio Credentials': check_twilio_credentials(),
        'Firestore Connection': check_firestore_connection(),
        'Appointments': check_appointments(),
    }
    
    # Try to generate test token if we have an appointment
    try:
        docs = db.collection('appointments').limit(1).stream()
        for doc in docs:
            token_result = generate_test_token(doc.id)
            results['Token Generation'] = bool(token_result)
            break
    except:
        results['Token Generation'] = False
    
    # Try to test user permissions
    try:
        user = User.objects.filter(role='doctor').first()
        if user:
            results['User Permissions'] = test_user_permissions(user.email)
    except:
        results['User Permissions'] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ All checks passed! Video call should work.")
        return 0
    else:
        print(f"\n⚠ {total - passed} check(s) failed. See above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
