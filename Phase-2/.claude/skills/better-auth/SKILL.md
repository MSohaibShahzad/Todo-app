---
name: better-auth
description: Comprehensive authentication system implementation using Better-Auth. Use this skill when working with user authentication, including signup/signin flows, session management, JWT tokens, custom user fields, password handling, or integrating auth with Node.js/TypeScript and Python backends. Triggers when user asks to "add authentication", "implement login", "create auth service", "setup Better-Auth", "add signup/signin", or needs help with authentication workflows.
---

# Better-Auth Authentication Skill

Complete toolkit for implementing secure authentication with Better-Auth library.

## Overview

This skill provides everything needed to implement production-ready authentication:
- **Setup scripts** that generate complete auth service boilerplate
- **Workflow documentation** for common authentication patterns
- **Configuration guides** for customization and security
- **Testing utilities** to verify endpoints work correctly

Better-Auth is a modern authentication library for TypeScript/Node.js with built-in PostgreSQL support, session management, and JWT token generation.

## When to Use This Skill

Use this skill when users request:
- "Add authentication to my project"
- "Implement signup and signin"
- "Create auth service with Better-Auth"
- "Setup user login system"
- "Add custom user fields to authentication"
- "Generate JWT tokens from sessions"
- "Integrate auth with Python backend"

## Quick Start Workflow

### 1. Generate Auth Service

Run the setup script to create a complete auth service:

```bash
python scripts/setup_auth.py \
  --project-dir ./backend/auth \
  --database-url "postgresql://user:pass@localhost:5432/db" \
  --custom-fields "role:string tier:string" \
  --port 3001 \
  --project-name "my-auth-service"
```

**This creates:**
- TypeScript configuration and type definitions
- Better-Auth setup with email/password support
- HTTP server with CORS and rate limiting
- Session middleware for route protection
- JWT token generation utilities
- Database migration config
- Complete package.json with dependencies

**Custom fields** extend the user model with your application-specific data. Examples:
- E-learning platform: `softwareBackground:string hardwareBackground:string interestArea:string`
- SaaS application: `role:string tier:string companyId:string`
- E-commerce: `shippingAddress:string paymentMethod:string`

### 2. Configure Environment

```bash
cd backend/auth
cp .env.template .env
# Edit .env with your values:
# - DATABASE_URL (PostgreSQL connection string)
# - BETTER_AUTH_SECRET (generate with: openssl rand -base64 32)
# - JWT_SECRET
# - ALLOWED_ORIGINS
```

### 3. Install and Run

```bash
npm install
npm run migrate  # Create database tables
npm run dev      # Start auth server on port 3001
```

### 4. Test Endpoints

```bash
python scripts/test_auth.py \
  --base-url http://localhost:3001 \
  --email test@example.com \
  --password TestPassword123!
```

## Core Workflows

### User Registration (Signup)

**Backend API Endpoint:**
```
POST /api/auth/sign-up/email
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "Jane Doe",
  // Custom fields (if configured)
  "role": "user",
  "tier": "free"
}

Response (200 OK):
{
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "Jane Doe",
    "role": "user",
    "tier": "free",
    "emailVerified": false,
    "createdAt": "2024-01-01T00:00:00Z"
  },
  "session": {
    "id": "session_xyz789",
    "token": "...",
    "expiresAt": "2024-01-08T00:00:00Z"
  }
}
```

**Frontend Integration (React):**
```typescript
import { createAuthClient } from "@better-auth/react";

const authClient = createAuthClient({
  baseURL: "http://localhost:3001"
});

async function handleSignup(formData) {
  const { data, error } = await authClient.signUp.email({
    email: formData.email,
    password: formData.password,
    name: formData.name,
    // Pass custom fields
    role: "user",
    tier: "free",
  });

  if (error) {
    console.error("Signup failed:", error);
    return;
  }

  // User is auto-signed in
  console.log("Welcome:", data.user.name);
  window.location.href = "/dashboard";
}
```

### User Login (Signin)

**Backend API Endpoint:**
```
POST /api/auth/sign-in/email
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "rememberMe": true
}
```

**Frontend Integration:**
```typescript
async function handleLogin(credentials) {
  const { data, error } = await authClient.signIn.email({
    email: credentials.email,
    password: credentials.password,
    rememberMe: true,
  });

  if (error) {
    console.error("Login failed:", error);
    return;
  }

  window.location.href = "/dashboard";
}
```

### Session Management

**Check Current Session (Frontend):**
```typescript
import { useSession } from "@better-auth/react";

function Dashboard() {
  const { data: session, isPending } = useSession();

  if (isPending) return <div>Loading...</div>;

  if (!session) {
    window.location.href = "/login";
    return null;
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Role: {session.user.role}</p>
      <p>Tier: {session.user.tier}</p>
    </div>
  );
}
```

**Protect Backend Routes (Node.js):**
```typescript
import { sessionMiddleware } from "./middleware";

app.get("/api/protected", sessionMiddleware, (req, res) => {
  if (!req.user) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  res.json({
    message: "Protected data",
    user: req.user,
  });
});
```

**Python FastAPI Integration:**
```python
import httpx
from fastapi import Request, HTTPException

async def validate_session(cookie_header: str):
    """Validate session via Node.js auth service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:3001/api/validate-session",
            headers={"Cookie": cookie_header}
        )
        return response.json()

@app.get("/api/protected")
async def protected_route(request: Request):
    cookie_header = request.headers.get("cookie", "")
    session_data = await validate_session(cookie_header)

    if not session_data.get("user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "message": "Protected data",
        "user": session_data["user"]
    }
```

### JWT Token Generation

For stateless authentication or third-party API integration:

**Get JWT from Session:**
```typescript
async function getJWT() {
  const response = await fetch("http://localhost:3001/api/auth/jwt", {
    credentials: "include", // Send session cookies
  });

  if (!response.ok) {
    throw new Error("Not authenticated");
  }

  const { token } = await response.json();
  return token; // JWT token valid for 7 days
}
```

**Verify JWT (Python):**
```python
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET")

def verify_jwt(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer="better-auth"
        )
        return payload  # { sub: userId, email, name }
    except jwt.InvalidTokenError:
        return None

# Use in FastAPI dependency
from fastapi import Header, HTTPException

def require_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "No token provided")

    token = authorization[7:]
    payload = verify_jwt(token)

    if not payload:
        raise HTTPException(401, "Invalid token")

    return payload

@app.get("/api/protected")
async def protected(user = Depends(require_auth)):
    return {"user": user}
```

### Sign Out

```typescript
async function handleLogout() {
  await authClient.signOut();
  window.location.href = "/login";
}
```

## Decision Tree: Choosing the Right Approach

**When implementing authentication, consider:**

```
Is the project brand new?
├─ YES → Use setup_auth.py to generate complete service
└─ NO → Does authentication already exist?
    ├─ YES → Are you adding custom fields or features?
    │   ├─ YES → Review references/configuration.md for examples
    │   └─ NO → Need help with frontend integration?
    │       └─ See workflow examples above
    └─ NO → Use setup_auth.py to generate service
```

**Choosing custom fields:**
```
What user data do you need beyond email/name/password?
├─ User roles/permissions → Add "role:string" field
├─ Subscription tiers → Add "tier:string" field
├─ Profile customization → Add specific fields (e.g., "background:string")
├─ Multi-tenant → Add "tenantId:string" field
└─ E-commerce → Add "shippingAddress:string" etc.
```

**Frontend or backend integration?**
```
Frontend (React/Vue/etc)?
├─ Install @better-auth/react
├─ Use authClient.signUp.email() / signIn.email()
└─ Use useSession() hook for current user

Backend (Node.js)?
├─ Import sessionMiddleware
└─ Apply to protected routes

Backend (Python)?
├─ Call /api/validate-session endpoint
└─ Parse session data from response
```

## Common Use Cases

### E-Learning Platform (like Physical AI Book)

Custom fields for student background:

```bash
python scripts/setup_auth.py \
  --project-dir ./backend/auth \
  --custom-fields "softwareBackground:string hardwareBackground:string interestArea:string"
```

Users can then specify their learning profile during signup:
```typescript
await authClient.signUp.email({
  email: "student@example.com",
  password: "SecurePass123!",
  name: "Alex Student",
  softwareBackground: "Intermediate",
  hardwareBackground: "Beginner",
  interestArea: "Robotics",
});
```

### SaaS Application

Role-based access control with subscription tiers:

```bash
python scripts/setup_auth.py \
  --project-dir ./backend/auth \
  --custom-fields "role:string tier:string companyId:string"
```

Middleware for role-checking:
```typescript
function requireRole(allowedRoles: string[]) {
  return async (req, res, next) => {
    const { user } = await getSessionFromRequest(req);

    if (!user || !allowedRoles.includes(user.role)) {
      return res.status(403).json({ error: "Forbidden" });
    }

    next();
  };
}

// Admin-only route
app.get("/admin/*", requireRole(["admin"]), adminRoutes);
```

### Multi-Frontend Application

Configure multiple allowed origins:

```bash
# .env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://app.example.com
TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8000,https://app.example.com
```

The auth service automatically handles CORS for all configured origins.

## Advanced Topics

For detailed information on these topics, see the reference files:

### Configuration Deep-Dive

See `references/configuration.md` for:
- Complete configuration options
- Custom field validation and types
- Session storage options (memory, database, Redis)
- Security hardening (rate limiting, password strength, CORS)
- Database provider setup (Neon, Supabase, Railway, AWS RDS)
- Multi-tenant patterns
- Role-based access control (RBAC)
- OAuth integration (Google, GitHub)

### Complete Workflows

See `references/workflows.md` for:
- Initial setup workflow (step-by-step)
- Password reset flow
- Email verification flow
- Profile update workflow
- Production deployment checklist
- Multi-project configuration
- Monitoring and security best practices

## Scripts Reference

### setup_auth.py

Generate complete Better-Auth service:

```bash
python scripts/setup_auth.py \
  --project-dir <path> \
  --database-url <postgres-url> \
  --custom-fields "field1:type1 field2:type2" \
  --port <port-number> \
  --project-name <name>
```

**Parameters:**
- `--project-dir`: Directory to create auth service (e.g., `./backend/auth`)
- `--database-url`: PostgreSQL connection string (optional, added to .env.template)
- `--custom-fields`: Space-separated custom fields (e.g., `"role:string age:number"`)
- `--port`: Server port (default: 3001)
- `--project-name`: Package name (default: "auth-service")

### test_auth.py

Test authentication endpoints:

```bash
python scripts/test_auth.py \
  --base-url <auth-service-url> \
  --email <test-email> \
  --password <test-password> \
  --name <test-name> \
  --custom-fields '{"role": "user", "tier": "free"}'
```

Tests health, signup, signin, session retrieval, JWT generation, and signout.

## Security Best Practices

**Always follow these practices:**

1. **Strong Secrets**: Generate with `openssl rand -base64 32`, never commit to git
2. **HTTPS in Production**: Use secure cookies and HTTPS-only connections
3. **Rate Limiting**: Enabled by default (5 attempts per 15 minutes for auth endpoints)
4. **Password Requirements**: Minimum 8 characters, configurable in config.ts
5. **CORS Configuration**: Only allow trusted origins
6. **Database Security**: Use connection pooling, SSL for production databases
7. **Environment Variables**: Never hardcode secrets, use .env files
8. **Session Duration**: Balance convenience vs security (default: 7 days)

## Troubleshooting

**Auth server won't start:**
- Check DATABASE_URL is valid and database is reachable
- Verify BETTER_AUTH_SECRET is set (32+ characters)
- Run `npm run migrate` to create database tables

**CORS errors in browser:**
- Add frontend origin to ALLOWED_ORIGINS in .env
- Restart auth server after changing .env

**Session not persisting:**
- Check cookies are enabled in browser
- Verify `credentials: "include"` in fetch requests
- Check CORS headers allow credentials

**JWT verification fails:**
- Ensure JWT_SECRET matches between Node.js and Python
- Check token hasn't expired (default: 7 days)
- Verify issuer is "better-auth"

## Resources

### scripts/
- `setup_auth.py` - Generate complete Better-Auth service
- `test_auth.py` - Test authentication endpoints

### references/
- `workflows.md` - Complete workflow guides for all auth operations
- `configuration.md` - Comprehensive configuration reference and patterns

Both reference files provide production-ready patterns and detailed examples.
