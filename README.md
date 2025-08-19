# Appointment Management API

A Django REST Framework backend API for managing patient appointments.

## Overview

This project implements a simple appointment management system with the following features:
- Patient management (Create, List)
- Appointment creation and listing
- RESTful API design
- Swagger/OpenAPI documentation
- SQLite database (easily configurable for other databases)

## API Endpoints

### Base URL
- Local Development: `http://127.0.0.1:8000/`
- API Base: `http://127.0.0.1:8000/api/`

### Available Endpoints

1. **GET /api/patients/** - List all patients
2. **POST /api/patients/** - Create a new patient
3. **GET /api/appointments/** - List all appointments
4. **POST /api/appointments/create/** - Create a new appointment (Main requirement)

### Documentation
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

## Create Appointment API (Main Requirement)

### Endpoint
```
POST /api/appointments/create/
```

### Request Body (JSON)
```json
{
    "PatientId": 1,
    "AppointmentDate": "2025-08-25",
    "AppointmentTime": "14:30",
    "Reason": "Regular checkup"
}
```

### Response (JSON)
```json
{
    "AppointmentId": 101,
    "PatientId": 1,
    "AppointmentDate": "2025-08-25",
    "AppointmentTime": "14:30",
    "Reason": "Regular checkup",
    "Message": "Appointment created successfully"
}
```

### Error Response
```json
{
    "error": "Invalid data provided",
    "details": {
        "PatientId": ["Patient with this ID does not exist."]
    }
}
```

## Technology Stack

- **Backend Framework**: Django 5.2.5
- **API Framework**: Django REST Framework
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Database**: SQLite (default, configurable)
- **Python Version**: 3.12+

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd appointment_api
   ```

2. **Install dependencies**
   ```bash
   pip install django djangorestframework drf-yasg django-cors-headers
   ```

3. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create sample data (optional)**
   ```bash
   python manage.py populate_data
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - API Documentation: http://127.0.0.1:8000/swagger/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Base: http://127.0.0.1:8000/api/

## Database Schema

### Patient Model
- `id` (Primary Key)
- `name` (CharField, max_length=100)
- `email` (EmailField, unique=True)
- `phone` (CharField with validation)
- `date_of_birth` (DateField)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

### Appointment Model
- `id` (Primary Key)
- `patient` (ForeignKey to Patient)
- `appointment_date` (DateField)
- `appointment_time` (TimeField)
- `reason` (TextField)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

## API Validation

The Create Appointment API includes the following validations:
- Patient ID must exist in the database
- Appointment date cannot be in the past
- All required fields must be provided
- Unique constraint: One appointment per patient per date/time slot

## Testing the API

### Using Swagger UI
1. Navigate to `http://127.0.0.1:8000/swagger/`
2. Find the "POST /api/appointments/create/" endpoint
3. Click "Try it out"
4. Enter the request body and execute

### Using curl
```bash
curl -X POST http://127.0.0.1:8000/api/appointments/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "PatientId": 1,
    "AppointmentDate": "2025-08-25",
    "AppointmentTime": "14:30",
    "Reason": "Regular checkup"
  }'
```

### Using Python requests
```python
import requests

url = "http://127.0.0.1:8000/api/appointments/create/"
data = {
    "PatientId": 1,
    "AppointmentDate": "2025-08-25",
    "AppointmentTime": "14:30",
    "Reason": "Regular checkup"
}

response = requests.post(url, json=data)
print(response.json())
```

## Sample Data

The project includes 5 sample patients:
- John Doe (ID: 1)
- Jane Smith (ID: 2)
- Michael Johnson (ID: 3)
- Emily Davis (ID: 4)
- David Wilson (ID: 5)

## Project Structure

```
appointment_api/
├── appointments/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── populate_data.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── appointment_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## Deployment Notes

For production deployment, consider:
1. Change `DEBUG = False` in settings.py
2. Set proper `ALLOWED_HOSTS`
3. Use environment variables for sensitive settings
4. Use a production database (PostgreSQL, MySQL)
5. Configure static files serving
6. Set up proper logging
7. Use HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
