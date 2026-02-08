/**
 * Application configuration
 * Centralized config for environment-specific values
 */

// API URL for backend communication
// In production (Kubernetes), use the external port-forwarded URL
// In development, use relative URLs (Next.js proxy)
export const API_URL = process.env.NEXT_PUBLIC_API_URL || ""

// Other config values can be added here
export const CHATKIT_DOMAIN_KEY = process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY || "local-dev"
export const APP_URL = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"
