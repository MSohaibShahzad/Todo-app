# Todo Web Application - Phase 4: Kubernetes Deployment

A full-stack todo application with Next.js frontend and FastAPI backend, enhanced with a conversational AI layer powered by OpenAI and MCP (Model Context Protocol). **Phase 4** adds local Kubernetes deployment using Helm charts on Minikube.

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
cd Phase-4
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

### 5. Kubernetes/Helm Deployment (Phase 4 - Recommended)

Deploy the application on local Kubernetes using Minikube and Helm charts:

```bash
# Prerequisites: Minikube, kubectl, Helm 3.0+, Docker

# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable Ingress addon
minikube addons enable ingress

# Build Docker images in Minikube's environment
eval $(minikube docker-env)
cd backend && docker build -t todo-backend:latest .
cd ../frontend && docker build -t todo-frontend:latest .
cd ..

# Configure secrets in todo-helm/values.yaml
# Update: JWT_SECRET, OPENAI_API_KEY, BETTER_AUTH_SECRET, database password

# Deploy using Helm
kubectl create namespace todo-app
helm install todo-app ./todo-helm --namespace todo-app

# Configure local DNS
echo "$(minikube ip) todo-app.local" | sudo tee -a /etc/hosts

# Access the application
# Frontend: http://todo-app.local
# Backend API: http://todo-app.local/api/v1/health
# API Docs: http://todo-app.local/api/docs
```

For detailed deployment instructions, troubleshooting, and configuration options, see:
- **[HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md)** - Complete Helm deployment documentation
- **[todo-helm/README.md](./todo-helm/README.md)** - Helm chart documentation

## Project Structure

```
Phase-4/
├── todo-helm/             # Kubernetes Helm chart
│   ├── Chart.yaml         # Chart metadata (v1.0.0)
│   ├── values.yaml        # Configuration (secrets, resources, environment)
│   ├── README.md          # Helm chart documentation
│   └── templates/         # Kubernetes manifests
│       ├── configmap.yaml       # Environment variables
│       ├── secret.yaml          # Sensitive data (JWT, OpenAI, DB)
│       ├── pvc.yaml             # PostgreSQL persistent volume
│       ├── database-*.yaml      # PostgreSQL deployment & service
│       ├── backend-*.yaml       # FastAPI deployment & service
│       ├── frontend-*.yaml      # Next.js deployment & service
│       ├── ingress.yaml         # NGINX Ingress routing
│       └── hpa.yaml             # Horizontal Pod Autoscaler
│
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
- [x] Phase 3: Conversational AI ✅ **COMPLETED**
  - [x] Setup — dependencies (openai, mcp, redis, slowapi, chatkit)
  - [x] Foundation — conversation/message/tool_execution models + MCP server skeleton + AI agent service + chat router
  - [x] US1 (P1) — Quick task creation via chat
  - [x] US2 (P2) — View & search tasks via chat
  - [x] US3 (P3) — Update tasks via conversation
  - [x] US4 (P4) — Delete tasks via chat
  - [x] US5 (P5) — Advanced filtering & sorting via chat
  - [x] Undo — reverse last AI action
  - [x] Conversation management — list, archive, delete chats
  - [x] Streaming — real-time SSE token streaming
  - [x] Polish — error handling, prompt-injection guard, cost monitoring
- [x] Phase 4: Kubernetes Deployment ✅ **COMPLETED**
  - [x] Helm chart structure and templates
  - [x] Three-tier architecture (PostgreSQL, Backend, Frontend)
  - [x] ConfigMaps and Secrets management
  - [x] Persistent storage for PostgreSQL (5Gi PVC)
  - [x] NGINX Ingress with path-based routing
  - [x] Health probes (liveness/readiness)
  - [x] Resource limits and requests
  - [x] Horizontal Pod Autoscaler (HPA)
  - [x] Minikube deployment guide
  - [x] Troubleshooting documentation

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

### Kubernetes Deployment (Phase 4)
- **Helm Chart**: Fully configured Helm chart for Kubernetes deployment
- **Three-Tier Architecture**: Separate deployments for database, backend, and frontend
- **Ingress Routing**: NGINX Ingress with path-based routing (`/api/*` → backend, `/*` → frontend)
- **Persistent Storage**: PostgreSQL data persisted using Persistent Volume Claims (5Gi)
- **Configuration Management**: Separate ConfigMaps and Secrets for environment variables and sensitive data
- **High Availability**: Health probes, resource limits, and Horizontal Pod Autoscaler support
- **Local Development**: Optimized for Minikube with single hostname (`todo-app.local`)
- **Easy Scaling**: Scale services with simple `kubectl` commands or Helm values

## Deployment Options

1. **Local Development** (Quick Start): Direct npm/uv commands
2. **Docker Compose** (Containerized): Three-service orchestration
3. **Kubernetes/Helm** (Phase 4 - Production-like): Minikube deployment with Ingress

Choose the deployment method that best fits your needs. See [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md) for detailed Kubernetes deployment instructions.

## License

MIT
