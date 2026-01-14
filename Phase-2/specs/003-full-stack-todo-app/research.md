# Research & Technical Decisions: Phase II Full-Stack Todo Web Application

**Feature**: 003-full-stack-todo-app
**Date**: 2026-01-09
**Purpose**: Document technology choices, architectural patterns, and implementation strategies for transforming the console app into a full-stack web application

## Executive Summary

This document captures the research and technical decisions for implementing Phase II of the Todo application. The primary goal is to transform the existing Python console application into a full-stack web system while:
1. Preserving and migrating existing business logic
2. Adding multi-user authentication and data isolation
3. Providing a modern, responsive web interface
4. Maintaining clean architecture and separation of concerns

## Technology Stack Decisions

### 1. Frontend Framework: Next.js 16+ (App Router)

**Decision**: Use Next.js 16+ with App Router, TypeScript, and Tailwind CSS

**Rationale**:
- **App Router**: Modern routing with server components, better performance, and improved developer experience
- **TypeScript**: Type safety reduces bugs and improves developer productivity
- **Tailwind CSS**: Utility-first CSS framework enables rapid UI development with consistent design
- **React Server Components**: Reduces client-side JavaScript bundle, improves initial page load
- **Built-in Optimizations**: Image optimization, code splitting, and static generation out of the box

**Alternatives Considered**:
- **Vite + React**: More lightweight but lacks Next.js features like SSR, routing, and API routes
- **SvelteKit**: Excellent performance but smaller ecosystem and team familiarity concerns
- **Remix**: Strong alternative but Next.js has broader adoption and more resources

**Implementation Notes**:
- Use App Router (`app/` directory) for all routes
- Leverage Server Actions for form submissions
- Use React Server Components by default, client components only when needed
- Implement responsive design with Tailwind breakpoints (sm, md, lg, xl)

---

### 2. Backend Framework: FastAPI (Python)

**Decision**: Use FastAPI with Python 3.11+ for the backend API

**Rationale**:
- **Existing Codebase Reuse**: Current console app is Python-based; can reuse models and business logic
- **FastAPI Performance**: High performance with async support, comparable to Node.js/Go
- **Automatic API Documentation**: OpenAPI/Swagger docs generated automatically
- **Type Safety**: Pydantic models provide runtime validation and editor support
- **Developer Experience**: Excellent DX with automatic validation, serialization, and error handling

**Alternatives Considered**:
- **Django REST Framework**: More batteries-included but heavier, overkill for this scale
- **Flask**: Simpler but lacks async support and modern features
- **Node.js (Express/Fastify)**: Would require rewriting all existing Python logic

**Implementation Notes**:
- Use Pydantic v2 for request/response models
- Implement async route handlers for database operations
- Structure as: routers → services → models
- Enable CORS for frontend communication
- Use dependency injection for database sessions

---

### 3. Authentication: Better Auth (Frontend) + JWT Verification (Backend)

**Decision**: Better Auth handles authentication on the frontend; backend verifies JWT tokens

**Rationale**:
- **Better Auth**: Modern auth library for Next.js with built-in session management
- **JWT Tokens**: Stateless authentication, scalable, and framework-agnostic
- **Separation of Concerns**: Frontend handles user interaction, backend verifies identity
- **Security**: Backend independently verifies tokens, doesn't trust frontend blindly

**Alternatives Considered**:
- **NextAuth.js**: Excellent but Better Auth is more modern and lightweight
- **Auth0/Clerk**: SaaS solutions add cost and external dependencies
- **Backend-only auth (sessions)**: Requires session storage, less scalable

**Implementation Strategy**:
1. **Frontend (Better Auth)**:
   - Handles signup/signin UI and flows
   - Stores JWT tokens securely (httpOnly cookies preferred)
   - Includes JWT in Authorization header for API requests
   - Manages session refresh

2. **Backend (FastAPI)**:
   - Verifies JWT signature and expiration
   - Extracts user ID from valid tokens
   - Uses dependency injection to inject authenticated user into routes
   - Rejects invalid/expired tokens with 401 Unauthorized

**Security Considerations**:
- Use RS256 or HS256 for JWT signing
- Store JWT secret securely (environment variables)
- Implement token expiration (e.g., 24 hours) with refresh mechanism
- Hash passwords with bcrypt (handled by Better Auth)

---

### 4. Database: Neon Serverless PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL with SQLModel ORM

**Rationale**:
- **Serverless**: Auto-scaling, pay-per-use, zero ops for database management
- **PostgreSQL**: Robust, mature, supports complex queries and JSON
- **SQLModel**: Combines Pydantic and SQLAlchemy, type-safe ORM for FastAPI
- **Free Tier**: Generous free tier for development and low-traffic apps
- **Connection Pooling**: Built-in connection pooling for serverless environments

**Alternatives Considered**:
- **SQLite**: Too limited for multi-user, production-grade application
- **MongoDB**: NoSQL not ideal for structured task data with relationships
- **Supabase**: Good alternative but Neon is simpler (just database, no auth overhead)

**Migration Strategy**:
- Transform in-memory data structures to database tables
- Preserve existing business logic in service layer
- Use SQLModel models that mirror Pydantic models
- Implement indexes for user_id and common query patterns

---

### 5. ORM and Data Access: SQLModel

**Decision**: Use SQLModel for database interactions

**Rationale**:
- **Type Safety**: Integrates Pydantic models with SQLAlchemy
- **FastAPI Integration**: Seamless with FastAPI's dependency injection
- **Validation**: Combines ORM with request/response validation
- **Familiar**: Similar patterns to existing Pydantic usage

**Alternatives Considered**:
- **Raw SQLAlchemy**: More powerful but more boilerplate
- **Prisma Python**: Newer, less mature than SQLModel
- **Tortoise ORM**: Async-first but smaller ecosystem

**Implementation Notes**:
- Define models with both Pydantic and SQLModel features
- Use async session management
- Implement repository pattern if needed for complex queries

---

## Architectural Patterns

### 1. Monorepo Structure

**Decision**: Use monorepo with `/frontend` and `/backend` directories

**Rationale**:
- **Colocation**: Related code lives together, easier to coordinate changes
- **Shared Types**: Can potentially share TypeScript types between frontend/backend
- **Single Repository**: Simpler CI/CD, versioning, and dependency management

**Structure**:
```
Todo-app/Phase-2/
├── frontend/          # Next.js application
│   ├── app/          # App Router pages and layouts
│   ├── components/   # React components
│   ├── lib/          # Utilities and API client
│   ├── public/       # Static assets
│   └── package.json
├── backend/          # FastAPI application
│   ├── src/
│   │   ├── api/      # Route handlers (routers)
│   │   ├── models/   # SQLModel database models
│   │   ├── services/ # Business logic layer
│   │   ├── auth/     # JWT verification middleware
│   │   └── main.py   # FastAPI app entry
│   ├── tests/
│   └── pyproject.toml
├── specs/            # Specifications and documentation
└── .claude/          # Claude Code agents and skills
```

---

### 2. Backend Architecture: Three-Layer Pattern

**Decision**: Implement Router → Service → Model architecture

**Layers**:
1. **Routers (API Layer)**:
   - HTTP request handling
   - Input validation (Pydantic)
   - Authentication/authorization checks
   - Response formatting

2. **Services (Business Logic)**:
   - Reuse existing console app logic
   - Task CRUD operations
   - Filtering, sorting, search logic
   - Recurring task generation
   - User data isolation enforcement

3. **Models (Data Layer)**:
   - SQLModel definitions for database tables
   - Relationships (User → Tasks)
   - Validation rules

**Rationale**:
- **Separation of Concerns**: Clear boundaries between layers
- **Testability**: Each layer can be tested independently
- **Reusability**: Service layer reused across different interfaces
- **Migration Path**: Existing console app services can be adapted

---

### 3. Frontend Architecture: Feature-Based Components

**Decision**: Organize components by feature with shared UI components

**Structure**:
```
frontend/src/
├── app/              # App Router pages
│   ├── (auth)/      # Auth route group
│   │   ├── login/
│   │   └── signup/
│   └── (app)/       # Protected app routes
│       ├── dashboard/
│       └── tasks/
├── components/
│   ├── features/    # Feature-specific components
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── filters/
│   └── ui/          # Shared UI components (buttons, cards, etc.)
├── lib/
│   ├── api/         # API client for backend
│   ├── auth/        # Better Auth configuration
│   └── utils/       # Utility functions
└── types/           # TypeScript types
```

**Rationale**:
- **Scalability**: Easy to add new features without affecting existing code
- **Colocation**: Related components and logic live together
- **Reusability**: Shared UI components prevent duplication

---

### 4. API Design: RESTful Endpoints

**Decision**: Use REST architecture with resource-based URLs

**Resource**: Tasks

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/tasks` | List all tasks for authenticated user | Yes |
| POST | `/api/tasks` | Create a new task | Yes |
| GET | `/api/tasks/{id}` | Get a specific task | Yes |
| PUT | `/api/tasks/{id}` | Update a task | Yes |
| DELETE | `/api/tasks/{id}` | Delete a task | Yes |
| PATCH | `/api/tasks/{id}/complete` | Mark task complete | Yes |

**Query Parameters** (GET `/api/tasks`):
- `status`: filter by "pending" | "completed" | "all"
- `priority`: filter by "low" | "medium" | "high"
- `category`: filter by category string
- `search`: keyword search in title/description
- `sort_by`: "created" | "title" | "priority" | "due_date"
- `sort_order`: "asc" | "desc"

**Rationale**:
- **Standard REST**: Familiar patterns, predictable URLs
- **Filtering on Server**: Reduces data transfer, better performance
- **HTTP Semantics**: Use proper HTTP methods and status codes

**Alternatives Considered**:
- **GraphQL**: Overkill for this simple CRUD app, adds complexity
- **tRPC**: TypeScript-specific, would lock us into TS on backend

---

### 5. State Management: React Server Components + URL State

**Decision**: Minimize client-side state, use Server Components and URL params

**Strategy**:
- **Server Components** (default): Fetch data on server, reduces client JS
- **URL State**: Store filters/sort in URL params (shareable, bookmarkable)
- **Client Components**: Only for interactive elements (forms, modals, filters)
- **No Global State Library**: Avoid Redux/Zustand unless absolutely needed

**Rationale**:
- **Simplicity**: Less state management code, fewer bugs
- **Performance**: Server Components reduce client bundle size
- **SEO**: Server-rendered content is indexable
- **User Experience**: URL state enables sharing and browser history

**When to Use Client State**:
- Form inputs and validation
- UI state (modal open/closed, selected items)
- Optimistic updates for better UX

---

## Code Reuse Strategy

### Migrating Existing Console App Logic

**Current Console App Structure**:
```
src/
├── models/task.py       # Task dataclass
├── services/task_manager.py  # Business logic
└── cli/                 # Console interface
```

**Migration Plan**:

1. **Models (Task)**:
   - Current: Python `@dataclass` with in-memory storage
   - Target: SQLModel with database persistence
   - **Reuse**: Field definitions, validation logic, enums (Priority, Recurrence)
   - **Changes**: Add `id` (auto-increment), `user_id` (foreign key), timestamps

2. **Services (TaskManager)**:
   - Current: Methods like `add_task()`, `update_task()`, `filter_tasks()`, etc.
   - Target: FastAPI service layer
   - **Reuse**: ~80% of business logic (filtering, sorting, search, recurring task generation)
   - **Changes**:
     - Replace in-memory storage with database queries
     - Add `user_id` parameter to all methods
     - Make methods async for database operations
     - Add user data isolation checks

3. **CLI Layer**:
   - Current: Console menus and display logic
   - Target: Not migrated (replaced by web UI)
   - **Reuse**: None (console-specific)

**Code Reuse Examples**:

**Example 1: Task Validation**
```python
# REUSE: Validation logic from console app
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: Priority = Priority.MEDIUM
    category: str | None = None
    due_date: date | None = None
    recurrence: Recurrence = Recurrence.NONE
    completed: bool = False
```

**Example 2: Recurring Task Logic**
```python
# REUSE: Existing logic for calculating next due date
def calculate_next_due_date(current_due: date, recurrence: Recurrence) -> date:
    """Calculate next due date based on recurrence pattern"""
    # [Existing logic from console app can be copied directly]
```

**Example 3: Filtering Logic**
```python
# ADAPT: Add user_id filtering
async def filter_tasks(
    user_id: str,  # NEW: user data isolation
    status: str | None = None,
    priority: Priority | None = None,
    category: str | None = None,
    search: str | None = None
) -> list[Task]:
    # Base query with user isolation
    query = select(Task).where(Task.user_id == user_id)

    # REUSE: Existing filter logic
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    if priority:
        query = query.where(Task.priority == priority)

    # ... rest of filtering logic
```

---

## Authentication Implementation Details

### Frontend (Better Auth Setup)

**Configuration**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: {
    // Neon PostgreSQL connection
    url: process.env.DATABASE_URL,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,  // Start simple
  },
  session: {
    expiresIn: 60 * 60 * 24,  // 24 hours
    updateAge: 60 * 60,        // Refresh every hour
  },
})
```

**API Client with Auth**:
```typescript
// lib/api/client.ts
export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const session = await getSession();  // Better Auth helper

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session?.accessToken}`,
      ...options?.headers,
    },
  });

  if (response.status === 401) {
    // Handle unauthorized (redirect to login)
    redirect('/login');
  }

  return response.json();
}
```

---

### Backend (JWT Verification)

**JWT Dependency**:
```python
# src/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> str:
    """Extract and verify JWT token, return user_id"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

**Route Protection**:
```python
# src/api/tasks.py
@router.get("/api/tasks")
async def list_tasks(
    user_id: str = Depends(get_current_user),  # Auto-inject authenticated user
    status: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """List tasks for authenticated user only"""
    tasks = await task_service.get_user_tasks(db, user_id, status)
    return tasks
```

---

## Performance Considerations

### 1. Database Indexing

**Required Indexes**:
```sql
-- User lookup (most common query)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Filtering by status
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Filtering by priority
CREATE INDEX idx_tasks_priority ON tasks(priority);

-- Due date queries (overdue, due today)
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- Composite index for common query patterns
CREATE INDEX idx_tasks_user_status ON tasks(user_id, completed);
```

**Rationale**: Indexing user_id is critical since every query filters by user

---

### 2. Query Optimization

**N+1 Problem Prevention**:
- Use SQLModel `selectinload()` for relationships if needed
- Batch queries instead of individual fetches
- Limit result sets (pagination for large task lists)

**Example**:
```python
# Good: Single query with filters
query = select(Task).where(
    Task.user_id == user_id,
    Task.completed == False
).limit(100)

# Bad: Fetching all then filtering in Python
tasks = await db.execute(select(Task))
user_tasks = [t for t in tasks if t.user_id == user_id]  # Don't do this!
```

---

### 3. Frontend Performance

**Code Splitting**:
- Use Next.js dynamic imports for heavy components
- Lazy load non-critical features (filters, modals)

**Caching**:
- Use Next.js `fetch()` with `cache` option for data requests
- Implement SWR or React Query for optimistic updates

**Bundle Size**:
- Monitor bundle size (target < 500KB gzipped)
- Use tree-shaking (import only what's needed)

---

## Security Best Practices

### 1. Input Validation

**Frontend**:
- Validate user inputs before submission
- Use Zod or yup for form validation
- Sanitize display of user-generated content

**Backend**:
- Never trust frontend validation
- Use Pydantic models for request validation
- Implement max length constraints
- Sanitize inputs to prevent SQL injection (SQLModel handles this)

---

### 2. XSS Prevention

**Frontend**:
- React escapes by default (use `dangerouslySetInnerHTML` carefully)
- Sanitize any HTML content if rich text is added later

**Backend**:
- Return JSON, not HTML
- Set proper CORS headers

---

### 3. CSRF Protection

**Strategy**:
- Use httpOnly cookies for JWT storage (prevents XSS)
- Implement SameSite cookie attribute
- Better Auth handles CSRF tokens automatically

---

### 4. Rate Limiting

**Backend**:
- Implement rate limiting middleware (e.g., slowapi)
- Limit login attempts to prevent brute force
- Rate limit API endpoints (e.g., 100 requests/minute per user)

**Example**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/api/tasks")
@limiter.limit("10/minute")
async def create_task(...):
    ...
```

---

## Error Handling Strategy

### Frontend

**Error Types**:
1. **Network Errors**: Show retry button
2. **Validation Errors**: Display field-specific messages
3. **Auth Errors**: Redirect to login
4. **Server Errors**: Show generic error message

**Implementation**:
```typescript
try {
  const task = await createTask(data);
} catch (error) {
  if (error instanceof ValidationError) {
    setFieldErrors(error.fields);
  } else if (error instanceof AuthError) {
    redirect('/login');
  } else {
    toast.error('Something went wrong. Please try again.');
  }
}
```

---

### Backend

**HTTP Status Codes**:
- `200 OK`: Successful GET/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Missing/invalid token
- `403 Forbidden`: Authenticated but not allowed
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Unexpected errors

**Error Response Format**:
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "title",
      "message": "Title must be between 1 and 200 characters"
    }
  ]
}
```

---

## Testing Strategy

### Backend Testing

**Unit Tests** (pytest):
- Test service layer methods
- Mock database queries
- Test authentication helpers
- Test recurring task logic

**Integration Tests**:
- Test API endpoints with TestClient
- Use in-memory SQLite for testing
- Test authentication flow
- Test user data isolation

**Example**:
```python
def test_user_can_only_see_own_tasks():
    """Verify user data isolation"""
    # Create two users with tasks
    user1_task = create_task(user_id="user1", title="User 1 Task")
    user2_task = create_task(user_id="user2", title="User 2 Task")

    # User 1 should only see their task
    response = client.get("/api/tasks", headers={"Authorization": f"Bearer {user1_token}"})
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "User 1 Task"
```

---

### Frontend Testing

**Component Tests** (Jest + React Testing Library):
- Test form submissions
- Test task list rendering
- Test filter interactions

**E2E Tests** (Playwright/Cypress):
- Test full user flows (signup → create task → mark complete)
- Test authentication (login/logout)
- Test responsive design on different viewports

---

## Deployment Strategy

### Development Environment

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

**Backend**:
```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload  # Runs on http://localhost:8000
```

---

### Production Considerations

**Frontend**:
- Deploy to Vercel (optimal for Next.js)
- Environment variables for API URL
- Enable production optimizations (minification, compression)

**Backend**:
- Deploy to Railway, Render, or fly.io
- Use gunicorn + uvicorn workers
- Environment variables for JWT secret, database URL
- Enable HTTPS

**Database**:
- Neon production branch
- Enable connection pooling
- Regular backups

---

## Open Questions & Risks

### Questions
1. **Session Duration**: Should we implement refresh tokens for extended sessions?
2. **Password Reset**: Do we need password reset functionality in this phase?
3. **Email Verification**: Should we require email verification for signups?
4. **Pagination**: At what task count should we implement pagination?

### Risks
1. **Better Auth Compatibility**: Better Auth is relatively new; may encounter undocumented issues
2. **Database Connection Limits**: Neon free tier has connection limits; may need connection pooling
3. **CORS Configuration**: Need to ensure CORS is properly configured for dev/prod
4. **Token Storage**: Need to decide between localStorage (XSS risk) vs httpOnly cookies (CSRF consideration)

---

## Next Steps

1. **Phase 1 (Data Model)**: Define SQLModel schemas for User and Task entities
2. **Phase 1 (Contracts)**: Create OpenAPI spec for all API endpoints
3. **Phase 1 (Quickstart)**: Document local development setup
4. **Phase 2 (Tasks)**: Break down implementation into testable tasks

---

## References

- [Better Auth Documentation](https://better-auth.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js App Router](https://nextjs.org/docs/app)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
- [Neon Serverless Postgres](https://neon.tech/docs)
