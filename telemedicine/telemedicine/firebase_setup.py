import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from django.conf import settings

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.path.join(settings.BASE_DIR, 'telemedicine', 'firebase-credentials.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin Initialized Successfully")
        else:
            print(f"Firebase credentials not found at {cred_path}")

def get_firestore_db():
    if not firebase_admin._apps:
        initialize_firebase()
    return firestore.client()
