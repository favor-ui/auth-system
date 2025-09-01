# Infrastructure Setup

This guide explains how to set up the environment for local development and cloud deployment.

---

## 🖥 Local Development

### Requirements

- Python 3.11+
- Docker & Docker Compose (recommended)
- PostgreSQL (via Docker)
- Redis (via Docker)

---

## 🐳 Docker Setup (Recommended)

### 1. Start All Services with Docker Compose

```bash
# Start all services (PostgreSQL, Redis, and Django app)
docker-compose up --build

# Or run in background
docker-compose up -d --build
2. Run Migrations and Create Superuser
bash
# Run migrations in the correct order
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py migrate auth
docker-compose exec web python manage.py migrate users
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
3. Access Services
Django App: http://localhost:8000

PostgreSQL: localhost:5432

Redis: localhost:6379

Admin Interface: http://localhost:8000/admin

📋 Docker Compose Configuration
docker-compose.yml
yaml
version: "3.9"

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    environment:
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: auth_service
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
.env File for Docker
env
DEBUG=True
SECRET_KEY=your-local-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=auth_service
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# JWT Settings
ACCESS_TOKEN_LIFETIME_MIN=30
REFRESH_TOKEN_LIFETIME_DAYS=7
🚀 Cloud Deployment
Railway Deployment
Create new project on Railway

Add PostgreSQL plugin from marketplace

Add Redis plugin from marketplace

Connect GitHub repository

Add environment variables:

SECRET_KEY (generate a secure one)

DEBUG=False

ALLOWED_HOSTS=your-app.railway.app

Automatic deploys on push to main

Render Deployment
Create Web Service on Render

Add PostgreSQL database add-on

Add Redis add-on

Connect GitHub repository

Configure environment variables:

env
DEBUG=False
SECRET_KEY=your-render-secret-key
ALLOWED_HOSTS=your-app.onrender.com
Set build command: ./build.sh

Set start command: gunicorn auth_service.wsgi:application --bind 0.0.0.0:$PORT

render.yaml for Render
yaml
services:
  - type: web
    name: auth-service
    plan: free
    runtime: python
    buildCommand: ./build.sh
    startCommand: gunicorn auth_service.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: auth-postgres
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: auth-redis
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"

databases:
  - name: auth-postgres
    plan: free
    databaseName: auth_service
    user: auth_service

  - type: redis
    name: auth-redis
    plan: free
    maxmemoryPolicy: allkeys-lfu
🔧 Manual Local Setup (Without Docker)
1. Install Dependencies
bash
# Install PostgreSQL (macOS)
brew install postgresql redis

# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib redis-server

# Start services
brew services start postgresql
brew services start redis

# Or on Ubuntu
sudo service postgresql start
sudo service redis-server start
2. Create Database
sql
CREATE DATABASE auth_service;
CREATE USER auth_user WITH PASSWORD 'auth_password';
GRANT ALL PRIVILEGES ON DATABASE auth_service TO auth_user;
3. Python Setup
bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
4. Environment Configuration
env
DEBUG=True
SECRET_KEY=your-local-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_service
DB_USER=postgres
DB_PASSWORD=postgres

# Redis
REDIS_URL=redis://localhost:6379/0
5. Run Application
bash
python manage.py migrate
python manage.py runserver
📊 Service Connections
Local Development:
PostgreSQL: localhost:5432 or db:5432 (Docker)

Redis: localhost:6379 or redis:6379 (Docker)

Django App: localhost:8000

Production (Cloud):
PostgreSQL: Provided via DATABASE_URL

Redis: Provided via REDIS_URL

Django App: Your custom domain or .railway.app/.onrender.com

🛠 Troubleshooting
Common Issues:
Database Connection Refused
bash
# Check if PostgreSQL is running
ps aux | grep postgres

# Check if Redis is running
redis-cli ping
Migration Errors
bash
# Reset and reapply migrations
python manage.py migrate users zero
python manage.py migrate auth zero
python manage.py migrate contenttypes zero
python manage.py makemigrations users
python manage.py migrate
Docker Port Conflicts
bash
# Stop existing services
docker-compose down

# Check for running containers
docker ps

# Remove conflicting containers
docker rm -f container_name
Container Management:
bash
# View logs
docker-compose logs
docker-compose logs web
docker-compose logs db
docker-compose logs redis

# Restart specific service
docker-compose restart web

# Rebuild and restart
docker-compose up -d --build

# Stop all services
docker-compose down
📝 Environment Variables Reference
Required for Production:
env
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
Optional:
env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
FRONTEND_URL=https://your-frontend.com
