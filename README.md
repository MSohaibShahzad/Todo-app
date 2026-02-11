# Todo Application - Complete Project

**🌐 Live Production App:** [https://nexus-tasks.vercel.app](https://nexus-tasks.vercel.app)

A comprehensive todo application showcasing the evolution from a console-based application to a full-stack web application with conversational AI, deployed on Kubernetes.

## 🎯 Project Evolution

```
Phase 1: Console App          Phase 2: Full-Stack Web      Phase 3: AI Integration       Phase 4: Cloud Native
   (Python CLI)          →    (Next.js + FastAPI)      →   (+ OpenAI + MCP)          →   (Kubernetes + Helm)

   ┌─────────┐               ┌──────────────┐            ┌──────────────┐             ┌─────────────────┐
   │ Console │               │   Browser    │            │   Browser    │             │ Browser (Ingress)│
   │   CLI   │               │   (React)    │            │ (React+Chat) │             │  (Load Balanced) │
   └────┬────┘               └──────┬───────┘            └──────┬───────┘             └────────┬─────────┘
        │                           │                           │                               │
   ┌────▼────┐               ┌──────▼───────┐            ┌──────▼────────┐            ┌────────▼──────────┐
   │In-Memory│               │    FastAPI   │            │  FastAPI + AI │            │  FastAPI Pods     │
   │ Storage │               │   + SQLModel │            │  + MCP Tools  │            │  (Auto-scaling)   │
   └─────────┘               └──────┬───────┘            └──────┬────────┘            └────────┬──────────┘
                                    │                           │                              │
                             ┌──────▼──────┐            ┌──────▼────────┐            ┌────────▼──────────┐
                             │  PostgreSQL │            │  PostgreSQL   │            │ PostgreSQL Pod    │
                             │   (Neon)    │            │ + Conversation│            │ (Persistent Vol)  │
                             └─────────────┘            └───────────────┘            └───────────────────┘
```

## 📋 Overview

This project demonstrates a complete development journey from a simple console application to a production-ready Kubernetes deployment:

- **Phase 1**: Console-based todo app with in-memory storage (Python)
- **Phase 2**: Full-stack web application with authentication and persistent storage (Next.js + FastAPI)
- **Phase 3**: Conversational AI layer — manage tasks through natural language chat (OpenAI GPT-4 + MCP)
- **Phase 4**: Kubernetes deployment — production-ready deployment on Kubernetes/Minikube using Helm charts

### What Each Phase Adds

| Phase | New Capabilities | Key Technologies |
|-------|-----------------|-----------------|
| **1** | Task CRUD, priorities, categories, due dates, recurring tasks | Python, TDD, pytest |
| **2** | Web UI, multi-user auth, persistent storage, responsive design | Next.js, FastAPI, PostgreSQL, Better Auth |
| **3** | Natural language task management, AI agent, conversation history | OpenAI GPT-4, MCP, Redis, ChatKit |
| **4** | Container orchestration, auto-scaling, health monitoring, production deployment | Kubernetes, Helm, Ingress, PVCs |

## 🗂️ Project Structure

```
Todo-app/
├── Phase-1/              # Console Application (Python)
│   ├── src/
│   │   ├── models/      # Task data structures
│   │   ├── services/    # Business logic
│   │   └── cli/         # Console interface
│   └── tests/           # Unit & integration tests
│
├── Phase-2/              # Full-Stack Web Application
│   ├── frontend/         # Next.js 16 + TypeScript
│   ├── backend/          # FastAPI + PostgreSQL
│   └── specs/            # Feature specifications
│
├── Phase-3/              # Conversational AI Enhancement
│   ├── frontend/         # Next.js 16 + TypeScript + ChatKit
│   │   ├── app/
│   │   │   ├── (app)/
│   │   │   │   ├── dashboard/   # Task dashboard
│   │   │   │   └── chat/        # AI chat interface
│   │   │   └── (auth)/          # Login / signup
│   │   ├── components/
│   │   │   ├── chat/            # ChatInterface (OpenAI ChatKit)
│   │   │   ├── features/        # Auth, dashboard, task components
│   │   │   └── ui/              # Reusable UI primitives
│   │   └── lib/                 # API client, hooks, auth config
│   │
│   ├── backend/          # FastAPI + PostgreSQL + AI
│   │   ├── src/
│   │   │   ├── api/             # Routes: health, auth, tasks, chat
│   │   │   ├── models/          # SQLModel: user, task, conversation, message, tool_execution
│   │   │   ├── services/        # Task, conversation, AI agent, cleanup
│   │   │   ├── middleware/      # Rate limiting (SlowAPI + Redis)
│   │   │   └── mcp/             # MCP server — stateless task tools for AI agent
│   │   ├── alembic/             # Database migrations
│   │   └── tests/               # Unit & integration tests
│   │
│   └── specs/            # Feature specifications
│       ├── 003-full-stack-todo-app/
│       └── 004-conversational-ai/
│
└── Phase-4/              # Kubernetes Deployment
    ├── todo-helm/        # Helm Chart for Kubernetes
    │   ├── Chart.yaml           # Chart metadata v1.0.0
    │   ├── values.yaml          # Configuration (250+ lines)
    │   ├── README.md            # Helm chart documentation
    │   └── templates/           # Kubernetes manifests
    │       ├── configmap.yaml       # Environment variables
    │       ├── secret.yaml          # Sensitive data (JWT, OpenAI, DB)
    │       ├── pvc.yaml             # PostgreSQL persistent storage
    │       ├── database-*.yaml      # PostgreSQL deployment & service
    │       ├── backend-*.yaml       # FastAPI deployment & service
    │       ├── frontend-*.yaml      # Next.js deployment & service
    │       ├── ingress.yaml         # NGINX Ingress routing
    │       └── hpa.yaml             # Horizontal Pod Autoscaler
    │
    ├── HELM_DEPLOYMENT_GUIDE.md # Complete deployment guide
    ├── frontend/         # Next.js application (same as Phase-3)
    ├── backend/          # FastAPI application (same as Phase-3)
    └── specs/            # Feature specifications
```

---

## 🖥️ Phase 1: Console Todo Application

A feature-rich console-based todo application with in-memory storage.

### Features

#### Task Organization
- **Priority Levels**: Low/Medium/High with color-coded display (Red/Yellow/Blue)
- **Categories**: Organize tasks into custom categories (Work, Personal, Shopping, etc.)
- **Due Dates**: Set due dates with smart reminders and visual indicators
- **Recurring Tasks**: Daily/Weekly/Monthly recurring tasks that auto-regenerate

#### Search & Filter
- **Keyword Search**: Find tasks by title or description (case-insensitive)
- **Multi-Criteria Filtering**: Filter by status, priority, and category (AND logic)
- **Advanced Sorting**: Sort by ID, priority, title, or due date

#### Smart Notifications
- **Startup Reminders**: Automatic alerts for overdue, due today, and tomorrow's tasks
- **Visual Indicators**: Color-coded OVERDUE (red/bold) and DUE TODAY (yellow/bold) badges

### Tech Stack
- Python 3.13+
- Type hints with mypy strict mode
- 100% test coverage with pytest
- TDD approach (Red-Green-Refactor)

### Quick Start

```bash
cd Phase-1

# Install dependencies
uv sync

# Run the application
uv run python -m src.cli.app

# Run tests
uv run pytest -v
```

### Performance
- Startup time: < 1ms
- Add 100 tasks: ~0.3ms
- All operations complete in under 1 second

📖 **[Full Phase-1 Documentation](Phase-1/README.md)**

---

## 🌐 Phase 2: Full-Stack Web Application

A production-ready web application with user authentication and persistent storage.

### Features

#### User Authentication
- Secure account creation and sign-in with Better Auth
- JWT-based authentication with session persistence
- Protected routes and complete data isolation between users

#### Task Management
- Full CRUD operations with real-time updates
- Priority levels (low, medium, high) with color-coded badges
- **Category Autocomplete**: Type-ahead suggestions from existing categories
- Due dates with overdue indicators and alerts
- Recurring tasks with auto-generation of next occurrence

#### Advanced Features
- **Search**: Find tasks by title, description, or category
- **Filter**: By status, priority, and category
- **Sort**: By created date, title, priority, or due date
- **Real-time Dashboard**: 6 stat cards (total, pending, completed, overdue, due today, due tomorrow)
- **Responsive Design**: Mobile-first, works on all devices
- **Toast Notifications**: User feedback for all actions
- **Form Validation**: Real-time error messages

### Tech Stack

#### Frontend
- Next.js 16.1.1 (App Router with Turbopack)
- TypeScript
- Tailwind CSS 4
- Better Auth for authentication
- SWR for data fetching and caching
- Lucide React icons

#### Backend
- FastAPI (Python)
- SQLModel ORM
- PostgreSQL (Neon)
- JWT authentication with python-jose
- Alembic migrations
- Uvicorn server

### Quick Start

#### Prerequisites
- Python 3.12+
- Node.js 20+
- uv package manager
- PostgreSQL database

#### Backend Setup
```bash
cd Phase-2/backend

# Setup environment
cp .env.example .env
# Edit .env with your DATABASE_URL and JWT_SECRET

# Install and run
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:app --reload --port 8000
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

#### Frontend Setup
```bash
cd Phase-2/frontend

# Setup environment
cp .env.local.example .env.local
# Edit .env.local with your credentials

# Install and run
npm install
npm run dev
```

Frontend: http://localhost:3000

#### Docker Compose (Alternative)
```bash
cd Phase-2
docker-compose up

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

📖 **[Full Phase-2 Documentation](Phase-2/README.md)**

---

## 🤖 Phase 3: Conversational AI

Adds a natural-language chat interface on top of the Phase 2 application. Users can create, view, update, delete, and search tasks by typing plain English — no forms required.

### How It Works

1. **Chat UI** (`/chat`) built with OpenAI ChatKit sends messages to the backend.
2. The **AI Agent** (GPT-4) interprets intent and selects the right **MCP tool** (`add_task`, `list_tasks`, `update_task`, etc.).
3. Each MCP tool is **stateless**: it runs the operation against PostgreSQL via the existing task service and returns a structured result.
4. The agent formats the result into a conversational reply.
5. Full **conversation history** (messages + tool executions) is persisted in the database for context continuity across sessions.

### Features

#### Natural Language Task Management
- **Create**: "remind me to call John tomorrow at 2pm" → task created with title + due date
- **View & Search**: "what's due today?" / "show my high priority work tasks"
- **Update**: "mark groceries as done" / "reschedule report to next Monday"
- **Delete**: "delete the grocery task" / "clear all completed tasks"
- **Advanced Queries**: "high priority work tasks due this week sorted by date"

#### Safety & Resource Management
- **Undo**: Reverse the last AI action to recover from misinterpretations
- **Clarification**: AI asks follow-up questions when intent is ambiguous
- **Per-User Rate Limiting**: Fair API usage with request queuing (SlowAPI + Redis)
- **Concurrent Conversation Limit**: Max 3 active conversations per user
- **30-Day Retention**: Conversation history is automatically cleaned up daily
- **User Isolation**: All MCP tools filter by `user_id`; AI agent never touches the DB directly

### Tech Stack (additions over Phase 2)

| Layer | New Dependencies |
|-------|-----------------|
| Frontend | `@openai/chatkit-react` |
| Backend | `openai`, `mcp`, `redis`, `slowapi`, `apscheduler` |
| Infrastructure | Redis (rate-limit store & request queue) |

### Quick Start

```bash
cd Phase-3/backend
cp .env.example .env
# Add to .env:  OPENAI_API_KEY, AI_MODEL=gpt-4o, REDIS_URL, RATE_LIMIT_PER_MINUTE=10
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:app --reload --port 8000

# second terminal
cd Phase-3/frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Frontend: http://localhost:3000 | Chat: http://localhost:3000/chat | API Docs: http://localhost:8000/docs

📖 **[Full Phase-3 Documentation](Phase-3/README.md)**

---

## ☸️ Phase 4: Kubernetes Deployment

Phase 4 takes the complete Phase 3 application and packages it for production-ready deployment on Kubernetes using Helm charts. Optimized for local development on Minikube with clear paths to production deployment.

### What's New

#### Helm Chart
- **Complete Kubernetes manifests**: ConfigMaps, Secrets, PVCs, Deployments, Services, Ingress, HPA
- **Three-tier architecture**: Separate deployments for PostgreSQL, Backend (FastAPI), and Frontend (Next.js)
- **Configuration management**: Environment variables in ConfigMaps, sensitive data in Secrets
- **Version**: 1.0.0 with 250+ lines of configuration

#### Infrastructure
- **Persistent Storage**: 5Gi Persistent Volume Claim for PostgreSQL data
- **NGINX Ingress**: Path-based routing with single hostname (`todo-app.local`)
  - `/api/*` routes to Backend service
  - `/*` routes to Frontend service
- **Health Probes**: Liveness and readiness checks for all services
- **Resource Management**: CPU/Memory requests and limits configured
- **Auto-scaling**: Horizontal Pod Autoscaler support (optional)

#### Deployment Features
- **Minikube Optimized**: Designed for local Kubernetes development
- **Easy Secrets Management**: All secrets configured in `values.yaml`
- **Docker Image Support**: Built from Phase 3 Dockerfiles
- **Single Command Deploy**: `helm install` deploys entire stack
- **Production Ready**: Clear upgrade path to production Kubernetes

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    NGINX Ingress                         │
│                  (todo-app.local)                        │
│                                                           │
│  /api/*  →  Backend Service    /*  →  Frontend Service  │
└────────────┬──────────────────────────┬─────────────────┘
             │                          │
    ┌────────▼────────┐        ┌────────▼────────┐
    │  Backend Pods   │        │  Frontend Pods  │
    │   (FastAPI)     │        │   (Next.js)     │
    │                 │        │                 │
    │ - Health checks │        │ - Health checks │
    │ - Resource limits│        │ - Resource limits│
    │ - HPA ready     │        │ - HPA ready     │
    └────────┬────────┘        └────────┬────────┘
             │                          │
             └──────────┬───────────────┘
                        │
                ┌───────▼────────┐
                │ Database Pod   │
                │  (PostgreSQL)  │
                │                │
                │ - 5Gi PVC      │
                │ - Persistent   │
                └────────────────┘
```

### Prerequisites

- **Minikube**: Kubernetes cluster for local development
- **kubectl**: Kubernetes CLI tool
- **Helm 3.0+**: Package manager for Kubernetes
- **Docker**: For building images
- **OpenAI API Key**: For conversational AI features

### Quick Start

```bash
# 1. Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Enable Ingress addon
minikube addons enable ingress

# 3. Build Docker images in Minikube's environment
eval $(minikube docker-env)
cd Phase-4/backend
docker build -t todo-backend:latest .
cd ../frontend
docker build -t todo-frontend:latest .
cd ..

# 4. Configure secrets (REQUIRED!)
# Edit todo-helm/values.yaml and update:
# - backend.secrets.JWT_SECRET (32+ characters)
# - backend.secrets.OPENAI_API_KEY (your OpenAI key)
# - frontend.secrets.BETTER_AUTH_SECRET (32+ characters)
# - database.auth.password (strong password)

# 5. Deploy with Helm
kubectl create namespace todo-app
helm install todo-app ./todo-helm --namespace todo-app

# 6. Configure local DNS
echo "$(minikube ip) todo-app.local" | sudo tee -a /etc/hosts

# 7. Access the application
# Frontend: http://todo-app.local
# Backend API Health: http://todo-app.local/api/v1/health
# API Docs: http://todo-app.local/api/docs
```

### Helm Commands

```bash
# Install the chart
helm install todo-app ./todo-helm --namespace todo-app

# Upgrade (after making changes)
helm upgrade todo-app ./todo-helm --namespace todo-app

# Rollback to previous version
helm rollback todo-app --namespace todo-app

# View release history
helm history todo-app --namespace todo-app

# Uninstall
helm uninstall todo-app --namespace todo-app
```

### Kubernetes Operations

```bash
# Check pod status
kubectl get pods -n todo-app

# View logs
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app-backend -f

# Check ingress
kubectl get ingress -n todo-app

# Port forward (bypass Ingress)
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:3000

# Scale services
kubectl scale deployment todo-app-backend -n todo-app --replicas=3

# Execute command in pod
kubectl exec -it -n todo-app <pod-name> -- /bin/sh
```

### Configuration Options

Key settings in `todo-helm/values.yaml`:

```yaml
# Image tags
backend.image.tag: "latest"
frontend.image.tag: "latest"

# Replica counts
backend.replicas: 1
frontend.replicas: 1

# Resource limits
backend.resources.limits.cpu: "1000m"
backend.resources.limits.memory: "1Gi"

# Autoscaling
backend.autoscaling.enabled: true
backend.autoscaling.minReplicas: 2
backend.autoscaling.maxReplicas: 10

# Storage
database.persistence.size: "5Gi"

# AI configuration
backend.env.AI_MODEL: "gpt-4-turbo"
backend.env.RATE_LIMIT_REQUESTS_PER_MINUTE: "10"
backend.env.CONVERSATION_RETENTION_DAYS: "30"
```

### Monitoring & Troubleshooting

#### Common Issues

**Pods not starting (ImagePullBackOff)**:
```bash
# Ensure using Minikube's Docker
eval $(minikube docker-env)
docker images | grep todo
```

**Ingress not working**:
```bash
# Check Ingress addon
minikube addons list | grep ingress
minikube addons enable ingress
```

**Database connection issues**:
```bash
# Check database pod
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-database
kubectl logs -n todo-app <database-pod-name>
```

#### Health Checks

All services include health probes:

- **Liveness Probe**: Restarts pod if failing
- **Readiness Probe**: Removes from load balancer if failing
- **Endpoint**: `/api/v1/health` (backend), Next.js ready endpoint (frontend)

### Production Considerations

For production deployment:

1. **Secret Management**: Use external secret managers (Sealed Secrets, External Secrets Operator, Vault)
2. **TLS/HTTPS**: Configure TLS certificates in Ingress
3. **Monitoring**: Add Prometheus + Grafana for observability
4. **Backup**: Implement PostgreSQL backup strategy
5. **Autoscaling**: Enable HPA based on CPU/memory metrics
6. **Network Policies**: Restrict pod-to-pod communication
7. **CI/CD**: Automate builds and deployments
8. **Multi-zone**: Deploy across availability zones for high availability

### Tech Stack (Infrastructure)

| Component | Technology |
|-----------|-----------|
| **Container Orchestration** | Kubernetes (Minikube locally) |
| **Package Manager** | Helm 3 |
| **Ingress Controller** | NGINX Ingress |
| **Storage** | Persistent Volume Claims (local-path) |
| **Configuration** | ConfigMaps + Secrets |
| **Autoscaling** | Horizontal Pod Autoscaler |
| **Load Balancing** | Kubernetes Services (ClusterIP) |

### Files & Documentation

- **HELM_DEPLOYMENT_GUIDE.md**: Complete 590-line deployment guide with:
  - Detailed deployment steps
  - Troubleshooting section (ImagePullBackOff, Ingress issues, DB connection)
  - Configuration reference
  - Update and maintenance procedures
  - Cleanup instructions
  - Deployment checklist

- **todo-helm/README.md**: Helm chart specific documentation
- **todo-helm/values.yaml**: All configurable values (250+ lines)
- **todo-helm/templates/**: 12 Kubernetes manifest templates

📖 **[Full Phase-4 Documentation](Phase-4/README.md)**
📖 **[Helm Deployment Guide](Phase-4/HELM_DEPLOYMENT_GUIDE.md)**
📖 **[Helm Chart README](Phase-4/todo-helm/README.md)**

---

## 🚀 Development Journey

### Phase 1 → Phase 2 → Phase 3 → Phase 4 Evolution

| Feature | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---------|---------|---------|---------|---------|
| **Interface** | Console (CLI) | Web UI (React) | Web UI + Chat | Web UI + Chat |
| **Storage** | In-memory | PostgreSQL | PostgreSQL (+ conversation tables) | PostgreSQL (Kubernetes PVC) |
| **Users** | Single | Multi-user + auth | Multi-user + auth | Multi-user + auth |
| **Task Input** | Menu prompts | Forms + modals | Forms **or** natural language | Forms **or** natural language |
| **AI / LLM** | — | — | GPT-4 via OpenAI SDK | GPT-4 via OpenAI SDK |
| **Tool Protocol** | — | — | MCP (stateless tools) | MCP (stateless tools) |
| **Rate Limiting** | — | — | SlowAPI + Redis | SlowAPI + Redis |
| **Conversation State** | — | — | DB-backed, 30-day retention | DB-backed, 30-day retention |
| **Deployment** | Local script | Docker Compose | Docker Compose | **Kubernetes + Helm** |
| **Infrastructure** | — | — | — | **Ingress, PVCs, ConfigMaps, Secrets** |
| **Orchestration** | — | — | — | **Kubernetes (Minikube)** |
| **Scaling** | — | — | — | **Horizontal Pod Autoscaler** |
| **Health Monitoring** | — | — | — | **Liveness/Readiness Probes** |
| **Testing** | 100 unit tests | Unit + integration | Unit + integration + MCP tool tests | Unit + integration + MCP + K8s deployment tests |

### Key Features Present in All Phases
✅ Priority levels with color coding
✅ Category organization
✅ Due dates with overdue tracking
✅ Recurring tasks
✅ Search and filtering
✅ Advanced sorting
✅ Comprehensive testing

---

## 🧪 Testing

### Phase 1
```bash
cd Phase-1
uv run pytest -v                    # All tests
uv run pytest --cov=src             # With coverage
uv run mypy src/ --strict           # Type checking
```

### Phase 2, 3 & 4

**Backend:**
```bash
cd Phase-2/backend   # or Phase-3/backend or Phase-4/backend
uv run pytest -v                    # All tests
uv run pytest --cov=src             # With coverage
uv run ruff check src/              # Linting
```

**Frontend:**
```bash
cd Phase-2/frontend  # or Phase-3/frontend or Phase-4/frontend
npm test                            # Run tests
npm run lint                        # ESLint
npm run type-check                  # TypeScript
```

### Phase 4 - Kubernetes

**Verify Deployment:**
```bash
cd Phase-4

# Check all resources
kubectl get all -n todo-app

# Check pod health
kubectl get pods -n todo-app

# Verify ingress
kubectl get ingress -n todo-app

# Test backend health
curl http://todo-app.local/api/v1/health

# View logs
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app-backend
```

---

## 📦 Code Quality Standards

### Phase 1
- ✅ Full type hints with mypy strict mode
- ✅ PEP 8 compliant with ruff
- ✅ 100 unit tests with 99% coverage
- ✅ TDD approach (Red-Green-Refactor)

### Phase 2
- ✅ TypeScript strict mode
- ✅ ESLint + Prettier formatting
- ✅ Comprehensive API documentation (Swagger)
- ✅ Integration tests for data isolation
- ✅ Type-safe database models (SQLModel)

### Phase 3
- ✅ All Phase 2 standards carried forward
- ✅ MCP tool unit tests (per-tool isolation)
- ✅ Integration tests for full chat → tool → DB flow
- ✅ Data-isolation tests (cross-user task access prevention)
- ✅ Prompt-injection input sanitization

### Phase 4
- ✅ All Phase 3 standards carried forward
- ✅ Infrastructure as Code (Helm charts with 12 manifests)
- ✅ Configuration management (ConfigMaps + Secrets separation)
- ✅ Health probes on all services (liveness + readiness)
- ✅ Resource limits and requests defined
- ✅ Comprehensive deployment documentation (590+ lines)
- ✅ Production-ready architecture (three-tier with persistent storage)

---

## 📚 Additional Resources

### Documentation by Phase

- **Phase-1 Details**: [Phase-1/README.md](Phase-1/README.md)
- **Phase-2 Details**: [Phase-2/README.md](Phase-2/README.md)
- **Phase-3 Details**: [Phase-3/README.md](Phase-3/README.md)
- **Phase-3 Spec**: [Phase-3/specs/004-conversational-ai/spec.md](Phase-3/specs/004-conversational-ai/spec.md)
- **Phase-4 Details**: [Phase-4/README.md](Phase-4/README.md)
- **Phase-4 Helm Guide**: [Phase-4/HELM_DEPLOYMENT_GUIDE.md](Phase-4/HELM_DEPLOYMENT_GUIDE.md) ⭐
- **Phase-4 Helm Chart**: [Phase-4/todo-helm/README.md](Phase-4/todo-helm/README.md)

### Component Documentation

- **Backend README**: [Phase-4/backend/README.md](Phase-4/backend/README.md)
- **Frontend README**: [Phase-4/frontend/README.md](Phase-4/frontend/README.md) (coming soon)
- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Kubernetes Dashboard**: `minikube dashboard` (when using Minikube)

### External Resources

- **Helm Documentation**: https://helm.sh/docs/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Minikube Guide**: https://minikube.sigs.k8s.io/docs/
- **OpenAI API**: https://platform.openai.com/docs/
- **MCP Protocol**: https://modelcontextprotocol.io/

---

## 🔄 Deployment Options Comparison

Choose the deployment method that best fits your needs:

| Feature | Local Dev (Phase 2/3) | Docker Compose (Phase 2/3) | Kubernetes/Helm (Phase 4) |
|---------|----------------------|---------------------------|--------------------------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐ Moderate | ⭐⭐⭐ Advanced |
| **Prerequisites** | Python, Node.js, PostgreSQL | Docker, Docker Compose | Minikube, Helm, kubectl |
| **Startup Time** | Fast (~30s) | Medium (~2min) | Slower (~5min first time) |
| **Isolation** | None (local processes) | Container isolation | Pod + namespace isolation |
| **Scaling** | Manual | Manual | Automatic (HPA) |
| **Production-like** | ❌ No | ⚠️ Somewhat | ✅ Yes |
| **Persistent Data** | Local files | Docker volumes | Persistent Volume Claims |
| **Load Balancing** | ❌ No | ❌ No | ✅ Yes (Ingress) |
| **Health Monitoring** | ❌ No | ❌ No | ✅ Yes (probes) |
| **Resource Limits** | ❌ No | ⚠️ Basic | ✅ Full (requests/limits) |
| **Configuration Management** | .env files | .env + docker-compose.yml | ConfigMaps + Secrets |
| **Best For** | Quick prototyping | Local full-stack dev | Learning K8s, pre-production testing |

### Recommendations

- **First Time / Quick Testing**: Use Local Dev (Phase 2/3)
- **Full-Stack Development**: Use Docker Compose (Phase 2/3)
- **Learning Kubernetes**: Use Phase 4 with Minikube
- **Pre-Production Testing**: Use Phase 4 with full Kubernetes cluster
- **Production**: Use Phase 4 with managed Kubernetes (EKS, GKE, AKS)

---

## 📄 License

MIT

---

## 🤝 Contributing

All phases follow strict code quality standards:
- Type safety (Python type hints / TypeScript)
- Comprehensive testing
- Clean code principles
- Documentation for all public APIs

Feel free to explore the implementations to understand the evolution from a console application to a production-ready Kubernetes deployment with conversational AI!

---

## 🚢 Quick Start by Phase

### Phase 1 - Console App (Fastest)
```bash
cd Phase-1 && uv sync && uv run python -m src.cli.app
```

### Phase 2 - Full-Stack Web (Recommended for Development)
```bash
cd Phase-2 && docker-compose up
# Visit: http://localhost:3000
```

### Phase 3 - With AI Chat
```bash
cd Phase-3 && docker-compose up
# Visit: http://localhost:3000/chat
```

### Phase 4 - Kubernetes (Production-like)
```bash
cd Phase-4
minikube start --cpus=4 --memory=8192
eval $(minikube docker-env)
# Build images, configure secrets, deploy with Helm
# See Phase-4/HELM_DEPLOYMENT_GUIDE.md for complete instructions
```

---

## 📊 Project Statistics

- **Total Lines of Code**: ~15,000+
- **Backend Tests**: 100+ unit + integration tests
- **Frontend Components**: 30+ React components
- **API Endpoints**: 15+ REST endpoints
- **MCP Tools**: 7 AI agent tools
- **Kubernetes Manifests**: 12 Helm templates
- **Documentation Files**: 10+ comprehensive guides
- **Docker Images**: 2 (backend + frontend)
- **Database Tables**: 5 (users, tasks, conversations, messages, tool_executions)
