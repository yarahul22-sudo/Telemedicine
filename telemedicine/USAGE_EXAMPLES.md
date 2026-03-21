# Code Examples for Using the Authentication System

## 1. Using Role-Based Access Control in Views

### Protect views by role

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_only_view(request):
    """Only accessible by doctors"""
    if not request.user.is_doctor():
        return Response({'error': 'Only doctors can access this'}, status=403)
    return Response({'message': 'Welcome Doctor!'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_only_view(request):
    """Only accessible by patients"""
    if not request.user.is_patient():
        return Response({'error': 'Only patients can access this'}, status=403)
    return Response({'message': 'Welcome Patient!'})
```

## 2. Creating Permission Decorators

```python
from functools import wraps
from rest_framework.response import Response

def require_role(required_role):
    """Decorator to check user role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == required_role:
                return view_func(request, *args, **kwargs)
            return Response({'error': f'This action requires {required_role} role'}, 
                          status=403)
        return wrapper
    return decorator

# Usage:
@api_view(['GET'])
@require_role('doctor')
def schedule_appointment(request):
    # Only doctors can access
    pass
```

## 3. Querying Users by Role

```python
from users.models import CustomUser

# Get all doctors
all_doctors = CustomUser.objects.filter(role='doctor')

# Get verified doctors only
verified_doctors = CustomUser.objects.filter(role='doctor', is_verified=True)

# Get all patients
all_patients = CustomUser.objects.filter(role='patient')

# Get doctors by specialization
cardiologists = CustomUser.objects.filter(
    role='doctor', 
    specialization='Cardiology',
    is_verified=True
)

# Search doctors by name
doctor_results = CustomUser.objects.filter(
    role='doctor',
    first_name__icontains='Smith'
)
```

## 4. Getting User Information

```python
from django.contrib.auth.decorators import login_required

@login_required
def get_user_details(request):
    user = request.user
    
    # Basic info
    full_name = user.get_full_name()
    email = user.email
    phone = user.phone
    role = user.get_role_display()  # 'Patient', 'Doctor', etc.
    
    # Role-specific info
    if user.is_doctor():
        spec = user.specialization
        license = user.license_number
        experience = user.experience_years
    
    elif user.is_patient():
        history = user.medical_history
        dob = user.date_of_birth
    
    return {
        'name': full_name,
        'email': email,
        'phone': phone,
        'role': role,
        'verified': user.is_verified
    }
```

## 5. Creating Users Programmatically

```python
from users.models import CustomUser

# Create a patient
patient = CustomUser.objects.create_user(
    username='patient1',
    email='patient@example.com',
    password='secure123456',
    first_name='John',
    last_name='Doe',
    role='patient',
    phone='+1234567890',
    date_of_birth='1990-01-15'
)

# Create a doctor
doctor = CustomUser.objects.create_user(
    username='doctor1',
    email='doctor@example.com',
    password='secure123456',
    first_name='Jane',
    last_name='Smith',
    role='doctor',
    phone='+1987654321',
    specialization='Cardiology',
    license_number='LIC123456',
    experience_years=10
)

# Create an admin
admin = CustomUser.objects.create_user(
    username='admin1',
    email='admin@example.com',
    password='secure123456',
    first_name='Admin',
    last_name='User',
    role='admin'
)
```

## 6. Verifying Users in Admin Panel

```python
from users.models import CustomUser

# In Django shell
doctor = CustomUser.objects.get(username='doctor1')
doctor.is_verified = True
doctor.save()

# Or bulk verify doctors
verified_count = CustomUser.objects.filter(
    role='doctor'
).update(is_verified=True)
```

## 7. Checking Authentication in Templates

```html
{% if user.is_authenticated %}
    <p>Welcome {{ user.get_full_name }}!</p>
    
    {% if user.is_doctor %}
        <a href="/doctor-dashboard/">Doctor Dashboard</a>
    {% elif user.is_patient %}
        <a href="/patient-dashboard/">Patient Dashboard</a>
    {% elif user.is_admin_user %}
        <a href="/admin-dashboard/">Admin Dashboard</a>
    {% endif %}
{% else %}
    <a href="/api/users/login/">Login</a>
    <a href="/api/users/register/">Register</a>
{% endif %}
```

## 8. Serializing User Data

```python
from rest_framework import serializers
from users.models import CustomUser
from users.serializers import UserSerializer

# Use the built-in serializer
serializer = UserSerializer(user)
user_data = serializer.data

# Or create a custom serializer
class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 
                  'specialization', 'license_number', 'experience_years']

doctor = CustomUser.objects.get(role='doctor', username='doctor1')
serializer = DoctorDetailSerializer(doctor)
return Response(serializer.data)
```

## 9. Signal Handlers for User Creation

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Hook to run when user is created"""
    if created:
        # Send welcome email
        send_welcome_email(instance)
        
        # Create related profile if needed
        if instance.is_doctor():
            create_doctor_profile(instance)
        elif instance.is_patient():
            create_patient_profile(instance)
```

## 10. Updating User Profile

```python
from rest_framework.response import Response
from rest_framework import status

def update_user_profile(request):
    user = request.user
    data = request.data
    
    # Update allowed fields
    allowed_fields = ['first_name', 'last_name', 'phone', 'date_of_birth']
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    # Doctor-specific updates
    if user.is_doctor() and 'specialization' in data:
        user.specialization = data['specialization']
    
    user.save()
    return Response({'message': 'Profile updated successfully'}, 
                   status=status.HTTP_200_OK)
```

## 11. Token Authentication in Requests

```python
import requests

# Register and get token
response = requests.post('http://127.0.0.1:8000/api/users/register/', json={
    'username': 'user1',
    'email': 'user@example.com',
    'password': 'secure123456',
    'password_confirm': 'secure123456',
    'role': 'patient'
})

token = response.json()['token']

# Use token in subsequent requests
headers = {'Authorization': f'Token {token}'}
profile_response = requests.get(
    'http://127.0.0.1:8000/api/users/profile/',
    headers=headers
)
```

## 12. Batch User Creation for Testing

```python
from users.models import CustomUser

# Create multiple test patients
for i in range(10):
    CustomUser.objects.create_user(
        username=f'patient{i}',
        email=f'patient{i}@example.com',
        password='secure123456',
        role='patient',
        first_name=f'Patient{i}'
    )

# Create multiple test doctors
doctors_data = [
    {'spec': 'Cardiology', 'name': 'Dr. Smith'},
    {'spec': 'Neurology', 'name': 'Dr. Jones'},
    {'spec': 'Orthopedics', 'name': 'Dr. Brown'},
]

for idx, doc in enumerate(doctors_data):
    CustomUser.objects.create_user(
        username=f'doctor{idx}',
        email=f'doctor{idx}@example.com',
        password='secure123456',
        role='doctor',
        first_name=doc['name'],
        specialization=doc['spec'],
        license_number=f'LIC{idx:05d}',
        experience_years=5 + idx
    )
```

