import os
import secrets
import logging
import redis
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

# ----------------------
# Password reset tokens
# ----------------------
RESET_PREFIX = "pwdreset:"
RESET_TTL = int(os.getenv("RESET_TOKEN_TTL_SECONDS", 600))  # 10 minutes

# Redis connection (if available)
_redis_client = None

def get_redis_client():
    """Get Redis client with connection pooling and error handling"""
    global _redis_client
    if _redis_client is None:
        try:
            redis_url = getattr(settings, 'REDIS_URL', None)
            if redis_url:
                _redis_client = redis.from_url(redis_url, socket_timeout=1, socket_connect_timeout=1)
                # Test connection
                _redis_client.ping()
                logger.info("Redis connection established successfully")
            else:
                logger.info("Redis URL not configured, using Django cache")
        except (redis.ConnectionError, ImproperlyConfigured) as e:
            logger.warning(f"Redis connection failed: {e}. Falling back to Django cache")
            _redis_client = None
    return _redis_client

def generate_reset_token(email: str) -> str:
    """Create a password reset token and store in cache/redis; failsafe."""
    token = secrets.token_urlsafe(32)
    key = f"{RESET_PREFIX}{token}"
    
    try:
        redis_client = get_redis_client()
        if redis_client:
            # Use Redis if available
            redis_client.setex(key, RESET_TTL, email)
        else:
            # Fallback to Django cache
            cache.set(key, email, timeout=RESET_TTL)
            
        logger.info(f"Reset token generated for: {email}")
        return token
        
    except Exception as e:
        logger.error(f"Failed to store reset token for {email}: {e}")
        # Still return token even if storage fails (for graceful degradation)
        return token

def consume_reset_token(token: str) -> str | None:
    """Retrieve and delete a password reset token; safe fallback."""
    key = f"{RESET_PREFIX}{token}"
    
    try:
        redis_client = get_redis_client()
        if redis_client:
            # Use Redis if available
            email = redis_client.get(key)
            if email:
                redis_client.delete(key)
                return email.decode('utf-8') if isinstance(email, bytes) else email
        else:
            # Fallback to Django cache
            email = cache.get(key)
            if email:
                cache.delete(key)
                return email
                
        return None
        
    except Exception as e:
        logger.error(f"Failed to consume reset token: {e}")
        return None

def validate_reset_token(token: str) -> bool:
    """Check if a reset token exists without consuming it."""
    key = f"{RESET_PREFIX}{token}"
    
    try:
        redis_client = get_redis_client()
        if redis_client:
            return redis_client.exists(key) == 1
        else:
            return cache.get(key) is not None
            
    except Exception as e:
        logger.error(f"Failed to validate reset token: {e}")
        return False

# ----------------------
# JWT Token Utilities
# ----------------------
def add_token_to_blacklist(token):
    """Add JWT token to blacklist (for logout functionality)"""
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        
        # Extract token type and determine expiry
        refresh = RefreshToken(token)
        expiry = refresh.access_token.payload['exp'] - refresh.current_time
        
        key = f"token_blacklist:{token}"
        
        redis_client = get_redis_client()
        if redis_client:
            redis_client.setex(key, int(expiry), "blacklisted")
        else:
            cache.set(key, "blacklisted", timeout=int(expiry))
            
    except Exception as e:
        logger.error(f"Failed to blacklist token: {e}")

def is_token_blacklisted(token):
    """Check if a JWT token is blacklisted"""
    key = f"token_blacklist:{token}"
    
    try:
        redis_client = get_redis_client()
        if redis_client:
            return redis_client.exists(key) == 1
        else:
            return cache.get(key) is not None
            
    except Exception as e:
        logger.error(f"Failed to check token blacklist: {e}")
        return False

# ----------------------
# Rate Limiting Utilities
# ----------------------
def check_rate_limit(key: str, limit: int, period: int) -> bool:
    """Check if rate limit is exceeded for a given key"""
    try:
        current_count = 0
        
        redis_client = get_redis_client()
        if redis_client:
            current_count = redis_client.incr(key)
            if current_count == 1:  # First request, set expiry
                redis_client.expire(key, period)
        else:
            current_count = cache.get(key, 0) + 1
            cache.set(key, current_count, timeout=period)
            
        return current_count <= limit
        
    except Exception as e:
        logger.error(f"Rate limit check failed for key {key}: {e}")
        return True  # Fail open - don't block requests if rate limiting fails