# 📄 `IMPLEMENTATION.md`

```markdown
# Implementation Details

This document explains **how** the project was implemented and **why** specific choices were made.

---

## 1. Project Setup
- Framework: **Django**
- Database: **PostgreSQL** (instead of default SQLite for production readiness)
- Cache/Token store: **Redis** (for password reset tokens)
- Authentication: **JWT** (stateless, scalable)

---

## 2. User Model
- Extended Django’s `AbstractUser`
- Email used as username (`USERNAME_FIELD = "email"`)
- Added `full_name` field

---

## 3. Registration
- Users provide `full_name`, `email`, and `password`
- Passwords are hashed automatically by Django

---

## 4. Login
- JWT authentication implemented using `djangorestframework-simplejwt`
- Only registered users can log in
- Access + Refresh tokens issued

---

## 5. Forgot Password
- User requests reset → Generate token
- Token stored in **Redis** with 10 min expiry
- User submits token + new password to reset

Why Redis?
- Fast in-memory cache
- Supports TTL (time-to-live) for auto-expiry
- Prevents storing temporary tokens in DB

---

## 6. Deployment
- Configured environment variables:
  - `DATABASE_URL`
  - `REDIS_URL`
  - `SECRET_KEY`
  - `DEBUG`
- Compatible with Railway / Render free-tier services

---

## 7. Bonus Features
- **Docker Support**: Easy local setup
- **Unit Tests**: Cover registration, login, password reset
- **Rate Limiting** (optional): Could use DRF throttling or Redis-based limiter
````

---