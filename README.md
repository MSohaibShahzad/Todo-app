# Todo Application - Complete Project

A comprehensive todo application showcasing the evolution from a console-based application to a full-stack web application.

## 📋 Overview

This project demonstrates a complete development journey:
- **Phase 1**: Console-based todo app with in-memory storage (Python)
- **Phase 2**: Full-stack web application with authentication and persistent storage (Next.js + FastAPI)

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
└── Phase-2/              # Full-Stack Web Application
    ├── frontend/         # Next.js 16 + TypeScript
    │   ├── app/         # App router pages
    │   ├── components/  # React components
    │   └── lib/         # Utilities & API client
    │
    ├── backend/          # FastAPI + PostgreSQL
    │   ├── src/         # API, auth, models, services
    │   ├── alembic/     # Database migrations
    │   └── tests/       # Backend tests
    │
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

## 🚀 Development Journey

### Phase 1 → Phase 2 Evolution

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| **Storage** | In-memory | PostgreSQL (persistent) |
| **Interface** | Console (CLI) | Web (React + TypeScript) |
| **Users** | Single user | Multi-user with authentication |
| **Platform** | Terminal | Cross-platform web browser |
| **Data Persistence** | Lost on exit | Persisted in database |
| **Authentication** | None | JWT + Better Auth |
| **API** | Direct function calls | REST API (FastAPI) |
| **UI/UX** | Text-based menu | Modern responsive web UI |
| **Testing** | 100 unit tests | Unit + integration tests |

### Key Features Present in Both Phases
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

### Phase 2

**Backend:**
```bash
cd Phase-2/backend
uv run pytest -v                    # All tests
uv run pytest --cov=src             # With coverage
uv run ruff check src/              # Linting
```

**Frontend:**
```bash
cd Phase-2/frontend
npm test                            # Run tests
npm run lint                        # ESLint
npm run type-check                  # TypeScript
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

---

## 📚 Additional Resources

- **Phase-1 Details**: [Phase-1/README.md](Phase-1/README.md)
- **Phase-2 Details**: [Phase-2/README.md](Phase-2/README.md)
- **Quick Start Guide**: [Phase-2/QUICKSTART.md](Phase-2/QUICKSTART.md)
- **API Documentation**: http://localhost:8000/docs (when backend is running)

---

## 📄 License

MIT

---

## 🤝 Contributing

Both phases follow strict code quality standards:
- Type safety (Python type hints / TypeScript)
- Comprehensive testing
- Clean code principles
- Documentation for all public APIs

Feel free to explore both implementations to understand the evolution from a console application to a full-stack web application!
