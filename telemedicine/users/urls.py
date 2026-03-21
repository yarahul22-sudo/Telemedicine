from django.urls import path
from users import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('role/', views.get_user_role, name='get_user_role'),
    
    # Patient endpoints
    path('patient/profile/create/', views.create_patient_profile, name='create_patient_profile'),
    path('patient/profile/get/', views.get_patient_profile, name='get_patient_profile'),
    path('patient/profile/update/', views.update_patient_profile, name='update_patient_profile'),
    path('patients/', views.list_patients, name='list_patients'),
    
    # Doctor endpoints
    path('doctor/profile/create/', views.create_doctor_profile, name='create_doctor_profile'),
    path('doctor/profile/get/', views.get_doctor_profile, name='get_doctor_profile'),
    path('doctor/profile/update/', views.update_doctor_profile, name='update_doctor_profile'),
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('doctors/search/', views.search_doctors_by_specialization, name='search_doctors'),
    path('doctors/<int:doctor_id>/', views.get_doctor_by_id, name='get_doctor_by_id'),
]
