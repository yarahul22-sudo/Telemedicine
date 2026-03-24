from django.core.management.base import BaseCommand
from users.models import CustomUser, DoctorProfile


class Command(BaseCommand):
    help = 'Create test doctors for the system'

    def handle(self, *args, **options):
        doctors_data = [
            {
                'email': 'dermatologist@example.com',
                'username': 'dermatologist',
                'first_name': 'Dr. Rachel',
                'last_name': 'Nelson',
                'specialization': 'dermatology',
                'license_number': 'DL12345',
                'experience_years': 8,
                'qualification': 'MD, Dermatology Specialist',
                'consultation_fee': 50.00,
                'bio': 'Experienced dermatologist specializing in skin conditions, acne, and psoriasis',
                'rating': 4.8,
            },
            {
                'email': 'cardiologist@example.com',
                'username': 'cardiologist',
                'first_name': 'Dr. Michael',
                'last_name': 'Chen',
                'specialization': 'cardiology',
                'license_number': 'CL67890',
                'experience_years': 12,
                'qualification': 'MD, MS in Cardiology',
                'consultation_fee': 75.00,
                'bio': 'Board-certified cardiologist with 12 years of experience',
                'rating': 4.9,
            },
            {
                'email': 'neurolog@example.com',
                'username': 'neurologist',
                'first_name': 'Dr. Sarah',
                'last_name': 'Kumar',
                'specialization': 'neurology',
                'license_number': 'NL24680',
                'experience_years': 10,
                'qualification': 'MD, Neurology Specialist',
                'consultation_fee': 60.00,
                'bio': 'Neurologist specializing in migraines and headaches',
                'rating': 4.7,
            },
        ]
        
        for doctor_data in doctors_data:
            try:
                if CustomUser.objects.filter(email=doctor_data['email']).exists():
                    self.stdout.write(f"Doctor {doctor_data['email']} already exists")
                    continue
                
                user = CustomUser.objects.create_user(
                    email=doctor_data['email'],
                    username=doctor_data['username'],
                    password='testpass123',
                    first_name=doctor_data['first_name'],
                    last_name=doctor_data['last_name'],
                    role='doctor'
                )
                
                profile_data = {k: v for k, v in doctor_data.items() if k not in ['email', 'username', 'first_name', 'last_name']}
                doctor_profile = DoctorProfile.objects.create(
                    user=user,
                    is_available=True,
                    **profile_data
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f"Created doctor: {user.get_full_name()} ({doctor_data['specialization']})")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating {doctor_data['email']}: {e}")
                )
        
        self.stdout.write(self.style.SUCCESS('Done!'))
