from django.db import models
from django.core.validators import RegexValidator
from .base import CustomUser

class DoctorProfile(models.Model):
    """Extended profile model for Doctor users"""
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('gynecology', 'Gynecology'),
        ('psychiatry', 'Psychiatry'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Practitioner'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        limit_choices_to={'role': 'doctor'}
    )
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        help_text="Medical specialization"
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Medical license number"
    )
    experience_years = models.IntegerField(
        default=0,
        help_text="Years of medical experience"
    )
    qualification = models.CharField(
        max_length=200,
        blank=True,
        help_text="Medical qualifications (e.g., MD, MBBS)"
    )
    clinic_address = models.TextField(blank=True)
    clinic_phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number')]
    )
    consultation_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Consultation fee in USD"
    )
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    profile_image_url = models.URLField(max_length=500, blank=True, help_text="Public URL to profile photo")
    bio = models.TextField(blank=True, help_text="Professional biography")
    available_days = models.CharField(
        max_length=100,
        blank=True,
        help_text="Available days (e.g., Monday,Tuesday,Wednesday,Thursday,Friday)",
        default="Monday,Tuesday,Wednesday,Thursday,Friday"
    )
    is_approved = models.BooleanField(
        default=False,
        help_text="Admin approval status for doctor account"
    )
    rating = models.FloatField(default=5.0, help_text="Doctor rating (1-5)")
    total_appointments = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Doctor Profile"
        verbose_name_plural = "Doctor Profiles"
        ordering = ['-rating', '-created_at']
        indexes = [
            models.Index(fields=['specialization']),
            models.Index(fields=['is_available']),
        ]
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"
