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
    
    doctors = DoctorProfile.objects.filter(is_available=True, is_approved=True)
    
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
            is_available=True,
            is_approved=True
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
    Required fields: doctor_id, appointment_date, consultation_type, notes
    Optional fields: disease_id
    """
    try:
        patient_profile = request.user.patient_profile
        doctor_id = request.data.get('doctor_id')
        appointment_date = request.data.get('appointment_date')
        disease_id = request.data.get('disease_id', None)
        notes = request.data.get('notes', '')
        consultation_type = request.data.get('consultation_type', 'video')
        
        if not doctor_id or not appointment_date:
            return Response(
                {'error': 'doctor_id and appointment_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if doctor is approved
        if not doctor.is_approved:
            return Response(
                {'error': 'This doctor is not yet approved. Please choose another doctor.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
            notes=notes,
            consultation_type=consultation_type
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
        
        # Check if doctor is approved
        if not doctor_profile.is_approved:
            return Response(
                {'error': 'Your doctor account is pending admin approval. You cannot view patients yet.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsPatient])
def reschedule_appointment(request, appointment_id):
    """
    Reschedule an appointment to a new date/time
    Request body: { "appointment_date": "ISO datetime string" }
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Verify patient owns this appointment
        if appointment.patient.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only allow rescheduling scheduled appointments
        if appointment.status != 'scheduled':
            return Response(
                {'error': f'Cannot reschedule a {appointment.status} appointment'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get new appointment date
        from django.utils.dateparse import parse_datetime
        new_date = request.data.get('appointment_date')
        
        if not new_date:
            return Response({'error': 'appointment_date is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.utils import timezone
            new_datetime = parse_datetime(new_date)
            if new_datetime is None:
                raise ValueError('Invalid datetime format')
            
            # Ensure the datetime is timezone-aware
            if timezone.is_naive(new_datetime):
                new_datetime = timezone.make_aware(new_datetime)
            
            appointment.appointment_date = new_datetime
            appointment.save()
            
            serializer = AppointmentSerializer(appointment)
            return Response(
                {'message': 'Appointment rescheduled successfully', 'appointment': serializer.data},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({'error': f'Invalid datetime format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsPatient])
def cancel_appointment(request, appointment_id):
    """
    Cancel an appointment
    Request body: { "reason": "cancellation reason (optional)" }
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Verify patient owns this appointment
        if appointment.patient.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only allow cancelling scheduled appointments
        if appointment.status != 'scheduled':
            return Response(
                {'error': f'Cannot cancel a {appointment.status} appointment'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel the appointment
        appointment.status = 'cancelled'
        appointment.save()
        
        serializer = AppointmentSerializer(appointment)
        return Response(
            {'message': 'Appointment cancelled successfully', 'appointment': serializer.data},
            status=status.HTTP_200_OK
        )
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsDoctor])
def mark_appointment_complete(request, appointment_id):
    """
    Mark an appointment as completed (Doctor only)
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Verify doctor owns this appointment
        if appointment.doctor.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mark as completed
        appointment.status = 'completed'
        appointment.save()
        
        serializer = AppointmentSerializer(appointment)
        return Response(
            {'message': 'Appointment marked as completed', 'appointment': serializer.data},
            status=status.HTTP_200_OK
        )
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsDoctor])
def update_appointment_notes(request, appointment_id):
    """
    Update appointment notes (Doctor only)
    Request body: { "notes": "consultation notes" }
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Verify doctor owns this appointment
        if appointment.doctor.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notes = request.data.get('notes', '')
        if notes:
            appointment.notes = notes
            appointment.save()
        
        serializer = AppointmentSerializer(appointment)
        return Response(
            {'message': 'Notes updated successfully', 'appointment': serializer.data},
            status=status.HTTP_200_OK
        )
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def create_prescription(request):
    """
    Create a prescription for an appointment (Doctor only)
    Request body: {
        "appointment_id": int,
        "medication_name": str,
        "dosage": str,
        "frequency": str,
        "duration_days": int,
        "instructions": str (optional)
    }
    """
    try:
        appointment_id = request.data.get('appointment_id')
        medication_name = request.data.get('medication_name')
        dosage = request.data.get('dosage')
        frequency = request.data.get('frequency')
        duration_days = request.data.get('duration_days', 7)
        instructions = request.data.get('instructions', '')
        
        # Validate required fields
        if not all([appointment_id, medication_name, dosage, frequency]):
            return Response(
                {'error': 'appointment_id, medication_name, dosage, and frequency are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get appointment
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Verify doctor owns this appointment
        if appointment.doctor.user != request.user:
            return Response(
                {'error': 'You do not have permission to create prescription for this appointment'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create prescription
        from appointments.models import Prescription
        prescription = Prescription.objects.create(
            appointment=appointment,
            doctor=appointment.doctor,
            patient=appointment.patient,
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            duration_days=int(duration_days),
            instructions=instructions,
            status='active'
        )
        
        return Response(
            {
                'message': 'Prescription created successfully',
                'prescription': {
                    'id': prescription.id,
                    'medication_name': prescription.medication_name,
                    'dosage': prescription.dosage,
                    'frequency': prescription.frequency,
                    'duration_days': prescription.duration_days,
                    'status': prescription.status,
                    'issued_at': prescription.issued_at
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

