from rest_framework import serializers
from appointments.models import Appointment, Disease
from users.models.doctor import DoctorProfile


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ['id', 'name', 'description', 'specialization_required']


class DoctorListSerializer(serializers.ModelSerializer):
    """Serializer for listing doctors"""
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'full_name', 'email', 'specialization', 'specialization_display',
            'experience_years', 'qualification', 'consultation_fee', 'profile_picture',
            'bio', 'rating', 'is_available', 'clinic_address', 'clinic_phone'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for appointments"""
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    disease_name = serializers.CharField(source='disease.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name', 
            'disease', 'disease_name', 'appointment_date', 'status', 'status_display',
            'notes', 'consultation_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
