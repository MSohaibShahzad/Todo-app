"""Rate limiting middleware for API endpoints."""
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.config import settings

# Initialize SlowAPI limiter
# Use in-memory storage for test environment (when Redis is unavailable)
# Use Redis storage for development/production
try:
    # Try Redis first for distributed rate limiting
    from redis import Redis
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=1)
    redis_client.ping()  # Test connection
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=settings.redis_url,
        default_limits=[]  # No default limits - we'll apply per-endpoint
    )
except Exception:
    # Fall back to in-memory storage for tests
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[]  # No default limits - we'll apply per-endpoint
    )


def get_rate_limit_key(request):
    """Get rate limit key for authenticated users.

    Uses user ID if authenticated, otherwise falls back to IP address.
    """
    # Try to get user from request state (set by auth dependency)
    user = getattr(request.state, "user", None)
    if user:
        return f"user:{user.id}"
    return get_remote_address(request)


# Rate limit decorator for chat endpoints
# Usage: @limiter.limit("10/minute", key_func=get_rate_limit_key)
