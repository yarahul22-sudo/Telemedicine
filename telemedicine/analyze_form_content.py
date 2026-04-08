#!/usr/bin/env python
"""
Extract and show what's rendered on the booking form page
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')
django.setup()

from django.test import Client
from users.models import CustomUser

client = Client()
user = CustomUser.objects.get(email='pshyam@telemedicine.com')
user.set_password('test123')
user.save()
client.force_login(user)

# Get booking form
response = client.get('/book-appointment/?doctor_id=7')
content = response.content.decode('utf-8')

# Extract doctor info section
print("\n" + "=" * 80)
print("BOOKING FORM CONTENT ANALYSIS")
print("=" * 80)

# Check if bookingForm is in content
if 'id="bookingForm"' in content:
    print("\n✓ Booking form element found")
else:
    print("\n✗ Booking form element NOT found")

# Check for doctor info in template
if 'Dr. Ramlal' in content or 'dramlal' in content.lower():
    print("✓ Doctor name found in page")
else:
    print("✗ Doctor name NOT found")

# Check for doctor-card div
if 'class="doctor-card"' in content:
    print("✓ Doctor card div found")
else:
    print("✗ Doctor card div NOT found")

# Show booking container
if 'class="booking-container"' in content:
    print("✓ Booking container found")
else:
    print("✗ Booking container NOT found")

# Extract just the booking form section
start_booking = content.find('id="bookingForm"')
if start_booking > 0:
    form_section = content[start_booking-200:start_booking+800]
    print("\n" + "=" * 80)
    print("FORM SECTION SNIPPET:")
    print("=" * 80)
    print(form_section[:500])

# Check for CSS styles
if 'booking-container {' in content:
    print("\n✓ CSS styles included in page")
else:
    print("\n✗ CSS styles NOT included")

# Check base.html block
if '{% block content %}' in content or 'block content' in content or '<div' in content:
    print("✓ Content block found")
else:
    print("✗ Content block NOT found")

# Show file size
print(f"\n📊 Page size: {len(content)} characters")

# Check for key form fields
fields = ['appointment_date', 'consultation_type', 'disease_id', 'notes']
print("\n" + "=" * 80)
print("FORM FIELDS CHECK:")
print("=" * 80)

for field in fields:
    if f'id="{field}"' in content:
        print(f"✓ {field} field found")
    else:
        print(f"✗ {field} field NOT found")

# Save sample to file for inspection
with open('booking_form_content.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ Full content saved to: booking_form_content.txt")
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
