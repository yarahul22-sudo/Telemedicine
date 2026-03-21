from rest_framework import serializers
from users.models.base import CustomUser
from django.contrib.auth import authenticate

class BaseUserSerializer(serializers.ModelSerializer):
    """Base serializer for CustomUser"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'role', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'first_name', 'last_name', 'phone', 'role']
    
    def validate(self, data):
        if data.get('password') != data.pop('password_confirm'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', 'patient')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        data['user'] = user
        return data
