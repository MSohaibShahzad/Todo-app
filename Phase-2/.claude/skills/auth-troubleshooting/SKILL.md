---
name: auth-troubleshooting
description: Comprehensive authentication troubleshooting guide. Use this skill when diagnosing auth problems, fixing CORS issues, debugging session persistence, solving JWT verification errors, handling rate limiting, or troubleshooting any Better-Auth integration issues. Triggers when user says "auth not working", "CORS error", "session not persisting", "can't login", "JWT verification failed", or needs help debugging authentication.
---

# Authentication Troubleshooting Guide

Complete guide to diagnose and fix common authentication problems in Better-Auth implementations.

## Quick Diagnostic Checklist

Use this to quickly identify the problem:

```
[ ] Problem Area:
    [ ] Can't sign up
    [ ] Can't sign in
    [ ] Session not persisting
    [ ] Frontend can't call backend
    [ ] CORS errors
    [ ] JWT verification fails
    [ ] Rate limiting issues
    [ ] Custom fields not working
```

---

## Problem 1: User Can't Sign Up

### Symptoms
- Signup form submits but nothing happens
- Error: "Email already exists"
- Error: "Password too weak"
- Network error during signup

### Diagnosis Steps

**1. Check Auth Service is Running**
```bash
curl http://localhost:3001/health

# Should return: {"status":"healthy","service":"auth-service"}
```

**2. Check Signup Request**
```javascript
// Browser console
const response = await fetch('http://localhost:3001/api/auth/sign-up/email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'TestPass123!',
    name: 'Test User'
  })
});
console.log(await response.json());
```

**3. Check Database Connection**
```bash
# Check DATABASE_URL in auth service .env
cat backend/auth/.env | grep DATABASE_URL
```

### Solutions

**Solution 1: Auth Service Not Running**
```bash
cd backend/auth
npm run dev
# Should start on port 3001
```

**Solution 2: Database Not Accessible**
```bash
# Check PostgreSQL is running
# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

**Solution 3: Password Too Weak**
```typescript
// Ensure password meets requirements
password.length >= 8  // Minimum 8 characters
```

**Solution 4: Email Already Exists**
```sql
-- Check if email exists in database
SELECT email FROM user WHERE email = 'test@example.com';

-- Delete if testing
DELETE FROM user WHERE email = 'test@example.com';
```

---

## Problem 2: User Can't Sign In

### Symptoms
- Error: "Invalid credentials"
- Error: "User not found"
- Login form submits but nothing happens
- Network error during signin

### Diagnosis Steps

**1. Verify User Exists**
```sql
SELECT email, name FROM user WHERE email = 'your@email.com';
```

**2. Test Signin Endpoint**
```javascript
const response = await fetch('http://localhost:3001/api/auth/sign-in/email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'TestPass123!'
  })
});
console.log('Status:', response.status);
console.log('Data:', await response.json());
```

**3. Check Password Hash**
```sql
-- Password should be hashed (starts with $2)
SELECT id, email, password FROM user WHERE email = 'test@example.com';
```

### Solutions

**Solution 1: Wrong Password**
- Reset user password in database
- Or create new test user

**Solution 2: Rate Limiting**
```bash
# Wait 15 minutes or restart auth service to clear rate limits
pkill -f "node.*auth"
cd backend/auth && npm run dev
```

**Solution 3: Session Not Created**
```javascript
// Check Set-Cookie header in response
const response = await fetch('http://localhost:3001/api/auth/sign-in/email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include', // IMPORTANT!
  body: JSON.stringify({ email, password })
});

// Check cookies
console.log('Cookies:', document.cookie);
// Should see: better-auth.session_token=...
```

---

## Problem 3: Session Not Persisting

### Symptoms
- User logs in successfully
- Page refresh → user logged out
- Session cookie disappears
- `useSession()` returns null after refresh

### Diagnosis Steps

**1. Check Session Cookie**
```javascript
// Browser console
console.log(document.cookie);
// Should contain: better-auth.session_token=...
```

**2. Check Cookie Attributes**
```javascript
// Open DevTools → Application → Cookies
// Check better-auth.session_token:
// - HttpOnly: true
// - SameSite: Lax
// - Secure: false (dev), true (prod)
// - Path: /
// - Domain: localhost
```

**3. Test Session Endpoint**
```javascript
const response = await fetch('http://localhost:3001/api/auth/get-session', {
  method: 'GET',
  credentials: 'include' // CRITICAL!
});
console.log(await response.json());
```

### Solutions

**Solution 1: Missing credentials: 'include'**
```typescript
// WRONG ❌
const { data: session } = useSession();

// If using custom fetch, ensure credentials
fetch('/api/auth/get-session', {
  credentials: 'include' // Add this!
});
```

**Solution 2: CORS Blocks Cookies**
```typescript
// Auth service CORS config (server.ts)
res.setHeader("Access-Control-Allow-Origin", origin); // Exact origin
res.setHeader("Access-Control-Allow-Credentials", "true"); // Required!
```

**Solution 3: SameSite Cookie Issue**
```typescript
// If frontend and auth on different domains in prod
// Auth service needs SameSite=None; Secure
// Or use same domain (recommended)
```

**Solution 4: Session Expired**
```bash
# Check session duration (default 7 days)
# See backend/auth/src/config.ts:23
session: {
  expiresIn: 60 * 60 * 24 * 7, // 7 days
}
```

---

## Problem 4: CORS Errors

### Symptoms
- Browser console: "CORS policy blocked"
- Error: "No 'Access-Control-Allow-Origin' header"
- Preflight request fails
- Credentials blocked by CORS

### Diagnosis Steps

**1. Check CORS Error Details**
```
Access to fetch at 'http://localhost:3001/api/auth/sign-in/email'
from origin 'http://localhost:3000' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present
```

**2. Check Allowed Origins**
```bash
# Auth service
cat backend/auth/.env | grep ALLOWED_ORIGINS

# Backend API
cat backend/.env | grep CORS_ORIGINS
```

**3. Test Preflight Request**
```bash
curl -X OPTIONS http://localhost:3001/api/auth/sign-in/email \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Should return:
# Access-Control-Allow-Origin: http://localhost:3000
# Access-Control-Allow-Credentials: true
```

### Solutions

**Solution 1: Add Origin to Allowed List**

**Auth Service (backend/auth/.env):**
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
TRUSTED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Backend API (backend/.env):**
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Solution 2: Enable Credentials**

**Auth Service (backend/auth/src/server.ts:94):**
```typescript
res.setHeader("Access-Control-Allow-Credentials", "true");
```

**Backend API (backend/src/main.py:47):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,  # Must be True for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Frontend:**
```typescript
fetch('http://localhost:3001/api/auth/sign-in/email', {
  credentials: 'include' // Required for CORS with cookies
});
```

**Solution 3: Wildcard Not Allowed with Credentials**
```python
# WRONG ❌
allow_origins=["*"],
allow_credentials=True,

# RIGHT ✅
allow_origins=["http://localhost:3000"],
allow_credentials=True,
```

---

## Problem 5: Backend Returns 401 (User Logged In)

### Symptoms
- User successfully logs in
- Frontend has session cookie
- Backend API returns 401 Unauthorized
- "Backend doesn't know user is logged in"

### Solution
This is the **JWT Access Token Flow problem**. See the `jwt-access-token` skill for the complete solution.

**Quick Fix:**
```typescript
// Frontend: Get JWT before calling backend
import { getJWTToken } from './lib/auth-client';

const token = await getJWTToken();

fetch('http://localhost:8000/api/endpoint', {
  headers: {
    'Authorization': `Bearer ${token}` // Add JWT!
  }
});
```

---

## Problem 6: JWT Verification Fails

### Symptoms
- Backend error: "Invalid JWT token"
- Backend error: "JWT signature verification failed"
- 401 even with valid JWT

### Diagnosis Steps

**1. Check JWT Secret Matches**
```bash
# Auth service
cat backend/auth/.env | grep JWT_SECRET

# Backend API
cat backend/.env | grep JWT_SECRET

# MUST BE IDENTICAL!
```

**2. Check JWT Structure**
```javascript
// Decode JWT (without verification)
const parts = token.split('.');
const payload = JSON.parse(atob(parts[1]));
console.log(payload);

// Should have:
// - sub (user ID)
// - email
// - name
// - iss: "auth-service"
// - aud: "api-service"
// - exp (expiration)
```

**3. Test JWT Verification**
```python
import jwt
import os

token = "eyJhbGc..."
secret = os.getenv("JWT_SECRET")

try:
    payload = jwt.decode(
        token,
        secret,
        algorithms=["HS256"],
        issuer="auth-service",
        audience="api-service",
    )
    print("✅ Valid:", payload)
except jwt.ExpiredSignatureError:
    print("❌ Token expired")
except jwt.InvalidTokenError as e:
    print("❌ Invalid:", e)
```

### Solutions

**Solution 1: Secret Mismatch**
```bash
# Copy JWT_SECRET from auth service to backend
JWT_SECRET=$(grep JWT_SECRET backend/auth/.env | cut -d '=' -f2)
echo "JWT_SECRET=$JWT_SECRET" >> backend/.env
```

**Solution 2: Wrong Issuer/Audience**
```python
# Backend JWT verification
payload = jwt.decode(
    token,
    JWT_SECRET,
    algorithms=["HS256"],
    issuer="auth-service",     # Must match auth service
    audience="api-service",    # Must match auth service
)
```

**Solution 3: Token Expired**
```typescript
// Get fresh token before each API call
const token = await getJWTToken(); // Fresh token!
```

---

## Problem 7: Rate Limiting Blocking Requests

### Symptoms
- Error 429: "Too many requests"
- Can't login after multiple attempts
- "Retry after X seconds"

### Diagnosis Steps

**1. Check Rate Limit Settings**
```typescript
// backend/auth/src/server.ts:32
const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes
const RATE_LIMIT_MAX_REQUESTS = 5; // 5 attempts
```

**2. Test if Rate Limited**
```bash
curl -X POST http://localhost:3001/api/auth/sign-in/email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"wrong"}' \
  -v

# If rate limited, response headers show:
# Retry-After: 900
```

### Solutions

**Solution 1: Wait for Window to Expire**
Wait 15 minutes, or...

**Solution 2: Restart Auth Service** (clears in-memory rate limits)
```bash
pkill -f "node.*auth"
cd backend/auth && npm run dev
```

**Solution 3: Adjust Rate Limits** (for development)
```typescript
// backend/auth/src/server.ts:32
const RATE_LIMIT_MAX_REQUESTS = 100; // Increase for dev
```

---

## Problem 8: Custom Fields Not Working

### Symptoms
- Custom fields not appearing in session
- Error: "Unknown field"
- Fields not saved during signup

### Diagnosis Steps

**1. Check Field Configuration**
```typescript
// backend/auth/src/config.ts:30
user: {
  additionalFields: {
    softwareBackground: {
      type: "string",
      required: false,
      input: true, // IMPORTANT: Must be true!
    }
  }
}
```

**2. Check Signup Request Includes Fields**
```javascript
await authClient.signUp.email({
  email: "test@example.com",
  password: "TestPass123!",
  name: "Test",
  softwareBackground: "Intermediate", // Custom field
});
```

**3. Check Database Schema**
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'user';

-- Should see: softwareBackground | character varying
```

### Solutions

**Solution 1: Run Database Migration**
```bash
cd backend/auth
npm run migrate
```

**Solution 2: Enable Input**
```typescript
softwareBackground: {
  type: "string",
  input: true, // MUST BE TRUE to accept during signup!
}
```

**Solution 3: Frontend Plugin Config**
```typescript
// textbook/src/lib/auth-client.ts:40
plugins: [
  inferAdditionalFields({
    user: {
      softwareBackground: { type: "string" },
      hardwareBackground: { type: "string" },
      interestArea: { type: "string" },
    },
  }),
],
```

---

## Common Error Messages & Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "Invalid credentials" | Wrong password or user not found | Verify email/password, check user exists |
| "CORS policy blocked" | Origin not in allowed list | Add origin to ALLOWED_ORIGINS |
| "No 'Access-Control-Allow-Credentials'" | CORS not allowing cookies | Set `allow_credentials=True` |
| "Too many requests" | Rate limit exceeded | Wait 15 min or restart auth service |
| "JWT signature verification failed" | JWT_SECRET mismatch | Ensure secrets match exactly |
| "Token has expired" | JWT older than 7 days | Get fresh token with getJWTToken() |
| "Unauthorized" (but user logged in) | JWT not sent to backend | Add Authorization header with JWT |
| "Session not found" | Session cookie missing | Use credentials: 'include' in fetch |

---

## Debugging Tools

### Browser DevTools

**1. Network Tab**
- Check request/response headers
- Verify Authorization header is sent
- Check Set-Cookie headers

**2. Application Tab → Cookies**
- Verify `better-auth.session_token` exists
- Check cookie attributes (HttpOnly, SameSite, Domain)

**3. Console Tab**
- Enable console logs in auth-client.ts
- Check for error messages

### Backend Logs

**Auth Service:**
```bash
cd backend/auth
npm run dev
# Watch for errors in console
```

**Backend API:**
```bash
cd backend
uvicorn src.main:app --reload
# Watch for JWT verification logs
```

### Testing Scripts

**Test Auth Flow:**
```bash
# Test signup
curl -X POST http://localhost:3001/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!","name":"Test"}'

# Test signin
curl -X POST http://localhost:3001/api/auth/sign-in/email \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Test session
curl -X GET http://localhost:3001/api/auth/get-session \
  -b cookies.txt

# Test JWT
curl -X GET http://localhost:3001/api/auth/jwt \
  -b cookies.txt
```

---

## Quick Reference: Environment Variables

**Auth Service (backend/auth/.env):**
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/db
BETTER_AUTH_SECRET=<32+ chars>
JWT_SECRET=<same as backend>
AUTH_SERVER_PORT=3001
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
TRUSTED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Backend API (backend/.env):**
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=<same as auth service>
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Frontend (textbook/.env):**
```bash
REACT_APP_AUTH_URL=http://localhost:3001
REACT_APP_API_URL=http://localhost:8000
```

---

## Summary: Troubleshooting Workflow

1. **Identify the problem area** (signup, signin, session, CORS, JWT, etc.)
2. **Run diagnostic steps** (check logs, test endpoints, verify config)
3. **Apply the solution** (fix config, restart services, update code)
4. **Test the fix** (verify problem is resolved)
5. **Document the fix** (note what worked for future reference)

This skill covers the most common authentication problems and their solutions!
