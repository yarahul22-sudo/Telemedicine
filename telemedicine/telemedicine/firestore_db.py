import firebase_admin
from firebase_admin import credentials, firestore
import os
from django.conf import settings

def get_firestore_db():
    if not firebase_admin._apps:
        try:
            cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Fallback to default if environment variable is set
                firebase_admin.initialize_app()
        except Exception as e:
            print(f"Error initializing Firebase Admin: {e}")
            return None
    return firestore.client()

db = get_firestore_db()
