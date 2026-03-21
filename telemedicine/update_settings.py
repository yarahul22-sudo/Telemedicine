import sys
sys.path.insert(0, '.')

# Read settings.py
with open('telemedicine/settings.py', 'r') as f:
    content = f.read()

# Check what needs to be added
if "'rest_framework.authtoken'" not in content:
    # Add authtoken to INSTALLED_APPS
    content = content.replace(
        "    'appointments',\n]",
        "    'appointments',\n    'rest_framework.authtoken',\n]"
    )

if 'AUTH_USER_MODEL' not in content:
    # Add AUTH_USER_MODEL at the end
    content += "\n\nAUTH_USER_MODEL = 'users.CustomUser'\n"

# Write back
with open('telemedicine/settings.py', 'w') as f:
    f.write(content)
    
print('Settings updated successfully')
