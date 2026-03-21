from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import CustomUser, PatientProfile, DoctorProfile, AdminProfile

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin for CustomUser model"""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'is_verified', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('username', 'email', 'role', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    """Admin for PatientProfile model"""
    list_display = ('get_full_name', 'get_email', 'date_of_birth', 'emergency_contact', 'created_at')
    list_filter = ('created_at', 'date_of_birth')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'emergency_contact')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Info', {
            'fields': ('date_of_birth', 'emergency_contact', 'emergency_phone', 'profile_picture')
        }),
        ('Medical Info', {
            'fields': ('medical_history', 'allergies')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Patient Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """Admin for DoctorProfile model"""
    list_display = ('get_full_name', 'specialization', 'experience_years', 'rating', 'is_available', 'created_at')
    list_filter = ('specialization', 'is_available', 'created_at', 'rating')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'total_appointments')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Professional Info', {
            'fields': ('specialization', 'license_number', 'qualification', 'experience_years')
        }),
        ('Clinic Details', {
            'fields': ('clinic_address', 'clinic_phone', 'consultation_fee')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'bio', 'is_available')
        }),
        ('Performance', {
            'fields': ('rating', 'total_appointments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_full_name.short_description = 'Doctor Name'

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    """Admin for AdminProfile model"""
    list_display = ('get_full_name', 'department', 'designation', 'is_active', 'created_at')
    list_filter = ('department', 'is_active', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Employment', {
            'fields': ('employee_id', 'department', 'designation', 'is_active')
        }),
        ('Permissions', {
            'fields': ('permissions',),
            'classes': ('collapse',)
        }),
        ('Activity', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Admin Name'
