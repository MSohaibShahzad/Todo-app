# Implementation Plan: Phase II – Full-Stack Todo Web Application

**Branch**: `003-full-stack-todo-app` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-full-stack-todo-app/spec.md`

## Summary

Transform the existing Python console Todo application into a full-stack web application with multi-user support while preserving all Phase-1 functionality (CRUD, priorities, categories, due dates, recurring tasks, search/filter/sort). The system will use a monorepo structure with Next.js 16+ frontend and FastAPI backend, authenticated via Better Auth with JWT tokens, and persisted in Neon PostgreSQL.

**Key Objectives**:
1. Migrate in-memory task logic to database-backed persistence
2. Add multi-user authentication and data isolation
3. Provide responsive web interface accessible from any device
4. Reuse ~80% of existing business logic from console app
5. Maintain clean separation between frontend, backend, and auth concerns

## Technical Context

**Frontend**:
- Language/Version: TypeScript 5.x with Node.js 18.17+
- Framework: Next.js 16+ (App Router)
- Styling: Tailwind CSS 3.x
- Auth: Better Auth with JWT
- Testing: Jest + React Testing Library, Playwright (E2E)
- Target Platform: Modern browsers (Chrome, Firefox, Safari, Edge)

**Backend**:
- Language/Version: Python 3.11+
- Framework: FastAPI 0.110+
- ORM: SQLModel (Pydantic + SQLAlchemy)
- Testing: pytest with async support
- Server: Uvicorn (ASGI)
- Target Platform: Linux server (or serverless)

**Database**:
- Storage: Neon Serverless PostgreSQL
- Migrations: Alembic
- Connection: SQLModel with async session

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- API response time: <500ms (p95)
- Page load time: <3s on 3G connection
- Search/filter operations: <1s for 1000 tasks
- Support 100 concurrent users without degradation

**Constraints**:
- Must preserve all Phase-1 features
- 100% user data isolation (users can only see own tasks)
- Responsive design (320px mobile to 1920px desktop)
- No third-party auth providers (email/password only via Better Auth)

**Scale/Scope**:
- Target: Small to medium user base (100-1000 users)
- Per-user task limit: ~1000 tasks (with pagination if needed)
- 7 API endpoints + health check
- ~15-20 React components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Applicable Principles (from console app constitution - adapted for web)

**✓ Simplicity First**:
- Use standard patterns (REST API, JWT auth, conventional Next.js structure)
- No over-engineering: Start with single database, no microservices
- External services limited to: Better Auth, Neon PostgreSQL
- **Status**: PASS - Minimal dependencies, proven technologies

**✓ Clean Code**:
- Frontend: TypeScript with strict mode, ESLint
- Backend: Python with type hints, mypy strict, ruff linting
- Descriptive naming, clear separation of concerns
- **Status**: PASS - Enforced via tooling

**✓ Test-Driven Development**:
- Backend: TDD with pytest (services first, then routes)
- Frontend: Component tests before implementation
- Integration tests for auth flow and CRUD operations
- **Status**: PASS - Same TDD approach as console app

**✓ Separation of Concerns**:
- Frontend: Components (UI) → API Client (fetch) → Backend
- Backend: Routers (HTTP) → Services (logic) → Models (data)
- Auth: Better Auth (frontend) → JWT verification (backend middleware)
- **Status**: PASS - Clear layer boundaries

**✓ Incremental Complexity**:
- Phase-1 (console): CRUD + advanced features ✅ COMPLETED
- Phase-2 (web): Same features + auth + persistence + web UI
- Phase-3 (future): AI chatbot integration
- **Status**: PASS - Building on proven foundation

### New Principles (Web-Specific)

**✓ API Contract First**:
- Define OpenAPI spec before implementation
- Frontend and backend develop against contract
- **Status**: PASS - See [contracts/openapi.yaml](./contracts/openapi.yaml)

**✓ Security by Design**:
- JWT verification on every endpoint
- User data isolation enforced at database query level
- Input validation on both frontend and backend
- **Status**: PASS - Security requirements in spec (FR-037 to FR-042)

**✓ Responsive Design**:
- Mobile-first approach with Tailwind breakpoints
- Test on 320px (mobile), 768px (tablet), 1920px (desktop)
- **Status**: PASS - FR-033, SC-005

### Gates Evaluation

**GATE 1: No violations** - All principles satisfied with justified complexity
**GATE 2: Re-check after implementation** - Verify no architectural drift

## Complexity Tracking

*No violations requiring justification. All complexity is necessary for multi-user web application.*

## Project Structure

### Documentation (this feature)

```text
specs/003-full-stack-todo-app/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file - implementation plan
├── research.md          # Phase 0 output - tech decisions (COMPLETED)
├── data-model.md        # Phase 1 output - database schema (COMPLETED)
├── quickstart.md        # Phase 1 output - local dev setup (COMPLETED)
├── contracts/           # Phase 1 output - API contracts (COMPLETED)
│   ├── openapi.yaml    # OpenAPI 3.1 specification
│   └── README.md       # Contract documentation
└── checklists/          # Quality validation
    └── requirements.md  # Spec quality checklist (COMPLETED)
```

### Source Code (repository root)

```text
Phase-2/
├── frontend/                # Next.js application
│   ├── app/                # App Router pages and layouts
│   │   ├── (auth)/         # Auth route group (public)
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   ├── (app)/          # Protected app routes
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   └── tasks/
│   │   │       ├── page.tsx
│   │   │       ├── [id]/
│   │   │       │   └── page.tsx
│   │   │       └── new/
│   │   │           └── page.tsx
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Home/landing page
│   ├── components/         # React components
│   │   ├── features/       # Feature-specific components
│   │   │   ├── auth/       # Login, signup forms
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── SignupForm.tsx
│   │   │   ├── tasks/      # Task components
│   │   │   │   ├── TaskList.tsx
│   │   │   │   ├── TaskCard.tsx
│   │   │   │   ├── TaskForm.tsx
│   │   │   │   └── TaskFilters.tsx
│   │   │   └── dashboard/  # Dashboard components
│   │   │       ├── StatsCard.tsx
│   │   │       └── TaskSummary.tsx
│   │   └── ui/             # Shared UI components
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       ├── Select.tsx
│   │       └── Modal.tsx
│   ├── lib/                # Utilities and services
│   │   ├── api/            # API client
│   │   │   ├── client.ts   # Base fetch wrapper with auth
│   │   │   └── tasks.ts    # Task API functions
│   │   ├── auth/           # Better Auth config
│   │   │   └── config.ts
│   │   ├── hooks/          # Custom React hooks
│   │   │   ├── useTasks.ts
│   │   │   └── useAuth.ts
│   │   └── utils/          # Helper functions
│   │       ├── dates.ts
│   │       └── cn.ts       # Tailwind merge utility
│   ├── types/              # TypeScript types
│   │   ├── task.ts
│   │   └── api.ts
│   ├── public/             # Static assets
│   │   ├── favicon.ico
│   │   └── images/
│   ├── .env.local          # Environment variables (gitignored)
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── backend/                # FastAPI application
│   ├── src/
│   │   ├── api/            # Route handlers (routers)
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py    # Task endpoints
│   │   │   └── health.py   # Health check
│   │   ├── models/         # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py     # User model
│   │   │   └── task.py     # Task model
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   └── task.py     # TaskCreate, TaskUpdate, TaskResponse
│   │   ├── services/       # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── task_service.py     # Task CRUD, filtering, sorting
│   │   │   └── recurrence_service.py  # Recurring task logic
│   │   ├── auth/           # JWT verification
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py  # get_current_user dependency
│   │   │   └── jwt.py      # JWT decode/verify utilities
│   │   ├── database.py     # Database session management
│   │   ├── config.py       # Settings (env vars)
│   │   └── main.py         # FastAPI app entry point
│   ├── tests/              # Backend tests
│   │   ├── conftest.py     # Pytest fixtures
│   │   ├── unit/           # Unit tests (services, utilities)
│   │   │   ├── test_task_service.py
│   │   │   └── test_recurrence.py
│   │   ├── integration/    # Integration tests (API endpoints)
│   │   │   ├── test_auth_flow.py
│   │   │   ├── test_task_crud.py
│   │   │   └── test_data_isolation.py
│   │   └── fixtures/       # Test data fixtures
│   ├── alembic/            # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── .env                # Environment variables (gitignored)
│   ├── alembic.ini         # Alembic configuration
│   ├── pyproject.toml      # Python dependencies (uv)
│   └── README.md
│
├── specs/                  # Specifications and documentation
│   └── 003-full-stack-todo-app/  # This feature
│
└── .claude/                # Claude Code agents and skills
    ├── agents/             # Custom agents
    └── skills/             # Custom skills
```

**Structure Decision**: Monorepo with frontend/ and backend/ directories. This structure:
- Keeps related code together
- Simplifies deployment (single repository)
- Allows for potential shared types in the future (via code generation)
- Clear separation between client and server concerns

## Phase 0: Research & Technical Decisions

**Status**: ✅ COMPLETED

**Output**: [research.md](./research.md)

**Key Decisions Documented**:
1. **Frontend**: Next.js 16+ (App Router) with TypeScript and Tailwind CSS
2. **Backend**: FastAPI with SQLModel ORM
3. **Database**: Neon Serverless PostgreSQL
4. **Authentication**: Better Auth (frontend) + JWT verification (backend)
5. **Architecture**: Three-layer backend (Router → Service → Model), feature-based frontend components
6. **API Design**: RESTful with 7 endpoints, query-based filtering
7. **Code Reuse**: ~80% of Phase-1 business logic reusable with modifications for persistence and multi-user

## Phase 1: Design & Contracts

**Status**: ✅ COMPLETED

### Data Model

**Output**: [data-model.md](./data-model.md)

**Entities**:
- **User**: id (TEXT PK), email (UNIQUE), name, created_at, updated_at
- **Task**: id (INT PK), user_id (FK), title, description, completed, priority, category, due_date, recurrence, created_at, updated_at

**Relationships**:
- User → Tasks (1:N with CASCADE delete)

**Indexes**:
- `idx_tasks_user_id` (critical for multi-tenant queries)
- `idx_tasks_completed` (status filtering)
- `idx_tasks_priority` (priority filtering)
- `idx_tasks_due_date` (overdue/due-today queries)
- `idx_tasks_user_status` (composite index for common pattern)

**Enums**:
- `Priority`: low, medium, high
- `Recurrence`: none, daily, weekly, monthly

### API Contracts

**Output**: [contracts/openapi.yaml](./contracts/openapi.yaml), [contracts/README.md](./contracts/README.md)

**Endpoints**:
1. `GET /health` - Health check (no auth)
2. `GET /api/tasks` - List tasks with filtering/sorting
3. `POST /api/tasks` - Create task
4. `GET /api/tasks/{id}` - Get specific task
5. `PUT /api/tasks/{id}` - Update task
6. `DELETE /api/tasks/{id}` - Delete task
7. `PATCH /api/tasks/{id}/complete` - Toggle completion (handles recurring tasks)
8. `GET /api/tasks/summary` - Get task statistics

**Authentication**: Bearer JWT in `Authorization` header for all `/api/*` endpoints

### Quickstart Guide

**Output**: [quickstart.md](./quickstart.md)

**Contents**:
- Prerequisites and installation steps
- Database setup (Neon PostgreSQL)
- Backend setup and running
- Frontend setup and running
- Development workflow
- Troubleshooting guide

### Agent Context Update

**Status**: ⏭️ SKIPPED (Manual update not required for this workflow)

## Phase 2: Implementation Tasks

**Status**: ⏭️ NEXT STEP - Use `/sp.tasks` command

**Note**: Implementation tasks will be generated by `/sp.tasks` command based on this plan. Tasks will be broken down into testable units following TDD approach (Red-Green-Refactor).

**Expected Task Categories**:
1. **Backend Core** (10-15 tasks):
   - Database models and migrations
   - Service layer (reuse from console app)
   - API routes with authentication
   - JWT verification middleware
   - Testing (unit + integration)

2. **Frontend Core** (15-20 tasks):
   - Better Auth setup
   - API client with auth headers
   - Authentication pages (login/signup)
   - Task CRUD components
   - Filtering and search UI
   - Responsive layouts

3. **Integration & Testing** (5-8 tasks):
   - End-to-end auth flow
   - User data isolation verification
   - Recurring task behavior
   - Error handling and edge cases

## Implementation Strategy

### Code Reuse from Phase-1 Console App

**High Reuse (80-90%)**:
- ✅ Task model validation logic (field constraints, enums)
- ✅ Filtering logic (status, priority, category)
- ✅ Sorting logic (by date, title, priority)
- ✅ Search logic (keyword matching)
- ✅ Recurring task calculation (next due date logic)
- ✅ Priority and recurrence enums

**Moderate Reuse (50-70% with modifications)**:
- 🔧 CRUD operations (add `user_id`, make async, use database)
- 🔧 Task creation (add timestamps, auto-increment ID)
- 🔧 Task completion (add recurring task creation logic)

**No Reuse (0%)**:
- ❌ CLI interface (replaced by web UI)
- ❌ In-memory storage (replaced by PostgreSQL)
- ❌ Menu system (replaced by React components)

**Migration Example**:

**Phase-1 (Console)**:
```python
# src/services/task_manager.py
def filter_tasks(
    self,
    status: str | None = None,
    priority: Priority | None = None,
    category: str | None = None
) -> list[Task]:
    tasks = self.tasks  # In-memory list
    if status == "pending":
        tasks = [t for t in tasks if not t.completed]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    # ...
```

**Phase-2 (Web - Backend)**:
```python
# backend/src/services/task_service.py
async def filter_tasks(
    db: AsyncSession,
    user_id: str,  # NEW: user data isolation
    status: str | None = None,
    priority: Priority | None = None,
    category: str | None = None
) -> list[Task]:
    # NEW: Database query instead of in-memory list
    query = select(Task).where(Task.user_id == user_id)

    # REUSED: Same filtering logic
    if status == "pending":
        query = query.where(Task.completed == False)
    if priority:
        query = query.where(Task.priority == priority)
    # ...

    result = await db.execute(query)
    return result.scalars().all()
```

### Authentication Integration

**Frontend Flow**:
1. User signs up/logs in via Better Auth forms
2. Better Auth creates session and returns JWT
3. Frontend stores JWT (httpOnly cookie preferred)
4. Frontend includes JWT in `Authorization: Bearer <token>` header for all API calls
5. On 401 response, redirect to login

**Backend Flow**:
1. Extract JWT from `Authorization` header via `HTTPBearer` dependency
2. Verify JWT signature and expiration using `python-jose`
3. Extract `user_id` from token payload
4. Inject `user_id` into route handler via FastAPI dependency injection
5. Use `user_id` to filter all queries (data isolation)

**Security Principle**: Backend never trusts frontend. Every request is independently verified.

### Data Isolation Strategy

**Critical Requirement**: Users must NEVER see other users' tasks.

**Implementation**:
1. **All queries filter by `user_id`**:
   ```python
   query = select(Task).where(Task.user_id == user_id)
   ```

2. **Extract `user_id` from JWT, not request body**:
   ```python
   @router.get("/api/tasks")
   async def list_tasks(
       user_id: str = Depends(get_current_user),  # From JWT
       db: AsyncSession = Depends(get_db)
   ):
       # user_id is trusted because it's from verified JWT
   ```

3. **Verify ownership before updates/deletes**:
   ```python
   task = await db.get(Task, task_id)
   if task.user_id != user_id:
       raise HTTPException(status_code=403)
   ```

4. **Database-level enforcement**: Foreign key with CASCADE delete

**Testing**: Dedicated integration tests verify user A cannot access user B's data

### Responsive Design Approach

**Tailwind Breakpoints**:
- `sm`: 640px (small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large desktops)

**Mobile-First Strategy**:
1. Design for 320px (mobile) first
2. Add `md:` classes for tablet adjustments
3. Add `lg:` classes for desktop layouts

**Example**:
```tsx
<div className="
  grid grid-cols-1     /* Mobile: single column */
  md:grid-cols-2       /* Tablet: two columns */
  lg:grid-cols-3       /* Desktop: three columns */
  gap-4
">
  {tasks.map(task => <TaskCard key={task.id} task={task} />)}
</div>
```

## Testing Strategy

### Backend Testing

**Unit Tests** (pytest):
- Service layer methods (CRUD, filtering, sorting, search)
- Recurring task logic
- Authentication helpers (JWT verification)

**Integration Tests**:
- API endpoints with TestClient
- Authentication flow (signup → login → access protected route)
- User data isolation (critical security test)
- Recurring task creation on completion

**Test Database**: In-memory SQLite for fast tests

### Frontend Testing

**Component Tests** (Jest + React Testing Library):
- Task list rendering
- Task form submission
- Filters and search
- Authentication forms

**E2E Tests** (Playwright):
- Full user journey: signup → create task → filter → mark complete → logout
- Responsive design on multiple viewports

### Contract Testing

**Backend**: Verify responses match OpenAPI schema
**Frontend**: Verify requests match OpenAPI schema

## Deployment Considerations

**Frontend (Next.js)**:
- Platform: Vercel (optimal for Next.js) or Netlify
- Environment variables: `NEXT_PUBLIC_API_URL`, `BETTER_AUTH_SECRET`, `DATABASE_URL`
- Build command: `npm run build`

**Backend (FastAPI)**:
- Platform: Railway, Render, or fly.io
- Environment variables: `DATABASE_URL`, `JWT_SECRET`, `FRONTEND_URL` (CORS)
- Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

**Database (Neon)**:
- Production branch separate from development
- Connection pooling enabled
- Regular backups

**CORS**:
- Development: Allow `http://localhost:3000`
- Production: Allow only production frontend domain

## Risk Mitigation

### Risk 1: Better Auth Integration Complexity

**Mitigation**:
- Start with simplest Better Auth setup (email/password only)
- Defer features like email verification, password reset
- Test auth flow early in development

### Risk 2: Database Connection Limits (Neon Free Tier)

**Mitigation**:
- Implement connection pooling
- Close database sessions properly (use context managers)
- Monitor connection usage
- Upgrade to paid tier if needed

### Risk 3: CORS Issues

**Mitigation**:
- Configure CORS early in backend setup
- Test cross-origin requests in development
- Document CORS configuration for production

### Risk 4: JWT Token Management

**Mitigation**:
- Use httpOnly cookies (prevents XSS)
- Implement token refresh mechanism
- Clear documentation of token flow

## Success Metrics

**Implementation is successful when**:
1. ✅ All Phase-1 features work via web interface
2. ✅ Users can create accounts and sign in
3. ✅ User data is completely isolated (verified by tests)
4. ✅ Application is responsive on mobile, tablet, desktop
5. ✅ All API endpoints match OpenAPI specification
6. ✅ Test coverage >80% for critical paths (auth, data isolation, CRUD)
7. ✅ Performance meets targets (SC-002, SC-003, SC-006, SC-007 from spec)

## Next Steps

1. **Run `/sp.tasks` command** to generate detailed implementation tasks
2. **Set up development environment** following [quickstart.md](./quickstart.md)
3. **Backend First**: Implement database models, migrations, and core API endpoints
4. **Frontend Second**: Implement authentication pages and task management UI
5. **Integration Testing**: Verify full user flows work end-to-end
6. **Deploy**: Set up staging environment for testing

---

**Plan Status**: ✅ COMPLETE - Ready for task generation (`/sp.tasks`)

**Artifacts Generated**:
- ✅ research.md - Technical decisions and architecture
- ✅ data-model.md - Database schema and SQLModel definitions
- ✅ contracts/openapi.yaml - API specification
- ✅ contracts/README.md - API documentation
- ✅ quickstart.md - Local development setup guide
- ✅ plan.md - This implementation plan
