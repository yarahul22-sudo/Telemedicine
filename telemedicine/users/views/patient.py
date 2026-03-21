from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models.patient import PatientProfile
from users.serializers.patient import PatientProfileSerializer, PatientDetailSerializer
from users.permissions.role_permissions import IsPatient

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def create_patient_profile(request):
    """Create patient profile"""
    if hasattr(request.user, 'patient_profile'):
        return Response({'error': 'Patient profile already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    serializer = PatientProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save(user=request.user)
        return Response(PatientDetailSerializer(profile).data, 
                       status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def get_patient_profile(request):
    """Get patient profile"""
    try:
        profile = request.user.patient_profile
        return Response(PatientDetailSerializer(profile).data, 
                       status=status.HTTP_200_OK)
    except PatientProfile.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsPatient])
def update_patient_profile(request):
    """Update patient profile"""
    try:
        profile = request.user.patient_profile
        serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(PatientDetailSerializer(profile).data, 
                           status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PatientProfile.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_patients(request):
    """List all patients (admin/doctor only)"""
    if not (request.user.is_admin_user() or request.user.is_doctor()):
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    patients = PatientProfile.objects.all()
    serializer = PatientDetailSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
