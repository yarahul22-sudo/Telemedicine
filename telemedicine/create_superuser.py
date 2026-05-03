"""
Run this script ONCE to create the Django /djangoadmin/ superuser.
Usage: python create_superuser.py

This creates a local Django database user (NOT Firebase).
Login at: http://127.0.0.1:8000/djangoadmin/
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credentials for /djangoadmin/ login
USERNAME = "admin@gmail.com"
PASSWORD = "Rahul12345"

try:
    if User.objects.filter(username=USERNAME).exists():
        user = User.objects.get(username=USERNAME)
        user.set_password(PASSWORD)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.role = 'admin'
        user.save()
        print(f"Updated existing superuser: {USERNAME}")
    else:
        user = User.objects.create_superuser(
            username=USERNAME,
            email=USERNAME,
            password=PASSWORD,
        )
        user.role = 'admin'
        user.save()
        print(f"Created superuser: {USERNAME}")

    print(f"\nDjango Admin Login:")
    print(f"  URL:      http://127.0.0.1:8000/djangoadmin/")
    print(f"  Username: {USERNAME}")
    print(f"  Password: {PASSWORD}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
