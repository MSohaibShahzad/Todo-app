"""FastAPI dependencies for authentication."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.jwt import verify_token

# HTTPBearer security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """Get current authenticated user ID from JWT token.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        User ID from token

    Raises:
        HTTPException: If token is invalid or missing user_id
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Try different possible user ID field names from Better-Auth
    user_id: str | None = None
    for field in ["userId", "user_id", "sub", "id"]:
        if field in payload:
            user_id = payload[field]
            # Ensure it's a string
            if not isinstance(user_id, str):
                user_id = str(user_id)
            break

    if user_id is None:
        print(f"[DEBUG] No user ID found in token payload. Available fields: {list(payload.keys())}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload - missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
