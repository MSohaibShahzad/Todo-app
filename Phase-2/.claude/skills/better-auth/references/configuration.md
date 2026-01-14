# Better-Auth Configuration Reference

Complete reference for configuring Better-Auth for different use cases.

## Table of Contents
1. [Core Configuration Options](#core-configuration-options)
2. [Custom User Fields](#custom-user-fields)
3. [Session Configuration](#session-configuration)
4. [Security Configuration](#security-configuration)
5. [Database Configuration](#database-configuration)
6. [Common Patterns](#common-patterns)

## Core Configuration Options

### Basic Configuration

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  secret: process.env.BETTER_AUTH_SECRET, // 32+ char secret
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3001",
  trustedOrigins: ["http://localhost:3000"],
});
```

### Email and Password Configuration

```typescript
emailAndPassword: {
  enabled: true,
  minPasswordLength: 8,     // Minimum password length
  maxPasswordLength: 128,   // Maximum password length
  autoSignIn: true,         // Auto sign-in after signup
  requireEmailVerification: false, // Require email verification before signin
  sendResetPasswordEmail: async ({ user, url }) => {
    // Custom email sending logic
    // url contains the reset token
  },
  sendVerificationEmail: async ({ user, url }) => {
    // Custom verification email logic
  },
}
```

### Advanced Configuration

```typescript
{
  // Account management
  account: {
    accountLinking: {
      enabled: true, // Allow linking multiple auth methods to one account
      trustedProviders: ["google", "github"],
    },
  },

  // Rate limiting
  rateLimit: {
    enabled: true,
    window: 60, // seconds
    max: 10, // requests per window
    storage: "memory", // or "redis"
  },

  // Advanced session options
  advanced: {
    cookiePrefix: "better-auth", // Prefix for cookies
    crossSubDomainCookies: {
      enabled: false,
      domain: ".example.com", // Share cookies across subdomains
    },
    useSecureCookies: process.env.NODE_ENV === "production",
    generateId: async () => {
      // Custom ID generation
      return customIdGenerator();
    },
  },
}
```

## Custom User Fields

### Defining Custom Fields

Custom fields extend the default user model with application-specific data.

**Basic Example:**
```typescript
user: {
  additionalFields: {
    role: {
      type: "string",
      required: true,
      defaultValue: "user",
      input: true, // Allow input during signup
    },
    age: {
      type: "number",
      required: false,
      input: true,
    },
    newsletter: {
      type: "boolean",
      required: false,
      defaultValue: false,
      input: true,
    },
  },
}
```

**Advanced Example (Physical AI Book):**
```typescript
user: {
  additionalFields: {
    softwareBackground: {
      type: "string",
      required: false,
      defaultValue: "Beginner",
      input: true,
      // Validation (if using validators)
      validator: (value) => {
        const valid = ["Beginner", "Intermediate", "Advanced", "Expert"];
        return valid.includes(value);
      },
    },
    hardwareBackground: {
      type: "string",
      required: false,
      defaultValue: "None",
      input: true,
    },
    interestArea: {
      type: "string",
      required: false,
      defaultValue: "AI",
      input: true,
    },
    enrollmentDate: {
      type: "date",
      required: false,
      defaultValue: () => new Date(),
      input: false, // Not user-provided, auto-generated
    },
  },
}
```

### Field Types

| Type | TypeScript Type | Example Value | Use Case |
|------|----------------|---------------|-----------|
| `string` | `string` | `"John Doe"` | Names, text fields |
| `number` | `number` | `25` | Age, counters |
| `boolean` | `boolean` | `true` | Flags, opt-ins |
| `date` | `Date` | `new Date()` | Timestamps, dates |

### Custom Field Best Practices

1. **Keep fields minimal**: Only add fields you actively use
2. **Use defaults wisely**: Provide sensible defaults for optional fields
3. **Consider privacy**: Avoid storing sensitive data in user fields
4. **Validate input**: Always validate custom field inputs on the backend
5. **Document fields**: Add TypeScript types for type safety

### TypeScript Types for Custom Fields

```typescript
// types.ts
export interface User {
  // Default Better-Auth fields
  id: string;
  name: string;
  email: string;
  emailVerified: boolean;
  image?: string;
  createdAt: Date;
  updatedAt: Date;

  // Custom fields - define explicitly for type safety
  softwareBackground: "Beginner" | "Intermediate" | "Advanced" | "Expert";
  hardwareBackground: "None" | "Beginner" | "Intermediate" | "Advanced";
  interestArea: "AI" | "Robotics" | "Computer Vision" | "Motion Control" | "General";
}
```

## Session Configuration

### Session Duration and Updates

```typescript
session: {
  expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
  updateAge: 60 * 60 * 24,     // Update session every 24 hours

  // Cookie cache for performance
  cookieCache: {
    enabled: true,
    maxAge: 60 * 5, // 5 minutes
  },
}
```

**Session Lifetime Options:**
- **Short-lived (1 day)**: `expiresIn: 60 * 60 * 24`
- **Standard (7 days)**: `expiresIn: 60 * 60 * 24 * 7`
- **Extended (30 days)**: `expiresIn: 60 * 60 * 24 * 30`
- **Long-term (90 days)**: `expiresIn: 60 * 60 * 24 * 90`

### Session Storage Options

```typescript
// In-memory (development only)
session: {
  storage: "memory",
}

// Database (production recommended)
session: {
  storage: "database", // Uses main database connection
}

// Redis (high-performance production)
session: {
  storage: "redis",
  redis: {
    host: "localhost",
    port: 6379,
    password: process.env.REDIS_PASSWORD,
    db: 0,
  },
}
```

## Security Configuration

### CORS Configuration

```typescript
// In server.ts or your HTTP server
const allowedOrigins = [
  "http://localhost:3000",   // Local development
  "http://localhost:8000",   // API server
  "https://your-app.com",    // Production
  "https://staging.your-app.com", // Staging
];

// CORS middleware
if (allowedOrigins.includes(origin)) {
  res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, Cookie");
}
```

### Rate Limiting Configuration

```typescript
// In server.ts
const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes
const RATE_LIMIT_MAX_REQUESTS = 5; // 5 attempts per window

// Endpoints to rate limit
const rateLimitedPaths = [
  "/api/auth/sign-in",
  "/api/auth/sign-up",
  "/api/auth/reset-password",
];
```

**Recommended Limits:**
- **Authentication endpoints**: 5 requests per 15 minutes
- **Session endpoints**: 60 requests per minute
- **Public endpoints**: 100 requests per minute

### Password Security

```typescript
emailAndPassword: {
  minPasswordLength: 12,     // Strong passwords
  maxPasswordLength: 128,
  requirePasswordStrength: true, // Enable strength checking
  passwordStrength: {
    minStrength: 3,          // 0-4 scale
    requireUppercase: true,
    requireLowercase: true,
    requireNumbers: true,
    requireSpecialChars: false,
  },
}
```

### Secrets and Environment Variables

```bash
# Generate secure secrets
openssl rand -base64 32  # For BETTER_AUTH_SECRET
openssl rand -base64 32  # For JWT_SECRET

# .env file
BETTER_AUTH_SECRET=your-generated-secret-here
JWT_SECRET=your-jwt-secret-here
DATABASE_URL=postgresql://user:pass@host:5432/db

# Never commit these to version control!
```

## Database Configuration

### PostgreSQL Configuration

```typescript
// Basic connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Advanced connection
const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || "5432"),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  ssl: process.env.NODE_ENV === "production" ? {
    rejectUnauthorized: false,
  } : false,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Database Providers

**Neon (Serverless PostgreSQL):**
```bash
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require
```

**Supabase:**
```bash
DATABASE_URL=postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres
```

**Railway:**
```bash
DATABASE_URL=postgresql://postgres:pass@xxx.railway.app:5432/railway
```

**AWS RDS:**
```bash
DATABASE_URL=postgresql://user:pass@xxx.rds.amazonaws.com:5432/dbname
```

### Database Migrations

```bash
# Using Drizzle Kit (recommended with Better-Auth)
npm install drizzle-kit -D

# drizzle.config.ts
export default {
  schema: "./node_modules/better-auth/dist/db/schema.js",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
};

# Run migrations
npx drizzle-kit push
```

## Common Patterns

### Multi-Tenant Configuration

```typescript
// Store tenant ID in custom field
user: {
  additionalFields: {
    tenantId: {
      type: "string",
      required: true,
      input: false, // Set programmatically
    },
  },
}

// Middleware to filter by tenant
app.use(async (req, res, next) => {
  const { user } = await getSessionFromRequest(req);

  if (user && req.params.tenantId !== user.tenantId) {
    return res.status(403).json({ error: "Forbidden" });
  }

  next();
});
```

### Role-Based Access Control (RBAC)

```typescript
user: {
  additionalFields: {
    role: {
      type: "string",
      required: true,
      defaultValue: "user",
      input: false,
    },
    permissions: {
      type: "string", // Store as JSON string
      required: false,
      defaultValue: "[]",
      input: false,
    },
  },
}

// Middleware for role checking
function requireRole(role: string) {
  return async (req, res, next) => {
    const { user } = await getSessionFromRequest(req);

    if (!user || user.role !== role) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }

    next();
  };
}

// Usage
app.get("/admin/*", requireRole("admin"), adminRoutes);
```

### OAuth Integration (Future Extension)

```typescript
// Better-Auth supports OAuth providers
import { google, github } from "better-auth/providers";

export const auth = betterAuth({
  database: pool,
  providers: [
    google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    github({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
  ],
  account: {
    accountLinking: {
      enabled: true, // Allow linking OAuth to email/password
    },
  },
});
```

### Development vs Production Config

```typescript
const isDevelopment = process.env.NODE_ENV !== "production";

export const auth = betterAuth({
  database: pool,
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: isDevelopment
    ? "http://localhost:3001"
    : process.env.BETTER_AUTH_URL!,
  trustedOrigins: isDevelopment
    ? ["http://localhost:3000", "http://localhost:8000"]
    : process.env.TRUSTED_ORIGINS!.split(','),
  session: {
    expiresIn: isDevelopment
      ? 60 * 60 * 24 * 90 // 90 days in dev (convenient)
      : 60 * 60 * 24 * 7,  // 7 days in prod (secure)
  },
  advanced: {
    useSecureCookies: !isDevelopment,
    generateId: isDevelopment ? simpleId : secureId,
  },
});
```
