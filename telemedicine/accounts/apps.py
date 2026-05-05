from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(self):
        """Initialize Firebase Admin SDK when the app is ready"""
        try:
            from telemedicine.firebase_setup import initialize_firebase
            initialize_firebase()
            print("✅ Firebase initialized in AccountsConfig.ready()")
        except Exception as e:
            print(f"❌ Error initializing Firebase in AccountsConfig: {e}")
