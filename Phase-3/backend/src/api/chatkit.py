"""ChatKit API endpoints."""
import secrets
from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response, StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from chatkit.server import StreamingResult

from src.auth.dependencies import get_current_user
from src.database import get_session
from src.services.chatkit_server import TaskManagementChatKitServer
from src.services.chatkit_store import SQLAlchemyStore

# Security scheme
security = HTTPBearer()

router = APIRouter(prefix="/chatkit", tags=["chatkit"])

# Initialize ChatKit server with store
store = SQLAlchemyStore()
chatkit_server = TaskManagementChatKitServer(data_store=store, attachment_store=None)


@router.post("/session")
async def create_session(
    user_id: str = Depends(get_current_user),
):
    """Create a new ChatKit session.

    This endpoint generates a client secret that the frontend uses
    to authenticate with the ChatKit server.

    Args:
        user_id: Authenticated user ID from JWT

    Returns:
        JSON with client_secret
    """
    # Generate a secure random token for this session
    # In a production app, you might want to:
    # 1. Store this in a database with expiration
    # 2. Associate it with the user_id
    # 3. Validate it on subsequent requests
    client_secret = secrets.token_urlsafe(32)

    return {
        "client_secret": client_secret,
        "user_id": user_id
    }


@router.post("")
async def chatkit_endpoint(
    request: Request,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """ChatKit protocol endpoint.

    This endpoint handles all ChatKit communication including:
    - Creating new threads (conversations)
    - Sending messages
    - Streaming AI responses

    Args:
        request: FastAPI request containing ChatKit protocol data
        user_id: Authenticated user ID from JWT
        session: Database session
        credentials: JWT token credentials

    Returns:
        StreamingResponse for SSE or JSON Response
    """
    try:
        print(f"[ChatKit] Request received from user: {user_id}")

        # Ensure user exists in database (auto-create if needed for Better Auth users)
        from src.models.user import User
        from sqlalchemy import select as sql_select
        from src.auth.jwt import verify_token

        user_result = await session.execute(
            sql_select(User).where(User.id == user_id)
        )
        existing_user = user_result.scalar_one_or_none()

        if not existing_user:
            # Extract email from JWT token payload
            token_payload = verify_token(credentials.credentials)
            email = token_payload.get("email", f"{user_id}@unknown.com")

            print(f"[ChatKit] Creating new user record for {user_id} with email {email}")
            new_user = User(
                id=user_id,
                email=email,  # Get from JWT token
                name="Better Auth User",  # Placeholder - managed by Better Auth
                hashed_password=""  # Empty string - password managed by Better Auth
            )
            session.add(new_user)
            await session.commit()
            print(f"[ChatKit] User {user_id} created successfully")

        # Read raw request body
        body = await request.body()
        print(f"[ChatKit] Request body length: {len(body)}")

        # Create context with user_id and database session
        context = {
            "user_id": user_id,
            "session": session
        }

        # Process the ChatKit request
        print(f"[ChatKit] Processing request...")
        result = await chatkit_server.process(body, context)
        print(f"[ChatKit] Request processed, result type: {type(result).__name__}")

        # Return appropriate response type
        if isinstance(result, StreamingResult):
            # Stream Server-Sent Events
            print(f"[ChatKit] Returning streaming response")
            return StreamingResponse(
                result,
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            # Return JSON response
            print(f"[ChatKit] Returning JSON response")
            return Response(
                content=result.json,
                media_type="application/json"
            )
    except Exception as e:
        print(f"[ChatKit] ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
