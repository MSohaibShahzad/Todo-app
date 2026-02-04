# Quick Start Guide - Todo App Phase 2

## ✅ What's Already Done

All dependencies have been installed and the core MVP is implemented:

### Backend (Installed ✓)
- FastAPI with async SQLModel
- JWT authentication
- PostgreSQL async drivers
- All Python dependencies installed via `uv`

### Frontend (Installed ✓)
- Next.js 16 with TypeScript
- Better Auth for authentication
- SWR for data fetching
- Tailwind CSS 4
- All npm packages installed

---

## 🚀 Getting Started (3 Steps)

### Step 1: Set Up Database

**Create PostgreSQL database:**
```bash
# Using createdb (if you have PostgreSQL installed locally)
createdb todoapp

# Or using psql
psql -U postgres -c "CREATE DATABASE todoapp;"
```

**For production (Neon PostgreSQL recommended):**
1. Go to https://neon.tech
2. Create a new project
3. Copy the connection string

---

### Step 2: Configure Environment Variables

**Backend environment (`backend/.env`):**
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```env
# Update with your actual database URL
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp

# Generate a strong secret (run: openssl rand -hex 32)
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

**Frontend environment (`frontend/.env.local`):**
```bash
cd ../frontend
cp .env.local.example .env.local
```

Edit `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000

# Same database URL as backend
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp

# Generate a strong secret (run: openssl rand -hex 32)
BETTER_AUTH_SECRET=your-secret-key-change-this-in-production
BETTER_AUTH_URL=http://localhost:3000
```

---

### Step 3: Initialize Database

**Create and run migrations:**
```bash
cd ../backend

# Create initial migration
uv run alembic revision --autogenerate -m "Initial schema with users and tasks"

# Apply migrations
uv run alembic upgrade head
```

**Initialize Better Auth tables:**
```bash
cd ../frontend

# Better Auth will auto-create its tables on first run
# No manual setup needed!
```

---

## 🎯 Run the Application

### Terminal 1 - Backend Server
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

### Terminal 2 - Frontend Server
```bash
cd frontend
npm run dev
```

Expected output:
```
▲ Next.js 16.1.1
- Local:        http://localhost:3000
- Ready in 1.2s
```

---

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 📝 First-Time Usage

1. **Go to** http://localhost:3000
   - You'll be redirected to `/login` (no account yet)

2. **Click "Sign up"**
   - Create an account with email and password
   - You'll be auto-redirected to `/dashboard`

3. **Create your first task**
   - Click "New Task" button
   - Fill in title, description, priority, category
   - Click "Create Task"

4. **Manage tasks**
   - ✓ Mark complete/incomplete
   - ✏️ Edit task details
   - 🗑️ Delete tasks (with confirmation)
   - See task count (total and completed)

---

## 🔧 Development Commands

### Backend

**Start server:**
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

**Run tests (once Phase 9 is complete):**
```bash
uv run pytest
uv run pytest -v  # Verbose
uv run pytest --cov=src  # With coverage
```

**Code quality:**
```bash
uv run ruff check src/  # Linting
uv run ruff format src/  # Formatting
uv run mypy src/  # Type checking
```

**Database migrations:**
```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Show current revision
uv run alembic current

# Show migration history
uv run alembic history
```

### Frontend

**Start dev server:**
```bash
cd frontend
npm run dev
```

**Build for production:**
```bash
npm run build
npm start
```

**Code quality:**
```bash
npm run lint  # ESLint
```

---

## 🧪 Test the API (Optional)

### Using curl

**Health check:**
```bash
curl http://localhost:8000/api/v1/health
```

**Create a task (requires JWT token):**
```bash
# First, get a token by signing up/logging in through the frontend
# Then use the token:
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "high"}'
```

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click "Authorize" button (top-right)
3. Enter your JWT token (get it from browser dev tools after logging in)
4. Try out the endpoints!

---

## 📂 Project Structure

```
Phase-2/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/               # API endpoints
│   │   │   ├── health.py      # Health check
│   │   │   └── tasks.py       # Task CRUD endpoints
│   │   ├── auth/              # Authentication
│   │   │   ├── jwt.py         # JWT token creation/verification
│   │   │   └── dependencies.py  # get_current_user()
│   │   ├── models/            # Database models
│   │   │   ├── user.py        # User model
│   │   │   └── task.py        # Task model
│   │   ├── schemas/           # Pydantic schemas
│   │   │   └── task.py        # Task schemas
│   │   ├── services/          # Business logic
│   │   │   └── task_service.py  # Task CRUD service
│   │   ├── config.py          # Settings
│   │   ├── database.py        # DB connection
│   │   └── main.py            # FastAPI app
│   ├── alembic/               # Database migrations
│   └── tests/                 # Tests (Phase 9)
│
├── frontend/                   # Next.js frontend
│   ├── app/
│   │   ├── (auth)/            # Auth pages
│   │   │   ├── login/         # Login page
│   │   │   └── signup/        # Signup page
│   │   ├── (app)/             # Protected app pages
│   │   │   ├── dashboard/     # Main dashboard
│   │   │   └── layout.tsx     # App layout with auth guard
│   │   └── page.tsx           # Home (redirects to dashboard)
│   ├── components/
│   │   ├── ui/                # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Select.tsx
│   │   └── features/          # Feature components
│   │       ├── auth/          # Auth components
│   │       └── tasks/         # Task components
│   ├── lib/
│   │   ├── api/               # API clients
│   │   │   ├── client.ts      # Base API client
│   │   │   └── tasks.ts       # Task API functions
│   │   ├── auth/              # Auth config
│   │   │   └── config.ts      # Better Auth setup
│   │   ├── hooks/             # React hooks
│   │   │   ├── useAuth.ts     # Auth hook
│   │   │   └── useTasks.ts    # Tasks SWR hook
│   │   └── utils/             # Utilities
│   │       └── cn.ts          # Class merger
│   └── types/                 # TypeScript types
│       ├── task.ts            # Task types
│       └── api.ts             # API types
│
└── specs/                      # Feature specifications
    └── 003-full-stack-todo-app/
```

---

## 🐛 Troubleshooting

### Database Connection Errors

**Error: `connection refused`**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Start PostgreSQL if not running
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

**Error: `database "todoapp" does not exist`**
```bash
createdb todoapp
```

### Backend Won't Start

**Error: `ModuleNotFoundError`**
```bash
cd backend
uv sync  # Reinstall dependencies
```

**Error: `Alembic upgrade failed`**
```bash
# Check migration files
uv run alembic current
uv run alembic history

# Reset and recreate (⚠️ WARNING: Deletes all data)
dropdb todoapp
createdb todoapp
uv run alembic upgrade head
```

### Frontend Won't Start

**Error: `Cannot find module`**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: `Better Auth database error`**
- Check that `DATABASE_URL` is correct in `frontend/.env.local`
- Better Auth will auto-create tables on first signup

### CORS Errors

**Error: `CORS policy blocked`**
- Check `FRONTEND_URL` in `backend/.env` matches frontend URL
- Default should be `http://localhost:3000`
- Restart backend after changing

---

## 🎉 You're Ready!

Your full-stack todo application is now running with:

✅ User authentication (signup, login, logout)
✅ Task CRUD operations
✅ Secure data isolation
✅ Professional UI
✅ Type-safe TypeScript
✅ Production-ready architecture

**Next steps:**
- Use the app and create tasks!
- Explore additional features in Phase 5-9
- Deploy to production (see `README.md` for deployment guide)

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Better Auth Docs**: https://better-auth.dev
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Tailwind CSS**: https://tailwindcss.com

**Having issues?** Check `IMPLEMENTATION_STATUS.md` for detailed implementation notes.
