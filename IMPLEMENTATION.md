# Implementation Details

This document explains **how** the project was implemented and **why** specific choices were made.

---

## 1. Project Setup

- **Framework**: Django (batteries-included, robust ecosystem)
- **Database**: PostgreSQL (instead of default SQLite for production readiness)
- **Cache/Token store**: Redis (for password reset tokens and caching)
- **Authentication**: JWT (stateless, scalable, modern approach)
- **API Documentation**: Swagger/OpenAPI with drf-spectacular

---

## 2. User Model

- Extended Django's `AbstractUser` for full customization
- **Email as username**: `USERNAME_FIELD = "email"` (more modern than username)
- **Removed username field**: Completely replaced with email
- **Added `full_name` field**: Required for user identification
- **Custom UserManager**: Proper email normalization and validation

---

## 3. Registration

- **Serializer validation**: Email format, password strength, password confirmation
- **Email normalization**: All emails converted to lowercase
- **Password hashing**: Automatic secure hashing by Django
- **Unique email enforcement**: Database-level constraints

---

## 4. Login

- **JWT authentication**: Implemented using `djangorestframework-simplejwt`
- **Stateless sessions**: No server-side session storage required
- **Token rotation**: Refresh tokens can be rotated for security
- **Token blacklisting**: Support for logout functionality
- **Custom authentication**: Email/password instead of username/password

---

## 5. Password Reset Flow

1. **Request reset**: User provides email → token generated
2. **Token storage**: Token stored in **Redis** with configurable TTL (default: 1 hour)
3. **Email delivery**: Reset link sent to user's email (console backend in development)
4. **Password validation**: New password must meet strength requirements
5. **Token consumption**: Single-use tokens deleted after successful reset

### Why Redis?

- **Fast in-memory cache**: Sub-millisecond response times
- **TTL support**: Automatic token expiration after configured time
- **Scalable**: Handles high volumes of temporary data
- **Production-ready**: Used by major platforms for similar purposes

---

## 6. Security Features

- **Rate limiting**: Django Ratelimit on authentication endpoints
- **Password validation**: Django's built-in password validators
- **CORS configured**: Proper cross-origin request handling
- **HTTPS enforcement**: In production environments
- **Secure cookies**: When using session-based authentication

---

## 7. Deployment Configuration

- **Environment variables**: All configuration via environment variables
- **Database**: PostgreSQL with connection pooling
- **Redis**: For caching and token storage
- **Static files**: WhiteNoise for efficient static file serving
- **WSGI server**: Gunicorn for production deployment

### Environment Variables:

```env
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
8. Testing Strategy
Unit tests: Model methods, serializer validation

Integration tests: API endpoint testing

Authentication tests: Login/register flow verification

Password reset tests: Token generation and consumption

Database isolation: Test database with proper teardown

9. Bonus Features
Docker support: Complete containerization for development and production

Health endpoints: System status monitoring

API documentation: Interactive Swagger UI

Logging: Structured logging for debugging and monitoring

Custom middleware: Additional security headers

10. Technology Choices Rationale
Django REST Framework
Why: Mature, well-documented, extensive ecosystem

Benefits: Serializers, authentication, permissions, throttling

JWT Authentication
Why: Stateless, scalable, mobile-friendly

Benefits: No server-side session storage, easy to scale horizontally

PostgreSQL
Why: Production-ready, ACID compliant, JSON support

Benefits: Reliability, performance, advanced features

Redis
Why: High performance, TTL support, atomic operations

Benefits: Perfect for temporary data like password reset tokens

Docker
Why: Environment consistency, easy deployment

Benefits: Reproducible builds, simplified DevOps

11. Future Enhancements
Social authentication: OAuth2 with Google/GitHub

Email verification: Required for new registrations

Two-factor authentication: Additional security layer

API rate limiting: More sophisticated throttling

Monitoring: Performance metrics and error tracking

Background tasks: Async email sending with Celery