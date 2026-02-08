import { auth } from "@/lib/auth/config";
import { NextRequest, NextResponse } from "next/server";
import { sign } from "jsonwebtoken";

/**
 * JWT endpoint for exchanging Better-Auth session for JWT token.
 *
 * This endpoint:
 * 1. Validates Better-Auth session (via cookies)
 * 2. Generates custom JWT token with user_id for backend API
 * 3. Returns JWT to frontend
 *
 * Frontend calls this with credentials: 'include' to send session cookies.
 */
export async function GET(request: NextRequest) {
  try {
    // Get session from Better-Auth using cookies
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session || !session.user) {
      return NextResponse.json(
        { error: "No active session" },
        { status: 401 }
      );
    }

    // Extract user ID from Better-Auth session
    const userId = session.user.id;

    if (!userId) {
      return NextResponse.json(
        { error: "User ID not found in session" },
        { status: 400 }
      );
    }

    // Generate JWT token with user_id claim for backend
    // Use the same secret as defined in backend/.env
    const jwtSecret = process.env.JWT_SECRET || process.env.BETTER_AUTH_SECRET;

    if (!jwtSecret) {
      console.error("[JWT] No JWT_SECRET or BETTER_AUTH_SECRET found in environment");
      return NextResponse.json(
        { error: "Server configuration error" },
        { status: 500 }
      );
    }

    const token = sign(
      {
        user_id: userId,
        email: session.user.email,
      },
      jwtSecret,
      {
        expiresIn: "30m", // 30 minutes
        algorithm: "HS256",
      }
    );

    console.log(`[JWT] Generated JWT token for user_id=${userId}`);

    return NextResponse.json({
      token,
    });
  } catch (error) {
    console.error("[JWT] Error generating JWT token:", error);
    return NextResponse.json(
      { error: "Failed to generate JWT token" },
      { status: 500 }
    );
  }
}
