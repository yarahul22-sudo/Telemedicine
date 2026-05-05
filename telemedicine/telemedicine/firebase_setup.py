import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from django.conf import settings

def initialize_firebase():
    """Initialize Firebase Admin SDK with error handling and fallback strategies"""
    if not firebase_admin._apps:
        try:
            # Try loading from environment variable first (more secure)
            service_account_info = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
            
            if service_account_info:
                import json
                # Handle potential single quotes from .env
                if service_account_info.startswith("'") and service_account_info.endswith("'"):
                    service_account_info = service_account_info[1:-1]
                
                try:
                    cred_dict = json.loads(service_account_info)
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    print("✅ Firebase Admin Initialized Successfully (from env variable)")
                    return True
                except json.JSONDecodeError as je:
                    print(f"⚠️ Failed to parse FIREBASE_SERVICE_ACCOUNT JSON: {je}")
            
            # Fallback to credentials file for local development
            cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
            
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Firebase credentials not found at {cred_path}")
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin Initialized Successfully (from credentials file)")
            return True
        except Exception as e:
            print(f"❌ Firebase Initialization Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    return True

def get_firestore_db():
    """Get Firestore database client with error handling"""
    try:
        if not firebase_admin._apps:
            initialize_firebase()
        return firestore.client()
    except Exception as e:
        print(f"❌ Firestore Connection Error: {e}")
        raise
