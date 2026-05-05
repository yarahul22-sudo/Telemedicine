from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    # API v1 endpoints
    path("v1/", include("api.urls")),
    path("api/", include("api.urls")),
    
    # Admin panel
    path("admin/", account_views.admin_dashboard, name="admin_root"),
    path("admin/login/", account_views.login_view, name="admin_login"),
    path("djangoadmin/", admin.site.urls),
    
    # Legacy API routes
    path("api/users/", include("users.urls")),
    path("api/appointments/", include("appointments.urls")),
    
    # Web pages
    path("", account_views.home, name="home"),
    path("register/", account_views.register_view, name="register"),
    path("login/", account_views.login_view, name="login"),
    path("logout/", account_views.logout_view, name="logout"),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("my-appointments/", account_views.my_appointments, name="my_appointments"),
    path("doctor-appointments/", account_views.doctor_appointments, name="doctor_appointments"),
    path("find-doctor/", account_views.find_doctor, name="find_doctor"),
    path("book-appointment/", account_views.book_appointment, name="book_appointment"),
    path("doctor-patients/", account_views.doctor_patients, name="doctor_patients"),
    path("profile/edit/", account_views.edit_profile, name="edit_profile"),
    path("change-role/", account_views.change_role, name="change_role"),
    # Admin Dashboard & Management
    path("admin/dashboard/", account_views.admin_dashboard, name="admin_dashboard"),
    path("admin/approve-doctor/<str:doctor_id>/", account_views.approve_doctor, name="approve_doctor"),
    path("admin/delete-user/<str:user_id>/", account_views.delete_user_admin, name="delete_user_admin"),
    path("admin-setup/", account_views.admin_setup_view, name="admin_setup"),
    path("about/", account_views.about, name="about"),
    path("services/", account_views.services, name="services"),
    path("booking-status/", account_views.booking_status, name="booking_status"),
    path("video-call/<str:appointment_id>/", account_views.video_call, name="video_call"),
]
