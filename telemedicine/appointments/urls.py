from django.urls import path
from appointments import views

urlpatterns = [
    # Doctor search and discovery
    path('doctors/search/', views.search_doctors_by_specialty, name='search_doctors_by_specialty'),
    path('doctors/recommended/', views.get_recommended_doctors, name='recommended_doctors'),
    
    # Diseases
    path('diseases/', views.get_all_diseases, name='all_diseases'),
    
    # Appointments
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/my/', views.get_my_appointments, name='my_appointments'),
    
    # Doctor views
    path('doctor/patients/', views.get_doctor_patients, name='doctor_patients'),
]
