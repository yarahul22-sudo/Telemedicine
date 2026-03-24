from django.core.management.base import BaseCommand
from appointments.models import Disease


class Command(BaseCommand):
    help = 'Load sample diseases into the database'

    def handle(self, *args, **options):
        diseases_data = [
            {
                'name': 'Heart Disease',
                'description': 'Cardiovascular diseases including heart attack, angina, and arrhythmia',
                'specialization_required': 'cardiology'
            },
            {
                'name': 'Hypertension',
                'description': 'High blood pressure condition',
                'specialization_required': 'cardiology'
            },
            {
                'name': 'Diabetes',
                'description': 'Blood sugar disorders and metabolic conditions',
                'specialization_required': 'general'
            },
            {
                'name': 'Skin Disease',
                'description': 'Dermatological conditions including acne, psoriasis, eczema',
                'specialization_required': 'dermatology'
            },
            {
                'name': 'Acne',
                'description': 'Skin condition causing pimples and inflammatory lesions',
                'specialization_required': 'dermatology'
            },
            {
                'name': 'Psoriasis',
                'description': 'Chronic autoimmune skin condition',
                'specialization_required': 'dermatology'
            },
            {
                'name': 'Headache',
                'description': 'Various types of headaches including migraines and tension',
                'specialization_required': 'neurology'
            },
            {
                'name': 'Migraine',
                'description': 'Severe headaches often with visual disturbances',
                'specialization_required': 'neurology'
            },
            {
                'name': 'Back Pain',
                'description': 'Lower or upper back pain conditions',
                'specialization_required': 'orthopedics'
            },
            {
                'name': 'Joint Pain',
                'description': 'Arthritis and joint-related conditions',
                'specialization_required': 'orthopedics'
            },
            {
                'name': 'Anxiety Disorder',
                'description': 'Mental health condition characterized by persistent worry',
                'specialization_required': 'psychiatry'
            },
            {
                'name': 'Depression',
                'description': 'Mental health condition affecting mood and motivation',
                'specialization_required': 'psychiatry'
            },
            {
                'name': 'Childhood Illness',
                'description': 'Common pediatric conditions',
                'specialization_required': 'pediatrics'
            },
            {
                'name': 'Cold and Flu',
                'description': 'Viral respiratory infections',
                'specialization_required': 'general'
            },
            {
                'name': 'Cough',
                'description': 'Persistent coughing conditions',
                'specialization_required': 'general'
            },
        ]
        
        created_count = 0
        for disease_data in diseases_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults={
                    'description': disease_data['description'],
                    'specialization_required': disease_data['specialization_required']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created disease: {disease.name}')
                )
            else:
                self.stdout.write(f'Disease already exists: {disease.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new diseases!')
        )
