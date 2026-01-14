#!/usr/bin/env python3
"""
Setup Better-Auth authentication system for a project

This script generates all necessary files for Better-Auth integration:
- Configuration file (config.ts)
- Type definitions (types.ts)
- Route handlers (routes.ts)
- Middleware (middleware.ts)
- Server file (server.ts)
- JWT utilities (jwt.ts)
- Drizzle config
- Package.json with dependencies

Usage:
    python setup_auth.py --project-dir /path/to/project --database-url postgres://...
    python setup_auth.py --project-dir . --custom-fields software:string hardware:string
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

def parse_custom_fields(fields_str: str) -> Dict[str, str]:
    """
    Parse custom fields from command line
    Format: "field1:type1 field2:type2"
    """
    if not fields_str:
        return {}

    fields = {}
    for field in fields_str.split():
        if ':' in field:
            name, field_type = field.split(':', 1)
            fields[name] = field_type
    return fields

def generate_package_json(custom_name: str = "auth-service"):
    """Generate package.json for Better-Auth project"""
    return {
        "name": custom_name,
        "version": "1.0.0",
        "description": "Better-Auth authentication service",
        "main": "dist/server.js",
        "scripts": {
            "dev": "tsx watch src/server.ts",
            "build": "tsc",
            "start": "node dist/server.js",
            "migrate": "drizzle-kit push"
        },
        "dependencies": {
            "better-auth": "^1.3.0",
            "pg": "^8.11.3",
            "dotenv": "^16.3.1",
            "jsonwebtoken": "^9.0.2"
        },
        "devDependencies": {
            "@types/node": "^20.10.0",
            "@types/jsonwebtoken": "^9.0.5",
            "typescript": "^5.3.3",
            "tsx": "^4.7.0",
            "drizzle-kit": "^0.20.0"
        }
    }

def generate_config_ts(custom_fields: Dict[str, str], base_url: str = "http://localhost:3001"):
    """Generate config.ts with Better-Auth configuration"""

    # Generate additionalFields object
    additional_fields_code = ""
    if custom_fields:
        additional_fields_code = "\n    additionalFields: {\n"
        for field_name, field_type in custom_fields.items():
            additional_fields_code += f"""      {field_name}: {{
        type: "{field_type}",
        required: false,
        defaultValue: "",
        input: true,
      }},\n"""
        additional_fields_code += "    },"

    return f'''import {{ betterAuth }} from "better-auth";
import {{ Pool }} from "pg";
import * as dotenv from "dotenv";

dotenv.config();

const pool = new Pool({{
  connectionString: process.env.DATABASE_URL,
}});

export const auth = betterAuth({{
  database: pool,
  emailAndPassword: {{
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
    autoSignIn: true,
  }},
  session: {{
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // Update every 24 hours
    cookieCache: {{
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    }},
  }},
  user: {{{additional_fields_code}
  }},
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL || "{base_url}",
  trustedOrigins: process.env.TRUSTED_ORIGINS
    ? process.env.TRUSTED_ORIGINS.split(',').map(origin => origin.trim())
    : ["http://localhost:3000"],
}});

export type AuthUser = typeof auth.$Infer.Session.user;
export type AuthSession = typeof auth.$Infer.Session.session;
'''

def generate_types_ts(custom_fields: Dict[str, str]):
    """Generate types.ts with TypeScript type definitions"""

    # Generate custom fields in User interface
    custom_fields_code = ""
    if custom_fields:
        for field_name, field_type in custom_fields.items():
            ts_type = "string" if field_type == "string" else "number" if field_type == "number" else "boolean"
            custom_fields_code += f"  {field_name}: {ts_type};\n"

    return f'''export interface User {{
  id: string;
  name: string;
  email: string;
  emailVerified: boolean;
  image?: string;
  createdAt: Date;
  updatedAt: Date;
{custom_fields_code}}}

export interface Session {{
  id: string;
  userId: string;
  expiresAt: Date;
  token: string;
  ipAddress?: string;
  userAgent?: string;
  user?: User;
}}

export interface SignupRequest {{
  email: string;
  password: string;
  name: string;
{custom_fields_code.replace('  ', '  ', 1).replace(': ', '?: ') if custom_fields else ''}}}

export interface SigninRequest {{
  email: string;
  password: string;
  rememberMe?: boolean;
}}

export interface AuthError {{
  error: string;
  code: string;
  details?: Record<string, any>;
}}

export interface AuthResponse {{
  user: User;
  session: Session;
}}
'''

def generate_routes_ts():
    """Generate routes.ts with Better-Auth route handlers"""
    return '''import { auth } from "./config";
import { toNodeHandler } from "better-auth/node";

export const authHandler = toNodeHandler(auth);
export { auth };
'''

def generate_middleware_ts():
    """Generate middleware.ts for session management"""
    return '''import { auth } from "./config";
import type { User, Session } from "./types";

export interface SessionRequest {
  user?: User;
  session?: Session;
}

export async function getSessionFromRequest(
  req: any
): Promise<{ user: User | null; session: Session | null }> {
  try {
    const cookies = req.headers.cookie || "";
    const sessionToken = parseCookie(cookies, "better-auth.session_token");

    if (!sessionToken) {
      return { user: null, session: null };
    }

    const sessionData = await auth.api.getSession({
      headers: req.headers,
    });

    if (!sessionData) {
      return { user: null, session: null };
    }

    return {
      user: sessionData.user as User,
      session: sessionData.session as Session,
    };
  } catch (error) {
    console.error("Session validation error:", error);
    return { user: null, session: null };
  }
}

function parseCookie(cookieHeader: string, name: string): string | null {
  const cookies = cookieHeader.split(";").map((c) => c.trim());
  for (const cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split("=");
    if (cookieName === name) {
      return decodeURIComponent(cookieValue);
    }
  }
  return null;
}

export async function sessionMiddleware(req: any, res: any, next: any) {
  const { user, session } = await getSessionFromRequest(req);
  req.user = user;
  req.session = session;
  next();
}

export async function getSessionForPython(
  cookieHeader: string
): Promise<string> {
  try {
    const sessionToken = parseCookie(cookieHeader, "better-auth.session_token");

    if (!sessionToken) {
      return JSON.stringify({ user: null, session: null });
    }

    const mockRequest = {
      headers: {
        cookie: cookieHeader,
      },
    };

    const sessionData = await auth.api.getSession({
      headers: mockRequest.headers,
    });

    if (!sessionData) {
      return JSON.stringify({ user: null, session: null });
    }

    return JSON.stringify({
      user: sessionData.user,
      session: sessionData.session,
    });
  } catch (error) {
    console.error("Session validation error:", error);
    return JSON.stringify({ user: null, session: null, error: error.message });
  }
}
'''

def generate_jwt_ts():
    """Generate jwt.ts for JWT token generation"""
    return '''import jwt from "jsonwebtoken";
import type { User } from "./types";

const JWT_SECRET = process.env.JWT_SECRET || process.env.BETTER_AUTH_SECRET || "fallback-secret";
const JWT_EXPIRY = "7d";

export function generateJWT(user: User): string {
  const payload = {
    sub: user.id,
    email: user.email,
    name: user.name,
  };

  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: JWT_EXPIRY,
    issuer: "better-auth",
  });
}

export function verifyJWT(token: string): any {
  try {
    return jwt.verify(token, JWT_SECRET, {
      issuer: "better-auth",
    });
  } catch (error) {
    console.error("JWT verification error:", error);
    return null;
  }
}
'''

def generate_server_ts(port: int = 3001):
    """Generate server.ts for standalone HTTP server"""
    return f'''#!/usr/bin/env node
import http from "http";
import {{ authHandler }} from "./routes";
import {{ getSessionForPython }} from "./middleware";
import {{ generateJWT }} from "./jwt";
import {{ auth }} from "./config";
import * as dotenv from "dotenv";

dotenv.config();

const PORT = process.env.AUTH_SERVER_PORT || {port};
const HOST = process.env.AUTH_SERVER_HOST || "0.0.0.0";

const rateLimitStore = new Map<string, {{ count: number; resetTime: number }}>();
const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes
const RATE_LIMIT_MAX_REQUESTS = 5;

function checkRateLimit(ip: string, path: string): {{ allowed: boolean; retryAfter?: number }} {{
  if (!path.startsWith("/api/auth/sign-in") && !path.startsWith("/api/auth/sign-up")) {{
    return {{ allowed: true }};
  }}

  const key = `${{ip}}:${{path}}`;
  const now = Date.now();
  const record = rateLimitStore.get(key);

  if (!record || now > record.resetTime) {{
    rateLimitStore.set(key, {{
      count: 1,
      resetTime: now + RATE_LIMIT_WINDOW_MS,
    }});
    return {{ allowed: true }};
  }}

  if (record.count >= RATE_LIMIT_MAX_REQUESTS) {{
    const retryAfter = Math.ceil((record.resetTime - now) / 1000);
    return {{ allowed: false, retryAfter }};
  }}

  record.count++;
  rateLimitStore.set(key, record);
  return {{ allowed: true }};
}}

setInterval(() => {{
  const now = Date.now();
  for (const [key, record] of rateLimitStore.entries()) {{
    if (now > record.resetTime) {{
      rateLimitStore.delete(key);
    }}
  }}
}}, 60 * 60 * 1000);

const server = http.createServer(async (req, res) => {{
  const allowedOrigins = process.env.ALLOWED_ORIGINS
    ? process.env.ALLOWED_ORIGINS.split(',').map(origin => origin.trim())
    : ["http://localhost:3000"];

  const origin = req.headers.origin || "";
  const isOriginAllowed = allowedOrigins.includes(origin);

  if (isOriginAllowed) {{
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Credentials", "true");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, Cookie, Set-Cookie");
    res.setHeader("Access-Control-Expose-Headers", "Set-Cookie");
  }}

  if (req.method === "OPTIONS") {{
    res.writeHead(204);
    res.end();
    return;
  }}

  if (req.url === "/health") {{
    res.writeHead(200, {{ "Content-Type": "application/json" }});
    res.end(JSON.stringify({{ status: "healthy", service: "auth-service" }}));
    return;
  }}

  if (req.url === "/api/auth/jwt" && req.method === "GET") {{
    try {{
      const sessionData = await auth.api.getSession({{
        headers: req.headers,
      }});

      if (!sessionData || !sessionData.user) {{
        res.writeHead(401, {{ "Content-Type": "application/json" }});
        res.end(JSON.stringify({{ error: "Unauthorized - no valid session" }}));
        return;
      }}

      const token = generateJWT(sessionData.user);

      res.writeHead(200, {{ "Content-Type": "application/json" }});
      res.end(JSON.stringify({{
        token,
        user: sessionData.user,
        expiresIn: "7d"
      }}));
    }} catch (error) {{
      console.error("JWT generation error:", error);
      res.writeHead(500, {{ "Content-Type": "application/json" }});
      res.end(JSON.stringify({{ error: "Failed to generate JWT" }}));
    }}
    return;
  }}

  if (req.url === "/api/validate-session") {{
    try {{
      const cookieHeader = req.headers.cookie || "";
      const sessionData = await getSessionForPython(cookieHeader);
      res.writeHead(200, {{ "Content-Type": "application/json" }});
      res.end(sessionData);
    }} catch (error) {{
      console.error("Session validation error:", error);
      res.writeHead(500, {{ "Content-Type": "application/json" }});
      res.end(JSON.stringify({{ error: "Session validation failed" }}));
    }}
    return;
  }}

  if (req.url?.startsWith("/api/auth")) {{
    try {{
      const clientIp = req.headers["x-forwarded-for"] || req.socket.remoteAddress || "unknown";
      const ip = Array.isArray(clientIp) ? clientIp[0] : clientIp.split(",")[0];
      const rateLimit = checkRateLimit(ip, req.url);

      if (!rateLimit.allowed) {{
        res.writeHead(429, {{
          "Content-Type": "application/json",
          "Retry-After": rateLimit.retryAfter?.toString() || "900",
        }});
        res.end(
          JSON.stringify({{
            error: "Too many requests",
            message: "Too many authentication attempts. Please try again later.",
            retryAfter: rateLimit.retryAfter,
          }})
        );
        return;
      }}

      await authHandler(req, res);
    }} catch (error) {{
      console.error("Auth handler error:", error);
      res.writeHead(500, {{ "Content-Type": "application/json" }});
      res.end(JSON.stringify({{ error: "Internal server error" }}));
    }}
    return;
  }}

  res.writeHead(404, {{ "Content-Type": "application/json" }});
  res.end(JSON.stringify({{ error: "Not found" }}));
}});

server.listen(Number(PORT), HOST, () => {{
  console.log(`🔐 Auth Service running on http://${{HOST}}:${{PORT}}`);
  console.log(`   Auth endpoints: http://${{HOST}}:${{PORT}}/api/auth/*`);
  console.log(`   JWT endpoint: http://${{HOST}}:${{PORT}}/api/auth/jwt`);
  console.log(`   Session validation: http://${{HOST}}:${{PORT}}/api/validate-session`);
  console.log(`   Health check: http://${{HOST}}:${{PORT}}/health`);
}});

process.on("SIGTERM", () => {{
  console.log("SIGTERM signal received: closing HTTP server");
  server.close(() => {{
    console.log("HTTP server closed");
    process.exit(0);
  }});
}});

process.on("SIGINT", () => {{
  console.log("SIGINT signal received: closing HTTP server");
  server.close(() => {{
    console.log("HTTP server closed");
    process.exit(0);
  }});
}});
'''

def generate_drizzle_config():
    """Generate drizzle.config.ts for database migrations"""
    return '''import type { Config } from "drizzle-kit";
import * as dotenv from "dotenv";

dotenv.config();

export default {
  schema: "./node_modules/better-auth/dist/db/schema.js",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
} satisfies Config;
'''

def generate_tsconfig():
    """Generate tsconfig.json for TypeScript"""
    return {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "moduleResolution": "node"
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }

def generate_env_template(database_url: str = ""):
    """Generate .env.template file"""
    return f'''# Database
DATABASE_URL={database_url or "postgresql://user:password@localhost:5432/dbname"}

# Better-Auth Configuration
BETTER_AUTH_SECRET=your-32-char-secret-key-here
BETTER_AUTH_URL=http://localhost:3001

# JWT Configuration
JWT_SECRET=your-jwt-secret-here

# Server Configuration
AUTH_SERVER_PORT=3001
AUTH_SERVER_HOST=0.0.0.0

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8000
'''

def setup_auth_project(project_dir: str, database_url: str, custom_fields: Dict[str, str], port: int, project_name: str):
    """
    Setup complete Better-Auth project structure
    """
    project_path = Path(project_dir).resolve()
    src_path = project_path / "src"

    # Create directories
    src_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Creating Better-Auth project in: {project_path}")

    # Generate and write files
    files_to_create = {
        "package.json": json.dumps(generate_package_json(project_name), indent=2),
        "tsconfig.json": json.dumps(generate_tsconfig(), indent=2),
        "drizzle.config.ts": generate_drizzle_config(),
        ".env.template": generate_env_template(database_url),
        "src/config.ts": generate_config_ts(custom_fields),
        "src/types.ts": generate_types_ts(custom_fields),
        "src/routes.ts": generate_routes_ts(),
        "src/middleware.ts": generate_middleware_ts(),
        "src/jwt.ts": generate_jwt_ts(),
        "src/server.ts": generate_server_ts(port),
    }

    for file_path, content in files_to_create.items():
        full_path = project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        print(f"✅ Created: {file_path}")

    print(f"\n🎉 Better-Auth project setup complete!")
    print(f"\nNext steps:")
    print(f"1. cd {project_path}")
    print(f"2. Copy .env.template to .env and fill in your values")
    print(f"3. npm install")
    print(f"4. npm run migrate  # Setup database tables")
    print(f"5. npm run dev      # Start development server")

def main():
    parser = argparse.ArgumentParser(description="Setup Better-Auth authentication system")
    parser.add_argument("--project-dir", required=True, help="Project directory path")
    parser.add_argument("--database-url", default="", help="PostgreSQL connection string")
    parser.add_argument("--custom-fields", default="", help="Custom user fields (format: field1:type1 field2:type2)")
    parser.add_argument("--port", type=int, default=3001, help="Server port (default: 3001)")
    parser.add_argument("--project-name", default="auth-service", help="Project name for package.json")

    args = parser.parse_args()

    custom_fields = parse_custom_fields(args.custom_fields)

    setup_auth_project(
        project_dir=args.project_dir,
        database_url=args.database_url,
        custom_fields=custom_fields,
        port=args.port,
        project_name=args.project_name
    )

if __name__ == "__main__":
    main()
