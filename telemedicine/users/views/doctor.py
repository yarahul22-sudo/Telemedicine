from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models.doctor import DoctorProfile
from users.serializers.doctor import DoctorProfileSerializer, DoctorDetailSerializer
from users.permissions.role_permissions import IsDoctor, IsVerified

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def create_doctor_profile(request):
    """Create doctor profile"""
    if hasattr(request.user, 'doctor_profile'):
        return Response({'error': 'Doctor profile already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    serializer = DoctorProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save(user=request.user)
        return Response(DoctorDetailSerializer(profile).data, 
                       status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def get_doctor_profile(request):
    """Get doctor profile"""
    try:
        profile = request.user.doctor_profile
        return Response(DoctorDetailSerializer(profile).data, 
                       status=status.HTTP_200_OK)
    except DoctorProfile.DoesNotExist:
        return Response({'error': 'Doctor profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsDoctor])
def update_doctor_profile(request):
    """Update doctor profile"""
    try:
        profile = request.user.doctor_profile
        serializer = DoctorProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(DoctorDetailSerializer(profile).data, 
                           status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except DoctorProfile.DoesNotExist:
        return Response({'error': 'Doctor profile not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_doctors(request):
    """List all verified doctors"""
    doctors = DoctorProfile.objects.filter(user__is_verified=True, is_available=True)
    serializer = DoctorDetailSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_doctors_by_specialization(request):
    """Search doctors by specialization"""
    specialization = request.query_params.get('specialization', None)
    if not specialization:
        return Response({'error': 'Specialization parameter required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    doctors = DoctorProfile.objects.filter(
        specialization=specialization,
        user__is_verified=True,
        is_available=True
    )
    serializer = DoctorDetailSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_by_id(request, doctor_id):
    """Get doctor profile by ID"""
    try:
        profile = DoctorProfile.objects.get(id=doctor_id, user__is_verified=True)
        return Response(DoctorDetailSerializer(profile).data, 
                       status=status.HTTP_200_OK)
    except DoctorProfile.DoesNotExist:
        return Response({'error': 'Doctor not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
