# Import all serializers
from .serializers.base import BaseUserSerializer, UserRegistrationSerializer, UserLoginSerializer
from .serializers.patient import PatientProfileSerializer, PatientDetailSerializer
from .serializers.doctor import DoctorProfileSerializer, DoctorDetailSerializer

__all__ = [
    'BaseUserSerializer',
    'UserRegistrationSerializer',
    'UserLoginSerializer',
    'PatientProfileSerializer',
    'PatientDetailSerializer',
    'DoctorProfileSerializer',
    'DoctorDetailSerializer',
]
