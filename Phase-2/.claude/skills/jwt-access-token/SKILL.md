---
name: jwt-access-token
description: Solve the "user logged in but backend doesn't know" problem. Use this skill when frontend users are successfully authenticated but backend API returns 401 unauthorized, JWT tokens are not being sent to backend, or you need to implement the frontend-to-backend JWT flow. Triggers when user says "backend not getting JWT tokens", "user logged in but API says unauthorized", "how to send JWT to backend", or needs to fix authentication between frontend and backend.
---

# JWT Access Token Flow

Fix the common problem: **"User is logged in (has session cookie) but backend API doesn't recognize them"**

## The Problem

When you have this architecture:

```
Frontend (React/Vue)  →  Auth Service (Node.js)  →  Backend API (Python/FastAPI)
    ↓                         ↓                            ↓
User signs in          Session cookie set         Needs JWT token!
```

**What happens:**
1. ✅ User signs in successfully
2. ✅ Frontend has session cookie (`better-auth.session_token`)
3. ❌ Frontend calls backend API
4. ❌ Backend returns **401 Unauthorized** - "Backend doesn't know user is logged in!"

**Why this happens:**
- Session cookies only work with the auth service (port 3001)
- Backend API (port 8000) needs a **JWT token** in the `Authorization` header
- Frontend is not sending the JWT token!

## The Solution: JWT Access Token Flow

### Step 1: Frontend - Get JWT Token from Auth Service

**`lib/auth-client.ts`:**
```typescript
/**
 * Get JWT token from auth service using the current session cookie
 * This token is required for authenticated API requests to the backend
 */
export async function getJWTToken(): Promise<string | null> {
  try {
    console.log('[Auth] Fetching JWT token from auth service');

    const response = await fetch('http://localhost:3001/api/auth/jwt', {
      method: 'GET',
      credentials: 'include', // IMPORTANT: Send session cookie
    });

    if (!response.ok) {
      console.error('[Auth] Failed to get JWT token:', response.status);
      return null;
    }

    const data = await response.json();
    console.log('[Auth] JWT token received');
    return data.token || null;
  } catch (error) {
    console.error('[Auth] Error getting JWT token:', error);
    return null;
  }
}
```

**What this does:**
1. Calls auth service `/api/auth/jwt` endpoint
2. Sends session cookie automatically (via `credentials: 'include'`)
3. Auth service validates session and returns JWT token
4. Frontend stores token temporarily (in memory, not localStorage!)

### Step 2: Frontend - Send JWT to Backend API

**Pattern 1: Per-Request (Recommended)**
```typescript
import { getJWTToken } from './lib/auth-client';

async function callProtectedAPI() {
  // Get JWT token
  const token = await getJWTToken();

  if (!token) {
    // User not authenticated
    console.error('No JWT token - user not logged in');
    window.location.href = '/signin';
    return;
  }

  // Call backend API with JWT
  const response = await fetch('http://localhost:8000/api/personalize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // CRITICAL: Add JWT here!
    },
    body: JSON.stringify({ chapter_id: 'ch1' }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      console.error('JWT token invalid or expired');
      // Redirect to login
    }
    throw new Error('API call failed');
  }

  return response.json();
}
```

**Pattern 2: Helper Function (Reusable)**
```typescript
// lib/apiClient.ts
import { getJWTToken } from './auth-client';

export async function makeAuthenticatedRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get JWT token
  const token = await getJWTToken();

  if (!token) {
    throw new Error('Please sign in to continue');
  }

  // Add Authorization header
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    ...options.headers,
  };

  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers,
    credentials: 'include', // Also send cookies
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Token expired or invalid
      window.location.href = '/signin';
    }
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// Usage
const result = await makeAuthenticatedRequest('/api/personalize', {
  method: 'POST',
  body: JSON.stringify({ chapter_id: 'ch1' }),
});
```

### Step 3: Backend - Verify JWT Token

Your Python backend already has this (from `backend-auth-integration` skill):

**`middleware/jwt_auth.py`:**
```python
import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract Authorization header
        auth_header = request.headers.get("authorization", "")

        user = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix
            user = verify_jwt_token(token)

        # Attach user to request
        request.state.user = user

        return await call_next(request)

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer="auth-service",
            audience="api-service",
        )
        return payload
    except jwt.InvalidTokenError:
        return None
```

**Access user in routes:**
```python
from fastapi import Request

@app.post("/api/personalize")
async def personalize(request: Request):
    user = request.state.user

    if not user:
        return {"error": "Unauthorized"}, 401

    # User is authenticated!
    print(f"User: {user['email']}")
    print(f"Background: {user['softwareBackground']}")

    return {"personalized_content": "..."}
```

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER SIGNS IN                                            │
└─────────────────────────────────────────────────────────────┘
   Frontend calls: POST /api/auth/sign-in/email
                        ↓
   Auth Service validates credentials
                        ↓
   Sets session cookie: better-auth.session_token
                        ↓
   ✅ User is logged in!

┌─────────────────────────────────────────────────────────────┐
│ 2. FRONTEND NEEDS TO CALL BACKEND API                       │
└─────────────────────────────────────────────────────────────┘
   Frontend calls: getJWTToken()
                        ↓
   GET http://localhost:3001/api/auth/jwt
   (sends session cookie automatically)
                        ↓
   Auth Service validates session
                        ↓
   Returns: { token: "eyJhbGc..." }
                        ↓
   Frontend stores JWT in memory

┌─────────────────────────────────────────────────────────────┐
│ 3. FRONTEND CALLS BACKEND WITH JWT                          │
└─────────────────────────────────────────────────────────────┘
   Frontend calls: POST /api/personalize
   Headers: { Authorization: "Bearer eyJhbGc..." }
                        ↓
   Backend middleware extracts JWT
                        ↓
   Backend verifies JWT signature
                        ↓
   Backend attaches user to request.state.user
                        ↓
   ✅ Backend knows user is authenticated!
                        ↓
   Route handler accesses user data
                        ↓
   Returns personalized response
```

## Common Mistakes and Fixes

### Mistake 1: Not Sending JWT to Backend

**Wrong:**
```typescript
// ❌ Backend won't know user is logged in!
fetch('http://localhost:8000/api/personalize', {
  method: 'POST',
  body: JSON.stringify({ chapter_id: 'ch1' }),
});
```

**Right:**
```typescript
// ✅ Backend receives JWT and knows user
const token = await getJWTToken();
fetch('http://localhost:8000/api/personalize', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`, // Add JWT!
  },
  body: JSON.stringify({ chapter_id: 'ch1' }),
});
```

### Mistake 2: Storing JWT in localStorage

**Wrong:**
```typescript
// ❌ Security risk! XSS attacks can steal token
const token = await getJWTToken();
localStorage.setItem('jwt', token);
```

**Right:**
```typescript
// ✅ Get fresh JWT for each API call
const token = await getJWTToken();
// Use immediately, don't store
```

### Mistake 3: Not Handling Token Expiration

**Wrong:**
```typescript
// ❌ Token might be expired
const token = await getJWTToken();
// Use token hours later
```

**Right:**
```typescript
// ✅ Get fresh token before each API call
async function callAPI() {
  const token = await getJWTToken(); // Fresh token!
  // Use immediately
}
```

### Mistake 4: Missing credentials: 'include'

**Wrong:**
```typescript
// ❌ Session cookie not sent to auth service
fetch('http://localhost:3001/api/auth/jwt', {
  method: 'GET',
});
```

**Right:**
```typescript
// ✅ Session cookie sent, JWT returned
fetch('http://localhost:3001/api/auth/jwt', {
  method: 'GET',
  credentials: 'include', // Send cookies!
});
```

### Mistake 5: Wrong Authorization Header Format

**Wrong:**
```typescript
// ❌ Missing "Bearer " prefix
headers: {
  'Authorization': token
}
```

**Right:**
```typescript
// ✅ Correct format
headers: {
  'Authorization': `Bearer ${token}`
}
```

## Quick Reference

### Frontend Checklist

- [ ] Created `getJWTToken()` function
- [ ] Calls `/api/auth/jwt` with `credentials: 'include'`
- [ ] Gets fresh JWT before each API call
- [ ] Adds `Authorization: Bearer ${token}` header
- [ ] Handles token fetch failures (redirect to login)
- [ ] Handles API 401 responses (token expired)

### Backend Checklist

- [ ] JWT middleware installed and configured
- [ ] JWT_SECRET matches auth service
- [ ] Middleware extracts `Authorization` header
- [ ] Middleware verifies JWT signature
- [ ] User attached to `request.state.user`
- [ ] Routes check if user is authenticated
- [ ] Proper error responses (401 Unauthorized)

## Testing the Flow

**Test Script:**
```typescript
// test-jwt-flow.ts
import { getJWTToken } from './lib/auth-client';

async function testJWTFlow() {
  console.log('1. Testing JWT token fetch...');
  const token = await getJWTToken();

  if (!token) {
    console.error('❌ Failed to get JWT - user not logged in?');
    return;
  }

  console.log('✅ JWT token received:', token.substring(0, 20) + '...');

  console.log('2. Testing backend API call...');
  const response = await fetch('http://localhost:8000/api/personalize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ chapter_id: 'ch1' }),
  });

  if (response.status === 401) {
    console.error('❌ Backend rejected JWT token');
    return;
  }

  if (!response.ok) {
    console.error('❌ API call failed:', response.status);
    return;
  }

  const data = await response.json();
  console.log('✅ Backend authenticated user successfully!');
  console.log('Response:', data);
}

testJWTFlow();
```

## When to Use This Skill

Use this skill when:
- "User logged in but backend says unauthorized"
- "How do I send JWT token to backend?"
- "Backend not getting authentication"
- "401 error even though user is signed in"
- "Session cookie doesn't work with backend API"
- "Frontend and backend on different ports"

## Real-World Example

This is the actual pattern used in the Physical AI Book project:

**Frontend (`personalizationService.ts`):**
```typescript
import { getJWTToken } from './auth-client';

async function makeAuthenticatedRequest(endpoint: string) {
  // Get JWT token
  const token = await getJWTToken();

  if (!token) {
    throw new Error('Please sign in to personalize chapters');
  }

  // Call backend with JWT
  const response = await fetch(`http://localhost:8000${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
```

**Backend (`middleware/jwt_auth.py`):**
```python
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("authorization", "")

        user = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            user = verify_jwt_token(token)

        request.state.user = user
        return await call_next(request)
```

**Result:** ✅ User authenticated end-to-end!

## Summary

**The Problem:**
User logged in → Frontend has session cookie → Backend doesn't know

**The Solution:**
1. Frontend: Call `getJWTToken()` to get JWT from auth service
2. Frontend: Add `Authorization: Bearer ${token}` to API requests
3. Backend: Verify JWT and extract user data

**Key Points:**
- Session cookies only work with auth service
- Backend needs JWT in Authorization header
- Get fresh JWT before each API call
- Never store JWT in localStorage
- Always use `credentials: 'include'` when fetching JWT

This pattern solves the "backend doesn't know user is logged in" problem!
