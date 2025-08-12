# Udyam Registration API

A FastAPI-based REST API for Udyam registration form validation and data storage in PostgreSQL.

## Features

- **Aadhaar Verification**: Validate 12-digit Aadhaar numbers and entrepreneur names
- **OTP Validation**: Generate and validate 6-digit OTP codes
- **PAN Validation**: Validate PAN numbers and associated details
- **Database Storage**: Store all registrations in PostgreSQL with audit trails
- **Validation Logging**: Track all validation attempts and results
- **RESTful API**: Clean, documented API endpoints with automatic OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Documentation**: OpenAPI/Swagger

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection and session
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── validators.py      # Validation logic
│   └── api/
│       ├── __init__.py
│       ├── api.py         # Main API router
│       └── endpoints/
│           ├── __init__.py
│           └── registration.py  # Registration endpoints
├── alembic/               # Database migrations
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
├── alembic.ini          # Alembic configuration
└── README.md            # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### 2. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE udyam_db;
CREATE USER udyam_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE udyam_db TO udyam_user;
```

### 3. Environment Configuration

Copy the environment example file and configure it:

```bash
cp env.example .env
```

Edit `.env` with your database credentials:

```env
DATABASE_URL=postgresql://udyam_user:your_password@localhost:5432/udyam_db
SECRET_KEY=your-secret-key-here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Migrations

Initialize Alembic and create initial migration:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Run the Application

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python main.py
```

The API will be available at:
- **API Base URL**: http://localhost:8000/api/v1
- **Documentation**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## API Endpoints

### 1. Aadhaar Verification
```http
POST /api/v1/registration/aadhaar-verification
```

**Request Body:**
```json
{
  "aadhaar_number": "123456789012",
  "entrepreneur_name": "John Doe",
  "consent_given": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Aadhaar verification successful. OTP sent to registered mobile number.",
  "registration_id": 1,
  "otp_sent": true
}
```

### 2. OTP Validation
```http
POST /api/v1/registration/otp-validation
```

**Request Body:**
```json
{
  "registration_id": 1,
  "otp_code": "123456"
}
```

### 3. PAN Validation
```http
POST /api/v1/registration/pan-validation
```

**Request Body:**
```json
{
  "registration_id": 1,
  "pan_number": "ABCDE1234F",
  "pan_name": "John Doe",
  "date_of_incorporation": "2023-01-01",
  "organization_type": "proprietorship"
}
```

### 4. Get Registration
```http
GET /api/v1/registration/registration/{registration_id}
```

### 5. List Registrations
```http
GET /api/v1/registration/registrations?skip=0&limit=100
```

### 6. Health Check
```http
GET /api/v1/registration/health
```

## Database Schema

### Main Tables

1. **udyam_registrations**: Main registration records
2. **validation_logs**: Validation attempt logs
3. **otp_logs**: OTP generation and usage logs

### Key Fields

- `aadhaar_number`: 12-digit Aadhaar number (indexed)
- `pan_number`: 10-character PAN (indexed)
- `registration_number`: Auto-generated Udyam registration number
- `status`: Registration status (pending, verified, rejected, completed)
- `consent_given`: Aadhaar usage consent
- `ip_address`: Client IP for audit
- `user_agent`: Browser/client information

## Validation Rules

### Aadhaar Number
- Must be exactly 12 digits
- Only numeric characters allowed
- Duplicate check against existing registrations

### PAN Number
- Format: ABCDE1234F (5 letters + 4 digits + 1 letter)
- Case-insensitive input, stored in uppercase
- Duplicate check against existing registrations

### OTP
- 6-digit numeric code
- Expires after 10 minutes
- Single-use only

### Entrepreneur Name
- Minimum 2 characters
- Maximum 255 characters
- Only letters, spaces, and dots allowed

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `409`: Conflict (duplicate entries)
- `500`: Internal Server Error

Error responses include detailed messages:

```json
{
  "detail": "Aadhaar number must be exactly 12 digits"
}
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Production Deployment

### Environment Variables

Set these in production:

```env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=strong-secret-key
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Rate Limiting**: Implement rate limiting for OTP endpoints
3. **Input Sanitization**: All inputs are validated and sanitized
4. **Audit Logging**: All actions are logged with IP and user agent
5. **Database Security**: Use connection pooling and prepared statements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 