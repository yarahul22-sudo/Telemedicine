from rest_framework.permissions import BasePermission, IsAuthenticated

class IsPatient(BasePermission):
    """Permission class for patient users"""
    message = 'This action is only available for patients.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_patient())

class IsDoctor(BasePermission):
    """Permission class for doctor users"""
    message = 'This action is only available for doctors.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_doctor())

class IsAdminUser(BasePermission):
    """Permission class for admin users"""
    message = 'This action is only available for administrators.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_user())

class IsVerified(BasePermission):
    """Permission class for verified users"""
    message = 'This action is only available for verified users.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_verified)

class IsPatientOrReadOnly(BasePermission):
    """Allow patients to edit, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user and request.user.is_patient()

class IsDoctorOrReadOnly(BasePermission):
    """Allow doctors to edit, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user and request.user.is_doctor()
