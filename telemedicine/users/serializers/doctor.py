from rest_framework import serializers
from users.models.doctor import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for Doctor Profile"""
    class Meta:
        model = DoctorProfile
        fields = ['id', 'specialization', 'license_number', 'experience_years',
                  'qualification', 'clinic_address', 'clinic_phone', 
                  'consultation_fee', 'profile_picture', 'bio', 'rating',
                  'total_appointments', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_appointments', 'rating', 'created_at', 'updated_at']

class DoctorDetailSerializer(serializers.ModelSerializer):
    """Full doctor details with user info"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    is_verified = serializers.BooleanField(source='user.is_verified', read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'is_verified', 'specialization', 'license_number', 'experience_years',
                  'qualification', 'clinic_address', 'clinic_phone', 'consultation_fee',
                  'profile_picture', 'bio', 'rating', 'total_appointments', 'is_available']
