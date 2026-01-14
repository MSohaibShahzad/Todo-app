---
id: 002
title: Full-Stack Implementation Plan
stage: plan
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-full-stack-todo-app
branch: 002-intermediate-advanced-features
user: sohaib
command: /sp.plan
labels: ["planning", "architecture", "full-stack", "monorepo", "api-design", "code-reuse"]
links:
  spec: specs/003-full-stack-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/003-full-stack-todo-app/plan.md
 - specs/003-full-stack-todo-app/research.md
 - specs/003-full-stack-todo-app/data-model.md
 - specs/003-full-stack-todo-app/quickstart.md
 - specs/003-full-stack-todo-app/contracts/openapi.yaml
 - specs/003-full-stack-todo-app/contracts/README.md
tests:
 - No tests created (planning phase)
 - Test strategy documented in plan.md
---

## Prompt

Title: Phase II – Todo Full-Stack Web Application (Plan)

Plan the upgrade of the existing Todo application into a full-stack system
using a monorepo structure while reusing and extending existing logic
wherever possible.

Monorepo Structure:
- frontend/ for the web client
- backend/ for the API server
- specs/003-full-stack-todo-app/ for specifications and plans
- .claude/agents for agents
- .claude/skills for skills

Backend Plan:
- Use Python with FastAPI
- Expose RESTful API endpoints for:
  - authentication
  - task CRUD operations
  - search, filter, and sorting
- Use Neon Serverless PostgreSQL as the database
- Migrate in-memory task logic to persistent storage
- Enforce user-level data isolation

Authentication Plan:
- Implement user signup and signin using Better Auth
- Integrate authentication as middleware
- Ensure future compatibility with existing agents and skills
- Do not embed auth logic directly into business logic

Frontend Plan:
- Use Next.js 16+ with App Router
- Build a responsive UI for task management
- Consume backend APIs for all operations
- Protect routes based on authentication state

Authentication Integration Strategy:

- Better Auth runs on the Next.js frontend.
- The FastAPI backend acts as a separate service and does not handle login UI.

Frontend Responsibilities:
- Authenticate users using Better Auth
- Include user authentication context (e.g., session token or user identifier)
  in API requests to the backend

Backend Responsibilities:
- Verify the authenticity of incoming requests
- Validate user identity for each request
- Enforce user-level authorization on all task operations
- Reject unauthenticated or invalid requests

Design Constraint:
- Authentication logic must remain decoupled from core business logic
- Backend must trust but verify frontend-provided authentication data
- Implementation should allow future replacement or extension of auth mechanisms

Constraints:
- Reuse existing code where possible
- Avoid unnecessary rewrites
- Maintain clean separation of frontend, backend, and auth concerns

## Response snapshot

Created comprehensive implementation plan with complete Phase 0 (Research) and Phase 1 (Design & Contracts) artifacts:

**Phase 0 - Research (research.md)**:
- **Technology Stack Decisions**: Next.js 16+ (App Router), FastAPI, Neon PostgreSQL, Better Auth, SQLModel
- **Architecture Patterns**: Monorepo structure, three-layer backend (Router → Service → Model), feature-based frontend components
- **API Design**: RESTful with 7 task endpoints + health check, JWT authentication
- **Code Reuse Strategy**: Detailed analysis showing ~80% reuse of Phase-1 business logic with adaptations for persistence and multi-user
- **Authentication**: Better Auth on frontend with JWT, backend verifies tokens independently
- **Security**: Input validation, XSS prevention, CSRF protection, rate limiting strategies
- **Performance**: Database indexing strategy, query optimization, frontend code splitting
- **Testing**: Unit, integration, E2E strategies for both frontend and backend

**Phase 1 - Data Model (data-model.md)**:
- **Entities**: User (managed by Better Auth), Task (with full Phase-1 feature set)
- **Schema**: 2 tables, 1:N relationship, 6 indexes (including composite for common queries)
- **Enums**: Priority (low/medium/high), Recurrence (none/daily/weekly/monthly)
- **SQLModel Definitions**: Complete models with validation rules
- **Pydantic Schemas**: TaskCreate, TaskUpdate, TaskResponse for API layer
- **Query Patterns**: Optimized queries for filtering, searching, overdue tasks, recurring tasks
- **Data Isolation**: User-level security enforced at database query level
- **Migration from Phase-1**: Mapping of console app data structures to database tables

**Phase 1 - API Contracts (contracts/)**:
- **OpenAPI 3.1 Spec**: Complete specification for all 8 endpoints
- **Authentication**: Bearer JWT on all `/api/*` endpoints
- **Filtering**: Query params for status, priority, category, search, sort_by, sort_order
- **Error Responses**: Standardized format with proper HTTP status codes
- **Examples**: Request/response examples for all operations
- **TypeScript Integration**: Frontend API client example with type safety

**Phase 1 - Quickstart (quickstart.md)**:
- **Prerequisites**: Node.js, Python, uv, Neon account
- **Setup Steps**: Database (Neon), backend (FastAPI), frontend (Next.js)
- **Environment Variables**: Complete .env templates for both frontend and backend
- **Development Workflow**: Running servers, testing, useful commands
- **Troubleshooting**: Common issues and solutions for all layers

**Implementation Plan (plan.md)**:
- **Summary**: Transform console app to full-stack web with multi-user support
- **Technical Context**: Complete stack details (Next.js 16+, FastAPI, Neon, Better Auth)
- **Constitution Check**: Adapted console app principles for web (all gates PASS)
- **Project Structure**: Detailed monorepo layout with frontend/ and backend/ directories
- **Code Reuse Strategy**: Concrete examples of migrating console app logic to web
- **Authentication Integration**: Frontend and backend responsibilities, security principles
- **Data Isolation**: Three-layer enforcement strategy (JWT → service → database)
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints
- **Testing Strategy**: Unit, integration, E2E, and contract testing approaches
- **Risk Mitigation**: 4 identified risks with mitigation strategies
- **Success Metrics**: 7 criteria for successful implementation

**Key Architectural Decisions**:
1. **Monorepo**: Frontend and backend in same repository for simplicity
2. **Authentication Separation**: Better Auth (frontend) + JWT verification (backend) - never embedded in business logic
3. **Code Reuse**: ~80% of Phase-1 service logic reusable with modifications for async and multi-user
4. **Data Isolation**: Triple enforcement (JWT extraction → service filtering → database queries)
5. **API-First**: OpenAPI contract defined before implementation
6. **Responsive Design**: Mobile-first with Tailwind, targeting 320px-1920px range

## Outcome

- ✅ Impact: Complete implementation plan for Phase II full-stack transformation. All Phase 0 and Phase 1 artifacts created. Ready for task breakdown.
- 🧪 Tests: Testing strategies documented for all layers (backend unit/integration, frontend component/E2E, contract tests)
- 📁 Files: 6 planning documents created (plan, research, data-model, quickstart, openapi.yaml, contracts README) totaling ~1200 lines
- 🔁 Next prompts: `/sp.tasks` to generate detailed implementation tasks from this plan
- 🧠 Reflection: Successfully designed a full-stack architecture that reuses Phase-1 business logic while adding multi-user authentication and web UI. Authentication is properly separated from business logic (Better Auth on frontend, JWT verification on backend). Data isolation enforced at three levels for security.

## Evaluation notes (flywheel)

- Failure modes observed: None. All planning phases completed successfully with comprehensive documentation.
- Graders run and results (PASS/FAIL):
  - Constitution Check: PASS (all principles satisfied, no unjustified complexity)
  - Code Reuse Analysis: PASS (~80% of Phase-1 logic reusable)
  - Security Design: PASS (triple-layer data isolation, JWT verification, input validation)
  - API Contract Completeness: PASS (8 endpoints fully specified with examples)
- Prompt variant (if applicable): Standard /sp.plan workflow with user-provided monorepo structure and auth integration strategy
- Next experiment (smallest change to try): Consider adding API versioning (e.g., /api/v1/tasks) from the start to enable future evolution without breaking changes

**ADR Suggestion**:
📋 Architectural decision detected: Authentication Integration Strategy (Better Auth on frontend + JWT verification on backend)
   Document reasoning and tradeoffs? Run `/sp.adr authentication-integration-strategy`

Significant decisions made:
1. Better Auth vs NextAuth vs Auth0/Clerk (chose Better Auth for lightweight, modern approach)
2. Monorepo vs separate repositories (chose monorepo for simplicity)
3. REST vs GraphQL (chose REST for simplicity and familiarity)
4. SQLModel vs raw SQLAlchemy vs Prisma Python (chose SQLModel for FastAPI integration)
