from django.db import models
from users.models.patient import PatientProfile
from users.models.doctor import DoctorProfile


class Disease(models.Model):
    """Model for diseases/conditions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    specialization_required = models.CharField(
        max_length=50,
        choices=[
            ('cardiology', 'Cardiology'),
            ('neurology', 'Neurology'),
            ('orthopedics', 'Orthopedics'),
            ('dermatology', 'Dermatology'),
            ('gynecology', 'Gynecology'),
            ('psychiatry', 'Psychiatry'),
            ('pediatrics', 'Pediatrics'),
            ('general', 'General Practitioner'),
            ('other', 'Other'),
        ],
        help_text="Recommended specialization for this disease"
    )
    
    class Meta:
        verbose_name = "Disease"
        verbose_name_plural = "Diseases"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Appointment(models.Model):
    """Model for appointments between patients and doctors"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    disease = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    appointment_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(blank=True, help_text="Patient notes about symptoms/concerns")
    consultation_type = models.CharField(
        max_length=20,
        choices=[
            ('video', 'Video Call'),
            ('audio', 'Audio Call'),
            ('in_person', 'In-Person'),
        ],
        default='video'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['-appointment_date']
        indexes = [
            models.Index(fields=['patient', 'doctor']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Appointment: {self.patient.user.get_full_name()} with Dr. {self.doctor.user.get_full_name()}"
