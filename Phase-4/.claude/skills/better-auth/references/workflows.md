# Better-Auth Workflows

Complete workflow guide for implementing Better-Auth authentication.

## Table of Contents
1. [Initial Setup Workflow](#initial-setup-workflow)
2. [User Registration Workflow](#user-registration-workflow)
3. [User Login Workflow](#user-login-workflow)
4. [Session Management Workflow](#session-management-workflow)
5. [JWT Token Workflow](#jwt-token-workflow)
6. [Password Reset Workflow](#password-reset-workflow)
7. [Profile Update Workflow](#profile-update-workflow)
8. [Multi-Project Configuration](#multi-project-configuration)

## Initial Setup Workflow

### Step 1: Project Structure Setup

Run the setup script to generate all necessary files:

```bash
python scripts/setup_auth.py \
  --project-dir ./backend/auth \
  --database-url "postgresql://user:pass@localhost:5432/db" \
  --custom-fields "softwareBackground:string hardwareBackground:string" \
  --port 3001 \
  --project-name "my-auth-service"
```

This creates:
- `src/config.ts` - Better-Auth configuration
- `src/types.ts` - TypeScript type definitions
- `src/routes.ts` - Route handlers
- `src/middleware.ts` - Session middleware
- `src/server.ts` - Standalone HTTP server
- `src/jwt.ts` - JWT utilities
- `package.json` - Dependencies
- `tsconfig.json` - TypeScript config
- `drizzle.config.ts` - Database migrations
- `.env.template` - Environment variables template

### Step 2: Environment Configuration

Copy `.env.template` to `.env` and configure:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
BETTER_AUTH_SECRET=your-32-char-secret-key-here  # Generate with: openssl rand -base64 32
BETTER_AUTH_URL=http://localhost:3001
JWT_SECRET=your-jwt-secret-here
AUTH_SERVER_PORT=3001
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Step 3: Install Dependencies & Migrate

```bash
cd backend/auth
npm install
npm run migrate  # Creates database tables
npm run dev      # Start development server
```

### Step 4: Test Endpoints

```bash
python scripts/test_auth.py \
  --base-url http://localhost:3001 \
  --email test@example.com \
  --password TestPass123!
```

## User Registration Workflow

### Backend Setup (Already Done by setup script)

The `src/config.ts` configures email/password signup:

```typescript
emailAndPassword: {
  enabled: true,
  minPasswordLength: 8,
  maxPasswordLength: 128,
  autoSignIn: true, // Auto-signin after signup
}
```

### Frontend Implementation (React Example)

```typescript
// 1. Install Better-Auth React client
// npm install @better-auth/react

// 2. Create auth client
import { createAuthClient } from "@better-auth/react";

const authClient = createAuthClient({
  baseURL: "http://localhost:3001",
});

// 3. Signup component
function SignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const { data, error } = await authClient.signUp.email({
        email,
        password,
        name,
        // Custom fields (if configured)
        softwareBackground: "Beginner",
        hardwareBackground: "None",
      });

      if (error) {
        console.error("Signup error:", error);
        return;
      }

      console.log("Signup successful:", data.user);
      // User is auto-signed in, redirect to dashboard
      window.location.href = "/dashboard";
    } catch (error) {
      console.error("Signup failed:", error);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        minLength={8}
      />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

### API Endpoint

```
POST http://localhost:3001/api/auth/sign-up/email
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe",
  "softwareBackground": "Intermediate",
  "hardwareBackground": "Beginner"
}

Response (200 OK):
{
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "softwareBackground": "Intermediate",
    "hardwareBackground": "Beginner"
  },
  "session": {
    "id": "session_456",
    "token": "...",
    "expiresAt": "2024-01-15T00:00:00Z"
  }
}
```

## User Login Workflow

### Frontend Implementation

```typescript
function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const { data, error } = await authClient.signIn.email({
        email,
        password,
        rememberMe: true, // Optional: extend session duration
      });

      if (error) {
        console.error("Login error:", error);
        return;
      }

      console.log("Login successful:", data.user);
      window.location.href = "/dashboard";
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Sign In</button>
    </form>
  );
}
```

### API Endpoint

```
POST http://localhost:3001/api/auth/sign-in/email
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "rememberMe": true
}

Response (200 OK):
{
  "user": { ... },
  "session": { ... }
}
```

## Session Management Workflow

### Getting Current Session (Frontend)

```typescript
import { useSession } from "@better-auth/react";

function Dashboard() {
  const { data: session, isPending } = useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (!session) {
    // Not authenticated, redirect to login
    window.location.href = "/login";
    return null;
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### Session Validation (Backend Middleware)

For Node.js/Express routes:

```typescript
import { sessionMiddleware } from "./middleware";

app.get("/api/protected", sessionMiddleware, (req, res) => {
  // req.user is populated by middleware
  if (!req.user) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  res.json({ message: "Protected data", user: req.user });
});
```

For Python FastAPI integration:

```python
import httpx

async def validate_session(cookie_header: str):
    """Call Node.js auth service to validate session"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:3001/api/validate-session",
            headers={"Cookie": cookie_header}
        )
        return response.json()

# In FastAPI route:
@app.get("/api/protected")
async def protected_route(request: Request):
    cookie_header = request.headers.get("cookie", "")
    session_data = await validate_session(cookie_header)

    if not session_data.get("user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"message": "Protected data", "user": session_data["user"]}
```

### Sign Out

```typescript
function LogoutButton() {
  const handleLogout = async () => {
    try {
      await authClient.signOut();
      window.location.href = "/login";
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return <button onClick={handleLogout}>Sign Out</button>;
}
```

API Endpoint:
```
POST http://localhost:3001/api/auth/sign-out
Cookie: better-auth.session_token=...

Response (200 OK):
{ "success": true }
```

## JWT Token Workflow

### Generating JWT from Session

Useful for stateless API authentication or third-party integrations:

```typescript
// Frontend: Get JWT token
async function getJWTToken() {
  try {
    const response = await fetch("http://localhost:3001/api/auth/jwt", {
      credentials: "include", // Include session cookies
    });

    if (!response.ok) {
      throw new Error("Not authenticated");
    }

    const data = await response.json();
    return data.token; // JWT token
  } catch (error) {
    console.error("Failed to get JWT:", error);
    return null;
  }
}

// Use JWT for API calls
async function callProtectedAPI() {
  const token = await getJWTToken();

  const response = await fetch("https://api.example.com/protected", {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  return response.json();
}
```

### Verifying JWT (Backend)

```typescript
import { verifyJWT } from "./jwt";

// Node.js/Express middleware
function jwtMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "No token provided" });
  }

  const token = authHeader.substring(7);
  const payload = verifyJWT(token);

  if (!payload) {
    return res.status(401).json({ error: "Invalid token" });
  }

  req.user = payload; // { sub: userId, email, name }
  next();
}
```

Python FastAPI example:

```python
import jwt
from fastapi import Header, HTTPException

JWT_SECRET = os.getenv("JWT_SECRET")

def verify_jwt_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")

    token = authorization[7:]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer="better-auth")
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/protected")
async def protected_route(user_data = Depends(verify_jwt_token)):
    return {"message": "Protected data", "user": user_data}
```

## Profile Update Workflow

### Updating User Profile

```typescript
async function updateProfile(updates) {
  try {
    const response = await fetch("http://localhost:3001/api/auth/user/profile", {
      method: "PATCH",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      throw new Error("Update failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Profile update error:", error);
    throw error;
  }
}

// Usage
await updateProfile({
  softwareBackground: "Advanced",
  hardwareBackground: "Intermediate",
});
```

## Multi-Project Configuration

### Configuring for Multiple Frontends

Update `.env`:

```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://your-app.com
TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8000,https://your-app.com
```

### Production Deployment Checklist

1. **Environment Variables**:
   - Generate secure secrets: `openssl rand -base64 32`
   - Set `BETTER_AUTH_URL` to production URL
   - Add production origins to `ALLOWED_ORIGINS`

2. **Database**:
   - Use production PostgreSQL (e.g., Neon, Supabase, AWS RDS)
   - Run migrations: `npm run migrate`

3. **Rate Limiting**:
   - Consider using Redis for rate limit store (production)
   - Adjust `RATE_LIMIT_MAX_REQUESTS` based on needs

4. **Security**:
   - Enable HTTPS only in production
   - Set secure cookie flags
   - Implement CSRF protection
   - Add email verification flow

5. **Monitoring**:
   - Log authentication events
   - Monitor failed login attempts
   - Set up alerts for suspicious activity
