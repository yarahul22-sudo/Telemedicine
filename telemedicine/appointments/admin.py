from django.contrib import admin
from appointments.models import Appointment, Disease, Prescription


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization_required')
    search_fields = ('name',)
    list_filter = ('specialization_required',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'disease', 'appointment_date', 'status')
    search_fields = ('patient__user__email', 'doctor__user__email')
    list_filter = ('status', 'appointment_date', 'consultation_type')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()
    get_doctor_name.short_description = 'Doctor'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'get_patient_name', 'get_doctor_name', 'status', 'issued_at')
    search_fields = ('patient__user__email', 'doctor__user__email', 'medication_name')
    list_filter = ('status', 'issued_at')
    readonly_fields = ('issued_at', 'updated_at')
    fieldsets = (
        ('Appointment & Participants', {
            'fields': ('appointment', 'doctor', 'patient')
        }),
        ('Medication Details', {
            'fields': ('medication_name', 'dosage', 'frequency', 'duration_days', 'instructions')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('issued_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()
    get_doctor_name.short_description = 'Doctor'
