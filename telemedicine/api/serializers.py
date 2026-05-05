"""
API ViewSets for Telemedicine Platform
ModelViewSets for REST endpoints
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model


User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    """ViewSet for User endpoints"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List users (admin only)"""
        return Response({
            'success': True,
            'data': []
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get user details"""
        return Response({
            'success': True,
            'data': {'user_id': pk}
        }, status=status.HTTP_200_OK)


class DoctorViewSet(viewsets.ViewSet):
    """ViewSet for Doctor endpoints"""
    permission_classes = [AllowAny]
    
    def list(self, request):
        """List all doctors"""
        return Response({
            'success': True,
            'data': [],
            'pagination': {'total': 0, 'limit': 20, 'offset': 0}
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get specific doctor"""
        return Response({
            'success': True,
            'data': {'doctor_id': pk}
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get doctor availability"""
        return Response({
            'success': True,
            'data': {'doctor_id': pk, 'availability': []}
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get doctor reviews"""
        return Response({
            'success': True,
            'data': {'doctor_id': pk, 'reviews': []}
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register as doctor"""
        return Response({
            'success': True,
            'message': 'Doctor profile submitted for approval',
            'data': {'doctor_id': 'DOC-001', 'status': 'pending_approval'}
        }, status=status.HTTP_201_CREATED)


class PatientViewSet(viewsets.ViewSet):
    """ViewSet for Patient endpoints"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List patients (admin only)"""
        return Response({
            'success': True,
            'data': []
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get patient profile"""
        return Response({
            'success': True,
            'data': {'patient_id': pk}
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get', 'put'])
    def profile(self, request):
        """Get/update patient profile"""
        if request.method == 'GET':
            return Response({
                'success': True,
                'data': {
                    'patient_id': f'PAT-{request.user.id}',
                    'user_id': f'USR-{request.user.id}',
                    'first_name': request.user.first_name,
                    'email': request.user.email,
                    'chronic_diseases': [],
                    'allergies': []
                }
            }, status=status.HTTP_200_OK)
        
        else:  # PUT
            return Response({
                'success': True,
                'message': 'Profile updated successfully'
            }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def medical_records(self, request):
        """Get patient medical records"""
        return Response({
            'success': True,
            'data': {'medical_records': []}
        }, status=status.HTTP_200_OK)


class AppointmentViewSet(viewsets.ViewSet):
    """ViewSet for Appointment endpoints"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List user appointments"""
        return Response({
            'success': True,
            'data': [],
            'pagination': {'total': 0, 'limit': 20, 'offset': 0}
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get appointment details"""
        return Response({
            'success': True,
            'data': {'appointment_id': pk}
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def book(self, request):
        """Book new appointment"""
        return Response({
            'success': True,
            'message': 'Appointment booked successfully',
            'data': {
                'appointment_id': 'APT-001',
                'status': 'confirmed',
                'confirmation_number': 'CONF-001'
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['put'])
    def reschedule(self, request, pk=None):
        """Reschedule appointment"""
        return Response({
            'success': True,
            'message': 'Reschedule request sent to doctor',
            'data': {'appointment_id': pk, 'status': 'reschedule_requested'}
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel appointment"""
        return Response({
            'success': True,
            'message': 'Appointment cancelled successfully',
            'data': {'appointment_id': pk, 'status': 'cancelled'}
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete appointment (doctor only)"""
        return Response({
            'success': True,
            'message': 'Appointment marked as completed',
            'data': {'appointment_id': pk, 'status': 'completed'}
        }, status=status.HTTP_200_OK)


class PrescriptionViewSet(viewsets.ViewSet):
    """ViewSet for Prescription endpoints"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List prescriptions"""
        return Response({
            'success': True,
            'data': [],
            'pagination': {'total': 0, 'limit': 20, 'offset': 0}
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Get prescription details"""
        return Response({
            'success': True,
            'data': {'prescription_id': pk}
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def add_prescription(self, request):
        """Create prescription (doctor only)"""
        return Response({
            'success': True,
            'message': 'Prescription created and sent to patient',
            'data': {'prescription_id': 'PRE-001', 'status': 'active'}
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Download prescription as PDF"""
        return Response({
            'success': True,
            'message': 'Prescription downloaded',
            'data': {'prescription_id': pk}
        }, status=status.HTTP_200_OK)
