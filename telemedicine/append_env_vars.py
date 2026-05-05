"""
Utility script to append missing security variables to .env safely.
Run once: python append_env_vars.py
"""
import os

env_path = os.path.join(os.path.dirname(__file__), '.env')

NEW_VARS = """
# ─── Django Core Security ────────────────────────────────────────────────────
# IMPORTANT: Generate a new SECRET_KEY for production using:
#   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=p@x2$k9!qm_g7#zjwR3d^Lv8Ys5Nue6FtCb4oPh1mXiAn0KwTeLeMedSecure2026

# Set to False in production
DEBUG=True

# Comma-separated. Add your production domain here when deploying
ALLOWED_HOSTS=localhost,127.0.0.1

# Set to True when running behind HTTPS (production only)
COOKIE_SECURE=False

# ─── Admin Setup Credentials ─────────────────────────────────────────────────
# Staff admin (Firestore-based, logs into /admin/)
ADMIN_EMAIL=admin@telemedicine.com
ADMIN_SETUP_PASSWORD=admin12345

# Super admin (Django local DB, logs into /djangoadmin/)
SUPER_ADMIN_EMAIL=admin@gmail.com
SUPER_ADMIN_PASSWORD=Rahul12345

# Token required to access /admin-setup/?token=... URL
# Change this to a long random string before deploying!
ADMIN_SETUP_TOKEN=TeLeMedSetup2026SecureToken
"""

with open(env_path, 'r', encoding='utf-8') as f:
    existing = f.read()

# Only append vars that aren't already defined
lines_to_add = []
for line in NEW_VARS.strip().split('\n'):
    key = line.split('=')[0].strip()
    if key.startswith('#') or not key:
        lines_to_add.append(line)
    elif key + '=' not in existing and key + ' =' not in existing:
        lines_to_add.append(line)

if lines_to_add:
    with open(env_path, 'a', encoding='utf-8') as f:
        f.write('\n' + '\n'.join(lines_to_add) + '\n')
    print(f"Added {len([l for l in lines_to_add if not l.startswith('#') and l])} new variables to .env")
else:
    print("All variables already present in .env")
