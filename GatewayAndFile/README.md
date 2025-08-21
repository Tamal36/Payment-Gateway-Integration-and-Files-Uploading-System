# GatewayAndFile - Payment Gateway Integration and File Upload System

## Project Overview

GatewayAndFile is a Django-based web application that integrates payment gateway functionality with a file upload and processing system. The application allows users to register, make payments through aamarPay payment gateway, and upload files after successful payment. The uploaded files are processed asynchronously using Celery to count words and update status.

## Features

- **User Authentication**: Registration, login, and profile management
- **Payment Integration**: Seamless integration with aamarPay payment gateway
- **File Upload System**: Upload and process text (.txt) and Word (.docx) files
- **Asynchronous Processing**: Background processing of uploaded files using Celery
- **Activity Tracking**: Logging of user activities and file processing status
- **RESTful API**: Comprehensive API endpoints for all functionality
- **Frontend Interface**: User-friendly web interface for all features
- **JWT Authentication**: Secure API access with JWT tokens

## Tech Stack

### Backend
- **Django 5.2.5**: Web framework
- **Django REST Framework 3.16.1**: API development
- **Celery 5.5.3**: Asynchronous task processing
- **Redis 6.4.0**: Message broker for Celery
- **JWT Authentication**: Using djangorestframework-simplejwt 5.5.1
- **python-docx 1.2.0**: For processing Word documents

### Frontend
- **Bootstrap 5**: CSS framework for responsive design
- **JavaScript**: For interactive UI components

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **SQLite**: Database (for development)

## Project Structure

```
GatewayAndFile/
├── .env                    # Environment variables
├── Dockerfile              # Docker configuration
├── GatewayAndFile/         # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py           # Celery configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py
├── db.sqlite3              # SQLite database
├── docker-compose.yml      # Docker Compose configuration
├── manage.py               # Django management script
├── payments/               # Payment app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py           # Payment models
│   ├── serializers.py      # API serializers
│   ├── tests.py
│   ├── urls.py             # Payment URLs
│   └── views.py            # Payment views
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── payments/           # Payment templates
|   |    ├── login.html
|   |    ├── transactions.html
│   └── uploads/            # Upload templates
|        ├── activity.html
|        ├── files.html
|        ├── upload.html
├── uploads/                # Upload app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py           # Upload models
│   ├── serializers.py      # API serializers
│   ├── tasks.py            # Celery tasks
│   ├── tests.py
│   ├── urls.py             # Upload URLs
│   └── views.py            # Upload views
└── uploadsFiles/           # Directory for uploaded files
```

## Installation and Setup

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GatewayAndFile
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   Create a `.env` file in the project root with the following content:
   ```
   SECRET_KEY='your-secret-key'
   DEBUG=True
   
   STORE_ID='aamarpaytest'
   SIGNATURE_KEY='dbb74894e82415a2f7ff0ec3a97e4183'
   AAMARPAY_ENDPOINT='https://sandbox.aamarpay.com/jsonpost.php'
   PAYMENT_AMOUNT='100'
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Redis server**
   ```bash
   # Install Redis first if not already installed
   # Windows: Download and install from https://github.com/microsoftarchive/redis/releases
   # Linux: sudo apt-get install redis-server
   
   # Start Redis server
   # Windows: redis-server
   # Linux: sudo service redis-server start
   ```

8. **Start Celery worker**
   ```bash
   # Windows
   celery -A GatewayAndFile worker -l info --pool=solo
   
   # Linux/Mac
   celery -A GatewayAndFile worker -l info
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Web Interface: http://127.0.0.1:8000/
    - Admin Interface: http://127.0.0.1:8000/admin/

### Docker Setup

1. **Build and start the containers**
   ```bash
   docker-compose up -d --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create a superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
    - Web Interface: http://localhost:8000/
    - Admin Interface: http://localhost:8000/admin/

## API Endpoints

### Authentication

- **JWT Token**: `POST /api/auth/token/`
  - Request: `{"username": "user", "password": "pass"}`
  - Response: `{"access": "token", "refresh": "token"}`

- **Refresh Token**: `POST /api/auth/token/refresh/`
  - Request: `{"refresh": "token"}`
  - Response: `{"access": "token"}`

### User Management

- **Register User**: `POST /api/register/`
  - Request: `{"username": "user", "email": "user@example.com", "password": "pass"}`

- **Get User Profile**: `GET /api/profile/`
  - Requires Authentication

### Payment

- **Initiate Payment**: `POST /api/initiate-payment/`
  - Requires Authentication
  - Response: `{"payment_url": "https://sandbox.aamarpay.com/..."}`

- **Payment Success**: `GET/POST /api/payment/success/`
  - Called by aamarPay after successful payment

- **Payment Failed**: `GET/POST /api/payment/failed/`
  - Called by aamarPay after failed payment

- **Payment Cancelled**: `GET /api/payment/cancelled/`
  - Called by aamarPay after cancelled payment

- **Get User Transactions**: `GET /api/payment/transactions/`
  - Requires Authentication

### File Upload

- **Upload File**: `POST /api/upload/`
  - Requires Authentication and successful payment
  - Form data: `{"file": file_object}`

- **List Files**: `GET /api/files/`
  - Requires Authentication

- **List Activity**: `GET /api/activity/`
  - Requires Authentication

### Frontend URLs

- **Login**: `/api/login-view/`
- **Transaction History**: `/api/transactions-view/`
- **Upload File**: `/api/upload-view/`
- **List Files**: `/api/files-view/`
- **Activity Log**: `/api/activity-view/`

## Validation/Business Logic

### Payment Flow

1. User must be authenticated to initiate payment
2. Payment amount is fixed at 100 BDT
3. Transaction ID is generated as a UUID
4. Payment status is tracked (Initiated, Success, Failed)
5. Payment verification is done by calling aamarPay's verification API

### File Upload

1. User must have at least one successful payment to upload files
2. Only .txt and .docx files are allowed
3. File size is limited to 5MB (configured in settings)
4. Files are processed asynchronously using Celery
5. Word count is calculated for each file
6. Processing status is tracked (Processing, Completed, Failed)

## Testing the Payment Flow with aamarPay Sandbox

1. **Register a new user** or login with an existing user
2. **Navigate to the dashboard** and click on "Initiate Payment"
3. **You will be redirected to the aamarPay sandbox payment page**
4. **Use the following test card details**:
   - Card Number: 1111 1111 1111 1111
   - Expiry Date: Any future date
   - CVV: Any 3-digit number
5. **Complete the payment process**
6. **You will be redirected back to the application** with payment status
7. **After successful payment**, you can upload files

## Celery and Redis Setup

### Redis Configuration

The application uses Redis as the message broker for Celery. The Redis connection is configured in `settings.py`:

```python
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = 'django-db'
```

### Celery Configuration

Celery is configured in `GatewayAndFile/celery.py`. It automatically discovers tasks in all installed apps.

### Running Celery

- **Local**: `celery -A GatewayAndFile worker -l info`
- **Docker**: Celery worker is automatically started by Docker Compose

### Celery Tasks

The main Celery task is `process_file` in `uploads/tasks.py`. It processes uploaded files to count words and update status.

## Additional Information

### Security Considerations

- JWT tokens are used for API authentication
- Sensitive information is stored in environment variables
- CSRF protection is enabled for form submissions
- File uploads are validated for type and size

### Error Handling

- API endpoints return appropriate HTTP status codes and error messages
- Celery tasks have retry mechanisms for handling failures
- Activity logs track user actions and system events

### Future Improvements

- Add more payment gateways
- Implement file type validation using content inspection
- Add user roles and permissions
- Implement file sharing functionality
- Add more comprehensive test coverage

## License

This project is licensed under the MIT License - see the LICENSE file for details.