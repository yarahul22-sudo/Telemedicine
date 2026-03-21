"""
Test script for the authentication API
"""
import json
import requests

BASE_URL = "http://127.0.0.1:8000/api/users"

# Test Registration
print("=" * 50)
print("Testing User Registration")
print("=" * 50)

# Register a Patient
patient_data = {
    "username": "john_patient",
    "email": "john@patient.com",
    "password": "secure123456",
    "password_confirm": "secure123456",
    "first_name": "John",
    "last_name": "Doe",
    "role": "patient",
    "phone": "+1234567890"
}

response = requests.post(f"{BASE_URL}/register/", json=patient_data)
print(f"Patient Registration: {response.status_code}")
print(json.dumps(response.json(), indent=2))
patient_token = response.json().get('token')

# Register a Doctor
doctor_data = {
    "username": "dr_smith",
    "email": "smith@doctor.com",
    "password": "secure123456",
    "password_confirm": "secure123456",
    "first_name": "Dr",
    "last_name": "Smith",
    "role": "doctor",
    "phone": "+1987654321",
    "specialization": "Cardiology",
    "license_number": "LIC12345",
    "experience_years": 10
}

response = requests.post(f"{BASE_URL}/register/", json=doctor_data)
print(f"\nDoctor Registration: {response.status_code}")
print(json.dumps(response.json(), indent=2))
doctor_token = response.json().get('token')

# Test Login
print("\n" + "=" * 50)
print("Testing User Login")
print("=" * 50)

login_data = {
    "username": "john_patient",
    "password": "secure123456"
}

response = requests.post(f"{BASE_URL}/login/", json=login_data)
print(f"Login: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test Get Profile
print("\n" + "=" * 50)
print("Testing Get Profile")
print("=" * 50)

headers = {"Authorization": f"Token {patient_token}"}
response = requests.get(f"{BASE_URL}/profile/", headers=headers)
print(f"Get Profile: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test Get User Role
print("\n" + "=" * 50)
print("Testing Get User Role")
print("=" * 50)

response = requests.get(f"{BASE_URL}/role/", headers=headers)
print(f"Get Role: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test List Doctors (Doctor not verified yet)
print("\n" + "=" * 50)
print("Testing List Doctors")
print("=" * 50)

response = requests.get(f"{BASE_URL}/doctors/", headers=headers)
print(f"List Doctors: {response.status_code}")
print(json.dumps(response.json(), indent=2))

print("\nAll tests completed!")
