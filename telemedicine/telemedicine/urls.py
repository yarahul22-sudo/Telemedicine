from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/appointments/", include("appointments.urls")),
    
    # Web pages
    path("", account_views.home, name="home"),
    path("register/", account_views.register_view, name="register"),
    path("login/", account_views.login_view, name="login"),
    path("logout/", account_views.logout_view, name="logout"),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("find-doctor/", account_views.find_doctor, name="find_doctor"),
    path("doctor-patients/", account_views.doctor_patients, name="doctor_patients"),
    path("about/", account_views.about, name="about"),
    path("services/", account_views.services, name="services"),
]
