"""
API URLs for Telemedicine Platform
Main API routing configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import API views
from api.serializers import UserViewSet, DoctorViewSet, PatientViewSet, AppointmentViewSet, PrescriptionViewSet
from api import views as api_views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', api_views.api_register, name='api_register'),
    path('auth/login/', api_views.api_login, name='api_login'),
    path('auth/logout/', api_views.api_logout, name='api_logout'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify-email/', api_views.verify_email, name='verify_email'),
    path('auth/password-reset/', api_views.password_reset, name='password_reset'),
    path('auth/password-reset-confirm/', api_views.password_reset_confirm, name='password_reset_confirm'),
    path('auth/2fa/enable/', api_views.enable_2fa, name='enable_2fa'),
    
    # User endpoints
    path('users/profile/', api_views.get_user_profile, name='user_profile'),
    path('users/preferences/', api_views.user_preferences, name='user_preferences'),
    
    # Router endpoints (ViewSets)
    path('', include(router.urls)),
    
    # Video calls
    path('video-calls/initialize/', api_views.initialize_video_call, name='initialize_video_call'),
    path('video-calls/<str:call_id>/stats/', api_views.get_call_stats, name='call_stats'),
    path('video-calls/<str:call_id>/end/', api_views.end_video_call, name='end_video_call'),
    path('video-calls/<str:call_id>/record/', api_views.record_call, name='record_call'),
    
    # Medical records
    path('medical-records/', api_views.get_medical_records, name='medical_records'),
    path('medical-records/upload/', api_views.upload_medical_record, name='upload_record'),
    path('medical-records/<str:record_id>/', api_views.delete_medical_record, name='delete_record'),
    
    # Payments
    path('payments/process/', api_views.process_payment, name='process_payment'),
    path('payments/history/', api_views.payment_history, name='payment_history'),
    path('payments/refund/', api_views.request_refund, name='request_refund'),
    path('payments/invoices/<str:invoice_id>/', api_views.get_invoice, name='get_invoice'),
    
    # Admin endpoints
    path('admin/dashboard/', api_views.admin_dashboard_api, name='admin_dashboard_api'),
    path('admin/doctors/pending/', api_views.pending_doctors, name='pending_doctors'),
    path('admin/doctors/<str:app_id>/approve/', api_views.approve_doctor_api, name='approve_doctor_api'),
    path('admin/doctors/<str:app_id>/reject/', api_views.reject_doctor_api, name='reject_doctor_api'),
    path('admin/payments/report/', api_views.payments_report, name='payments_report'),
]
