"""
API Views for Telemedicine Platform
Handles all REST API endpoints
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'expires_in': 86400
    }


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    """Register a new user via API"""
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['email', 'password', 'user_type', 'first_name', 'last_name', 'phone']
        for field in required_fields:
            if field not in data:
                return Response({
                    'success': False,
                    'error': 'MISSING_FIELD',
                    'message': f'{field} is required'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        from django.contrib.auth import get_user_model
        import uuid
        User = get_user_model()
        
        if User.objects.filter(email=data['email']).exists():
            return Response({
                'success': False,
                'error': 'EMAIL_EXISTS',
                'message': 'Email already registered'
            }, status=status.HTTP_409_CONFLICT)
        
        # Create user
        user = User.objects.create_user(
            id=str(uuid.uuid4())[:128],  # Generate unique ID for CharField primary key
            username=data['email'],  # Use email as username
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            role=data.get('user_type', 'patient'),
        )
        
        # Store additional info
        user.phone = data.get('phone', '')
        user.save()
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user_id': f'USR-{user.id}',
                'email': user.email,
                'user_type': user.role,
                'created_at': user.created_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"REGISTRATION ERROR: {str(e)}")
        print(f"Traceback:\n{error_traceback}")
        return Response({
            'success': False,
            'error': 'REGISTRATION_ERROR',
            'message': str(e),
            'debug': error_traceback if False else None  # Remove debug in production
        }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """Login user and return JWT tokens"""
    try:
        data = request.data
        
        if not data.get('email') or not data.get('password'):
            return Response({
                'success': False,
                'error': 'INVALID_CREDENTIALS',
                'message': 'Email and password required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Try to find user by email
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'INVALID_CREDENTIALS',
                'message': 'Email or password is incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check password
        if not user.check_password(data['password']):
            return Response({
                'success': False,
                'error': 'INVALID_CREDENTIALS',
                'message': 'Email or password is incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'expires_in': tokens['expires_in'],
                'user': {
                    'user_id': f'USR-{user.id}',
                    'email': user.email,
                    'first_name': user.first_name,
                    'user_type': user.role,
                    'verified': True
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'LOGIN_ERROR',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """Logout user"""
    return Response({
        'success': True,
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    user = request.user
    return Response({
        'success': True,
        'data': {
            'user_id': f'USR-{user.id}',
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', ''),
            'user_type': user.role if hasattr(user, 'role') else 'patient',
            'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') else user.date_joined.isoformat(),
            'verified': True
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    """Get user notification preferences"""
    return Response({
        'success': True,
        'data': {
            'email_notifications': True,
            'sms_notifications': True,
            'in_app_notifications': True,
            'marketing_emails': False,
            'appointment_reminders': '24_hours_before',
            'quiet_hours_enabled': False
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Verify email address"""
    return Response({
        'success': True,
        'message': 'Email verified successfully'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """Request password reset"""
    return Response({
        'success': True,
        'message': 'Password reset link sent to email'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Confirm password reset"""
    return Response({
        'success': True,
        'message': 'Password reset successful'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enable_2fa(request):
    """Enable two-factor authentication"""
    return Response({
        'success': True,
        'data': {
            'qr_code': 'data:image/png;base64,...',
            'backup_codes': ['XXXX-XXXX-XXXX', 'YYYY-YYYY-YYYY']
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initialize_video_call(request):
    """Initialize a video call session"""
    return Response({
        'success': True,
        'data': {
            'call_session_id': 'CALL-202605-001',
            'appointment_id': request.data.get('appointment_id'),
            'ice_servers': [
                {'urls': 'stun:stun.telemedicine.moscow:3478'}
            ],
            'signaling_url': 'wss://signaling.telemedicine.moscow',
            'room_id': 'ROOM-APT-001',
            'call_started_at': '2026-05-05T14:00:00Z'
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_call_stats(request, call_id):
    """Get video call statistics"""
    return Response({
        'success': True,
        'data': {
            'call_session_id': call_id,
            'duration_seconds': 125,
            'video_quality': {'resolution': '720p', 'frame_rate': 30},
            'connection_quality': 'excellent'
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_video_call(request, call_id):
    """End a video call session"""
    return Response({
        'success': True,
        'message': 'Call ended successfully',
        'data': {'call_session_id': call_id}
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_call(request, call_id):
    """Record a video call"""
    return Response({
        'success': True,
        'message': 'Recording started',
        'data': {'recording_id': 'REC-001', 'call_session_id': call_id}
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_records(request):
    """Get medical records"""
    return Response({
        'success': True,
        'data': {'medical_records': []}
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_medical_record(request):
    """Upload medical document"""
    return Response({
        'success': True,
        'message': 'Document uploaded successfully',
        'data': {'record_id': 'REC-001'}
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medical_record(request, record_id):
    """Delete medical record"""
    return Response({
        'success': True,
        'message': 'Record deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    """Process payment"""
    return Response({
        'success': True,
        'message': 'Payment processed successfully',
        'data': {'transaction_id': 'TXN-001', 'status': 'succeeded'}
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """Get payment history"""
    return Response({
        'success': True,
        'data': []
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_refund(request):
    """Request refund"""
    return Response({
        'success': True,
        'message': 'Refund processed successfully',
        'data': {'refund_id': 'REF-001'}
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoice(request, invoice_id):
    """Get invoice"""
    return Response({
        'success': True,
        'data': {'invoice_id': invoice_id, 'amount': 500}
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_api(request):
    """Admin dashboard metrics"""
    return Response({
        'success': True,
        'data': {
            'users': {'total_patients': 87532, 'new_today': 145},
            'doctors': {'total_doctors': 652, 'active_doctors': 612},
            'appointments': {'total_today': 234, 'completed_today': 198}
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_doctors(request):
    """Get pending doctor approvals"""
    return Response({
        'success': True,
        'data': []
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_doctor_api(request, app_id):
    """Approve doctor"""
    return Response({
        'success': True,
        'message': 'Doctor approved successfully',
        'data': {'doctor_id': 'DOC-001', 'status': 'active'}
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_doctor_api(request, app_id):
    """Reject doctor"""
    return Response({
        'success': True,
        'message': 'Application rejected'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payments_report(request):
    """Get payment report"""
    return Response({
        'success': True,
        'data': {'total_revenue': 2340000, 'platform_revenue': 468000}
    }, status=status.HTTP_200_OK)
