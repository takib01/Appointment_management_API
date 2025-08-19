from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/create/', views.create_appointment, name='create-appointment'),
    path('appointments/<int:appointment_id>/update/', views.update_appointment, name='update-appointment'),
    path('appointments/<int:appointment_id>/delete/', views.delete_appointment, name='delete-appointment'),
]
