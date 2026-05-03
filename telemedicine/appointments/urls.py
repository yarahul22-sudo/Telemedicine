from django.urls import path
from appointments import views

urlpatterns = [
    # Doctor search and discovery
    path('doctors/search/', views.search_doctors_by_specialty, name='search_doctors_by_specialty'),
    path('doctors/recommended/', views.get_recommended_doctors, name='recommended_doctors'),
    
    # Diseases
    path('diseases/', views.get_all_diseases, name='all_diseases'),
    
    # Appointments (API)
    path('book/', views.book_appointment, name='book_appointment_api'),
    path('my/', views.get_my_appointments, name='get_my_appointments_api'),
    path('<str:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('<str:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    
    # Video Call & Updates
    path('<str:appointment_id>/video-token/', views.generate_video_token, name='generate_video_token'),
    path('<str:appointment_id>/complete/', views.mark_appointment_complete, name='mark_complete'),
    path('<str:appointment_id>/update-notes/', views.update_appointment_notes, name='update_notes'),
    path('prescriptions/create/', views.create_prescription, name='create_prescription'),
    
    # Doctor views
    path('doctor/patients/', views.get_doctor_patients, name='doctor_patients'),
]
