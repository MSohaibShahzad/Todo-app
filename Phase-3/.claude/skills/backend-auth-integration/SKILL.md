---
name: backend-auth-integration
description: Backend authentication integration for Python FastAPI applications using Better-Auth. Use this skill when integrating auth into Python backends, implementing session validation middleware, protecting API routes, verifying JWT tokens, handling authentication errors, managing user sessions from Python, or working with FastAPI dependencies for auth. Triggers when user asks to "integrate auth in FastAPI", "protect Python API endpoints", "validate Better-Auth sessions in Python", "verify JWT in FastAPI", "add auth middleware", or needs Python backend authentication.
---

# Backend Auth Integration (Python/FastAPI)

Complete toolkit for integrating Better-Auth authentication into Python FastAPI backends.

## Overview

This skill provides everything needed to implement authentication in Python FastAPI applications:
- **Session validation** via Better-Auth service HTTP calls
- **JWT token verification** for stateless authentication
- **FastAPI middleware** for automatic route protection
- **Dependency injection** patterns for auth requirements
- **Error handling** for authentication failures
- **CORS configuration** for cross-origin requests
- **Testing utilities** for auth-protected endpoints

## When to Use This Skill

Use this skill when users request:
- "Protect FastAPI endpoints with authentication"
- "Integrate Better-Auth with Python backend"
- "Validate sessions from Node.js auth service"
- "Verify JWT tokens in FastAPI"
- "Add auth middleware to Python API"
- "Get current user in FastAPI routes"
- "Handle authentication errors in Python"
- "Setup CORS for auth requests"

## Quick Start Workflow

### 1. Install Dependencies

```bash
pip install fastapi httpx pyjwt python-multipart
# or
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
httpx>=0.25.0
pyjwt>=2.8.0
python-multipart>=0.0.6
```

### 2. Configure Environment Variables

**.env:**
```bash
# Better-Auth service URL
AUTH_SERVICE_URL=http://localhost:3001

# JWT secret (must match auth service JWT_SECRET)
JWT_SECRET=your-jwt-secret-here

# CORS settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional: API settings
API_PORT=8000
```

### 3. Create Auth Utilities

**`app/auth.py`:**
```python
import os
import jwt
import httpx
from fastapi import HTTPException, Header, Cookie
from typing import Optional, Dict, Any

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:3001")
JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is required")


async def validate_session(cookie_header: str) -> Optional[Dict[str, Any]]:
    """
    Validate session via Node.js auth service.

    Args:
        cookie_header: Raw Cookie header string

    Returns:
        Session data dict with 'user' key, or None if invalid
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/auth/get-session",
                headers={"Cookie": cookie_header},
                timeout=5.0,
            )

            if response.status_code == 200:
                data = response.json()
                return data if data.get("user") else None

            return None

        except (httpx.RequestError, httpx.TimeoutException):
            return None


def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token issued by Better-Auth.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload, or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer="better-auth",
        )
        return payload
    except jwt.InvalidTokenError:
        return None


async def get_current_user_from_session(cookie: Optional[str] = Cookie(None)) -> Dict[str, Any]:
    """
    FastAPI dependency: Get current user from session cookie.

    Usage:
        @app.get("/api/protected")
        async def protected(user = Depends(get_current_user_from_session)):
            return {"user": user}
    """
    if not cookie:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = await validate_session(f"better-auth.session_token={cookie}")

    if not session or not session.get("user"):
        raise HTTPException(status_code=401, detail="Invalid session")

    return session["user"]


async def get_current_user_from_jwt(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency: Get current user from JWT token.

    Usage:
        @app.get("/api/protected")
        async def protected(user = Depends(get_current_user_from_jwt)):
            return {"user": user}
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")

    token = authorization[7:]  # Remove "Bearer " prefix
    payload = verify_jwt(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
```

## Core Workflows

### Session-Based Authentication

Use this approach when your frontend and backend share the same domain or use CORS with credentials.

**Protect Single Route:**
```python
from fastapi import FastAPI, Depends
from app.auth import get_current_user_from_session

app = FastAPI()

@app.get("/api/profile")
async def get_profile(user = Depends(get_current_user_from_session)):
    """
    Protected route - requires valid session cookie.
    Returns current user's profile.
    """
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        # Access custom fields if configured
        "role": user.get("role"),
        "tier": user.get("tier"),
    }
```

**Test with curl:**
```bash
# Get session cookie from browser or signup/signin
curl -X GET http://localhost:8000/api/profile \
  -H "Cookie: better-auth.session_token=<session-token>"
```

**Protect Multiple Routes:**
```python
from fastapi import APIRouter, Depends

# Create protected router
protected_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(get_current_user_from_session)],
)

@protected_router.get("/dashboard")
async def dashboard():
    """All routes in this router require authentication"""
    return {"message": "Dashboard data"}

@protected_router.get("/settings")
async def settings():
    return {"message": "Settings data"}

app.include_router(protected_router)
```

**Access User in Protected Routes:**
```python
@app.get("/api/personalized")
async def personalized_content(user = Depends(get_current_user_from_session)):
    # Use user data for personalization
    software_bg = user.get("softwareBackground", "Beginner")

    return {
        "message": f"Content tailored for {software_bg} level",
        "user": user["name"],
    }
```

### JWT-Based Authentication

Use this approach for stateless authentication or when frontend and backend are on different domains.

**Protect Routes with JWT:**
```python
from fastapi import FastAPI, Depends
from app.auth import get_current_user_from_jwt

app = FastAPI()

@app.get("/api/data")
async def get_data(user = Depends(get_current_user_from_jwt)):
    """
    Protected route - requires valid JWT token.
    """
    return {
        "data": "Secret data",
        "user_id": user["sub"],  # JWT subject claim
        "email": user["email"],
    }
```

**Test with curl:**
```bash
# First, get JWT from auth service (requires valid session)
curl -X GET http://localhost:3001/api/auth/jwt \
  -H "Cookie: better-auth.session_token=<session-token>"

# Use JWT in API calls
curl -X GET http://localhost:8000/api/data \
  -H "Authorization: Bearer <jwt-token>"
```

**Frontend Integration:**
```typescript
// React/Vue frontend
async function callProtectedAPI() {
  // Get JWT from auth service
  const jwtResponse = await fetch("http://localhost:3001/api/auth/jwt", {
    credentials: "include",
  });
  const { token } = await jwtResponse.json();

  // Call Python API with JWT
  const apiResponse = await fetch("http://localhost:8000/api/data", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return apiResponse.json();
}
```

### Custom Middleware for Global Auth

For applying authentication globally with granular control:

**`app/middleware/auth.py`:**
```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth import validate_session

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Global authentication middleware.
    Validates session for all routes except public paths.
    """

    def __init__(self, app, public_paths: list = None):
        super().__init__(app)
        self.public_paths = public_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        ]

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public paths
        if any(request.url.path.startswith(path) for path in self.public_paths):
            return await call_next(request)

        # Get cookie from request
        cookie_header = request.headers.get("cookie", "")

        if not cookie_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Not authenticated"}
            )

        # Validate session
        session = await validate_session(cookie_header)

        if not session or not session.get("user"):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid session"}
            )

        # Attach user to request state
        request.state.user = session["user"]

        return await call_next(request)


# In main.py
from fastapi import FastAPI
from app.middleware.auth import AuthMiddleware

app = FastAPI()

# Add auth middleware
app.add_middleware(
    AuthMiddleware,
    public_paths=["/", "/docs", "/health", "/api/public/*"],
)

# Access user in routes
@app.get("/api/protected")
async def protected(request: Request):
    user = request.state.user
    return {"user": user}
```

### Role-Based Access Control

Implement role-based permissions:

**`app/auth.py` (add to existing file):**
```python
from functools import wraps
from fastapi import HTTPException

def require_role(allowed_roles: list):
    """
    Decorator for role-based access control.

    Usage:
        @app.get("/admin")
        async def admin_route(user = Depends(get_current_user_from_session)):
            return await require_role(["admin"])(lambda: {"data": "admin data"})()
    """
    async def check_role(user: Dict[str, Any]):
        user_role = user.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access forbidden. Required roles: {allowed_roles}"
            )

        return user

    return check_role


# Or use as dependency
from fastapi import Depends

def require_admin(user = Depends(get_current_user_from_session)):
    """Dependency that requires admin role"""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@app.get("/admin/users")
async def list_users(user = Depends(require_admin)):
    """Admin-only route"""
    return {"users": []}
```

### CORS Configuration

Enable CORS for cross-origin auth requests:

**`main.py`:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ["http://localhost:3000", "http://localhost:5173"]
    allow_credentials=True,  # IMPORTANT for session cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**IMPORTANT:** When using session-based auth, you MUST:
1. Set `allow_credentials=True` in CORS middleware
2. Specify exact origins (cannot use `["*"]` with credentials)
3. Use `credentials: "include"` in frontend fetch requests

## Advanced Patterns

### Rate Limiting by User

```python
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends

# Simple in-memory rate limiter (use Redis in production)
user_requests = defaultdict(list)

async def rate_limit_user(user = Depends(get_current_user_from_session)):
    """Rate limit: 10 requests per minute per user"""
    user_id = user["id"]
    now = datetime.now()
    cutoff = now - timedelta(minutes=1)

    # Remove old requests
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if req_time > cutoff
    ]

    # Check limit
    if len(user_requests[user_id]) >= 10:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Record this request
    user_requests[user_id].append(now)

    return user


@app.get("/api/limited")
async def limited_endpoint(user = Depends(rate_limit_user)):
    return {"message": "Success"}
```

### Caching User Data

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache user data for 5 minutes
user_cache = {}

async def get_user_with_cache(user_id: str, cookie_header: str):
    """Get user with 5-minute cache"""
    cache_key = user_id

    if cache_key in user_cache:
        cached_user, cached_time = user_cache[cache_key]
        if datetime.now() - cached_time < timedelta(minutes=5):
            return cached_user

    # Fetch fresh data
    session = await validate_session(cookie_header)
    if session and session.get("user"):
        user_cache[cache_key] = (session["user"], datetime.now())
        return session["user"]

    return None
```

### Custom Fields Access

If your auth service has custom fields:

```python
@app.get("/api/personalized-content")
async def personalized(user = Depends(get_current_user_from_session)):
    # Access custom user fields
    software_bg = user.get("softwareBackground", "Beginner")
    hardware_bg = user.get("hardwareBackground", "Beginner")
    interest = user.get("interestArea", "General")

    # Personalize response based on user profile
    if software_bg == "Advanced" and interest == "Robotics":
        content_level = "advanced-robotics"
    elif software_bg == "Beginner":
        content_level = "beginner-friendly"
    else:
        content_level = "intermediate"

    return {
        "content_level": content_level,
        "recommendations": get_recommendations(interest, software_bg),
    }
```

## Testing Auth-Protected Endpoints

**Test script (`test_auth.py`):**
```python
import httpx
import os

AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:3001")
API_URL = os.getenv("API_URL", "http://localhost:8000")

async def test_protected_endpoint():
    """Test protected endpoint with session auth"""
    async with httpx.AsyncClient() as client:
        # 1. Sign in to get session
        signin_response = await client.post(
            f"{AUTH_URL}/api/auth/sign-in/email",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

        if signin_response.status_code != 200:
            print("Signin failed:", signin_response.text)
            return

        # Extract session cookie
        session_cookie = signin_response.cookies.get("better-auth.session_token")

        # 2. Call protected API endpoint
        api_response = await client.get(
            f"{API_URL}/api/profile",
            cookies={"better-auth.session_token": session_cookie},
        )

        print("Status:", api_response.status_code)
        print("Response:", api_response.json())


async def test_jwt_endpoint():
    """Test protected endpoint with JWT"""
    async with httpx.AsyncClient() as client:
        # 1. Sign in and get JWT
        signin_response = await client.post(
            f"{AUTH_URL}/api/auth/sign-in/email",
            json={
                "email": "test@example.com",
                "password": "TestPassword123!",
            },
        )

        session_cookie = signin_response.cookies.get("better-auth.session_token")

        # Get JWT
        jwt_response = await client.get(
            f"{AUTH_URL}/api/auth/jwt",
            cookies={"better-auth.session_token": session_cookie},
        )

        jwt_token = jwt_response.json()["token"]

        # 2. Call API with JWT
        api_response = await client.get(
            f"{API_URL}/api/data",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )

        print("Status:", api_response.status_code)
        print("Response:", api_response.json())


if __name__ == "__main__":
    import asyncio

    print("Testing session-based auth...")
    asyncio.run(test_protected_endpoint())

    print("\nTesting JWT-based auth...")
    asyncio.run(test_jwt_endpoint())
```

**Run tests:**
```bash
python test_auth.py
```

## Decision Tree: Choosing Auth Approach

```
What type of authentication?
├─ Session-based (cookies)
│   ├─ Use when frontend and backend share domain
│   ├─ Use when using CORS with credentials
│   ├─ Dependency: get_current_user_from_session
│   └─ CORS: allow_credentials=True
│
└─ JWT-based (stateless)
    ├─ Use when frontend and backend are on different domains
    ├─ Use for microservices or third-party API access
    ├─ Dependency: get_current_user_from_jwt
    └─ No special CORS requirements

Global or per-route protection?
├─ Global → Use middleware (AuthMiddleware)
└─ Per-route → Use dependencies (Depends)

Need role-based access?
├─ YES → Use require_role or require_admin
└─ NO → Use basic get_current_user_*

Multiple routes to protect?
├─ YES → Group in APIRouter with dependencies
└─ NO → Use Depends on individual routes
```

## Common Use Cases

### E-Learning Platform (like Physical AI Book)

Personalized content based on user background:

```python
from fastapi import FastAPI, Depends
from app.auth import get_current_user_from_session

app = FastAPI()

@app.get("/api/chapters/{chapter_id}/personalize")
async def personalize_chapter(
    chapter_id: str,
    user = Depends(get_current_user_from_session)
):
    """Personalize chapter content based on user's background"""
    software_bg = user.get("softwareBackground", "Beginner")
    hardware_bg = user.get("hardwareBackground", "Beginner")
    interest = user.get("interestArea", "General")

    # Fetch and personalize chapter
    chapter = get_chapter(chapter_id)
    personalized = personalize_content(
        chapter,
        software_level=software_bg,
        hardware_level=hardware_bg,
        interest_area=interest,
    )

    return personalized
```

### SaaS Application

Tier-based feature access:

```python
@app.get("/api/premium-feature")
async def premium_feature(user = Depends(get_current_user_from_session)):
    """Premium feature - requires paid tier"""
    tier = user.get("tier", "free")

    if tier not in ["premium", "enterprise"]:
        raise HTTPException(
            status_code=403,
            detail="This feature requires a Premium subscription"
        )

    return {"feature_data": "Premium content"}
```

Admin dashboard:

```python
@app.get("/api/admin/analytics")
async def admin_analytics(user = Depends(get_current_user_from_session)):
    """Admin-only analytics dashboard"""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {
        "total_users": count_users(),
        "active_sessions": count_active_sessions(),
        "revenue": calculate_revenue(),
    }
```

## Troubleshooting

**Session validation fails:**
- Verify AUTH_SERVICE_URL points to running auth service
- Check auth service is accessible from Python backend
- Ensure cookie name is `better-auth.session_token`
- Verify CORS allows credentials

**JWT verification fails:**
- Ensure JWT_SECRET matches auth service exactly
- Check token hasn't expired (default: 7 days)
- Verify issuer is "better-auth"
- Check algorithm is HS256

**CORS errors:**
- Set `allow_credentials=True` for session auth
- Cannot use `allow_origins=["*"]` with credentials
- Specify exact allowed origins
- Check frontend uses `credentials: "include"`

**User data not available:**
- Check custom fields are configured in auth service
- Verify fields are passed during signup
- Ensure session is fresh (not stale)

## Security Best Practices

1. **Environment Variables**: Never hardcode JWT_SECRET or other secrets
2. **HTTPS in Production**: Use HTTPS for all auth endpoints
3. **CORS Configuration**: Only allow trusted origins
4. **Token Expiration**: Respect JWT expiration times
5. **Error Messages**: Don't reveal user existence in error messages
6. **Rate Limiting**: Implement rate limiting on auth-protected endpoints
7. **Logging**: Log authentication failures for security monitoring
8. **Input Validation**: Validate all user inputs on protected endpoints

## Resources

### Official Documentation
- FastAPI Security Docs: https://fastapi.tiangolo.com/tutorial/security/
- PyJWT Documentation: https://pyjwt.readthedocs.io/

### Related Skills
- `better-auth` - Auth service setup
- `frontend-auth-integration` - React/Vue integration
