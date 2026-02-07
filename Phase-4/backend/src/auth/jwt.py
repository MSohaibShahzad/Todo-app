"""JWT token creation and verification."""
from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from src.config import settings


def create_access_token(data: dict[str, Any]) -> str:
    """Create JWT access token.

    Args:
        data: Dictionary of claims to encode in token

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> dict[str, Any] | None:
    """Verify and decode JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        print(f"[DEBUG] Token verified successfully. Payload: {payload}")
        return payload
    except JWTError as e:
        print(f"[DEBUG] Token verification failed: {e}")
        print(f"[DEBUG] Token (first 50 chars): {token[:50]}...")
        return None
