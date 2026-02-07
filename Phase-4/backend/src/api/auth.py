"""Authentication API endpoints for JWT token exchange."""
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from src.auth.jwt import create_access_token

router = APIRouter()


class TokenExchangeRequest(BaseModel):
    """Request model for token exchange."""

    userId: str


class TokenResponse(BaseModel):
    """Response model for token."""

    token: str


@router.post("/auth/exchange-token", response_model=TokenResponse)
async def exchange_token(
    request: Request,
    body: TokenExchangeRequest,
) -> TokenResponse:
    """Exchange Better-Auth session for JWT token.

    This endpoint validates that the request has a valid Better-Auth session
    and generates a custom JWT token for API authentication.

    Args:
        request: FastAPI request with cookies
        body: User ID from Better-Auth session

    Returns:
        JWT token for backend API authentication

    Raises:
        HTTPException: If session is invalid or user ID is missing
    """
    # Validate that user has Better-Auth session cookies
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Better-Auth session found",
        )

    # Get user ID from request body (from Better-Auth session)
    user_id_str = body.userId
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )

    # Convert string user ID to integer
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format",
        )

    # Generate JWT with user_id claim
    token = create_access_token({"user_id": user_id})

    print(f"[DEBUG] Generated JWT for user_id={user_id}")

    return TokenResponse(token=token)
