from rest_framework import serializers
from users.models.patient import PatientProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    """Serializer for Patient Profile"""
    user_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = PatientProfile
        fields = ['id', 'user_id', 'date_of_birth', 'medical_history', 
                  'allergies', 'emergency_contact', 'emergency_phone', 
                  'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PatientDetailSerializer(serializers.ModelSerializer):
    """Full patient details with user info"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = PatientProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'date_of_birth', 'medical_history', 'allergies',
                  'emergency_contact', 'emergency_phone', 'profile_picture']
