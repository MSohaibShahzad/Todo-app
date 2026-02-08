/**
 * Better Auth configuration
 */
import { betterAuth } from "better-auth"
import { Pool } from "pg"

// Use a singleton pattern for the pool to avoid "Database already initialized" error
const globalForDb = globalThis as unknown as {
  pool: Pool | undefined
}

// Determine if we need SSL based on the connection string
// For Kubernetes internal services and localhost, SSL is not needed
const connectionString = process.env.DATABASE_URL || '';
const isKubernetesInternal = connectionString.includes('.svc.cluster.local') ||
                              connectionString.includes('todo-app-database') ||
                              connectionString.includes('todo-db');
const isLocalhost = connectionString.includes('localhost') || connectionString.includes('127.0.0.1');

const pool = globalForDb.pool ?? new Pool({
  connectionString: process.env.DATABASE_URL!,
  // Disable SSL for Kubernetes internal connections and localhost
  // Enable SSL with relaxed verification for external databases (like Neon)
  ssl: (isKubernetesInternal || isLocalhost) ? false : {
    rejectUnauthorized: false,
  },
  // Connection pool settings optimized for Neon
  max: 10, // Maximum number of clients in the pool
  idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
  connectionTimeoutMillis: 20000, // Wait up to 20 seconds for a connection
  query_timeout: 15000, // Wait up to 15 seconds for a query
})

if (process.env.NODE_ENV !== "production") {
  globalForDb.pool = pool
}

export const auth = betterAuth({
  database: pool,
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },
  plugins: [],
  trustedOrigins: [
    process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  ],
})
