from telemedicine.firestore_db import db

class FirestoreUser:
    # Django's login() and session system expect a _meta attribute
    class Meta:
        def __init__(self):
            # Django's session system calls value_to_string on the pk field
            self.pk = type('pk', (), {
                'name': 'uid', 
                'attname': 'uid', 
                'private': False,
                'to_python': lambda self, value: str(value),
                'value_to_string': lambda self, obj: str(obj.uid)
            })()
            self.model_name = 'firestoreuser'
            self.object_name = 'FirestoreUser'
            self.app_label = 'accounts'
            self.abstract = False
            self.swapped = False
    
    _meta = Meta()

    def __init__(self, uid, data):
        self.uid = uid
        self.data = data
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        
        # Pull basic fields from data
        self.email = data.get('email', '')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.role = data.get('role', 'patient')
        self.profile_image_url = data.get('profile_image_url', '')
        
    @property
    def id(self):
        return self.uid

    @property
    def pk(self):
        return self.uid

    @property
    def is_staff(self):
        return self.role == 'admin'

    @property
    def is_superuser(self):
        return self.role == 'admin'
        
    @property
    def is_verified(self):
        if self.role == 'doctor':
            return self.data.get('is_approved', False)
        return True # Patients are verified by default for now
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'

    def is_admin_user(self):
        return self.role == 'admin'

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Admin has all permissions"""
        return self.role == 'admin'

    def has_module_perms(self, app_label):
        """Admin has permissions for all modules"""
        return self.role == 'admin'

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.email

class FirestoreBackend:
    def authenticate(self, request, token=None, **kwargs):
        if not token:
            return None
            
        import firebase_admin.auth
        try:
            decoded_token = firebase_admin.auth.verify_id_token(token)
            uid = decoded_token['uid']
            
            # Fetch user from Firestore
            doc_ref = db.collection('users').document(uid)
            doc = doc_ref.get()
            if doc.exists:
                return FirestoreUser(uid, doc.to_dict())
            else:
                return None
        except Exception as e:
            print("FirestoreBackend auth error:", e)
            return None

    def get_user(self, user_id):
        try:
            doc_ref = db.collection('users').document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                return FirestoreUser(user_id, doc.to_dict())
            return None
        except Exception:
            return None
