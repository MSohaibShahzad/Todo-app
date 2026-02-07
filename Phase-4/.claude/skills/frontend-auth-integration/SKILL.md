---
name: frontend-auth-integration
description: Frontend authentication integration for React and Vue applications using Better-Auth. Use this skill when integrating auth into frontend applications, implementing login/signup UI components, managing auth state, protecting routes, handling session persistence, or working with @better-auth/react hooks. Triggers when user asks to "integrate auth in React", "add login page", "protect frontend routes", "setup auth client", "use Better-Auth React hooks", or needs frontend authentication implementation.
---

# Frontend Auth Integration

Complete toolkit for integrating Better-Auth authentication into React and Vue frontends.

## Overview

This skill provides everything needed to implement authentication UI and state management in modern frontend frameworks:
- **React integration** with @better-auth/react hooks and components
- **Vue integration** patterns for auth state management
- **UI component examples** for login, signup, and profile pages
- **Route protection** strategies for authenticated-only pages
- **Session persistence** and token management patterns
- **Error handling** for auth failures and edge cases

## When to Use This Skill

Use this skill when users request:
- "Add login page to React app"
- "Integrate Better-Auth with frontend"
- "Protect routes with authentication"
- "Setup auth state management"
- "Create signup form with validation"
- "Add user profile page"
- "Handle auth errors in UI"
- "Implement remember me functionality"

## Quick Start Workflow

### 1. Install Dependencies

**React:**
```bash
npm install @better-auth/react
# or
yarn add @better-auth/react
```

**Vue:**
```bash
npm install @better-auth/vue
# or
yarn add @better-auth/vue
```

### 2. Configure Auth Client

**React Setup (`src/lib/auth.ts`):**
```typescript
import { createAuthClient } from "@better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.REACT_APP_AUTH_URL || "http://localhost:3001",
});
```

**Vue Setup (`src/lib/auth.ts`):**
```typescript
import { createAuthClient } from "@better-auth/vue";

export const authClient = createAuthClient({
  baseURL: import.meta.env.VITE_AUTH_URL || "http://localhost:3001",
});
```

### 3. Wrap App with Auth Provider (React)

**`src/App.tsx`:**
```typescript
import { SessionProvider } from "@better-auth/react";
import { authClient } from "./lib/auth";

function App() {
  return (
    <SessionProvider client={authClient}>
      {/* Your app routes */}
    </SessionProvider>
  );
}
```

## Core Workflows

### User Registration (Signup)

**React Component (`src/pages/Signup.tsx`):**
```typescript
import { useState } from "react";
import { authClient } from "../lib/auth";
import { useNavigate } from "react-router-dom";

export function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const { data, error: signupError } = await authClient.signUp.email({
      email: formData.email,
      password: formData.password,
      name: formData.name,
      // Add custom fields if your auth service has them
      // role: "user",
      // tier: "free",
    });

    setLoading(false);

    if (signupError) {
      setError(signupError.message || "Signup failed");
      return;
    }

    // User is auto-signed in after signup
    console.log("Welcome:", data.user.name);
    navigate("/dashboard");
  };

  return (
    <div className="signup-page">
      <h1>Create Account</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name</label>
          <input
            id="name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>

        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            minLength={8}
            required
          />
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? "Creating account..." : "Sign Up"}
        </button>
      </form>

      <p>
        Already have an account? <a href="/login">Sign in</a>
      </p>
    </div>
  );
}
```

**Vue Component (`src/pages/Signup.vue`):**
```vue
<template>
  <div class="signup-page">
    <h1>Create Account</h1>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="name">Name</label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          required
        />
      </div>

      <div>
        <label for="email">Email</label>
        <input
          id="email"
          v-model="formData.email"
          type="email"
          required
        />
      </div>

      <div>
        <label for="password">Password</label>
        <input
          id="password"
          v-model="formData.password"
          type="password"
          minlength="8"
          required
        />
      </div>

      <div v-if="error" class="error">{{ error }}</div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Creating account..." : "Sign Up" }}
      </button>
    </form>

    <p>
      Already have an account? <router-link to="/login">Sign in</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { authClient } from "../lib/auth";

const router = useRouter();
const formData = ref({
  email: "",
  password: "",
  name: "",
});
const error = ref<string | null>(null);
const loading = ref(false);

async function handleSubmit() {
  error.value = null;
  loading.value = true;

  const { data, error: signupError } = await authClient.signUp.email({
    email: formData.value.email,
    password: formData.value.password,
    name: formData.value.name,
  });

  loading.value = false;

  if (signupError) {
    error.value = signupError.message || "Signup failed";
    return;
  }

  console.log("Welcome:", data.user.name);
  router.push("/dashboard");
}
</script>
```

### User Login (Signin)

**React Component (`src/pages/Login.tsx`):**
```typescript
import { useState } from "react";
import { authClient } from "../lib/auth";
import { useNavigate } from "react-router-dom";

export function Login() {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const { data, error: loginError } = await authClient.signIn.email({
      email: credentials.email,
      password: credentials.password,
      rememberMe: credentials.rememberMe,
    });

    setLoading(false);

    if (loginError) {
      setError(loginError.message || "Login failed");
      return;
    }

    console.log("Logged in:", data.user.email);
    navigate("/dashboard");
  };

  return (
    <div className="login-page">
      <h1>Sign In</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={credentials.email}
            onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
            required
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={credentials.password}
            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            required
          />
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={credentials.rememberMe}
              onChange={(e) => setCredentials({ ...credentials, rememberMe: e.target.checked })}
            />
            Remember me
          </label>
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign In"}
        </button>
      </form>

      <p>
        Don't have an account? <a href="/signup">Sign up</a>
      </p>
    </div>
  );
}
```

### Session Management and Current User

**React Hook Usage:**
```typescript
import { useSession } from "@better-auth/react";

export function Dashboard() {
  const { data: session, isPending, error } = useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (error || !session) {
    // Redirect to login
    window.location.href = "/login";
    return null;
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Email: {session.user.email}</p>
      {/* Access custom fields if configured */}
      {session.user.role && <p>Role: {session.user.role}</p>}
      {session.user.tier && <p>Tier: {session.user.tier}</p>}
    </div>
  );
}
```

**Vue Composable:**
```vue
<template>
  <div v-if="isPending">Loading...</div>
  <div v-else-if="error || !session">
    Redirecting to login...
  </div>
  <div v-else>
    <h1>Welcome, {{ session.user.name }}!</h1>
    <p>Email: {{ session.user.email }}</p>
  </div>
</template>

<script setup lang="ts">
import { useSession } from "@better-auth/vue";
import { watchEffect } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const { data: session, isPending, error } = useSession();

watchEffect(() => {
  if (!isPending.value && (error.value || !session.value)) {
    router.push("/login");
  }
});
</script>
```

### Protected Routes

**React Router v6:**
```typescript
import { useSession } from "@better-auth/react";
import { Navigate, Outlet } from "react-router-dom";

function ProtectedRoute() {
  const { data: session, isPending } = useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

// In your router setup:
import { BrowserRouter, Routes, Route } from "react-router-dom";

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

**Vue Router:**
```typescript
import { createRouter, createWebHistory } from "vue-router";
import { authClient } from "./lib/auth";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", component: () => import("./pages/Login.vue") },
    { path: "/signup", component: () => import("./pages/Signup.vue") },
    {
      path: "/dashboard",
      component: () => import("./pages/Dashboard.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/profile",
      component: () => import("./pages/Profile.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

// Navigation guard
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const session = await authClient.getSession();

    if (!session.data) {
      next("/login");
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
```

### Sign Out

**React:**
```typescript
import { authClient } from "../lib/auth";
import { useNavigate } from "react-router-dom";

export function Header() {
  const navigate = useNavigate();
  const { data: session } = useSession();

  const handleLogout = async () => {
    await authClient.signOut();
    navigate("/login");
  };

  if (!session) return null;

  return (
    <header>
      <nav>
        <span>Hello, {session.user.name}</span>
        <button onClick={handleLogout}>Sign Out</button>
      </nav>
    </header>
  );
}
```

**Vue:**
```vue
<template>
  <header v-if="session">
    <nav>
      <span>Hello, {{ session.user.name }}</span>
      <button @click="handleLogout">Sign Out</button>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { useSession } from "@better-auth/vue";
import { useRouter } from "vue-router";
import { authClient } from "../lib/auth";

const router = useRouter();
const { data: session } = useSession();

async function handleLogout() {
  await authClient.signOut();
  router.push("/login");
}
</script>
```

## Advanced Patterns

### Custom Fields in Signup

If your auth service has custom fields (e.g., `role`, `tier`, `background`):

```typescript
// React
const { data, error } = await authClient.signUp.email({
  email: formData.email,
  password: formData.password,
  name: formData.name,
  // Custom fields
  role: "student",
  tier: "free",
  softwareBackground: "Intermediate",
  hardwareBackground: "Beginner",
  interestArea: "Robotics",
});

// Access in session
const { data: session } = useSession();
console.log(session.user.role); // "student"
console.log(session.user.softwareBackground); // "Intermediate"
```

### Loading States and Error Handling

**Comprehensive error handling:**
```typescript
import { useState } from "react";
import { authClient } from "../lib/auth";

export function Login() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (credentials) => {
    setError(null);
    setLoading(true);

    try {
      const { data, error: loginError } = await authClient.signIn.email(credentials);

      if (loginError) {
        // Handle specific error codes
        if (loginError.message?.includes("Invalid credentials")) {
          setError("Incorrect email or password");
        } else if (loginError.message?.includes("too many requests")) {
          setError("Too many login attempts. Please try again later.");
        } else {
          setError("An error occurred. Please try again.");
        }
        return;
      }

      // Success
      window.location.href = "/dashboard";
    } catch (err) {
      setError("Network error. Please check your connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}
      {/* form fields */}
      <button type="submit" disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>
  );
}
```

### Profile Updates

```typescript
export function ProfilePage() {
  const { data: session } = useSession();
  const [formData, setFormData] = useState({
    name: session?.user.name || "",
    email: session?.user.email || "",
  });

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    const { error } = await authClient.updateUser({
      name: formData.name,
      // Add other updatable fields
    });

    if (error) {
      console.error("Update failed:", error);
      return;
    }

    alert("Profile updated successfully!");
  };

  return (
    <form onSubmit={handleUpdate}>
      <div>
        <label>Name</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        />
      </div>
      <button type="submit">Update Profile</button>
    </form>
  );
}
```

### JWT Token for API Calls

For calling protected backend APIs that use JWT:

```typescript
import { authClient } from "../lib/auth";

export async function callProtectedAPI() {
  // Get JWT from session
  const response = await fetch("http://localhost:3001/api/auth/jwt", {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Not authenticated");
  }

  const { token } = await response.json();

  // Use JWT in API calls
  const apiResponse = await fetch("http://localhost:8000/api/protected", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return apiResponse.json();
}
```

## Decision Tree: Choosing Integration Approach

```
Which frontend framework?
├─ React
│   ├─ Install @better-auth/react
│   ├─ Use useSession() hook
│   └─ Wrap app in SessionProvider
│
└─ Vue
    ├─ Install @better-auth/vue
    ├─ Use useSession() composable
    └─ Add navigation guards to router

Need to protect routes?
├─ React Router → Create ProtectedRoute component
└─ Vue Router → Use beforeEach navigation guard

Custom user fields?
├─ Pass in signUp.email() call
├─ Access via session.user.fieldName
└─ Add to TypeScript types if using TypeScript

API integration?
├─ Session-based (same domain) → Use credentials: "include"
├─ JWT-based (different domain) → Get JWT from /api/auth/jwt
└─ Cross-origin → Ensure CORS configured on auth service
```

## Common Use Cases

### E-Learning Platform

Student signup with background information:

```typescript
const { data, error } = await authClient.signUp.email({
  email: formData.email,
  password: formData.password,
  name: formData.name,
  softwareBackground: formData.softwareBackground, // "Beginner" | "Intermediate" | "Advanced"
  hardwareBackground: formData.hardwareBackground,
  interestArea: formData.interestArea, // "Robotics" | "AI" | "Computer Vision"
});
```

Access in dashboard:
```typescript
const { data: session } = useSession();
console.log(`Welcome ${session.user.name}!`);
console.log(`Software level: ${session.user.softwareBackground}`);
```

### SaaS Application

Role-based UI rendering:

```typescript
export function AdminPanel() {
  const { data: session } = useSession();

  if (session.user.role !== "admin") {
    return <Navigate to="/dashboard" />;
  }

  return (
    <div>
      <h1>Admin Panel</h1>
      {/* Admin-only content */}
    </div>
  );
}
```

Tier-based feature gating:

```typescript
export function PremiumFeature() {
  const { data: session } = useSession();
  const isPremium = session.user.tier === "premium";

  if (!isPremium) {
    return (
      <div>
        <p>This feature is only available on Premium tier.</p>
        <a href="/upgrade">Upgrade Now</a>
      </div>
    );
  }

  return <div>{/* Premium feature content */}</div>;
}
```

## Troubleshooting

**Session not persisting across page refreshes:**
- Ensure `credentials: "include"` in authClient config
- Check cookies are enabled in browser
- Verify CORS allows credentials on auth service

**CORS errors:**
- Add frontend origin to `ALLOWED_ORIGINS` in auth service .env
- Restart auth service after changing .env
- Ensure `credentials: "include"` in fetch requests

**useSession() returns null:**
- Check auth service is running
- Verify `baseURL` in authClient config is correct
- Check browser network tab for failed requests

**Protected routes not working:**
- Ensure SessionProvider wraps router
- Check navigation guard logic
- Verify session check is async/await

**Custom fields not accessible:**
- Verify fields are configured in auth service
- Check TypeScript types if using TypeScript
- Ensure fields are passed during signup

## Security Best Practices

1. **HTTPS in Production**: Always use HTTPS for auth endpoints
2. **Secure Cookies**: Auth service handles httpOnly cookies automatically
3. **CORS Configuration**: Only allow trusted frontend origins
4. **Password Validation**: Enforce minimum 8 characters client-side
5. **Error Messages**: Don't reveal if email exists during login failures
6. **Rate Limiting**: Auth service handles rate limiting server-side
7. **Token Storage**: Never store JWT in localStorage, use httpOnly cookies
8. **Logout on Sensitive Actions**: Force re-auth for account changes

## Resources

### Official Documentation
- Better-Auth React Docs: https://better-auth.com/docs/react
- Better-Auth Vue Docs: https://better-auth.com/docs/vue

### Related Skills
- `better-auth` - Backend auth service setup
- `backend-auth-integration` - Python/FastAPI integration
