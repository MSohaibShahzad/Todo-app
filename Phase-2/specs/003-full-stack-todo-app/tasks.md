# Implementation Tasks: Phase II – Full-Stack Todo Web Application

**Feature**: 003-full-stack-todo-app
**Branch**: `003-full-stack-todo-app`
**Date**: 2026-01-09
**Total Tasks**: 75
**Estimated Effort**: 8-10 days

## Overview

This document breaks down the implementation of Phase II Full-Stack Todo Web Application into testable, executable tasks organized by user story. Each user story is independently implementable and deliverable, following the MVP-first approach.

**User Stories by Priority**:
- **P1 (Must Have)**: US1 (Auth), US2 (Task CRUD)
- **P2 (Should Have)**: US3 (Priorities/Categories), US4 (Due Dates/Recurrence), US6 (Responsive UI)
- **P3 (Nice to Have)**: US5 (Search/Filter/Sort)

**Recommended MVP**: User Story 1 + User Story 2 (Authentication + Basic Task CRUD)

## Implementation Tooling

**IMPORTANT**: When implementing these tasks, leverage the following tools to accelerate development:

### Context7 MCP Server
Use the **Context7 MCP server** to:
- Retrieve relevant code context from the existing console app in `/home/sohaib/hackathon2/Todo-app/Phase-2/src/`
- Understand existing business logic for task management (filtering, sorting, recurring tasks)
- Reference console app implementations when adapting logic for the web version
- Get examples of validation rules, priority handling, and recurrence calculations

**Example Usage**:
- When implementing task filtering (T121-T125): Use Context7 to fetch console app filtering logic from `/home/sohaib/hackathon2/Todo-app/Phase-2/src/services/task_manager.py`
- When implementing recurring tasks (T097-T099): Reference existing recurrence logic from `/home/sohaib/hackathon2/Todo-app/Phase-2/src/services/task_manager.py`
- When implementing priority/category features (T088-T089): Check console app models in `/home/sohaib/hackathon2/Todo-app/Phase-2/src/models/task.py` for validation patterns

### Claude Agents (.claude/agents/) - **Better Auth Specialists**
Use **specialized authentication agents** from `.claude/agents/` for implementing Better Auth:

**Available Authentication Agents**:
1. **better-auth** agent - Setup Node.js auth service (not needed for this project - using Better Auth directly on frontend)
2. **frontend-auth-integration** agent - Integrate Better Auth into React/Next.js (USE FOR US1: T038-T051)
3. **backend-auth-integration** agent - Protect FastAPI endpoints with JWT verification (USE FOR US1: T034-T037)
4. **jwt-access-token** agent - Fix JWT token flow issues between frontend and backend
5. **auth-troubleshooting** agent - Debug authentication problems

### Claude Skills (.claude/skills/) - **Better Auth Implementation**
These skills are **automatically used by the agents above** - you don't call them directly:

**Available Skills**:
- `better-auth.skill` - Auth service setup (not needed for this project)
- `frontend-auth-integration.skill` - React/Next.js integration patterns
- `backend-auth-integration.skill` - FastAPI JWT verification patterns
- `jwt-access-token.skill` - JWT token flow solutions
- `auth-troubleshooting.skill` - Common auth problem fixes

### When to Use These Tools

**Context7 MCP Server** - Use for all task-related logic (US2, US3, US4, US5):
- Before implementing service layer methods → Query existing console app code
- Before implementing filtering/sorting → Reference existing logic patterns
- Before implementing recurring tasks → Get recurrence calculation code
- Example: "Use Context7 to fetch task filtering logic from Phase-2/src/services/task_manager.py"

**Authentication Agents** - Use ONLY for authentication tasks (US1):
- **frontend-auth-integration** agent: For tasks T038-T051 (Better Auth setup, login/signup pages)
- **backend-auth-integration** agent: For tasks T034-T037 (JWT verification, auth middleware)
- **jwt-access-token** agent: If frontend-backend JWT communication breaks
- **auth-troubleshooting** agent: If you encounter authentication errors

**Skills** - Automatically used by agents (don't call directly):
- Skills provide the knowledge and patterns that agents use
- They're triggered when you use the corresponding agent

**Best Practices**:
1. **For Task Logic (US2-US5)**: Always use Context7 to reference console app (`Phase-2/src/`)
2. **For Authentication (US1)**: Use the specialized Better Auth agents
3. **For Other Code**: Write manually or adapt from console app patterns

**Code Migration Path**:
- Console app: `Phase-2/src/` (models, services, cli)
- New structure: `Phase-2/backend/src/` + `Phase-2/frontend/`
- Keep `Phase-2/src/` as reference until migration complete

---

## Table of Contents

- [Phase 1: Project Setup](#phase-1-project-setup)
- [Phase 2: Foundational Infrastructure](#phase-2-foundational-infrastructure)
- [Phase 3: User Story 1 - Secure Account Access (P1)](#phase-3-user-story-1---secure-account-access-p1)
- [Phase 4: User Story 2 - Personal Task Management (P1)](#phase-4-user-story-2---personal-task-management-p1)
- [Phase 5: User Story 3 - Task Organization (P2)](#phase-5-user-story-3---task-organization-p2)
- [Phase 6: User Story 4 - Due Dates and Recurrence (P2)](#phase-6-user-story-4---due-dates-and-recurrence-p2)
- [Phase 7: User Story 6 - Responsive Web Interface (P2)](#phase-7-user-story-6---responsive-web-interface-p2)
- [Phase 8: User Story 5 - Search, Filter, and Sort (P3)](#phase-8-user-story-5---search-filter-and-sort-p3)
- [Phase 9: Polish & Cross-Cutting Concerns](#phase-9-polish--cross-cutting-concerns)
- [Dependencies & Execution Strategy](#dependencies--execution-strategy)

---

## Phase 1: Project Setup

**Goal**: Initialize monorepo structure with frontend and backend projects.

**Tasks**:

- [ ] T001 [P] Create monorepo directory structure at /home/sohaib/hackathon2/Todo-app/Phase-2/frontend and /home/sohaib/hackathon2/Todo-app/Phase-2/backend
- [ ] T002 [P] Initialize Next.js 16+ project with TypeScript and Tailwind CSS in frontend/
- [ ] T003 [P] Initialize FastAPI project with uv in backend/
- [ ] T004 [P] Create backend/pyproject.toml with dependencies: fastapi, sqlmodel, uvicorn, alembic, python-jose, passlib, python-multipart
- [ ] T005 [P] Create frontend/package.json with dependencies: next, react, react-dom, typescript, tailwind css, better-auth, lucide-react, react-hook-form, zod, date-fns
- [ ] T006 [P] Create backend/.env.example with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, FRONTEND_URL, ENVIRONMENT
- [ ] T007 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [ ] T008 [P] Create backend/.gitignore with .env, __pycache__, .pytest_cache, .mypy_cache, .coverage
- [ ] T009 [P] Create frontend/.gitignore with .env.local, .next, node_modules, .DS_Store
- [ ] T010 Create root README.md with project overview and quickstart instructions
- [ ] T011 [P] Set up backend linting configuration (ruff.toml) with line-length=100, target-version=py311
- [ ] T012 [P] Set up frontend linting configuration (.eslintrc.json) with TypeScript strict mode
- [ ] T013 [P] Create backend/alembic.ini for database migrations
- [ ] T014 Initialize Alembic in backend/alembic/ directory

**Parallel Execution**: T001-T009, T011-T012 can run in parallel (different files/directories)

---

## Phase 2: Foundational Infrastructure

**Goal**: Set up database models, migrations, and core utilities that all user stories depend on.

**Prerequisites**: Phase 1 complete

**Tasks**:

- [ ] T015 Create backend/src/config.py with Settings class loading environment variables
- [ ] T016 Create backend/src/database.py with async SQLModel engine and session management
- [ ] T017 Create backend/src/models/__init__.py exporting all models
- [ ] T018 Create backend/src/models/user.py with User SQLModel (id, email, name, created_at, updated_at)
- [ ] T019 Create backend/src/models/task.py with Task SQLModel (all fields from data-model.md)
- [ ] T020 Create backend/src/models/task.py with Priority enum (low, medium, high)
- [ ] T021 Create backend/src/models/task.py with Recurrence enum (none, daily, weekly, monthly)
- [ ] T022 Create Alembic migration 001_initial_schema.py for users and tasks tables with indexes
- [ ] T023 Create backend/src/schemas/__init__.py exporting all Pydantic schemas
- [ ] T024 [P] Create backend/src/schemas/task.py with TaskCreate schema (title, description, priority, category, due_date, recurrence)
- [ ] T025 [P] Create backend/src/schemas/task.py with TaskUpdate schema (all fields optional)
- [ ] T026 [P] Create backend/src/schemas/task.py with TaskResponse schema with computed fields (is_overdue, is_due_today)
- [ ] T027 [P] Create backend/src/api/__init__.py for router registration
- [ ] T028 Create backend/src/main.py with FastAPI app, CORS middleware, and router registration
- [ ] T029 [P] Create backend/src/api/health.py with GET /health endpoint returning {status, timestamp}
- [ ] T030 [P] Create frontend/lib/utils/cn.ts with Tailwind class merger utility (clsx + tailwind-merge)
- [ ] T031 [P] Create frontend/types/task.ts with Task, TaskCreate, TaskUpdate TypeScript interfaces
- [ ] T032 [P] Create frontend/types/api.ts with APIError interface
- [ ] T033 Create frontend/lib/api/client.ts with base fetch wrapper handling auth headers and errors

**Parallel Execution**: T024-T026 (schemas), T029 (health endpoint), T030-T032 (frontend types) can run in parallel

---

## Phase 3: User Story 1 - Secure Account Access (P1)

**Story Goal**: Users can create accounts, sign in, and sign out securely.

**Independent Test**: Create account → Sign out → Sign back in → Verify session restored

**Prerequisites**: Phase 2 complete

### Backend: JWT Authentication

**🤖 Use backend-auth-integration Agent**: This agent specializes in FastAPI JWT verification patterns

- [ ] T034 [US1] Create backend/src/auth/__init__.py exporting auth dependencies
- [ ] T035 [US1] Create backend/src/auth/jwt.py with create_access_token() and verify_token() functions (🤖 Agent: backend-auth-integration for JWT verification logic)
- [ ] T036 [US1] Create backend/src/auth/dependencies.py with get_current_user() dependency extracting user_id from JWT (🤖 Agent: backend-auth-integration for FastAPI dependency pattern)
- [ ] T037 [US1] Add HTTPBearer security scheme to backend/src/auth/dependencies.py

### Frontend: Better Auth Setup

**🤖 Use frontend-auth-integration Agent**: This agent specializes in Next.js/React auth integration

- [ ] T038 [P] [US1] Create frontend/lib/auth/config.ts with Better Auth configuration (database, emailAndPassword, session settings) (🤖 Agent: frontend-auth-integration for Better Auth config)
- [ ] T039 [P] [US1] Create frontend/lib/hooks/useAuth.ts with useSession() and useSignOut() hooks (🤖 Agent: frontend-auth-integration for session management hooks)
- [ ] T040 [P] [US1] Create frontend/components/ui/Button.tsx with variants (primary, secondary, outline, ghost)
- [ ] T041 [P] [US1] Create frontend/components/ui/Input.tsx with error state and label support
- [ ] T042 [P] [US1] Create frontend/components/ui/Card.tsx for container styling

### Frontend: Authentication Pages

**🤖 Use frontend-auth-integration Agent**: This agent can generate complete login/signup pages

- [ ] T043 [US1] Create frontend/app/(auth)/layout.tsx with centered auth layout
- [ ] T044 [US1] Create frontend/components/features/auth/SignupForm.tsx with email, password, name fields and validation (🤖 Agent: frontend-auth-integration for signup form)
- [ ] T045 [US1] Create frontend/app/(auth)/signup/page.tsx rendering SignupForm
- [ ] T046 [US1] Create frontend/components/features/auth/LoginForm.tsx with email and password fields (🤖 Agent: frontend-auth-integration for login form)
- [ ] T047 [US1] Create frontend/app/(auth)/login/page.tsx rendering LoginForm
- [ ] T048 [US1] Add sign-out functionality to frontend/components/features/auth/UserMenu.tsx with dropdown

### Integration

**🤖 Use jwt-access-token Agent if needed**: This agent fixes JWT token flow issues between frontend and backend

- [ ] T049 [US1] Update frontend/lib/api/client.ts to include Authorization header from Better Auth session (🤖 Agent: jwt-access-token if JWT not reaching backend)
- [ ] T050 [US1] Update frontend/lib/api/client.ts to redirect to /login on 401 responses
- [ ] T051 [US1] Create frontend/app/(app)/layout.tsx with auth guard redirecting unauthenticated users to /login (🤖 Agent: frontend-auth-integration for route protection)

**User Story 1 Complete**: Users can sign up, sign in, sign out, and session persists across browser reloads

**Parallel Execution**: T038-T042 (frontend UI components), T034-T037 (backend auth) can run in parallel

---

## Phase 4: User Story 2 - Personal Task Management (P1)

**Story Goal**: Authenticated users can create, view, update, and delete their own tasks.

**Independent Test**: Create task → View in list → Edit → Mark complete → Delete → Verify only own tasks visible

**Prerequisites**: Phase 3 (User Story 1) complete

### Backend: Task Service Layer

**💡 Use Context7 MCP Server**: Reference console app logic from `Phase-2/src/services/task_manager.py` for business logic patterns

- [ ] T052 [US2] Create backend/src/services/__init__.py exporting all services
- [ ] T053 [US2] Create backend/src/services/task_service.py with create_task(db, user_id, task_data) async function (🔧 Context7: Check `Phase-2/src/services/task_manager.py` add_task method)
- [ ] T054 [US2] Add get_user_tasks(db, user_id) to backend/src/services/task_service.py returning all tasks for user (🔧 Context7: Reference list_tasks from console app)
- [ ] T055 [US2] Add get_task_by_id(db, task_id, user_id) to backend/src/services/task_service.py with ownership check
- [ ] T056 [US2] Add update_task(db, task_id, user_id, task_data) to backend/src/services/task_service.py (🔧 Context7: Check update_task from console app)
- [ ] T057 [US2] Add delete_task(db, task_id, user_id) to backend/src/services/task_service.py (🔧 Context7: Reference delete_task)
- [ ] T058 [US2] Add toggle_task_complete(db, task_id, user_id, completed) to backend/src/services/task_service.py (🔧 Context7: Check mark_task_complete)

### Backend: Task API Endpoints

- [ ] T059 [US2] Create backend/src/api/tasks.py with APIRouter and dependency injection setup
- [ ] T060 [US2] Add POST /api/v1/tasks endpoint in backend/src/api/tasks.py creating tasks with user_id from JWT
- [ ] T061 [US2] Add GET /api/v1/tasks endpoint in backend/src/api/tasks.py listing tasks for authenticated user
- [ ] T062 [US2] Add GET /api/v1/tasks/{task_id} endpoint in backend/src/api/tasks.py with ownership verification
- [ ] T063 [US2] Add PUT /api/v1/tasks/{task_id} endpoint in backend/src/api/tasks.py updating task
- [ ] T064 [US2] Add DELETE /api/v1/tasks/{task_id} endpoint in backend/src/api/tasks.py
- [ ] T065 [US2] Add PATCH /api/v1/tasks/{task_id}/complete endpoint in backend/src/api/tasks.py
- [ ] T066 [US2] Register tasks router in backend/src/main.py with /api/v1 prefix

### Frontend: API Client

- [ ] T067 [P] [US2] Create frontend/lib/api/tasks.ts with getTasks() function
- [ ] T068 [P] [US2] Add createTask(data: TaskCreate) to frontend/lib/api/tasks.ts
- [ ] T069 [P] [US2] Add updateTask(id, data: TaskUpdate) to frontend/lib/api/tasks.ts
- [ ] T070 [P] [US2] Add deleteTask(id) to frontend/lib/api/tasks.ts
- [ ] T071 [P] [US2] Add toggleTaskComplete(id, completed) to frontend/lib/api/tasks.ts
- [ ] T072 [P] [US2] Create frontend/lib/hooks/useTasks.ts with SWR for task list fetching and caching

### Frontend: Task UI Components

- [ ] T073 [P] [US2] Create frontend/components/ui/Modal.tsx for dialogs with overlay and close button
- [ ] T074 [P] [US2] Create frontend/components/ui/Select.tsx dropdown component
- [ ] T075 [US2] Create frontend/components/features/tasks/TaskCard.tsx displaying task title, description, status with complete/delete buttons
- [ ] T076 [US2] Create frontend/components/features/tasks/TaskList.tsx rendering array of TaskCard components
- [ ] T077 [US2] Create frontend/components/features/tasks/TaskForm.tsx with title and description fields
- [ ] T078 [US2] Create frontend/components/features/tasks/CreateTaskModal.tsx wrapping TaskForm in Modal
- [ ] T079 [US2] Create frontend/components/features/tasks/EditTaskModal.tsx for editing existing tasks

### Frontend: Dashboard Page

- [ ] T080 [US2] Create frontend/app/(app)/dashboard/page.tsx with task list and create button
- [ ] T081 [US2] Add task count display to frontend/app/(app)/dashboard/page.tsx showing total and completed counts
- [ ] T082 [US2] Wire up create task button to open CreateTaskModal in frontend/app/(app)/dashboard/page.tsx
- [ ] T083 [US2] Wire up TaskCard complete button to call toggleTaskComplete() with optimistic updates
- [ ] T084 [US2] Wire up TaskCard delete button to call deleteTask() with confirmation dialog

### Data Isolation Testing

- [ ] T085 [US2] Create backend/tests/integration/test_data_isolation.py verifying user A cannot access user B's tasks
- [ ] T086 [US2] Add test to backend/tests/integration/test_data_isolation.py verifying 403 error when accessing other user's task
- [ ] T087 [US2] Add test to backend/tests/integration/test_data_isolation.py verifying DELETE returns 403 for other user's task

**User Story 2 Complete**: Users can fully manage their tasks with complete data isolation

**Parallel Execution**: T067-T071 (API client), T073-T074 (UI components), T053-T058 (service layer) can run in parallel

---

## Phase 5: User Story 3 - Task Organization (P2)

**Story Goal**: Users can assign priorities and categories to tasks with visual indicators.

**Independent Test**: Create tasks with different priorities and categories → Verify color-coded display

**Prerequisites**: Phase 4 (User Story 2) complete

### Backend: Priority and Category Support

- [ ] T088 [US3] Update backend/src/services/task_service.py to handle priority and category in create_task()
- [ ] T089 [US3] Update backend/src/services/task_service.py to handle priority and category in update_task()

### Frontend: Priority and Category UI

- [ ] T090 [P] [US3] Create frontend/lib/utils/priority-colors.ts with getPriorityColor() returning Tailwind classes (red/yellow/blue)
- [ ] T091 [P] [US3] Create frontend/components/ui/Badge.tsx for displaying labels with color variants
- [ ] T092 [US3] Update frontend/components/features/tasks/TaskCard.tsx to display priority badge with correct color
- [ ] T093 [US3] Update frontend/components/features/tasks/TaskCard.tsx to display category label if present
- [ ] T094 [US3] Update frontend/components/features/tasks/TaskForm.tsx to add priority dropdown (low/medium/high)
- [ ] T095 [US3] Update frontend/components/features/tasks/TaskForm.tsx to add category input field
- [ ] T096 [US3] Update frontend/types/task.ts to include priority and category fields

**User Story 3 Complete**: Tasks have priorities and categories with visual distinction

**Parallel Execution**: T090-T091 (utilities), T088-T089 (backend) can run in parallel

---

## Phase 6: User Story 4 - Due Dates and Recurrence (P2)

**Story Goal**: Users can set due dates and create recurring tasks that auto-regenerate.

**Independent Test**: Create task with due date → Verify overdue indicator → Create recurring task → Mark complete → Verify new instance created

**Prerequisites**: Phase 4 (User Story 2) complete

### Backend: Recurrence Logic

**💡 Use Context7 MCP Server**: Reference console app recurring task logic from `Phase-2/src/services/task_manager.py`

- [ ] T097 [US4] Create backend/src/services/recurrence_service.py with calculate_next_due_date(current_due, recurrence) function (🔧 Context7: Check console app recurrence calculation logic)
- [ ] T098 [US4] Add create_recurring_instance(db, original_task) to backend/src/services/recurrence_service.py (🔧 Context7: Reference recurring task generation from console app)
- [ ] T099 [US4] Update backend/src/services/task_service.py toggle_task_complete() to create recurring instance when marking recurring task complete
- [ ] T100 [US4] Update backend/src/services/task_service.py to compute is_overdue and is_due_today in get_user_tasks()

### Backend: Summary Endpoint

- [ ] T101 [US4] Add GET /api/v1/tasks/summary endpoint in backend/src/api/tasks.py returning task counts (total, pending, completed, overdue, due_today, due_tomorrow)

### Frontend: Due Date UI

- [ ] T102 [P] [US4] Create frontend/lib/utils/date-formatting.ts with formatDueDate() and isOverdue() helpers
- [ ] T103 [P] [US4] Create frontend/components/ui/DatePicker.tsx with calendar selection
- [ ] T104 [US4] Update frontend/components/features/tasks/TaskCard.tsx to display due date with OVERDUE/DUE TODAY badges
- [ ] T105 [US4] Update frontend/components/features/tasks/TaskForm.tsx to add due date picker
- [ ] T106 [US4] Update frontend/components/features/tasks/TaskForm.tsx to add recurrence dropdown (none/daily/weekly/monthly)
- [ ] T107 [US4] Update frontend/types/task.ts to include due_date, recurrence, is_overdue, is_due_today fields

### Frontend: Dashboard Summary

- [ ] T108 [US4] Create frontend/components/features/dashboard/StatsCard.tsx displaying count with label and icon
- [ ] T109 [US4] Create frontend/components/features/dashboard/TaskSummary.tsx fetching and displaying stats from /api/v1/tasks/summary
- [ ] T110 [US4] Add TaskSummary component to frontend/app/(app)/dashboard/page.tsx above task list
- [ ] T111 [US4] Add startup notifications to frontend/app/(app)/dashboard/page.tsx showing overdue and due-today counts

**User Story 4 Complete**: Tasks have due dates with visual indicators and recurring tasks work correctly

**Parallel Execution**: T102-T103 (frontend utils), T097-T098 (backend recurrence logic) can run in parallel

---

## Phase 7: User Story 6 - Responsive Web Interface (P2)

**Story Goal**: Application works seamlessly on mobile (320px), tablet (768px), and desktop (1920px).

**Independent Test**: Test on 320px, 768px, and 1920px viewports → Verify all features usable

**Prerequisites**: Phase 4 (User Story 2) complete

### Responsive Layouts

- [ ] T112 [P] [US6] Update frontend/app/layout.tsx with viewport meta tag and responsive container
- [ ] T113 [US6] Update frontend/components/features/tasks/TaskList.tsx to use responsive grid (1 col mobile, 2 col tablet, 3 col desktop)
- [ ] T114 [US6] Update frontend/components/features/tasks/TaskCard.tsx with mobile-optimized padding and font sizes
- [ ] T115 [US6] Update frontend/components/features/tasks/TaskForm.tsx with stacked layout on mobile, side-by-side on desktop
- [ ] T116 [US6] Update frontend/components/ui/Modal.tsx to be full-screen on mobile, centered dialog on desktop
- [ ] T117 [US6] Update frontend/app/(auth)/layout.tsx with responsive padding and max-width
- [ ] T118 [US6] Add mobile navigation menu to frontend/app/(app)/layout.tsx with hamburger icon

### Touch-Friendly UI

- [ ] T119 [US6] Update frontend/components/ui/Button.tsx with min-height 44px for touch targets
- [ ] T120 [US6] Update frontend/components/features/tasks/TaskCard.tsx with larger tap targets for complete/delete buttons on mobile

**User Story 6 Complete**: Application is fully responsive and touch-friendly

**Parallel Execution**: T112, T117 (layouts), T113-T116 (component updates) can run in parallel within their respective areas

---

## Phase 8: User Story 5 - Search, Filter, and Sort (P3)

**Story Goal**: Users can search, filter by status/priority/category, and sort tasks.

**Independent Test**: Create diverse tasks → Search by keyword → Filter by status and priority → Sort by due date

**Prerequisites**: Phase 4 (User Story 2) complete, Phase 5 (US3) recommended

### Backend: Filtering and Sorting

**💡 Use Context7 MCP Server**: Reference console app filtering and sorting logic from `Phase-2/src/services/task_manager.py`

- [ ] T121 [US5] Update backend/src/services/task_service.py get_user_tasks() to accept status filter (all/pending/completed) (🔧 Context7: Check filter_tasks method for status filtering)
- [ ] T122 [US5] Add priority filter parameter to backend/src/services/task_service.py get_user_tasks() (🔧 Context7: Reference priority filtering logic)
- [ ] T123 [US5] Add category filter parameter to backend/src/services/task_service.py get_user_tasks() (🔧 Context7: Check category filtering)
- [ ] T124 [US5] Add search parameter to backend/src/services/task_service.py get_user_tasks() with ILIKE query on title and description (🔧 Context7: Reference search_tasks method)
- [ ] T125 [US5] Add sort_by and sort_order parameters to backend/src/services/task_service.py get_user_tasks() supporting created_at, title, priority, due_date (🔧 Context7: Check sort_tasks logic)
- [ ] T126 [US5] Update backend/src/api/tasks.py GET /api/v1/tasks endpoint to accept query params: status, priority, category, search, sort_by, sort_order

### Frontend: Filter and Search UI

- [ ] T127 [P] [US5] Create frontend/components/features/tasks/SearchBar.tsx with debounced input
- [ ] T128 [P] [US5] Create frontend/components/features/tasks/FilterBar.tsx with dropdowns for status, priority, category
- [ ] T129 [P] [US5] Create frontend/components/features/tasks/SortControls.tsx with sort field and order selection
- [ ] T130 [US5] Add SearchBar, FilterBar, and SortControls to frontend/app/(app)/dashboard/page.tsx above task list
- [ ] T131 [US5] Update frontend/lib/hooks/useTasks.ts to accept filter, search, and sort parameters
- [ ] T132 [US5] Wire up filter/search/sort state to useTasks hook in frontend/app/(app)/dashboard/page.tsx with URL persistence
- [ ] T133 [US5] Add "Clear Filters" button to frontend/app/(app)/dashboard/page.tsx

**User Story 5 Complete**: Users can search, filter, and sort tasks efficiently

**Parallel Execution**: T127-T129 (UI components), T121-T125 (backend logic) can run in parallel

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Error handling, loading states, validation, and deployment readiness.

**Prerequisites**: Core user stories (US1, US2) complete

### Error Handling

- [ ] T134 [P] Create frontend/components/ui/Toast.tsx for success/error notifications
- [ ] T135 [P] Create frontend/lib/hooks/useToast.ts for toast state management
- [ ] T136 Update frontend/lib/api/client.ts to show toast on API errors
- [ ] T137 Add error boundaries to frontend/app/layout.tsx with fallback UI
- [ ] T138 Add loading states to frontend/components/features/tasks/TaskList.tsx with skeleton loaders
- [ ] T139 [P] Create frontend/components/ui/Skeleton.tsx for loading placeholders
- [ ] T140 Add optimistic updates to frontend/lib/hooks/useTasks.ts for create/update/delete operations

### Validation

- [ ] T141 [P] Create frontend/lib/validation/task-schema.ts with Zod schema for TaskCreate
- [ ] T142 Add frontend validation to frontend/components/features/tasks/TaskForm.tsx using react-hook-form + Zod
- [ ] T143 Add backend validation error handling to backend/src/api/tasks.py with detailed error messages
- [ ] T144 Add rate limiting middleware to backend/src/main.py (100 requests/minute per user)

### Testing & Documentation

- [ ] T145 [P] Create backend/tests/conftest.py with test database fixtures
- [ ] T146 [P] Create backend/tests/unit/test_task_service.py with tests for all CRUD operations
- [ ] T147 [P] Create backend/tests/integration/test_task_api.py with tests for all endpoints
- [ ] T148 [P] Create frontend/components/features/tasks/__tests__/TaskCard.test.tsx with component tests
- [ ] T149 Update root README.md with architecture overview, setup instructions, and API documentation links
- [ ] T150 Create CONTRIBUTING.md with development workflow and code standards

### Deployment Readiness

- [ ] T151 [P] Create backend/Dockerfile for FastAPI deployment
- [ ] T152 [P] Create frontend/Dockerfile for Next.js deployment
- [ ] T153 Create docker-compose.yml for local development with frontend, backend, and database services
- [ ] T154 Add health checks to backend/src/api/health.py with database connectivity check
- [ ] T155 Create .github/workflows/ci.yml with linting and testing for both frontend and backend

**Phase 9 Complete**: Application is production-ready with proper error handling, testing, and deployment configuration

**Parallel Execution**: T134-T135, T139, T141 (UI utilities), T145-T147 (tests), T151-T152 (Docker) can run in parallel

---

## Dependencies & Execution Strategy

### Story Completion Order

```
Phase 1 (Setup) → Phase 2 (Foundation)
                ↓
     Phase 3 (US1: Auth) ← REQUIRED FOR ALL BELOW
                ↓
     Phase 4 (US2: Task CRUD) ← MVP COMPLETE HERE
                ↓
     ┌──────────┴──────────┬──────────┬──────────┐
     ↓                     ↓          ↓          ↓
Phase 5 (US3)    Phase 6 (US4)  Phase 7 (US6)  Phase 8 (US5)
Priorities/      Due Dates/     Responsive     Search/Filter
Categories       Recurrence     UI             Sort
     ↓                     ↓          ↓          ↓
     └──────────┬──────────┴──────────┴──────────┘
                ↓
     Phase 9 (Polish & Deployment)
```

**Dependencies**:
- **US1 (Auth)**: Blocks all other user stories (required for authentication)
- **US2 (Task CRUD)**: Blocks US3, US4, US5, US6 (need basic task management first)
- **US3, US4, US5, US6**: Independent of each other (can be done in any order)
- **US5 (Search/Filter)**: Benefits from US3 (priorities/categories) but not required

### MVP Scope (Minimum Viable Product)

**Recommended First Release**: US1 + US2
- Users can sign up/in
- Users can create, view, update, delete tasks
- Complete data isolation
- Basic responsive UI

**Estimated effort**: 3-4 days with this task breakdown

### Incremental Delivery

**Release 1 (MVP)**: US1 + US2 (Tasks T001-T087, T134-T140, T145-T147)
**Release 2**: + US3 + US6 (Add priorities, categories, full responsive design)
**Release 3**: + US4 (Add due dates and recurring tasks)
**Release 4**: + US5 + Phase 9 (Add search/filter/sort, polish, deploy)

### Parallel Execution Examples

**Within US1 (Auth)**:
- Frontend auth UI (T040-T042, T044, T046, T048) || Backend JWT logic (T034-T037)

**Within US2 (Task CRUD)**:
- Backend service layer (T053-T058) || Frontend API client (T067-T071) || Frontend UI components (T073-T074)

**Within US4 (Due Dates)**:
- Backend recurrence logic (T097-T099) || Frontend date utilities (T102-T103) || Dashboard stats (T108-T109)

**Cross-Story**:
- US3 (Priorities) || US6 (Responsive) || US4 (Due Dates) - all independent after US2

### Testing Strategy

**Per User Story**:
- US1: Auth flow integration tests (signup → login → protected route)
- US2: Data isolation tests (critical security requirement)
- US3: Visual regression tests for priority colors
- US4: Recurring task generation tests
- US5: Filter logic unit tests with various combinations
- US6: Responsive design tests on multiple viewports

**TDD Approach** (if requested):
1. Write test for user story acceptance criteria
2. Implement backend service/endpoint to pass test
3. Implement frontend component/page to pass test
4. Refactor while keeping tests green

---

## Task Summary

**Total Tasks**: 155
**By Phase**:
- Phase 1 (Setup): 14 tasks
- Phase 2 (Foundation): 19 tasks
- Phase 3 (US1 - Auth): 18 tasks
- Phase 4 (US2 - Task CRUD): 36 tasks
- Phase 5 (US3 - Organization): 9 tasks
- Phase 6 (US4 - Due Dates): 15 tasks
- Phase 7 (US6 - Responsive): 9 tasks
- Phase 8 (US5 - Search/Filter): 13 tasks
- Phase 9 (Polish): 22 tasks

**By User Story**:
- US1 (Secure Account Access): 18 tasks
- US2 (Personal Task Management): 36 tasks
- US3 (Task Organization): 9 tasks
- US4 (Due Dates and Recurrence): 15 tasks
- US5 (Search, Filter, Sort): 13 tasks
- US6 (Responsive Web Interface): 9 tasks
- Setup + Foundation + Polish: 55 tasks

**Parallelizable Tasks**: 68 tasks marked with [P] (43% can run in parallel)

**Independent User Stories**: US3, US4, US5, US6 can be implemented in any order after US2

---

## Validation Checklist

✅ All tasks follow checkbox format: `- [ ] TXXX [P] [USX] Description with file path`
✅ Tasks organized by user story for independent implementation
✅ Each user story has independent test criteria
✅ Dependencies clearly documented
✅ Parallel execution opportunities identified
✅ MVP scope defined (US1 + US2)
✅ File paths included in all implementation tasks
✅ Story labels [US1]-[US6] applied to user story tasks
✅ Setup and foundational tasks have no story label
✅ Polish tasks have no story label

---

**Next Steps**:
1. Set up development environment following quickstart.md
2. Begin with Phase 1 (Setup) tasks
3. Proceed to Phase 2 (Foundation)
4. Implement MVP (US1 + US2) first
5. Add additional user stories incrementally

**Happy Building! 🚀**
