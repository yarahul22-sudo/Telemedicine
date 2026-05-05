from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta, datetime
import os
from users.models.base import CustomUser
from users.models.patient import PatientProfile
from users.models.doctor import DoctorProfile
from appointments.models import Appointment, Prescription
import firebase_admin.auth


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
        import json
        import firebase_admin.auth
        import firebase_admin
        from django.http import JsonResponse
        
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse({'error': 'No authentication token provided'}, status=400)
                
            # Ensure Firebase is initialized
            if not firebase_admin._apps:
                from telemedicine.firebase_setup import initialize_firebase
                initialize_firebase()
            
            # Verify Firebase token with clock skew tolerance
            try:
                decoded_token = firebase_admin.auth.verify_id_token(token, check_revoked=False, clock_skew_seconds=10)
            except firebase_admin.auth.InvalidIdTokenError as e:
                error_msg = str(e)
                # Handle clock skew errors more gracefully
                if "Token used too early" in error_msg or "token is not yet valid" in error_msg.lower():
                    print(f"⚠️ Clock skew detected, attempting with lenient verification: {error_msg}")
                    # For registration, we can be slightly more lenient with clock skew
                    # Re-attempt the verification with increased clock_skew_seconds
                    try:
                        decoded_token = firebase_admin.auth.verify_id_token(token, check_revoked=False, clock_skew_seconds=30)
                    except Exception as e2:
                        print(f"❌ Token verification failed even with retry: {e2}")
                        return JsonResponse({
                            'error': 'Token verification failed. Please try registering again.'
                        }, status=401)
                else:
                    print(f"❌ Token verification failed: {error_msg}")
                    return JsonResponse({'error': 'Invalid authentication token. Please try again.'}, status=401)
            
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            
            print(f"✅ Token verified for registration: UID={uid}, Email={email}")
            
            if not email:
                return JsonResponse({'error': 'Invalid token: No email found'}, status=400)

            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            role = data.get('role', 'patient')
            
            # Validation
            if not all([first_name, last_name, email]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            
            from telemedicine.firestore_db import db
            from firebase_admin import firestore
            users_ref = db.collection('users')
            
            # Check if user exists in Firestore
            doc = users_ref.document(uid).get()
            if doc.exists:
                return JsonResponse({'error': 'Email already registered. Please login instead.'}, status=400)
            
            user_data = {
                'uid': uid,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role,
                'profile_image_url': data.get('profile_image_url', '').strip(),
                'created_at': firestore.SERVER_TIMESTAMP,
            }
            
            if role == 'doctor':
                user_data['specialization'] = data.get('specialization', '').strip().lower()
                user_data['license_number'] = data.get('license_number', '').strip()
                user_data['experience_years'] = int(data.get('experience_years', '0'))
                user_data['available_days'] = data.get('available_days', [])
                user_data['qualification'] = data.get('qualification', '').strip()
                user_data['is_approved'] = False
            
            # Save user to Firestore
            users_ref.document(uid).set(user_data)
            
            return JsonResponse({'success': True, 'redirect': '/login/'})
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    
    from django.conf import settings
    context = {
        'title': 'Register',
        'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
        'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
        'FIREBASE_DATABASE_URL': getattr(settings, 'FIREBASE_DATABASE_URL', ''),
        'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
        'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
        'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
        'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
    }
    return render(request, 'register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view via Firebase Token"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        import json
        import firebase_admin.auth
        import firebase_admin
        from django.http import JsonResponse
        import time
        
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse({'error': 'No authentication token provided'}, status=400)
                
            # Verify Firebase token with detailed error handling
            try:
                # Ensure Firebase is initialized
                if not firebase_admin._apps:
                    from telemedicine.firebase_setup import initialize_firebase
                    initialize_firebase()
                
                print(f"\n🔍 TOKEN VERIFICATION ATTEMPT")
                print(f"   Token length: {len(token)}")
                print(f"   Server timestamp: {int(time.time())}")
                print(f"   Firebase apps initialized: {len(firebase_admin._apps)}")
                
                # Get the app and check credentials
                try:
                    app = list(firebase_admin._apps.values())[0]
                    print(f"   Firebase app project ID: {app.project_id if hasattr(app, 'project_id') else 'Unknown'}")
                except:
                    pass
                
                # Try token verification with detailed error handling and clock skew tolerance
                try:
                    decoded_token = firebase_admin.auth.verify_id_token(token, check_revoked=False, clock_skew_seconds=10)
                    print(f"✅ Token verified successfully (with clock_skew_seconds=10)!")
                    print(f"   Decoded UID: {decoded_token.get('uid')}")
                    print(f"   Decoded Email: {decoded_token.get('email')}")
                except firebase_admin.auth.InvalidIdTokenError as e1:
                    print(f"❌ Token verification failed (InvalidIdTokenError)")
                    print(f"   Error details: {str(e1)}")
                    print(f"   Error code: {getattr(e1, 'code', 'N/A')}")
                    raise e1
                except firebase_admin.auth.RevokedIdTokenError as e2:
                    print(f"❌ Token revoked (RevokedIdTokenError)")
                    print(f"   Error: {str(e2)}")
                    raise e2
                except Exception as e3:
                    print(f"❌ Unexpected token verification error")
                    print(f"   Error type: {type(e3).__name__}")
                    print(f"   Error message: {str(e3)}")
                    import traceback
                    traceback.print_exc()
                    raise e3
                        
            except firebase_admin.auth.InvalidIdTokenError as token_error:
                print(f"❌ Final: Invalid Firebase token")
                return JsonResponse({'error': 'Invalid Firebase token. Please try logging in again.'}, status=401)
            except firebase_admin.auth.RevokedIdTokenError as token_error:
                print(f"❌ Final: Token revoked")
                return JsonResponse({'error': 'Your session has expired. Please login again.'}, status=401)
            except Exception as token_error:
                print(f"❌ Final: Authentication token error")
                return JsonResponse({'error': 'Authentication token error. Please try again.'}, status=401)
            
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            
            print(f"✅ Token decoded: UID={uid}, Email={email}")
            
            if not uid or not email:
                return JsonResponse({'error': 'Invalid token: Missing user information'}, status=400)

            # Find user in Firestore via auth backend
            user = authenticate(request, token=token)
            if user is None:
                print(f"❌ User not found in Firestore for UID: {uid}, Email: {email}")
                return JsonResponse({
                    'error': f'Account not found in system. Please register first at /register/', 
                    'details': f'Email {email} is not registered. Visit /register/ to create an account.'
                }, status=404)
            
            # Force log the user in
            login(request, user, backend='accounts.firestore_auth.FirestoreBackend')
            
            print(f"✅ User logged in successfully: {email}")
            return JsonResponse({'success': True, 'redirect': '/dashboard/'})
            
        except firebase_admin.auth.InvalidIdTokenError:
            return JsonResponse({'error': 'Invalid Firebase authentication token'}, status=401)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    
    from django.conf import settings
    context = {
        'title': 'Login',
        'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
        'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
        'FIREBASE_DATABASE_URL': getattr(settings, 'FIREBASE_DATABASE_URL', ''),
        'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
        'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
        'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
        'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
    }
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logout_view(request):
    """User logout view"""
    reason = request.GET.get('reason')
    logout(request)
    if reason == 'timeout':
        messages.warning(request, 'Your session has timed out due to 10 minutes of inactivity. Please login again.')
    else:
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard view"""
    if request.user.role == 'admin':
        if request.user.email == 'admin@gmail.com':
            return redirect('/djangoadmin/')
        return redirect('/admin/')
        
    context = {
        'title': 'Dashboard',
        'user': request.user,
        'is_doctor_approved': True,
        'upcoming_appointments': [],
        'recent_consultations': [],
        'active_prescriptions': [],
    }
    
    # Check if doctor and approved
    if request.user.role == 'doctor':
        context['is_doctor_approved'] = request.user.data.get('is_approved', False)
        
    from telemedicine.firestore_db import db
    from datetime import datetime, timedelta
    
    try:
        now = datetime.now()
        appointments_ref = db.collection('appointments')
        
        def get_timestamp(app_date):
            """Convert various date formats to timestamp"""
            if not app_date:
                return 0
            if hasattr(app_date, 'timestamp'):
                # Firestore Timestamp object
                if callable(app_date.timestamp):
                    return app_date.timestamp()
                else:
                    return app_date.timestamp
            else:
                # String or other format - try to parse
                try:
                    from dateutil import parser
                    return parser.parse(str(app_date)).timestamp()
                except:
                    return 0
        
        if request.user.role == 'patient':
            # Upcoming appointments
            upcoming_query = appointments_ref.where('patient_id', '==', request.user.uid).where('status', '==', 'scheduled').stream()
            upcoming = []
            print(f"\n🔍 Dashboard: Fetching appointments for patient {request.user.uid}")
            for doc in upcoming_query:
                app_data = doc.to_dict()
                app_data['id'] = doc.id
                app_timestamp = get_timestamp(app_data.get('appointment_date'))
                print(f"   - Found appointment: {app_data.get('doctor_name', 'Unknown')} at {app_data.get('appointment_date')} (timestamp: {app_timestamp})")
                print(f"   - Current time: {now.timestamp()}")
                print(f"   - Is future? {app_timestamp >= now.timestamp()}")
                if app_timestamp >= now.timestamp():
                    upcoming.append(app_data)
            
            print(f"   - Total upcoming: {len(upcoming)}")
            # Sort by date
            upcoming.sort(key=lambda x: get_timestamp(x.get('appointment_date')))
            context['upcoming_appointments'] = upcoming[:5]
            
            # Recent consultations
            recent_query = appointments_ref.where('patient_id', '==', request.user.uid).where('status', '==', 'completed').stream()
            recent = []
            for doc in recent_query:
                app_data = doc.to_dict()
                app_data['id'] = doc.id
                recent.append(app_data)
                
            recent.sort(key=lambda x: get_timestamp(x.get('appointment_date')), reverse=True)
            context['recent_consultations'] = recent[:5]
            
            # Prescriptions
            prescriptions_ref = db.collection('prescriptions')
            active_rx_query = prescriptions_ref.where('patient_id', '==', request.user.uid).where('is_active', '==', True).stream()
            active_rx = []
            for doc in active_rx_query:
                rx_data = doc.to_dict()
                rx_data['id'] = doc.id
                active_rx.append(rx_data)
            context['active_prescriptions'] = active_rx
            
        elif request.user.role == 'doctor':
            # Upcoming appointments
            upcoming_query = appointments_ref.where('doctor_id', '==', request.user.uid).where('status', '==', 'scheduled').stream()
            upcoming = []
            for doc in upcoming_query:
                app_data = doc.to_dict()
                app_data['id'] = doc.id
                app_timestamp = get_timestamp(app_data.get('appointment_date'))
                if app_timestamp >= now.timestamp():
                    upcoming.append(app_data)
                    
            upcoming.sort(key=lambda x: get_timestamp(x.get('appointment_date')))
            context['upcoming_appointments'] = upcoming[:5]
            
            # Recent consultations
            recent_query = appointments_ref.where('doctor_id', '==', request.user.uid).where('status', '==', 'completed').stream()
            recent = []
            for doc in recent_query:
                app_data = doc.to_dict()
                app_data['id'] = doc.id
                recent.append(app_data)
                
            recent.sort(key=lambda x: get_timestamp(x.get('appointment_date')), reverse=True)
            context['recent_consultations'] = recent[:5]
            
    except Exception as e:
        print(f"Error loading dashboard data from Firestore: {e}")
    
    # Add Firebase config to context for real-time updates
    context.update({
        'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
        'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
        'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
        'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
        'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
        'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
        'FIREBASE_CUSTOM_TOKEN': firebase_admin.auth.create_custom_token(request.user.uid).decode('utf-8'),
    })
    
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
    """Patient page to book appointment with a doctor using Firestore data"""
    if request.user.role != 'patient':
        messages.error(request, 'This page is only for patients.')
        return redirect('dashboard')
    
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        messages.error(request, 'Doctor not specified.')
        return redirect('find_doctor')
    
    from telemedicine.firestore_db import db
    try:
        # Fetch doctor from Firestore
        doctor_doc = db.collection('users').document(str(doctor_id)).get()
        if not doctor_doc.exists:
            messages.error(request, 'Doctor not found.')
            return redirect('find_doctor')
            
        doctor_data = doctor_doc.to_dict()
        if doctor_data.get('role') != 'doctor' or not doctor_data.get('is_approved'):
            messages.error(request, 'Doctor is not available or not approved.')
            return redirect('find_doctor')
            
        doctor_data['id'] = doctor_doc.id
        # Compatibility wrappers for template expectations
        doctor_data['user'] = {
            'get_full_name': f"{doctor_data.get('first_name', '')} {doctor_data.get('last_name', '')}"
        }
        doctor_data['get_specialization_display'] = doctor_data.get('specialization', 'General').title()
        
        # Fetch diseases (static for now, or from Firestore)
        diseases = []
        try:
            from appointments.models import Disease
            diseases = list(Disease.objects.all())
        except Exception:
            pass
            
        if not diseases:
            diseases = [
                {'id': '1', 'name': 'General Consultation'},
                {'id': '2', 'name': 'Fever / Flu'},
                {'id': '3', 'name': 'Headache / Migraine'},
                {'id': '4', 'name': 'Stomach Pain'},
                {'id': '5', 'name': 'Back Pain'},
                {'id': '6', 'name': 'Skin Issue'},
            ]
            
        context = {
            'title': f"Book Appointment - Dr. {doctor_data['user']['get_full_name']}",
            'doctor': doctor_data,
            'diseases': diseases,
            'user': request.user,
        }
        return render(request, 'book-appointment.html', context)
    except Exception as e:
        messages.error(request, f'Error loading doctor: {e}')
        return redirect('find_doctor')


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
        # Firebase Config
        'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
        'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
        'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
        'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
        'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
        'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
        'FIREBASE_CUSTOM_TOKEN': firebase_admin.auth.create_custom_token(request.user.uid).decode('utf-8'),
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


@login_required(login_url='login')
def admin_dashboard(request):
    """Unified Admin Dashboard for Firestore data management"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
        
    from telemedicine.firestore_db import db
    from firebase_admin import auth, firestore
    
    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'add_user':
                email = request.POST.get('email')
                password = request.POST.get('password')
                role = request.POST.get('role', 'patient')
                first_name = request.POST.get('first_name', '')
                last_name = request.POST.get('last_name', '')
                
                try:
                    user = auth.create_user(email=email, password=password)
                    uid = user.uid
                    
                    user_data = {
                        'uid': uid,
                        'email': email,
                        'role': role,
                        'first_name': first_name,
                        'last_name': last_name,
                        'created_at': firestore.SERVER_TIMESTAMP
                    }
                    if role == 'doctor':
                        user_data['is_approved'] = True
                        user_data['specialization'] = request.POST.get('specialization', '')
                        user_data['license_number'] = request.POST.get('license_number', '')
                        
                    db.collection('users').document(uid).set(user_data)
                    messages.success(request, f'{role.capitalize()} added successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating user: {e}')
                    
            elif action == 'edit_user':
                uid = request.POST.get('user_id')
                update_data = {
                    'first_name': request.POST.get('first_name', ''),
                    'last_name': request.POST.get('last_name', ''),
                }
                role = request.POST.get('role', '')
                if role == 'doctor':
                    update_data['specialization'] = request.POST.get('specialization', '')
                    update_data['license_number'] = request.POST.get('license_number', '')
                    
                db.collection('users').document(uid).update(update_data)
                messages.success(request, 'User updated successfully!')
                
            elif action == 'delete_appointment':
                app_id = request.POST.get('appointment_id')
                db.collection('appointments').document(app_id).delete()
                messages.success(request, 'Appointment deleted successfully!')
                
            elif action == 'edit_appointment':
                app_id = request.POST.get('appointment_id')
                status = request.POST.get('status')
                db.collection('appointments').document(app_id).update({'status': status})
                messages.success(request, 'Appointment updated successfully!')
                
        except Exception as e:
            messages.error(request, f'Error: {e}')
            
        return redirect('admin_dashboard')

    try:
        # 1. Fetch All Doctors
        doctors_docs = db.collection('users').where('role', '==', 'doctor').stream()
        doctors = []
        for doc in doctors_docs:
            d = doc.to_dict()
            d['id'] = doc.id
            d['full_name'] = f"{d.get('first_name', '')} {d.get('last_name', '')}"
            doctors.append(d)
            
        # 2. Fetch All Patients
        patients_docs = db.collection('users').where('role', '==', 'patient').stream()
        patients = []
        for doc in patients_docs:
            p = doc.to_dict()
            p['id'] = doc.id
            p['full_name'] = f"{p.get('first_name', '')} {p.get('last_name', '')}"
            patients.append(p)
            
        # 3. Fetch All Appointments
        apps_docs = db.collection('appointments').order_by('created_at', direction='DESCENDING').stream()
        appointments = []
        for doc in apps_docs:
            a = doc.to_dict()
            a['id'] = doc.id
            appointments.append(a)
            
        context = {
            'title': 'Unified Admin Dashboard',
            'doctors': doctors,
            'patients': patients,
            'appointments': appointments,
            'total_users': len(doctors) + len(patients),
            'total_doctors': len(doctors),
            'total_patients': len(patients),
            'total_appointments': len(appointments),
        }
        return render(request, 'admin-dashboard.html', context)
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('dashboard')


def about(request):
    """About page view"""
    context = {'title': 'About Us'}
    return render(request, 'about.html', context)

def admin_setup_view(request):
    """
    Emergency view to create/reset the admin user.
    PROTECTED: requires ?token=<ADMIN_SETUP_TOKEN> query parameter.
    Set ADMIN_SETUP_TOKEN in your .env file. Remove this URL from urls.py after first use.
    """
    import os
    from firebase_admin import auth, firestore
    from telemedicine.firestore_db import db

    # Token-gate: prevent unauthorized access
    expected_token = os.environ.get('ADMIN_SETUP_TOKEN', '')
    provided_token = request.GET.get('token', '')
    if not expected_token or provided_token != expected_token:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('403 Forbidden — valid ?token= required.')

    email = os.environ.get('ADMIN_EMAIL', 'admin@telemedicine.com')
    password = os.environ.get('ADMIN_SETUP_PASSWORD', '')

    if not password:
        return HttpResponse('❌ Error: ADMIN_SETUP_PASSWORD is not set in .env', status=500)

    try:
        # Clean up existing
        try:
            old = auth.get_user_by_email(email)
            auth.delete_user(old.uid)
        except: pass

        # Create fresh
        user = auth.create_user(email=email, password=password)
        uid = user.uid

        # Firestore doc
        db.collection('users').document(uid).set({
            'uid': uid,
            'email': email,
            'role': 'admin',
            'first_name': 'System',
            'last_name': 'Admin',
            'is_approved': True
        })
        # Don't echo password back in the response
        return HttpResponse(f'✅ Admin created! Login with: {email}')
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")


@login_required(login_url='login')
def approve_doctor(request, doctor_id):
    """Admin action to approve a doctor in Firestore"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
        
    from telemedicine.firestore_db import db
    try:
        db.collection('users').document(str(doctor_id)).update({'is_approved': True})
        messages.success(request, 'Doctor approved successfully!')
    except Exception as e:
        messages.error(request, f'Error approving doctor: {e}')
        
    return redirect('admin_dashboard')


@login_required(login_url='login')
def my_appointments(request):
    """View all patient's appointments from Firestore"""
    if request.user.role != 'patient':
        messages.error(request, 'This page is only for patients.')
        return redirect('dashboard')
    
    from telemedicine.firestore_db import db
    from datetime import datetime
    try:
        appointments_ref = db.collection('appointments')
        
        # Get all appointments for this patient
        query = appointments_ref.where('patient_id', '==', request.user.uid).stream()
        
        all_appointments = []
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            all_appointments.append(data)
            
        # Categorize
        upcoming = [a for a in all_appointments if a.get('status') == 'scheduled']
        completed = [a for a in all_appointments if a.get('status') == 'completed']
        cancelled = [a for a in all_appointments if a.get('status') == 'cancelled']
        
        # Sort
        upcoming.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        completed.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        
        context = {
            'title': 'My Appointments',
            'user': request.user,
            'upcoming_appointments': upcoming,
            'completed_appointments': completed,
            'cancelled_appointments': cancelled,
            'total_appointments': len(all_appointments),
            # Firebase Config
            'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
            'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
            'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
            'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
            'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
            'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
            'FIREBASE_CUSTOM_TOKEN': firebase_admin.auth.create_custom_token(request.user.uid).decode('utf-8'),
        }
        
        return render(request, 'my-appointments.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading appointments: {str(e)}')
        return redirect('dashboard')


@login_required(login_url='login')
def doctor_appointments(request):
    """View all doctor's appointments from Firestore"""
    if request.user.role != 'doctor':
        messages.error(request, 'This page is only for doctors.')
        return redirect('dashboard')
    
    # Check if doctor is approved
    is_approved = request.user.data.get('is_approved', False)
    if not is_approved:
        messages.warning(request, '⏳ Your doctor account is pending admin approval. You cannot view patient appointments yet.')
        return redirect('dashboard')
    
    from telemedicine.firestore_db import db
    try:
        appointments_ref = db.collection('appointments')
        
        # Get all appointments for this doctor
        query = appointments_ref.where('doctor_id', '==', request.user.uid).stream()
        
        all_appointments = []
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            all_appointments.append(data)
            
        # Categorize
        upcoming = [a for a in all_appointments if a.get('status') == 'scheduled']
        completed = [a for a in all_appointments if a.get('status') == 'completed']
        cancelled = [a for a in all_appointments if a.get('status') == 'cancelled']
        
        # Sort
        upcoming.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        completed.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        
        context = {
            'title': 'My Appointments',
            'user': request.user,
            'upcoming_appointments': upcoming,
            'completed_appointments': completed,
            'cancelled_appointments': cancelled,
            'total_appointments': len(all_appointments),
            # Firebase Config
            'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
            'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
            'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
            'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
            'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
            'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
            'FIREBASE_CUSTOM_TOKEN': firebase_admin.auth.create_custom_token(request.user.uid).decode('utf-8'),
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


@login_required(login_url='login')
def video_call(request, appointment_id):
    """Video call UI using Firestore appointment data"""
    from telemedicine.firestore_db import db
    try:
        doc_ref = db.collection('appointments').document(str(appointment_id))
        doc = doc_ref.get()
        
        if not doc.exists:
            messages.error(request, 'Appointment not found.')
            return redirect('dashboard')
            
        appointment = doc.to_dict()
        appointment['id'] = doc.id
        
        # Verify access
        # Get all appointments for this patient
        query = appointments_ref = db.collection('appointments')
        query = appointments_ref.where('patient_id', '==', request.user.uid).stream()
        
        all_appointments = []
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            all_appointments.append(data)
            
        # Categorize
        upcoming = [a for a in all_appointments if a.get('status') == 'scheduled']
        completed = [a for a in all_appointments if a.get('status') == 'completed']
        cancelled = [a for a in all_appointments if a.get('status') == 'cancelled']
        
        # Sort
        upcoming.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        completed.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        
        context = {
            'title': 'My Appointments',
            'user': request.user,
            'upcoming_appointments': upcoming,
            'completed_appointments': completed,
            'cancelled_appointments': cancelled,
            'total_appointments': len(all_appointments),
            # Firebase Config
            'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
            'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
            'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
            'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
            'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
            'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
            'FIREBASE_CUSTOM_TOKEN': firebase_admin.auth.create_custom_token(request.user.uid).decode('utf-8'),
        }
        
        return render(request, 'my-appointments.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading appointments: {str(e)}')
        return redirect('dashboard')


@login_required(login_url='login')
def doctor_appointments(request):
    """View all doctor's appointments from Firestore"""
    if request.user.role != 'doctor':
        messages.error(request, 'This page is only for doctors.')
        return redirect('dashboard')
    
    # Check if doctor is approved
    is_approved = request.user.data.get('is_approved', False)
    if not is_approved:
        messages.warning(request, '⏳ Your doctor account is pending admin approval. You cannot view patient appointments yet.')
        return redirect('dashboard')
    
    from telemedicine.firestore_db import db
    try:
        appointments_ref = db.collection('appointments')
        
        # Get all appointments for this doctor
        query = appointments_ref.where('doctor_id', '==', request.user.uid).stream()
        
        all_appointments = []
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            all_appointments.append(data)
            
        # Categorize
        upcoming = [a for a in all_appointments if a.get('status') == 'scheduled']
        completed = [a for a in all_appointments if a.get('status') == 'completed']
        cancelled = [a for a in all_appointments if a.get('status') == 'cancelled']
        
        # Sort
        upcoming.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        completed.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
        
        context = {
            'title': 'My Appointments',
            'user': request.user,
            'upcoming_appointments': upcoming,
            'completed_appointments': completed,
            'cancelled_appointments': cancelled,
            'total_appointments': len(all_appointments),
            # Firebase Config
            'FIREBASE_API_KEY': settings.FIREBASE_API_KEY,
            'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_AUTH_DOMAIN,
            'FIREBASE_PROJECT_ID': settings.FIREBASE_PROJECT_ID,
            'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_STORAGE_BUCKET,
            'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_MESSAGING_SENDER_ID,
            'FIREBASE_APP_ID': settings.FIREBASE_APP_ID,
            'FIREBASE_CUSTOM_TOKEN': firebase_admin.auth.create_custom_token(request.user.uid).decode('utf-8'),
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


@login_required(login_url='login')
def video_call(request, appointment_id):
    """Video call UI using Firestore appointment data"""
    from telemedicine.firestore_db import db
    try:
        doc_ref = db.collection('appointments').document(str(appointment_id))
        doc = doc_ref.get()
        
        if not doc.exists:
            messages.error(request, 'Appointment not found.')
            return redirect('dashboard')
            
        appointment = doc.to_dict()
        appointment['id'] = doc.id
        
        # Verify access
        is_patient = request.user.role == 'patient' and appointment.get('patient_id') == request.user.uid
        is_doctor = request.user.role == 'doctor' and appointment.get('doctor_id') == request.user.uid
        
        if not (is_patient or is_doctor):
            messages.error(request, 'You do not have permission to join this call.')
            return redirect('dashboard')
            
        context = {
            'title': 'Video Consultation',
            'appointment': appointment,
            'user': request.user,
            'is_patient': is_patient,
            'is_doctor': is_doctor,
        }
        return render(request, 'video-call.html', context)
        
    except Exception as e:
        messages.error(request, f'Error joining call: {str(e)}')
        return redirect('dashboard')


@login_required(login_url='login')
def delete_user_admin(request, user_id):
    """Admin action to delete a user from Firestore"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
        
    from telemedicine.firestore_db import db
    try:
        # Note: This deletes from Firestore.
        db.collection('users').document(str(user_id)).delete()
        messages.success(request, 'User deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting user: {e}')
        
    return redirect('admin_dashboard')


@login_required(login_url='login')
def edit_profile(request):
    """View to allow users to edit their own profile"""
    from telemedicine.firestore_db import db
    uid = str(request.user.uid)
    
    try:
        user_doc_ref = db.collection('users').document(uid)
        user_doc = user_doc_ref.get()
        
        if not user_doc.exists:
            messages.error(request, 'User profile not found in database.')
            return redirect('dashboard')
            
        user_data = user_doc.to_dict()
        
        if request.method == 'POST':
            # Extract common fields
            update_data = {
                'first_name': request.POST.get('first_name', '').strip(),
                'last_name': request.POST.get('last_name', '').strip(),
                'profile_image_url': request.POST.get('profile_image_url', '').strip(),
            }
            
            # Role-specific fields
            if request.user.role == 'doctor':
                update_data.update({
                    'specialization': request.POST.get('specialization', '').strip().lower(),
                    'license_number': request.POST.get('license_number', '').strip(),
                    'experience_years': int(request.POST.get('experience_years', '0') or 0),
                    'qualification': request.POST.get('qualification', '').strip(),
                    'bio': request.POST.get('bio', '').strip(),
                    'consultation_fee': float(request.POST.get('consultation_fee', '0') or 0),
                })
                # Handle checkboxes for available days
                available_days = request.POST.getlist('available_days')
                if available_days:
                    update_data['available_days'] = available_days
            elif request.user.role == 'patient':
                update_data.update({
                    'date_of_birth': request.POST.get('date_of_birth', '').strip(),
                    'medical_history': request.POST.get('medical_history', '').strip(),
                    'allergies': request.POST.get('allergies', '').strip(),
                    'emergency_contact': request.POST.get('emergency_contact', '').strip(),
                    'emergency_phone': request.POST.get('emergency_phone', '').strip(),
                })
            
            # Update Firestore
            user_doc_ref.update(update_data)
            
            # Update local Django User representation (for immediate session sync)
            request.user.first_name = update_data['first_name']
            request.user.last_name = update_data['last_name']
            request.user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
            
        context = {
            'title': 'Edit Profile',
            'profile': user_data
        }
        return render(request, 'edit-profile.html', context)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        messages.error(request, f'Error loading profile: {e}')
        return redirect('dashboard')
