from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from users.models.doctor import DoctorProfile
from users.models.patient import PatientProfile
from appointments.models import Appointment, Disease
from users.permissions.role_permissions import IsPatient, IsDoctor
from appointments.serializers import AppointmentSerializer, DoctorListSerializer, DiseaseSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_doctors_by_specialty(request):
    """
    Search doctors by specialty and diseases.
    Query params: specialty (optional), disease (optional)
    """
    specialty = request.query_params.get('specialty', None)
    disease_name = request.query_params.get('disease', None)
    
    doctors = DoctorProfile.objects.filter(is_available=True)
    
    if specialty:
        doctors = doctors.filter(specialization=specialty)
    
    if disease_name:
        try:
            disease = Disease.objects.get(name__icontains=disease_name)
            doctors = doctors.filter(specialization=disease.specialization_required)
        except Disease.DoesNotExist:
            return Response({'error': 'Disease not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DoctorListSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_diseases(request):
    """Get list of all diseases"""
    diseases = Disease.objects.all()
    serializer = DiseaseSerializer(diseases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def get_recommended_doctors(request):
    """
    Get doctors recommended based on patient's current diseases
    """
    try:
        patient_profile = request.user.patient_profile
        current_diseases = patient_profile.current_diseases
        
        if not current_diseases:
            return Response(
                {'message': 'Please update your current diseases to get recommendations'},
                status=status.HTTP_200_OK
            )
        
        # Find diseases that match patient's current diseases
        diseases = Disease.objects.filter(
            name__icontains=current_diseases
        ).values_list('specialization_required', flat=True).distinct()
        
        # Get doctors with matching specializations
        doctors = DoctorProfile.objects.filter(
            specialization__in=diseases,
            is_available=True
        ).order_by('-rating', '-experience_years')
        
        serializer = DoctorListSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PatientProfile.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def book_appointment(request):
    """
    Book an appointment with a doctor
    Required fields: doctor_id, appointment_date, disease_id (optional), notes (optional)
    """
    try:
        patient_profile = request.user.patient_profile
        doctor_id = request.data.get('doctor_id')
        appointment_date = request.data.get('appointment_date')
        disease_id = request.data.get('disease_id', None)
        notes = request.data.get('notes', '')
        
        if not doctor_id or not appointment_date:
            return Response(
                {'error': 'doctor_id and appointment_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        disease = None
        if disease_id:
            try:
                disease = Disease.objects.get(id=disease_id)
            except Disease.DoesNotExist:
                return Response({'error': 'Disease not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor,
            disease=disease,
            appointment_date=appointment_date,
            notes=notes
        )
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except PatientProfile.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def get_doctor_patients(request):
    """
    Get list of patients assigned to this doctor
    """
    try:
        doctor_profile = request.user.doctor_profile
        appointments = Appointment.objects.filter(
            doctor=doctor_profile,
            status__in=['scheduled', 'completed']
        ).select_related('patient', 'disease')
        
        patients_data = []
        for appointment in appointments:
            patient = appointment.patient
            patients_data.append({
                'patient_id': patient.id,
                'patient_name': patient.user.get_full_name(),
                'patient_email': patient.user.email,
                'disease': appointment.disease.name if appointment.disease else 'Not specified',
                'appointment_date': appointment.appointment_date,
                'status': appointment.status,
                'notes': appointment.notes,
                'current_conditions': patient.current_diseases,
                'medical_history': patient.medical_history,
                'allergies': patient.allergies,
            })
        
        return Response(patients_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def get_my_appointments(request):
    """
    Get patient's appointments
    """
    try:
        patient_profile = request.user.patient_profile
        appointments = Appointment.objects.filter(patient=patient_profile).select_related('doctor', 'disease')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PatientProfile.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

