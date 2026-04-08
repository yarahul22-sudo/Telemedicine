#!/usr/bin/env python
"""
Create a status check view to debug booking form issues
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

# Create simple diagnostic view
def booking_status(request):
    """Show booking form status and debugging info"""
    
    doctor_id = request.GET.get('doctor_id')
    
    response_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Booking Form - Status Check</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; }}
            .status {{ padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .status.ok {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .status.error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .status.info {{ background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }}
            code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
            .steps {{ margin: 20px 0; }}
            .step {{ padding: 10px; margin: 10px 0; background: #f9f9f9; border-left: 4px solid #667eea; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Booking Form - Status Check</h1>
            
            <div class="status {'ok' if request.user.is_authenticated else 'error'}">
                <strong>Login Status:</strong> {'✓ LOGGED IN' if request.user.is_authenticated else '✗ NOT LOGGED IN'}
                {'<br/>User: ' + request.user.email if request.user.is_authenticated else ''}
                {'<br/>Role: ' + request.user.role if request.user.is_authenticated and hasattr(request.user, 'role') else ''}
            </div>
            
            <div class="status {'ok' if doctor_id else 'error'}">
                <strong>Doctor ID Parameter:</strong> {'✓ ' + doctor_id if doctor_id else '✗ MISSING'}
            </div>
            
            <div class="status info">
                <strong>Current URL:</strong> <code>{request.get_full_path()}</code>
            </div>
            
            <h2>🔧 Troubleshooting Steps:</h2>
            <div class="steps">
                <div class="step">
                    <strong>Step 1:</strong> If you see "NOT LOGGED IN" above:
                    <ul>
                        <li>Go to: <a href="/login/">http://127.0.0.1:8000/login/</a></li>
                        <li>Login with: <code>pshyam@telemedicine.com</code></li>
                        <li>Password: <code>pshyam123</code></li>
                        <li>Then come back to this page</li>
                    </ul>
                </div>
                
                <div class="step">
                    <strong>Step 2:</strong> If doctor_id is "MISSING":
                    <ul>
                        <li>Your URL should include <code>?doctor_id=7</code></li>
                        <li>Try this: <a href="/book-appointment/?doctor_id=7">/book-appointment/?doctor_id=7</a></li>
                        <li>Or try other doctor IDs: 1, 2, 3, 6, 8, 9</li>
                    </ul>
                </div>
                
                <div class="step">
                    <strong>Step 3:</strong> If both are OK but form not showing:
                    <ul>
                        <li>Clear browser cache: <code>Ctrl + Shift + Delete</code></li>
                        <li>Hard refresh: <code>Ctrl + Shift + F5</code></li>
                        <li>Try different browser</li>
                        <li>Make sure server is running in terminal</li>
                    </ul>
                </div>
            </div>
            
            <h2>✅ Next Steps:</h2>
            {'<div class="step" style="background: #d4edda;"><strong>✓ Ready to book!</strong><br/>Go to: <a href="/book-appointment/?doctor_id=' + doctor_id + '">/book-appointment/?doctor_id=' + doctor_id + '</a></div>' if (request.user.is_authenticated and doctor_id) else '<div class="step">Complete the troubleshooting steps above first</div>'}
            
            <h2>📞 Quick Links:</h2>
            <ul>
                <li><a href="/dashboard/">Dashboard</a></li>
                <li><a href="/find-doctor/">Find Doctor</a></li>
                <li><a href="/my-appointments/">My Appointments</a></li>
                <li><a href="/logout/">Logout</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(response_html)

# Print URL pattern
print("Add this to telemedicine/urls.py:")
print("""
from django.urls import path
from accounts.views import booking_status

urlpatterns = [
    # ... other urls ...
    path('booking-status/', booking_status, name='booking_status'),
]
""")

print("\nOr use this URL to test directly:")
print("http://127.0.0.1:8000/booking-status/?doctor_id=7")
