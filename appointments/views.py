from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Patient, Appointment
from .serializers import (
    PatientSerializer, 
    AppointmentCreateSerializer, 
    AppointmentResponseSerializer,
    AppointmentListSerializer,
    AppointmentUpdateSerializer
)

# Create your views here.

class PatientListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve list of patients or create a new patient
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @swagger_auto_schema(
        operation_description="Get list of all patients",
        responses={200: PatientSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new patient",
        request_body=PatientSerializer,
        responses={
            201: PatientSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AppointmentListView(generics.ListAPIView):
    """
    API view to retrieve list of appointments
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer

    @swagger_auto_schema(
        operation_description="Get list of all appointments",
        responses={200: AppointmentListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new appointment for a patient",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['PatientId', 'AppointmentDate', 'AppointmentTime', 'Reason'],
        properties={
            'PatientId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the patient'),
            'AppointmentDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of appointment (YYYY-MM-DD)'),
            'AppointmentTime': openapi.Schema(type=openapi.TYPE_STRING, description='Time of appointment (HH:MM)'),
            'Reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for the appointment'),
        }
    ),
    responses={
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'AppointmentId': openapi.Schema(type=openapi.TYPE_INTEGER),
                'PatientId': openapi.Schema(type=openapi.TYPE_INTEGER),
                'AppointmentDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'AppointmentTime': openapi.Schema(type=openapi.TYPE_STRING),
                'Reason': openapi.Schema(type=openapi.TYPE_STRING),
                'Message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING),
                'details': openapi.Schema(type=openapi.TYPE_OBJECT)
            }
        )
    }
)
@api_view(['POST'])
def create_appointment(request):
    """
    Create a new appointment for a patient
    """
    serializer = AppointmentCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            appointment = serializer.save()
            response_serializer = AppointmentResponseSerializer(appointment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': 'Failed to create appointment',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'error': 'Invalid data provided',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    operation_description="Update an existing appointment",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'AppointmentDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of appointment (YYYY-MM-DD)'),
            'AppointmentTime': openapi.Schema(type=openapi.TYPE_STRING, description='Time of appointment (HH:MM)'),
            'Reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for the appointment'),
        }
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'AppointmentId': openapi.Schema(type=openapi.TYPE_INTEGER),
                'PatientId': openapi.Schema(type=openapi.TYPE_INTEGER),
                'AppointmentDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'AppointmentTime': openapi.Schema(type=openapi.TYPE_STRING),
                'Reason': openapi.Schema(type=openapi.TYPE_STRING),
                'Message': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING),
                'details': openapi.Schema(type=openapi.TYPE_OBJECT)
            }
        ),
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    }
)
@api_view(['PUT'])
def update_appointment(request, appointment_id):
    """
    Update an existing appointment
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({
            'error': 'Appointment not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AppointmentUpdateSerializer(appointment, data=request.data, partial=True)
    
    if serializer.is_valid():
        try:
            updated_appointment = serializer.save()
            response_serializer = AppointmentResponseSerializer(updated_appointment)
            response_data = response_serializer.data
            response_data['Message'] = "Appointment updated successfully"
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to update appointment',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'error': 'Invalid data provided',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_description="Delete an existing appointment",
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'AppointmentId': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    }
)
@api_view(['DELETE'])
def delete_appointment(request, appointment_id):
    """
    Delete an existing appointment
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment_display_id = appointment.id + 100  # Convert to display ID (101+)
        appointment.delete()
        return Response({
            'message': 'Appointment deleted successfully',
            'AppointmentId': appointment_display_id
        }, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({
            'error': 'Appointment not found'
        }, status=status.HTTP_404_NOT_FOUND)
