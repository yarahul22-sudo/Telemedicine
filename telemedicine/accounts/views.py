from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from users.models.base import CustomUser
from users.models.patient import PatientProfile
from users.models.doctor import DoctorProfile
from appointments.models import Appointment, Prescription


def home(request):
    """Home page view"""
    context = {
        'title': 'Home',
    }
    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', 'patient')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        terms = request.POST.get('terms')

        # Validation
        errors = []
        
        if not all([first_name, last_name, email, password, confirm_password]):
            errors.append('All fields are required.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if CustomUser.objects.filter(email=email).exists():
            errors.append('Email already registered. Please use a different email or login.')
        
        if not terms:
            errors.append('You must agree to the Terms of Service and Privacy Policy.')
        
        if role not in ['patient', 'doctor']:
            errors.append('Invalid role selected.')
        
        # Doctor-specific validation
        if role == 'doctor':
            specialization = request.POST.get('specialization', '').strip()
            license_number = request.POST.get('license_number', '').strip()
            experience_years = request.POST.get('experience_years', '0')
            available_days = request.POST.getlist('available_days')
            qualification = request.POST.get('qualification', '').strip()
            
            if not specialization:
                errors.append('Specialization is required for doctors.')
            
            if not license_number:
                errors.append('Medical license number is required.')
            
            if not experience_years:
                errors.append('Years of experience is required.')
            
            if not available_days:
                errors.append('You must select at least one available day.')
            
            try:
                experience_years = int(experience_years)
                if experience_years < 0 or experience_years > 60:
                    errors.append('Years of experience must be between 0 and 60.')
            except ValueError:
                errors.append('Years of experience must be a valid number.')
            
            # Check if license already exists
            if DoctorProfile.objects.filter(license_number=license_number).exists():
                errors.append('This medical license number is already registered.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html', {
                'form': request.POST,
                'title': 'Register',
                'role': role
            })
        
        try:
            # Generate username from email
            username = email.split('@')[0]
            
            # Check if username already exists
            counter = 1
            original_username = username
            while CustomUser.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=role
            )
            
            # Create role-specific profile
            if role == 'patient':
                PatientProfile.objects.create(user=user)
                messages.success(request, 'Account created successfully! Please log in.')
            elif role == 'doctor':
                available_days_str = ','.join(available_days) if available_days else 'Monday,Tuesday,Wednesday,Thursday,Friday'
                DoctorProfile.objects.create(
                    user=user,
                    specialization=specialization,
                    license_number=license_number,
                    experience_years=experience_years,
                    available_days=available_days_str,
                    qualification=qualification,
                    is_approved=False  # Require admin approval
                )
                messages.success(request, '✓ Doctor account created! Please log in. Your account is pending admin approval.')
            
            return redirect('login')
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'register.html', {
                'form': request.POST,
                'title': 'Register',
                'role': role
            })
    
    return render(request, 'register.html', {'title': 'Register'})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'login.html', {'title': 'Login'})
        
        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Check if doctor is approved
                if user.role == 'doctor' and hasattr(user, 'doctor_profile'):
                    if not user.doctor_profile.is_approved:
                        messages.warning(request, '⏳ Your doctor account is pending admin approval. You will be able to accept appointments once approved.')
                
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
        except Exception as e:
            messages.error(request, 'An error occurred during login. Please try again.')
        
        return render(request, 'login.html', {
            'form': request.POST,
            'title': 'Login'
        })
    
    return render(request, 'login.html', {'title': 'Login'})


@login_required(login_url='login')
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard view"""
    context = {
        'title': 'Dashboard',
        'user': request.user,
        'is_doctor_approved': True,
        'upcoming_appointments': [],
        'recent_consultations': [],
        'active_prescriptions': [],
    }
    
    # Check if doctor and approved
    if request.user.role == 'doctor' and hasattr(request.user, 'doctor_profile'):
        context['is_doctor_approved'] = request.user.doctor_profile.is_approved
    
    # Get user's appointments and consultations
    try:
        if request.user.role == 'patient' and hasattr(request.user, 'patient_profile'):
            patient = request.user.patient_profile
            now = timezone.now()
            
            # Upcoming appointments (next 7 days, scheduled status)
            upcoming = Appointment.objects.filter(
                patient=patient,
                appointment_date__gte=now,
                appointment_date__lte=now + timedelta(days=7),
                status='scheduled'
            ).order_by('appointment_date')[:5]
            context['upcoming_appointments'] = upcoming
            
            # Recent consultations (completed appointments)
            recent = Appointment.objects.filter(
                patient=patient,
                status='completed'
            ).order_by('-appointment_date')[:5]
            context['recent_consultations'] = recent
            
            # Active prescriptions
            active_prescriptions = Prescription.objects.filter(
                patient=patient,
                status='active'
            ).order_by('-issued_at')[:5]
            context['active_prescriptions'] = active_prescriptions
        
        elif request.user.role == 'doctor' and hasattr(request.user, 'doctor_profile'):
            doctor = request.user.doctor_profile
            now = timezone.now()
            
            # Doctor's upcoming appointments
            upcoming = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__gte=now,
                appointment_date__lte=now + timedelta(days=7),
                status='scheduled'
            ).order_by('appointment_date')[:5]
            context['upcoming_appointments'] = upcoming
            
            # Doctor's recent consultations
            recent = Appointment.objects.filter(
                doctor=doctor,
                status='completed'
            ).order_by('-appointment_date')[:5]
            context['recent_consultations'] = recent
    
    except Exception as e:
        print(f"Error loading dashboard data: {e}")
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def find_doctor(request):
    """Patient page to find and book doctors"""
    if request.user.role != 'patient':
        messages.error(request, 'This page is only for patients.')
        return redirect('dashboard')
    
    context = {
        'title': 'Find Doctor',
        'user': request.user,
    }
    return render(request, 'find-doctor.html', context)


@login_required(login_url='login')
def book_appointment(request):
    """Patient page to book appointment with a doctor"""
    if request.user.role != 'patient':
        messages.error(request, 'This page is only for patients.')
        return redirect('dashboard')
    
    doctor_id = request.GET.get('doctor_id')
    
    if not doctor_id:
        messages.error(request, 'Doctor not specified.')
        return redirect('find_doctor')
    
    try:
        doctor = DoctorProfile.objects.select_related('user').get(id=doctor_id, is_approved=True)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor not found or not approved.')
        return redirect('find_doctor')
    
    from appointments.models import Disease
    diseases = Disease.objects.all()
    
    context = {
        'title': f'Book Appointment - Dr. {doctor.user.get_full_name()}',
        'doctor': doctor,
        'diseases': diseases,
        'user': request.user,
    }
    return render(request, 'book-appointment.html', context)


@login_required(login_url='login')
def doctor_patients(request):
    """Doctor page to view their assigned patients"""
    if request.user.role != 'doctor':
        messages.error(request, 'This page is only for doctors.')
        return redirect('dashboard')
    
    # Check if doctor is approved
    if hasattr(request.user, 'doctor_profile') and not request.user.doctor_profile.is_approved:
        messages.error(request, 'Your doctor account is pending admin approval. You cannot view patients yet.')
        return redirect('dashboard')
    
    context = {
        'title': 'My Patients',
        'user': request.user,
    }
    return render(request, 'doctor-patients.html', context)


@login_required(login_url='login')
def change_role(request):
    """Change user role (patient to doctor or vice versa)"""
    if request.method == 'POST':
        new_role = request.POST.get('new_role', '').strip()
        
        if new_role not in ['patient', 'doctor']:
            messages.error(request, 'Invalid role selected.')
            return render(request, 'change-role.html', {'user': request.user, 'title': 'Change Role'})
        
        # Don't allow changing if already have appointments
        has_appointments = False
        if request.user.role == 'doctor':
            from appointments.models import Appointment
            has_appointments = Appointment.objects.filter(doctor__user=request.user).exists()
        elif request.user.role == 'patient':
            from appointments.models import Appointment
            has_appointments = Appointment.objects.filter(patient__user=request.user).exists()
        
        if has_appointments:
            messages.error(request, 'Cannot change role while you have active appointments. Please cancel all appointments first.')
            return render(request, 'change-role.html', {'user': request.user, 'title': 'Change Role'})
        
        try:
            old_role = request.user.role
            
            # Delete old profile
            if old_role == 'patient' and hasattr(request.user, 'patient_profile'):
                request.user.patient_profile.delete()
            elif old_role == 'doctor' and hasattr(request.user, 'doctor_profile'):
                request.user.doctor_profile.delete()
            
            # Update user role
            request.user.role = new_role
            request.user.save()
            
            # Create new profile
            if new_role == 'patient':
                PatientProfile.objects.create(user=request.user)
                messages.success(request, 'Successfully changed to Patient role!')
            elif new_role == 'doctor':
                # Check if doctor fields provided
                specialization = request.POST.get('specialization', '').strip()
                license_number = request.POST.get('license_number', '').strip()
                experience_years = request.POST.get('experience_years', '0')
                available_days = request.POST.getlist('available_days')
                qualification = request.POST.get('qualification', '').strip()
                
                errors = []
                if not specialization:
                    errors.append('Specialization is required.')
                if not license_number:
                    errors.append('Medical license number is required.')
                if not experience_years:
                    errors.append('Years of experience is required.')
                if not available_days:
                    errors.append('You must select at least one available day.')
                
                if errors:
                    request.user.role = old_role
                    request.user.save()
                    if old_role == 'patient':
                        PatientProfile.objects.create(user=request.user)
                    for error in errors:
                        messages.error(request, error)
                    return render(request, 'change-role.html', {'user': request.user, 'title': 'Change Role'})
                
                try:
                    experience_years = int(experience_years)
                except ValueError:
                    experience_years = 0
                
                available_days_str = ','.join(available_days) if available_days else ''
                DoctorProfile.objects.create(
                    user=request.user,
                    specialization=specialization,
                    license_number=license_number,
                    experience_years=experience_years,
                    available_days=available_days_str,
                    qualification=qualification,
                    is_approved=False  # Require admin approval
                )
                messages.success(request, 'Successfully changed to Doctor role! Your account is pending admin approval.')
            
            return redirect('dashboard')
        
        except Exception as e:
            messages.error(request, f'Error changing role: {str(e)}')
            return render(request, 'change-role.html', {'user': request.user, 'title': 'Change Role'})
    
    context = {
        'user': request.user,
        'title': 'Change Role',
    }
    return render(request, 'change-role.html', context)


def about(request):
    """About page view"""
    context = {'title': 'About Us'}
    return render(request, 'about.html', context)


@login_required(login_url='login')
def admin_doctors_list(request):
    """Admin page to view list of all doctors"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    doctors = DoctorProfile.objects.select_related('user').all().order_by('-created_at')
    
    context = {
        'title': 'Manage Doctors',
        'doctors': doctors,
        'total_doctors': doctors.count(),
        'approved_doctors': doctors.filter(is_approved=True).count(),
        'pending_doctors': doctors.filter(is_approved=False).count(),
    }
    return render(request, 'admin-doctors-list.html', context)


@login_required(login_url='login')
def admin_doctor_detail(request, doctor_id):
    """Admin page to view specific doctor profile with their patients and diseases"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    try:
        doctor_profile = DoctorProfile.objects.select_related('user').get(id=doctor_id)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('admin_doctors_list')
    
    # Get all appointments for this doctor
    from appointments.models import Appointment
    appointments = Appointment.objects.filter(
        doctor=doctor_profile
    ).select_related('patient', 'disease').order_by('-appointment_date')
    
    # Prepare patient data
    patients_data = []
    unique_patients = {}
    
    for appointment in appointments:
        patient = appointment.patient
        
        if patient.id not in unique_patients:
            unique_patients[patient.id] = {
                'patient': patient,
                'diseases': [],
                'appointments': [],
            }
        
        if appointment.disease and appointment.disease.name not in unique_patients[patient.id]['diseases']:
            unique_patients[patient.id]['diseases'].append(appointment.disease.name)
        
        unique_patients[patient.id]['appointments'].append(appointment)
    
    patients_data = list(unique_patients.values())
    
    context = {
        'title': f'Doctor Profile - {doctor_profile.user.get_full_name()}',
        'doctor': doctor_profile,
        'patients_data': patients_data,
        'total_patients': len(unique_patients),
        'total_appointments': appointments.count(),
    }
    return render(request, 'admin-doctor-detail.html', context)


@login_required(login_url='login')
def my_appointments(request):
    """View all user's appointments with management options"""
    if request.user.role != 'patient':
        messages.error(request, 'This page is only for patients.')
        return redirect('dashboard')
    
    try:
        patient = request.user.patient_profile
        now = timezone.now()
        
        # Get all appointments
        all_appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
        
        # Categorize appointments
        upcoming = all_appointments.filter(
            appointment_date__gte=now,
            status='scheduled'
        )
        
        completed = all_appointments.filter(status='completed')
        cancelled = all_appointments.filter(status='cancelled')
        
        context = {
            'title': 'My Appointments',
            'user': request.user,
            'upcoming_appointments': upcoming,
            'completed_appointments': completed,
            'cancelled_appointments': cancelled,
            'total_appointments': all_appointments.count(),
        }
        
        return render(request, 'my-appointments.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading appointments: {str(e)}')
        return redirect('dashboard')


@login_required(login_url='login')
def doctor_appointments(request):
    """View all doctor's appointments with management options"""
    if request.user.role != 'doctor':
        messages.error(request, 'This page is only for doctors.')
        return redirect('dashboard')
    
    # Check if doctor is approved
    if hasattr(request.user, 'doctor_profile') and not request.user.doctor_profile.is_approved:
        messages.warning(request, '⏳ Your doctor account is pending admin approval. You cannot view patient appointments yet.')
        return redirect('dashboard')
    
    try:
        doctor = request.user.doctor_profile
        now = timezone.now()
        
        # Get all appointments
        all_appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
        
        # Categorize appointments
        upcoming = all_appointments.filter(
            appointment_date__gte=now,
            status='scheduled'
        )
        
        completed = all_appointments.filter(status='completed')
        cancelled = all_appointments.filter(status='cancelled')
        
        context = {
            'title': 'My Appointments',
            'user': request.user,
            'doctor': doctor,
            'upcoming_appointments': upcoming,
            'completed_appointments': completed,
            'cancelled_appointments': cancelled,
            'total_appointments': all_appointments.count(),
        }
        
        return render(request, 'doctor-appointments.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading appointments: {str(e)}')
        return redirect('dashboard')


def services(request):
    """Services page view"""
    context = {'title': 'Services'}
    return render(request, 'services.html', context)


def booking_status(request):
    """Status check page for debugging booking form issues"""
    from django.http import HttpResponse
    
    doctor_id = request.GET.get('doctor_id', 'N/A')
    is_logged_in = request.user.is_authenticated
    user_email = request.user.email if is_logged_in else 'N/A'
    user_role = request.user.role if (is_logged_in and hasattr(request.user, 'role')) else 'N/A'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Booking Status</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; }}
            .status {{ padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .ok {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .info {{ background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }}
            code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
            .step {{ padding: 10px; margin: 10px 0; background: #f9f9f9; border-left: 4px solid #667eea; }}
            a {{ color: #667eea; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Booking Form - Status Check</h1>
            
            <div class="status {'ok' if is_logged_in else 'error'}">
                <strong>✓ Login Status:</strong> {'LOGGED IN' if is_logged_in else 'NOT LOGGED IN'}
                {f'<br/>Email: {user_email}' if is_logged_in else ''}
                {f'<br/>Role: {user_role}' if is_logged_in else ''}
            </div>
            
            <div class="status {'ok' if doctor_id != 'N/A' else 'error'}">
                <strong>{'✓' if doctor_id != 'N/A' else '✗'} Doctor ID:</strong> {doctor_id}
            </div>
            
            <div class="status info">
                <strong>Current URL:</strong> <code>{request.get_full_path()}</code>
            </div>
            
            <h2>🔧 If Form Not Showing:</h2>
            
            {'<div class="step"><strong>1️⃣ Not Logged In</strong><br/>Visit: <a href="/login/">Login Page</a><br/>Use: pshyam@telemedicine.com</div>' if not is_logged_in else ''}
            
            {'<div class="step"><strong>2️⃣ No Doctor ID</strong><br/><a href="/book-appointment/?doctor_id=7">Try: /book-appointment/?doctor_id=7</a></div>' if doctor_id == 'N/A' else ''}
            
            {'<div class="step"><strong>3️⃣ Clear Cache</strong><br/>Press: Ctrl + Shift + Delete<br/>Then refresh page</div>' if is_logged_in and doctor_id != 'N/A' else ''}
            
            <h2>✅ Next Steps:</h2>
            {f'<div class="step" style="background: #d4edda;"><strong>✓ Ready!</strong><br/><a href="/book-appointment/?doctor_id={doctor_id}">Go to Booking Form (Doctor {doctor_id})</a></div>' if (is_logged_in and doctor_id != 'N/A') else '<div class="step">Complete troubleshooting above</div>'}
            
            <h2>📞 Quick Links:</h2>
            <ul>
                <li><a href="/dashboard/">🏠 Dashboard</a></li>
                <li><a href="/find-doctor/">🔍 Find Doctor</a></li>
                <li><a href="/my-appointments/">📅 My Appointments</a></li>
                <li><a href="/logout/">🚪 Logout</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
