# 📄 `INFRASTRUCTURE.md`

````markdown
# Infrastructure Setup

This guide explains how to set up the environment for local development and deployment.

---

## 🖥 Local Development

### Requirements
- Python 3.10+
- PostgreSQL
- Redis
- Docker & Docker Compose (recommended)

---

### Option A: Manual Setup
1. Install PostgreSQL & Redis
2. Create DB:
```sql
CREATE DATABASE auth_service;
````

3. Configure `.env`
4. Run migrations:

```bash
python manage.py migrate
```

5. Start server:

```bash
python manage.py runserver
```

---

### Option B: Docker Setup

Using Docker Compose:

```bash
docker-compose up --build
```

Services started:

* **app** – Django
* **db** – PostgreSQL
* **redis** – Redis

---

## 🚀 Deployment

### Railway

1. Create new project
2. Add **PostgreSQL** & **Redis** plugins
3. Deploy repo
4. Add environment variables:

   * `DATABASE_URL`
   * `REDIS_URL`
   * `SECRET_KEY`
   * `DEBUG`

### Render

1. Create new **Web Service**
2. Add **PostgreSQL** & **Redis** add-ons
3. Connect GitHub repo
4. Add environment variables
5. Deploy

---

## 🐳 Dockerfiles

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: "3.9"

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: auth_service
    ports:
      - "5432:5432"

  redis:
    image: redis:6
    ports:
      - "6379:6379"
```

```

---

✅ Now you’ll have **three clear docs** alongside your Django code:  

- **README.md** → How to use the repo  
- **IMPLEMENTATION.md** → Why & how it was built  
- **INFRASTRUCTURE.md** → Local & deploy setup  

---

Do you want me to now **regenerate the full repo ZIP** with these 3 docs, plus `Dockerfile`, `docker-compose.yml`, and test skeletons included?
```

