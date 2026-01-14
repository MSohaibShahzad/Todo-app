/**
 * Better Auth configuration
 */
import { betterAuth } from "better-auth"
import { Pool } from "pg"

// Use a singleton pattern for the pool to avoid "Database already initialized" error
const globalForDb = globalThis as unknown as {
  pool: Pool | undefined
}

const pool = globalForDb.pool ?? new Pool({
  connectionString: process.env.DATABASE_URL!,
  ssl: {
    rejectUnauthorized: false,
  },
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
