FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Don't use EXPOSE - Render handles ports automatically
# EXPOSE 8000  # ❌ Remove this line

# Use $PORT environment variable provided by Render
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:$PORT"]