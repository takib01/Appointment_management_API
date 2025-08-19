from django.core.management.base import BaseCommand
from appointments.models import Patient, Appointment
from datetime import date, time


class Command(BaseCommand):
    help = 'Populate the database with sample patients and appointments'

    def handle(self, *args, **options):
        # Create sample patients
        patients_data = [
            {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890',
                'date_of_birth': date(1990, 5, 15)
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'phone': '+1234567891',
                'date_of_birth': date(1985, 8, 22)
            },
            {
                'name': 'Michael Johnson',
                'email': 'michael.johnson@example.com',
                'phone': '+1234567892',
                'date_of_birth': date(1992, 12, 3)
            },
            {
                'name': 'Emily Davis',
                'email': 'emily.davis@example.com',
                'phone': '+1234567893',
                'date_of_birth': date(1988, 3, 18)
            },
            {
                'name': 'David Wilson',
                'email': 'david.wilson@example.com',
                'phone': '+1234567894',
                'date_of_birth': date(1995, 7, 9)
            }
        ]

        self.stdout.write(self.style.SUCCESS('Creating sample patients...'))
        
        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                self.stdout.write(f'Created patient: {patient.name}')
            else:
                self.stdout.write(f'Patient already exists: {patient.name}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(f'Total patients in database: {Patient.objects.count()}')
        self.stdout.write(f'Total appointments in database: {Appointment.objects.count()}')
