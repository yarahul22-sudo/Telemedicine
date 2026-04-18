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
    path('<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('<int:appointment_id>/complete/', views.mark_appointment_complete, name='mark_complete'),
    path('<int:appointment_id>/update-notes/', views.update_appointment_notes, name='update_notes'),
    path('prescriptions/create/', views.create_prescription, name='create_prescription'),
    
    # Doctor views
    path('doctor/patients/', views.get_doctor_patients, name='doctor_patients'),
]
