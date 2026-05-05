"""Firebase Token Authentication for DRF"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import firebase_admin.auth
from accounts.firestore_auth import FirestoreUser
from telemedicine.firestore_db import db

class FirebaseTokenAuthentication(BaseAuthentication):
    """
    Authenticate using Firebase ID tokens sent in Authorization header.
    Format: Authorization: Bearer <firebase_id_token>
    """
    
    def authenticate(self, request):
        # Check for Authorization header
        auth_header = request.META.get('Authorization', '').split()
        
        if not auth_header or len(auth_header) != 2:
            # No auth header - return None to try next authentication method
            return None
        
        if auth_header[0].lower() != 'bearer':
            return None
        
        token = auth_header[1]
        
        try:
            # Verify Firebase token
            decoded_token = firebase_admin.auth.verify_id_token(
                token, 
                check_revoked=False, 
                clock_skew_seconds=10
            )
            uid = decoded_token.get('uid')
            
            if not uid:
                raise AuthenticationFailed('Invalid token: No UID found')
            
            # Get user from Firestore
            user_doc = db.collection('users').document(uid).get()
            if not user_doc.exists:
                raise AuthenticationFailed(f'User {uid} not found in Firestore')
            
            user_data = user_doc.to_dict()
            user = FirestoreUser(uid, user_data)
            
            return (user, None)
            
        except firebase_admin.auth.InvalidIdTokenError as e:
            raise AuthenticationFailed(f'Invalid Firebase token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Firebase authentication error: {str(e)}')
