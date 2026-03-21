from .base import BaseUserSerializer, UserRegistrationSerializer, UserLoginSerializer
from .patient import PatientProfileSerializer, PatientDetailSerializer
from .doctor import DoctorProfileSerializer, DoctorDetailSerializer

__all__ = [
    'BaseUserSerializer',
    'UserRegistrationSerializer',
    'UserLoginSerializer',
    'PatientProfileSerializer',
    'PatientDetailSerializer',
    'DoctorProfileSerializer',
    'DoctorDetailSerializer',
]

