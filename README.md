# Django Authentication Service

A complete JWT authentication system with PostgreSQL and Redis.

## 🚀 Features

- User registration with email, password, and full name
- JWT authentication (access and refresh tokens)
- Password reset with Redis token storage
- PostgreSQL database for data persistence
- Rate limiting on authentication endpoints
- API documentation with Swagger/OpenAPI
- Health check endpoints
- Docker support for development

## 🛠️ Quick Start

### Prerequisites

- Python 3.11+
- Docker
- PostgreSQL (via Docker)
- Redis (via Docker)

### 1. Clone and Setup

```bash
git clone <your-repository>
cd auth_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Start Database and Redis
bash
# Start PostgreSQL container
docker run --name auth-postgres \
  -e POSTGRES_DB=auth_service \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15

# Start Redis container
docker run --name auth-redis \
  -p 6379:6379 \
  -d redis:7-alpine
3. Environment Configuration
Create .env file:

env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_service
DB_USER=postgres
DB_PASSWORD=postgres

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Settings
ACCESS_TOKEN_LIFETIME_MIN=30
REFRESH_TOKEN_LIFETIME_DAYS=7

# Email (optional)
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL=webmaster@localhost
FRONTEND_URL=http://localhost:3000
4. Database Setup - IMPORTANT MIGRATION STEPS
Critical: Follow these steps in order to avoid migration errors:

bash
# 1. First create migrations for the users app
python manage.py makemigrations users

# 2. Apply auth migrations first (required dependency)
python manage.py migrate auth

# 3. Apply users migrations
python manage.py migrate users

# 4. Apply all remaining migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser
5. Start Server
bash
python manage.py runserver
📋 API Endpoints
Authentication Endpoints
POST /api/auth/register/ - Register new user

POST /api/auth/login/ - Login and get JWT tokens

POST /api/auth/forgot-password/ - Request password reset

POST /api/auth/reset-password/ - Confirm password reset

GET /api/auth/me/ - Get current user profile

Utility Endpoints
GET /health/ - Health check status

GET /api/docs/ - API documentation (Swagger)

GET /admin/ - Django admin interface

🐳 Docker Compose Alternative
bash
# Start all services
docker-compose up

# Run migrations (follow the same order as above)
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py migrate auth
docker-compose exec web python manage.py migrate users
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
🧪 Testing
bash
# Run all tests
pytest

# Run specific test file
pytest users/tests/test_auth_api.py -v

# Run with coverage
pytest --cov=.
🔧 Environment Configuration
Required Environment Variables
env
# Core Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_service
DB_USER=postgres
DB_PASSWORD=postgres

# Redis
REDIS_URL=redis://localhost:6379/0
Optional Environment Variables
env
# JWT Settings
ACCESS_TOKEN_LIFETIME_MIN=30
REFRESH_TOKEN_LIFETIME_DAYS=7

# Email Settings
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL=webmaster@localhost

# Frontend
FRONTEND_URL=http://localhost:3000
📖 API Documentation
Interactive API documentation is available at:

Swagger UI - Interactive API explorer

ReDoc - Beautiful API documentation

🚀 Deployment
Railway Deployment
Connect GitHub repository to Railway

Set environment variables in dashboard

Automatic deploys on push to main

Render Deployment
Create Web Service on Render

Connect repository

Set build command: pip install -r requirements.txt

Set start command: gunicorn --bind 0.0.0.0:$PORT auth_service.wsgi:application

Configure environment variables

📁 Project Structure
text
auth_service/
├── auth_service/           # Django project
│   ├── __init__.py
│   ├── settings.py        # Application settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py
│   └── health.py         # Health check endpoints
├── users/                 # Authentication app
│   ├── __init__.py
│   ├── admin.py          # Django admin config
│   ├── apps.py
│   ├── models.py         # User model
│   ├── serializers.py    # Request/response serializers
│   ├── urls.py           # App URL routes
│   ├── utils.py          # Password reset utilities
│   ├── views.py          # API endpoints
│   └── tests/            # Test cases
├── docker-compose.yml    # Multi-container setup
├── Dockerfile           # Application container
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
├── INFRASTRUCTURE.md    # Infrastructure setup guide
└── README.md           # This file
🔐 Authentication Flow
Registration: User provides email, password, and full name

Login: User authenticates with email/password, receives JWT tokens

Password Reset:

User requests reset → Token generated and stored in Redis

User receives token → Submits token with new password

Token validated → Password updated → Token deleted from Redis

🆘 Troubleshooting
Common Issues
Database connection failed: Ensure PostgreSQL container is running

Redis connection failed: Check Redis container status

Migration errors: Follow the exact migration order above

Migration Troubleshooting
If you encounter migration issues:

bash
# Reset and start fresh (WARNING: deletes all data)
python manage.py migrate users zero
python manage.py migrate auth zero
python manage.py migrate contenttypes zero

# Then follow the migration steps in order:
python manage.py makemigrations users
python manage.py migrate auth
python manage.py migrate users
python manage.py migrate
Container Management
bash
# Check container status
docker ps

# View container logs
docker logs auth-postgres
docker logs auth-redis

# Restart containers
docker restart auth-postgres auth-redis
📝 License
This project is part of the Bill Station internship program.

🤝 Support
For assistance, ensure:

Docker containers are running (docker ps)

Environment variables are properly set

Database migrations are applied in the correct order

Follow the migration steps exactly as specified above

Refer to INFRASTRUCTURE.md for detailed setup instructions