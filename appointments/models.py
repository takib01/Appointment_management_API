from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Patient(models.Model):
    """
    Patient model to store patient information
    """
    name = models.CharField(max_length=100, help_text="Patient full name")
    email = models.EmailField(unique=True, help_text="Patient email address")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        help_text="Patient phone number"
    )
    date_of_birth = models.DateField(help_text="Patient date of birth")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    class Meta:
        ordering = ['name']


class Appointment(models.Model):
    """
    Appointment model to store appointment information
    """
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='appointments',
        help_text="Patient for this appointment"
    )
    appointment_date = models.DateField(help_text="Date of the appointment")
    appointment_time = models.TimeField(help_text="Time of the appointment")
    reason = models.TextField(help_text="Reason for the appointment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient.name} on {self.appointment_date} at {self.appointment_time}"

    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        unique_together = ['patient', 'appointment_date', 'appointment_time']
