# Quickstart Guide: Phase II Full-Stack Todo Web Application

**Feature**: 003-full-stack-todo-app
**Date**: 2026-01-09
**Estimated Setup Time**: 15-20 minutes

## Overview

This guide will help you set up the full-stack Todo application for local development. The application consists of:
- **Frontend**: Next.js 16+ (runs on port 3000)
- **Backend**: FastAPI (runs on port 8000)
- **Database**: Neon Serverless PostgreSQL (cloud-hosted)
- **Auth**: Better Auth (integrated in frontend)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

| Software | Minimum Version | Check Command | Install Link |
|----------|----------------|---------------|--------------|
| **Node.js** | 18.17+ | `node --version` | https://nodejs.org |
| **npm** or **pnpm** | Latest | `npm --version` | Included with Node.js |
| **Python** | 3.11+ | `python --version` | https://python.org |
| **uv** | Latest | `uv --version` | https://github.com/astral-sh/uv |
| **Git** | 2.0+ | `git --version` | https://git-scm.com |

### External Services

1. **Neon Account**: Sign up at https://neon.tech (free tier available)
2. **Database**: Create a new Neon project and get connection string

---

## Project Structure

```
Todo-app/Phase-2/
├── frontend/              # Next.js application
│   ├── app/              # App Router pages
│   ├── components/       # React components
│   ├── lib/              # Utilities and API client
│   ├── public/           # Static assets
│   ├── package.json
│   └── .env.local        # Frontend environment variables
├── backend/              # FastAPI application
│   ├── src/
│   │   ├── api/         # Route handlers
│   │   ├── models/      # SQLModel database models
│   │   ├── services/    # Business logic
│   │   ├── auth/        # JWT verification
│   │   └── main.py      # App entry point
│   ├── tests/           # Backend tests
│   ├── pyproject.toml
│   └── .env             # Backend environment variables
└── specs/               # Documentation (you are here!)
```

---

## Setup Instructions

### Step 1: Clone and Navigate to Project

```bash
# Navigate to Phase-2 directory
cd /home/sohaib/hackathon2/Todo-app/Phase-2

# Verify you're in the correct directory
pwd  # Should show: /home/sohaib/hackathon2/Todo-app/Phase-2
```

---

### Step 2: Database Setup (Neon PostgreSQL)

#### 2.1 Create Neon Project

1. Go to https://neon.tech and sign in
2. Click "New Project"
3. Name it "todo-app-dev"
4. Select region (choose closest to your location)
5. Click "Create Project"

#### 2.2 Get Connection String

1. In your Neon dashboard, click "Connection Details"
2. Copy the connection string (it looks like this):
   ```
   postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
3. Save this for the next step

#### 2.3 Run Database Migrations

```bash
# Navigate to backend directory
cd backend

# Set up environment variable (temporary)
export DATABASE_URL="postgresql://your-connection-string-here"

# Install dependencies
uv sync

# Run migrations (create tables)
uv run alembic upgrade head

# Verify tables were created
uv run python -c "from sqlmodel import create_engine; engine = create_engine('$DATABASE_URL'); print('Database connected successfully!')"
```

---

### Step 3: Backend Setup

#### 3.1 Create Environment File

```bash
# Still in backend/ directory
touch .env
```

Add the following content to `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://your-neon-connection-string-here

# JWT Secret (generate a random string)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Generate JWT Secret**:
```bash
# Generate a random secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy the output and use it as JWT_SECRET
```

#### 3.2 Install Dependencies

```bash
# Install Python dependencies using uv
uv sync

# This installs:
# - FastAPI
# - SQLModel
# - python-jose (JWT handling)
# - uvicorn (ASGI server)
# - alembic (migrations)
```

#### 3.3 Run Backend Server

```bash
# Start the development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 3.4 Verify Backend

Open a new terminal and test:

```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","timestamp":"2026-01-09T..."}

# View API documentation
open http://localhost:8000/docs  # macOS
# OR
xdg-open http://localhost:8000/docs  # Linux
# OR visit http://localhost:8000/docs in your browser
```

---

### Step 4: Frontend Setup

#### 4.1 Create Frontend Directory Structure

```bash
# From Phase-2 root
cd ..  # Back to Phase-2
mkdir -p frontend
cd frontend
```

#### 4.2 Initialize Next.js Project

```bash
# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest . --typescript --tailwind --app --use-npm

# Answer prompts:
# ✓ Would you like to use ESLint? Yes
# ✓ Would you like to use Turbopack for next dev? No
# ✓ Would you like to customize the import alias? No
```

#### 4.3 Install Additional Dependencies

```bash
# Install Better Auth
npm install better-auth

# Install UI dependencies
npm install lucide-react class-variance-authority clsx tailwind-merge

# Install form handling
npm install react-hook-form zod @hookform/resolvers

# Install date utilities
npm install date-fns
```

#### 4.4 Create Environment File

```bash
# Create .env.local in frontend directory
touch .env.local
```

Add the following content to `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
DATABASE_URL=postgresql://your-neon-connection-string-here
BETTER_AUTH_SECRET=your-random-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

**Generate Better Auth Secret**:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
# Copy the output and use it as BETTER_AUTH_SECRET
```

#### 4.5 Run Frontend Server

```bash
# Start the development server
npm run dev
```

**Expected Output**:
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Starting...
 ✓ Ready in 2.3s
```

#### 4.6 Verify Frontend

Visit http://localhost:3000 in your browser. You should see the Next.js welcome page.

---

## Development Workflow

### Running Both Servers Concurrently

#### Option 1: Use Two Terminals

**Terminal 1 (Backend)**:
```bash
cd backend
uv run uvicorn src.main:app --reload
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

#### Option 2: Use a Process Manager (Optional)

Install `concurrently`:
```bash
npm install -g concurrently
```

Create `package.json` in Phase-2 root:
```json
{
  "name": "todo-fullstack",
  "scripts": {
    "dev": "concurrently \"cd backend && uv run uvicorn src.main:app --reload\" \"cd frontend && npm run dev\"",
    "backend": "cd backend && uv run uvicorn src.main:app --reload",
    "frontend": "cd frontend && npm run dev"
  }
}
```

Then run:
```bash
npm run dev
```

#### Option 3: Use Docker Compose (Advanced)

Create `docker-compose.yml` in Phase-2 root:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend:/app
    command: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.local
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev
```

Run:
```bash
docker-compose up
```

---

## Testing the Application

### 1. Create an Account

1. Visit http://localhost:3000/signup
2. Enter email and password
3. Click "Sign Up"
4. You should be redirected to the dashboard

### 2. Create a Task

1. On the dashboard, click "New Task"
2. Enter:
   - Title: "Test Task"
   - Priority: High
   - Category: Personal
   - Due Date: Tomorrow
3. Click "Create"
4. Task should appear in the list

### 3. Test Filtering

1. Create multiple tasks with different priorities and categories
2. Use the filter dropdowns:
   - Filter by Status: Pending
   - Filter by Priority: High
   - Filter by Category: Personal
3. Verify only matching tasks appear

### 4. Test Search

1. Enter "Test" in the search box
2. Verify only tasks with "Test" in title or description appear

### 5. Test Recurring Tasks

1. Create a task with:
   - Title: "Daily Standup"
   - Recurrence: Daily
   - Due Date: Today
2. Mark the task as complete
3. Verify a new instance is created with tomorrow's due date

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
cd backend
uv sync
```

**Problem**: `sqlalchemy.exc.OperationalError: could not connect to server`
**Solution**:
- Verify `DATABASE_URL` in `backend/.env` is correct
- Check Neon dashboard to ensure database is running
- Verify your IP is allowed in Neon's IP whitelist (if applicable)

**Problem**: `401 Unauthorized` on all requests
**Solution**:
- Verify `JWT_SECRET` matches between frontend and backend
- Check that frontend is sending `Authorization` header
- Inspect JWT token in browser DevTools → Network → Request Headers

---

### Frontend Issues

**Problem**: `Error: Cannot find module 'better-auth'`
**Solution**:
```bash
cd frontend
npm install
```

**Problem**: `TypeError: fetch failed` when calling API
**Solution**:
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Look for CORS errors in browser console
- Verify backend CORS settings allow `http://localhost:3000`

**Problem**: Authentication not working
**Solution**:
- Verify `BETTER_AUTH_SECRET` is set in `frontend/.env.local`
- Check `DATABASE_URL` is correct (Better Auth needs database access)
- Clear browser cookies and localStorage
- Check browser console for errors

---

### Database Issues

**Problem**: `alembic.util.exc.CommandError: Target database is not up to date`
**Solution**:
```bash
cd backend
uv run alembic upgrade head
```

**Problem**: Tables not created
**Solution**:
```bash
# Check database connection
uv run python -c "from sqlmodel import create_engine, text; engine = create_engine('$DATABASE_URL'); with engine.connect() as conn: print(conn.execute(text('SELECT version()')).fetchone())"

# Re-run migrations
uv run alembic upgrade head
```

**Problem**: Connection pool exhausted
**Solution**:
- Restart backend server
- Check for leaked database connections in code
- Increase Neon connection limit (in Neon dashboard)

---

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `JWT_SECRET` | Secret key for signing JWT tokens | `random-32-char-string` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |
| `ENVIRONMENT` | Environment name | `development` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |
| `DATABASE_URL` | Neon connection (for Better Auth) | Same as backend |
| `BETTER_AUTH_SECRET` | Better Auth secret key | `random-base64-string` |
| `BETTER_AUTH_URL` | Frontend URL for auth callbacks | `http://localhost:3000` |

---

## Next Steps

1. **Explore API Documentation**: http://localhost:8000/docs
2. **Review Code Structure**: See [Architecture Documentation](./research.md)
3. **Run Tests**:
   ```bash
   # Backend tests
   cd backend && uv run pytest

   # Frontend tests
   cd frontend && npm test
   ```
4. **Start Development**: Begin implementing features from [tasks.md](./tasks.md)

---

## Useful Commands

### Backend

```bash
# Install dependencies
uv sync

# Run server
uv run uvicorn src.main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/

# Format code
uv run ruff format src/

# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

### Frontend

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run tests
npm test

# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format
```

---

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Better Auth Documentation](https://better-auth.com)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
- [Neon Documentation](https://neon.tech/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [API contracts](./contracts/README.md) for endpoint specifications
2. Review the [data model](./data-model.md) for database schema
3. Consult the [research document](./research.md) for architectural decisions
4. Check backend logs in the terminal running `uvicorn`
5. Check frontend logs in browser DevTools → Console
6. Search for error messages in relevant documentation

---

**Happy Coding! 🚀**
