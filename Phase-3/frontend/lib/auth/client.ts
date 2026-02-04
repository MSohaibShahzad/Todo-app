import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getSession,
} = authClient;

/**
 * Get JWT token from Better-Auth for backend API authentication.
 *
 * This follows the standard pattern:
 * 1. Check if user has active session
 * 2. Call Better-Auth /api/auth/jwt endpoint with credentials: 'include'
 * 3. Better-Auth generates JWT from session cookie
 * 4. Return JWT for use in Authorization header
 */
export async function getJWTToken(): Promise<string | null> {
  try {
    // Check if user has an active session
    const session = await authClient.getSession();
    if (!session.data?.session) {
      console.warn("[Auth] No active session, cannot get JWT token");
      return null;
    }

    const userId = session.data.user?.id;
    if (!userId) {
      console.warn("[Auth] No user ID in session");
      return null;
    }

    // Check localStorage first for cached token
    if (typeof window !== "undefined") {
      const cachedToken = localStorage.getItem("bearer_token");
      const cachedUserId = localStorage.getItem("bearer_token_user_id");

      if (cachedToken && cachedUserId === userId && cachedToken.split('.').length === 3) {
        // Verify token is not expired before using
        try {
          const payload = JSON.parse(atob(cachedToken.split('.')[1]));
          const expiresAt = payload.exp * 1000; // Convert to milliseconds
          const now = Date.now();

          // Check if token expires in more than 1 minute (60000ms buffer)
          if (expiresAt > now + 60000) {
            console.log("[Auth] Using cached JWT token from localStorage");
            return cachedToken;
          } else {
            console.log("[Auth] Cached token expired or expiring soon, fetching new token");
            localStorage.removeItem("bearer_token");
            localStorage.removeItem("bearer_token_user_id");
          }
        } catch (e) {
          console.warn("[Auth] Failed to parse cached token, will fetch new one");
          localStorage.removeItem("bearer_token");
          localStorage.removeItem("bearer_token_user_id");
        }
      }
    }

    // Call Better-Auth JWT endpoint with session cookie
    console.log("[Auth] Requesting JWT from Better-Auth service");
    const response = await fetch("/api/auth/jwt", {
      method: "GET",
      credentials: "include", // CRITICAL: Include session cookie for authentication
    });

    if (!response.ok) {
      console.error("[Auth] Failed to get JWT from Better-Auth:", response.status);
      const errorText = await response.text();
      console.error("[Auth] Error response:", errorText);
      return null;
    }

    const data = await response.json();
    const jwtToken = data.token;

    if (jwtToken) {
      console.log("[Auth] JWT token received from Better-Auth");
      console.log("[Auth] Token format check:", jwtToken.split('.').length === 3 ? "Valid JWT" : "Invalid format");

      // Store for future use
      if (typeof window !== "undefined") {
        localStorage.setItem("bearer_token", jwtToken);
        localStorage.setItem("bearer_token_user_id", userId);
      }
      return jwtToken;
    }

    console.warn("[Auth] No JWT token in Better-Auth response");
    return null;
  } catch (error) {
    console.error("[Auth] Error in getJWTToken:", error);
    return null;
  }
}
