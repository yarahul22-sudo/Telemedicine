import firebase_admin
from firebase_admin import credentials, firestore
import os
from django.conf import settings

def get_firestore_db():
    if not firebase_admin._apps:
        try:
            # Try loading from environment variable first
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
                except json.JSONDecodeError:
                    pass  # Fall through to file-based approach
            
            # Fallback to credentials file
            if not firebase_admin._apps:
                cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase Admin: {e}")
            return None
    return firestore.client()

db = get_firestore_db()
