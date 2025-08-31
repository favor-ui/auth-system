import os
import logging
from django.http import JsonResponse
from django.db import connections
from django.conf import settings
from django.utils import timezone
import redis
from django.core.cache import cache

logger = logging.getLogger(__name__)

def check_db():
    """Check database connectivity"""
    try:
        conn = connections['default']
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

def check_redis():
    """Check Redis connectivity"""
    try:
        # Use REDIS_URL from settings or environment, with fallback
        redis_url = getattr(settings, 'REDIS_URL', os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
        r = redis.from_url(redis_url, socket_timeout=1, socket_connect_timeout=1)
        r.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False

def check_cache():
    """Check Django cache functionality"""
    try:
        test_key = "healthcheck_test"
        cache.set(test_key, "ok", timeout=5)  # Increased timeout slightly
        result = cache.get(test_key)
        return result == "ok"
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        return False

def check_email_config():
    """Check if email is configured"""
    try:
        # Check if email backend is configured and settings exist
        email_backend = getattr(settings, 'EMAIL_BACKEND', '')
        has_smtp_config = (email_backend == 'django.core.mail.backends.smtp.EmailBackend' and
                          hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST and
                          hasattr(settings, 'DEFAULT_FROM_EMAIL') and settings.DEFAULT_FROM_EMAIL)
        return has_smtp_config
    except Exception as e:
        logger.error(f"Email config check failed: {e}")
        return False

def run_healthcheck() -> dict:
    """
    Check database, cache, and external services health.
    Returns {"database": "ok"/"error", "cache": "ok"/"error", ...}
    """
    checks = {
        'database': check_db(),
        'cache': check_cache(),
        'redis': check_redis(),
        'email_configured': check_email_config(),
    }
    
    # Convert boolean values to string status for better readability
    status_checks = {}
    for key, value in checks.items():
        if key in ['redis', 'email_configured']:
            # For optional services, provide more descriptive status
            if value:
                status_checks[key] = 'ok'
            else:
                status_checks[key] = 'not_configured'
        else:
            # For critical services, use ok/error
            status_checks[key] = 'ok' if value else 'error'
    
    return status_checks

def health(request):
    """Comprehensive health check endpoint"""
    checks = run_healthcheck()
    
    # Determine overall status - only database and cache are critical
    critical_services_ok = checks.get('database') == 'ok' and checks.get('cache') == 'ok'
    status = 'ok' if critical_services_ok else 'degraded'
    
    # Log the health check result
    if critical_services_ok:
        logger.info(f"Health check passed: {checks}")
    else:
        logger.warning(f"Health check failed: {checks}")
    
    response_data = {
        'status': status,
        'services': checks,
        'timestamp': timezone.now().isoformat(),
        'version': getattr(settings, 'VERSION', 'unknown'),
    }
    
    return JsonResponse(response_data, status=200 if critical_services_ok else 503)