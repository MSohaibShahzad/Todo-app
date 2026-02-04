# Todo Web Application - Phase 3: Conversational AI

A full-stack todo application with Next.js frontend and FastAPI backend, enhanced with a conversational AI layer powered by OpenAI and MCP (Model Context Protocol).

## Features

### User Authentication
- Secure account creation and sign-in with Better Auth
- Session persistence and JWT-based authentication
- Protected routes and data isolation

### Task Management
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Assign priorities (low, medium, high) with color-coded display
- Organize tasks into custom categories with autocomplete suggestions
- Set due dates with overdue indicators
- Create recurring tasks (daily, weekly, monthly)
- Auto-generate next occurrence when completing recurring tasks

### Conversational AI (Phase 3)
- **Natural Language Task Management**: Create, view, update, and delete tasks through chat (e.g. "remind me to call John tomorrow at 2pm")
- **AI-Powered Intent Recognition**: GPT-4 interprets free-form messages and maps them to structured task operations
- **MCP Tool Architecture**: All task operations are exposed as stateless MCP tools consumed by the AI agent — the agent never touches the database directly
- **Conversation Persistence**: Chat history is stored in PostgreSQL and restored across sessions; auto-deleted after 30 days
- **Per-User Rate Limiting**: Fair AI API usage with request queuing via Redis and SlowAPI
- **Concurrent Conversation Limit**: Up to 3 active conversations per user
- **Undo Support**: Reverse the last AI action to recover from misinterpretations
- **OpenAI ChatKit UI**: Production-ready chat interface built with `@openai/chatkit-react`

### Advanced Features
- Search tasks by title, description, or category
- Filter by status, priority, and category
- Sort by created date, title, priority, or due date
- Responsive design for mobile, tablet, and desktop
- Real-time task summary dashboard with 6 stat cards
- Toast notifications for user feedback
- Form validation with error messages

## Tech Stack

### Frontend
- **Framework**: Next.js 16.1.1 (App Router with Turbopack)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Authentication**: Better Auth with session management
- **State Management**: SWR for data fetching and caching
- **Chat UI**: OpenAI ChatKit (`@openai/chatkit-react`)
- **Icons**: Lucide React
- **Notifications**: Custom toast system

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT with python-jose
- **Migrations**: Alembic
- **Server**: Uvicorn
- **AI**: OpenAI GPT-4 via `openai` SDK
- **Tool Protocol**: MCP (`mcp` SDK) — stateless tools for AI agent
- **Rate Limiting**: SlowAPI with Redis backend
- **Scheduling**: APScheduler (conversation cleanup job)

## Prerequisites

- Python 3.12 or later
- Node.js 20 or later
- uv package manager
- PostgreSQL database

## Quick Start

### 1. Clone and Setup

```bash
cd Phase-3
```

### 2. Backend Setup

```bash
cd backend

# Copy environment file
cp .env.example .env

# Edit .env and add your DATABASE_URL and JWT_SECRET

# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Start backend server
uv run uvicorn src.main:app --reload --port 8000
```

Backend will be available at http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Copy environment file
cp .env.local.example .env.local

# Edit .env.local and add your DATABASE_URL, BETTER_AUTH_SECRET, and API URL

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

### 4. Docker Compose (Alternative)

```bash
# Start all services (frontend, backend, database)
docker-compose up

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Project Structure

```
Phase-3/
├── frontend/               # Next.js application
│   ├── app/
│   │   ├── (app)/
│   │   │   ├── dashboard/  # Main task dashboard
│   │   │   └── chat/       # Conversational AI interface
│   │   └── (auth)/         # Login / signup pages
│   ├── components/
│   │   ├── chat/           # ChatInterface (ChatKit)
│   │   ├── features/       # Auth, dashboard, task components
│   │   └── ui/             # Reusable UI primitives
│   ├── lib/
│   │   ├── api/            # HTTP client + task & conversation endpoints
│   │   ├── auth/           # Better Auth client config
│   │   └── hooks/          # useAuth, useTasks, useToast
│   └── types/              # TypeScript type definitions
│
├── backend/               # FastAPI application
│   ├── src/
│   │   ├── api/           # Route handlers (health, auth, tasks, chat, chatkit)
│   │   ├── auth/          # JWT helpers & FastAPI dependencies
│   │   ├── models/        # SQLModel models (user, task, conversation, message, tool_execution)
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── services/      # Business logic (task, conversation, AI agent, cleanup, recurrence)
│   │   ├── middleware/    # Rate limiting (SlowAPI + Redis)
│   │   ├── mcp/           # MCP server — stateless task tools for the AI agent
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database connection
│   │   └── main.py        # FastAPI app entry point + scheduler
│   ├── alembic/           # Database migrations
│   └── tests/             # Unit & integration tests
│
└── specs/                 # Feature specifications
    ├── 003-full-stack-todo-app/   # Phase 2 spec
    └── 004-conversational-ai/     # Phase 3 spec
```

## Development Workflow

### Running Tests

**Backend:**
```bash
cd backend
uv run pytest                    # Run all tests
uv run pytest -v                 # Verbose output
uv run pytest --cov=src          # With coverage
```

**Frontend:**
```bash
cd frontend
npm test                         # Run tests
npm run test:watch              # Watch mode
```

### Code Quality

**Backend:**
```bash
cd backend
uv run ruff check src/           # Linting
uv run ruff format src/          # Formatting
uv run mypy src/                 # Type checking
```

**Frontend:**
```bash
cd frontend
npm run lint                     # ESLint
npm run type-check              # TypeScript check
```

### Database Migrations

```bash
cd backend

# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development

# Phase 3 — Conversational AI
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4o
REDIS_URL=redis://localhost:6379/0
RATE_LIMIT_PER_MINUTE=10
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

## Features Roadmap

- [x] Phase 1: Console Todo App (See Phase-1/)
- [x] Phase 2: Full-Stack Web Application ✅ **COMPLETED (155/155 tasks)**
  - [x] Project setup and infrastructure
  - [x] User authentication (US1) - JWT-based auth with bcrypt
  - [x] Task CRUD operations (US2) - Full REST API with data isolation
  - [x] Task organization with priorities and categories (US3)
  - [x] Due dates and recurring tasks (US4) - Auto-generates next occurrences
  - [x] Search, filter, and sort (US5) - 8 sort options + advanced filters
  - [x] Responsive web interface (US6) - Mobile-first, touch-friendly
  - [x] Polish and error handling - Toast notifications, form validation
  - [x] Integration testing - 6 tests covering data isolation
- [ ] Phase 3: Conversational AI **(139 tasks — in progress)**
  - [x] Setup — dependencies (openai, mcp, redis, slowapi, chatkit)
  - [x] Foundation — conversation/message/tool_execution models + MCP server skeleton + AI agent service + chat router
  - [ ] US1 (P1) — Quick task creation via chat
  - [ ] US2 (P2) — View & search tasks via chat
  - [ ] US3 (P3) — Update tasks via conversation
  - [ ] US4 (P4) — Delete tasks via chat
  - [ ] US5 (P5) — Advanced filtering & sorting via chat
  - [ ] Undo — reverse last AI action
  - [ ] Conversation management — list, archive, delete chats
  - [ ] Streaming — real-time SSE token streaming
  - [ ] Polish — error handling, prompt-injection guard, cost monitoring

## Key Features Highlights

### Authentication
- JWT-based authentication with Better Auth
- Secure password hashing with bcrypt
- Session persistence across browser sessions
- Protected API routes with authentication middleware

### Task Organization
- **Category Autocomplete**: Type-ahead suggestions from existing categories
- **Priority Colors**: Visual indicators (red for high, yellow for medium, green for low)
- **Due Date Alerts**: Notifications for overdue and tasks due today
- **Recurring Tasks**: Automatic generation of next occurrence on completion

### User Experience
- **Instant Updates**: Optimistic UI updates with SWR caching
- **Responsive Design**: Mobile-first design that works on all devices
- **Real-time Stats**: Dashboard shows total, pending, completed, overdue, due today, and due tomorrow
- **Error Handling**: Graceful error messages and loading states

## License

MIT
