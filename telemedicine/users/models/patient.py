from django.db import models
from django.core.validators import RegexValidator
from .base import CustomUser

class PatientProfile(models.Model):
    """Extended profile model for Patient users"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        limit_choices_to={'role': 'patient'}
    )
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True, help_text="Patient medical history")
    allergies = models.TextField(blank=True, help_text="Known allergies")
    current_diseases = models.TextField(blank=True, help_text="Current health conditions/diseases")
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number')]
    )
    profile_picture = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)
    profile_image_url = models.URLField(max_length=500, blank=True, help_text="Public URL to profile photo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Patient Profile: {self.user.get_full_name()}"
