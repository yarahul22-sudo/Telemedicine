# Import all models
from .models.base import CustomUser
from .models.patient import PatientProfile
from .models.doctor import DoctorProfile
from .models.admin import AdminProfile

__all__ = [
    'CustomUser',
    'PatientProfile',
    'DoctorProfile',
    'AdminProfile',
]
