from django.db import models
from django.core.validators import RegexValidator
from .base import CustomUser

class AdminProfile(models.Model):
    """Extended profile model for Admin users"""
    DEPARTMENT_CHOICES = [
        ('management', 'Management'),
        ('support', 'Support'),
        ('compliance', 'Compliance'),
        ('finance', 'Finance'),
        ('it', 'IT'),
        ('hr', 'Human Resources'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='admin_profile',
        limit_choices_to={'role': 'admin'}
    )
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='management'
    )
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100)
    permissions = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Admin: {self.user.get_full_name()} ({self.get_department_display()})"
