from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from users.models.doctor import DoctorProfile
from users.models.patient import PatientProfile
from appointments.models import Appointment, Disease
from users.permissions.role_permissions import IsPatient, IsDoctor
# from appointments.serializers import AppointmentSerializer, DoctorListSerializer, DiseaseSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_doctors_by_specialty(request):
    """
    Search doctors by specialty and diseases from Firestore.
    Query params: specialty (optional), disease (optional)
    """
    from telemedicine.firestore_db import db
    specialty = request.query_params.get('specialty', None)
    disease_name = request.query_params.get('disease', None)
    
    try:
        users_ref = db.collection('users')
        # Start with all doctors who are approved
        query = users_ref.where('role', '==', 'doctor').where('is_approved', '==', True)
        
        if specialty:
            query = query.where('specialization', '==', specialty.lower())
        
        # In a real app with disease-specialty mapping in Firestore:
        # if disease_name:
        #    ... lookup specialty for disease ...
        
        doctors_docs = query.stream()
        doctors_list = []
        
        for doc in doctors_docs:
            data = doc.to_dict()
            data['id'] = doc.id
            # Handle full_name for the frontend
            data['full_name'] = f"{data.get('first_name', '')} {data.get('last_name', '')}"
            data['specialization_display'] = data.get('specialization', 'General').title()
            doctors_list.append(data)
            
        return Response(doctors_list, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Firestore Search Error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_diseases(request):
    """Get list of all diseases from Firestore (or static list)"""
    # For now returning a static list as diseases aren't fully migrated to Firestore yet
    diseases = [
        {'id': '1', 'name': 'Fever', 'specialization_required': 'general'},
        {'id': '2', 'name': 'Heart Ache', 'specialization_required': 'cardiology'},
    ]
    return Response(diseases, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def get_recommended_doctors(request):
    """
    Get doctors recommended based on Firestore profile
    """
    from telemedicine.firestore_db import db
    try:
        # Simplified recommendation logic: return highly rated doctors
        doctors_ref = db.collection('users')
        query = doctors_ref.where('role', '==', 'doctor').where('is_approved', '==', True).limit(5)
        
        docs = query.stream()
        doctors_list = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            data['full_name'] = f"{data.get('first_name', '')} {data.get('last_name', '')}"
            doctors_list.append(data)
            
        return Response(doctors_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny

from django.http import JsonResponse

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    """
    Book an appointment with a doctor in Firestore.
    Expects Firebase token in Authorization header: Bearer <token>
    """
    from telemedicine.firestore_db import db
    from firebase_admin import firestore
    
    try:


        data = request.data
        doctor_id = data.get('doctor_id')
        appointment_date_str = data.get('appointment_date')
        disease_id = data.get('disease_id')
        notes = data.get('notes', '')
        consultation_type = data.get('consultation_type', 'video')
        
        if not doctor_id or not appointment_date_str:
            return JsonResponse({'error': 'doctor_id and appointment_date are required'}, status=400)
        
        # Verify doctor
        doctor_doc = db.collection('users').document(str(doctor_id)).get()
        if not doctor_doc.exists:
            return JsonResponse({'error': 'Doctor not found'}, status=404)
            
        doctor_data = doctor_doc.to_dict()
        
        # Convert ISO date string to Firestore timestamp
        from datetime import datetime
        try:
            # Parse ISO string to datetime and convert to Firestore timestamp
            appointment_datetime = datetime.fromisoformat(appointment_date_str.replace('Z', '+00:00'))
            appointment_timestamp = firestore.Timestamp.from_datetime(appointment_datetime)
            print(f"✅ Converted appointment_date from ISO string to Firestore timestamp: {appointment_datetime} -> {appointment_timestamp}")
        except Exception as date_err:
            print(f"❌ Error converting appointment_date: {date_err}")
            appointment_timestamp = appointment_date_str  # Fallback to string if conversion fails
        
        # Create appointment data
        appointment_data = {
            'patient_id': request.user.uid,
            'patient_name': request.user.get_full_name(),
            'doctor_id': str(doctor_id),
            'doctor_name': f"Dr. {doctor_data.get('first_name', '')} {doctor_data.get('last_name', '')}",
            'appointment_date': appointment_timestamp, 
            'disease_id': disease_id,
            'notes': notes,
            'consultation_type': consultation_type,
            'status': 'scheduled',
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        print(f"📝 Booking appointment with patient_id: {request.user.uid}")
        print(f"   Patient: {request.user.get_full_name()} ({request.user.email})")
        print(f"   Doctor: {str(doctor_id)}")
        print(f"   Date: {appointment_timestamp}")
        
        # Save to Firestore
        doc_ref = db.collection('appointments').add(appointment_data)
        appointment_data['id'] = doc_ref[1].id
        
        print(f"✅ Appointment saved to Firestore with ID: {appointment_data['id']}")
        
        # Send Email Notifications (HTML Format)
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        from django.conf import settings
        
        try:
            dashboard_url = request.build_absolute_uri('/dashboard/')
            appointment_id_str = appointment_data['id']
            
            # 1. Email to Patient
            patient_context = {
                'patient_name': request.user.first_name,
                'doctor_name': appointment_data['doctor_name'],
                'appointment_date': appointment_date_str,
                'condition': notes or 'General Consultation',
                'consultation_type': consultation_type.title(),
                'dashboard_url': dashboard_url,
                'booking_id': appointment_id_str,
            }
            try:
                p_html = render_to_string('emails/patient_booking_confirmation.html', patient_context)
                p_text = strip_tags(p_html)
                p_email = EmailMultiAlternatives(
                    "✅ Booking Confirmed - TeleMed",
                    p_text,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email]
                )
                p_email.attach_alternative(p_html, "text/html")
                p_email.send(fail_silently=False)
                print(f"[EMAIL OK] Patient notification sent to {request.user.email}")
            except Exception as pe:
                import traceback
                print(f"[EMAIL FAIL] Patient email failed: {pe}")
                traceback.print_exc()

            # 2. Email to Doctor
            # Try multiple field names in case Firestore stores it differently
            doctor_email = (
                doctor_data.get('email') or
                doctor_data.get('email_address') or
                doctor_data.get('contact_email') or ''
            ).strip()

            print(f"[EMAIL] Doctor email resolved: '{doctor_email}'")

            if doctor_email:
                doctor_context = {
                    'doctor_name': doctor_data.get('last_name', doctor_data.get('first_name', 'Doctor')),
                    'patient_name': request.user.get_full_name(),
                    'patient_initial': request.user.first_name[0].upper() if request.user.first_name else 'P',
                    'patient_email': request.user.email,
                    'appointment_date': appointment_date_str,
                    'condition': notes or 'General Consultation',
                    'consultation_type': consultation_type.title(),
                    'dashboard_url': dashboard_url,
                    'booking_id': appointment_id_str,
                }
                try:
                    d_html = render_to_string('emails/doctor_new_appointment.html', doctor_context)
                    d_text = strip_tags(d_html)
                    d_email = EmailMultiAlternatives(
                        "📅 New Appointment Received - TeleMed",
                        d_text,
                        settings.DEFAULT_FROM_EMAIL,
                        [doctor_email]
                    )
                    d_email.attach_alternative(d_html, "text/html")
                    d_email.send(fail_silently=False)
                    print(f"[EMAIL OK] Doctor notification sent to {doctor_email}")
                except Exception as de:
                    import traceback
                    print(f"[EMAIL FAIL] Doctor email failed: {de}")
                    traceback.print_exc()
            else:
                print("[EMAIL SKIP] Doctor email skipped - no email address found in Firestore user document.")
                print(f"[EMAIL DEBUG] Doctor Firestore fields: {list(doctor_data.keys())}")
                
        except Exception as mail_err:
            import traceback
            print(f"[EMAIL FAIL] Notification block error: {mail_err}")
            traceback.print_exc()

        # Remove Sentinel objects before returning as JSON
        if 'created_at' in appointment_data:
            del appointment_data['created_at']

        return JsonResponse(appointment_data, status=201)
        
    except Exception as e:
        print(f"Booking Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def get_doctor_patients(request):
    """
    Get list of patients assigned to this doctor from Firestore
    """
    from telemedicine.firestore_db import db
    try:
        appointments_ref = db.collection('appointments')
        
        # Get all appointments for this doctor
        appointments = appointments_ref.where('doctor_id', '==', request.user.uid).stream()
        
        patients_list = []
        for doc in appointments:
            data = doc.to_dict()
            data['id'] = doc.id
            patients_list.append(data)
        
        return Response(patients_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def get_my_appointments(request):
    """
    Get patient's appointments from Firestore
    """
    from telemedicine.firestore_db import db
    try:
        appointments_ref = db.collection('appointments')
        query = appointments_ref.where('patient_id', '==', request.user.uid).stream()
        
        appointments_list = []
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            appointments_list.append(data)
            
        return Response(appointments_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE', 'POST']) # Support both for convenience
@permission_classes([IsAuthenticated, IsPatient])
def cancel_appointment(request, appointment_id):
    """
    Cancel an appointment in Firestore
    """
    from telemedicine.firestore_db import db
    try:
        doc_ref = db.collection('appointments').document(appointment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        data = doc.to_dict()
        if data.get('patient_id') != request.user.uid:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        doc_ref.update({'status': 'cancelled'})
        return Response({'message': 'Appointment cancelled successfully'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'POST'])
@permission_classes([IsAuthenticated, IsPatient])
def reschedule_appointment(request, appointment_id):
    """
    Reschedule an appointment in Firestore
    """
    from telemedicine.firestore_db import db
    try:
        new_date = request.data.get('appointment_date')
        if not new_date:
            return Response({'error': 'appointment_date is required'}, status=status.HTTP_400_BAD_REQUEST)

        doc_ref = db.collection('appointments').document(appointment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        data = doc.to_dict()
        if data.get('patient_id') != request.user.uid:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        doc_ref.update({'appointment_date': new_date})
        return Response({'message': 'Appointment rescheduled successfully'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def mark_appointment_complete(request, appointment_id):
    """
    Mark an appointment as completed in Firestore (Doctor only)
    """
    from telemedicine.firestore_db import db
    try:
        doc_ref = db.collection('appointments').document(appointment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        data = doc.to_dict()
        if data.get('doctor_id') != request.user.uid:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        doc_ref.update({'status': 'completed'})
        return Response({'message': 'Appointment marked as completed'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def update_appointment_notes(request, appointment_id):
    """
    Update appointment notes in Firestore (Doctor only)
    """
    from telemedicine.firestore_db import db
    try:
        doc_ref = db.collection('appointments').document(appointment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        data = doc.to_dict()
        if data.get('doctor_id') != request.user.uid:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        notes = request.data.get('notes', '')
        doc_ref.update({'notes': notes})
        return Response({'message': 'Notes updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def create_prescription(request):
    """
    Create a prescription in Firestore (Doctor only)
    """
    from telemedicine.firestore_db import db
    from firebase_admin import firestore
    try:
        appointment_id = request.data.get('appointment_id')
        medication_name = request.data.get('medication_name')
        dosage = request.data.get('dosage')
        frequency = request.data.get('frequency')
        duration_days = request.data.get('duration_days', 7)
        instructions = request.data.get('instructions', '')
        
        # Get appointment to verify ownership
        app_doc = db.collection('appointments').document(appointment_id).get()
        if not app_doc.exists:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        app_data = app_doc.to_dict()
        if app_data.get('doctor_id') != request.user.uid:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        prescription_data = {
            'appointment_id': appointment_id,
            'patient_id': app_data.get('patient_id'),
            'doctor_id': request.user.uid,
            'medication_name': medication_name,
            'dosage': dosage,
            'frequency': frequency,
            'duration_days': int(duration_days),
            'instructions': instructions,
            'is_active': True,
            'issued_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('prescriptions').add(prescription_data)
        return Response({'message': 'Prescription created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.conf import settings
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_video_token(request, appointment_id):
    """
    Generate a Twilio Video access token for a Firestore appointment
    Both patient and doctor roles can access
    """
    from telemedicine.firestore_db import db
    try:
        doc = db.collection('appointments').document(str(appointment_id)).get()
        if not doc.exists:
            print(f"ERROR: Appointment {appointment_id} not found in Firestore")
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        data = doc.to_dict()
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        user_id = getattr(request.user, 'uid', None)
        
        print(f"DEBUG: Token Request - Patient: {patient_id}, Doctor: {doctor_id}, User: {user_id}")
        
        # Verify user is either the patient or the doctor
        if user_id not in [patient_id, doctor_id]:
            print(f"ERROR: User {user_id} not authorized for appointment {appointment_id}")
            return Response({'error': 'You do not have permission to join this call'}, status=status.HTTP_403_FORBIDDEN)
            
        # Validate Twilio credentials exist
        if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY, settings.TWILIO_API_SECRET]):
            print("ERROR: Missing Twilio credentials in settings")
            return Response({'error': 'Twilio configuration error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        room_name = f"appointment_{appointment_id}"
        user_name = getattr(request.user, 'get_full_name', lambda: request.user.email)()
        identity = user_name or request.user.email or f"user_{user_id}"
        
        print(f"DEBUG: Generating Twilio Token - Identity: {identity}, Room: {room_name}")
        print(f"DEBUG: Account SID: {settings.TWILIO_ACCOUNT_SID[:10]}...")

        # Create token with proper credentials
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity=identity,
            ttl=3600  # Token valid for 1 hour
        )
        
        # Add video grant for the room
        video_grant = VideoGrant(room=room_name)
        token.add_grant(video_grant)
        
        jwt_token = token.to_jwt()
        print(f"DEBUG: Token generated successfully, length: {len(jwt_token)}")
        
        return Response({
            'token': jwt_token,
            'room_name': room_name,
            'identity': identity
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"ERROR in generate_video_token: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Token generation failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


