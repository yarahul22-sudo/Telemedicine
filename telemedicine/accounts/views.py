from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from users.models.base import CustomUser
from users.models.patient import PatientProfile
from users.models.doctor import DoctorProfile


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
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html', {
                'form': request.POST,
                'title': 'Register'
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
            elif role == 'doctor':
                DoctorProfile.objects.create(user=user)
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'register.html', {
                'form': request.POST,
                'title': 'Register'
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
    }
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
def doctor_patients(request):
    """Doctor page to view their assigned patients"""
    if request.user.role != 'doctor':
        messages.error(request, 'This page is only for doctors.')
        return redirect('dashboard')
    
    context = {
        'title': 'My Patients',
        'user': request.user,
    }
    return render(request, 'doctor-patients.html', context)


def about(request):
    """About page view"""
    context = {'title': 'About Us'}
    return render(request, 'about.html', context)


def services(request):
    """Services page view"""
    context = {'title': 'Services'}
    return render(request, 'services.html', context)
