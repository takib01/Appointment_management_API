from django.contrib import admin
from .models import Patient, Appointment

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'date_of_birth', 'created_at']
    list_filter = ['created_at', 'date_of_birth']
    search_fields = ['name', 'email', 'phone']
    ordering = ['name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'appointment_date', 'appointment_time', 'reason', 'created_at']
    list_filter = ['appointment_date', 'created_at']
    search_fields = ['patient__name', 'reason']
    ordering = ['appointment_date', 'appointment_time']
    raw_id_fields = ['patient']
