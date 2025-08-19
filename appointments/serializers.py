from rest_framework import serializers
from .models import Patient, Appointment
from datetime import date, time


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model
    """
    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'phone', 'date_of_birth', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating appointments
    """
    PatientId = serializers.IntegerField(source='patient.id', write_only=True)
    AppointmentDate = serializers.DateField(source='appointment_date', write_only=True)
    AppointmentTime = serializers.TimeField(source='appointment_time', write_only=True)
    Reason = serializers.CharField(source='reason', write_only=True)

    class Meta:
        model = Appointment
        fields = ['PatientId', 'AppointmentDate', 'AppointmentTime', 'Reason']

    def validate_PatientId(self, value):
        """
        Validate that the patient exists
        """
        if not Patient.objects.filter(id=value).exists():
            raise serializers.ValidationError("Patient with this ID does not exist.")
        return value

    def validate_AppointmentDate(self, value):
        """
        Validate that the appointment date is not in the past
        """
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    def validate_AppointmentTime(self, value):
        """
        Validate appointment time format
        """
        return value

    def create(self, validated_data):
        """
        Create and return a new Appointment instance
        """
        patient_id = validated_data.pop('patient')['id']
        patient = Patient.objects.get(id=patient_id)
        
        appointment = Appointment.objects.create(
            patient=patient,
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            reason=validated_data['reason']
        )
        return appointment


class AppointmentResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for appointment response
    """
    AppointmentId = serializers.SerializerMethodField()
    PatientId = serializers.IntegerField(source='patient.id', read_only=True)
    AppointmentDate = serializers.DateField(source='appointment_date', read_only=True)
    AppointmentTime = serializers.TimeField(source='appointment_time', read_only=True)
    Reason = serializers.CharField(source='reason', read_only=True)
    Message = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['AppointmentId', 'PatientId', 'AppointmentDate', 'AppointmentTime', 'Reason', 'Message']

    def get_AppointmentId(self, obj):
        """Return AppointmentId starting from 101 as per requirements"""
        return obj.id + 100

    def get_Message(self, obj):
        return "Appointment created successfully"


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating appointments
    """
    AppointmentDate = serializers.DateField(source='appointment_date', required=False)
    AppointmentTime = serializers.TimeField(source='appointment_time', required=False)
    Reason = serializers.CharField(source='reason', required=False)

    class Meta:
        model = Appointment
        fields = ['AppointmentDate', 'AppointmentTime', 'Reason']

    def validate_AppointmentDate(self, value):
        """
        Validate that the appointment date is not in the past
        """
        if value and value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    def update(self, instance, validated_data):
        """
        Update and return the appointment instance
        """
        instance.appointment_date = validated_data.get('appointment_date', instance.appointment_date)
        instance.appointment_time = validated_data.get('appointment_time', instance.appointment_time)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.save()
        return instance


class AppointmentListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing appointments
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_name', 'appointment_date', 'appointment_time', 'reason', 'created_at']
