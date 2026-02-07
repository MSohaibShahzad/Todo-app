# Backend Guidelines

## Stack
- **Framework**: FastAPI
- **ORM**: SQLModel (async via SQLAlchemy)
- **Database**: PostgreSQL (Neon) — async driver: asyncpg / psycopg[binary]
- **Migrations**: Alembic
- **Package manager**: uv
- **AI**: OpenAI GPT-4 via `openai` SDK + `openai-agents` (Agents SDK)
- **Chat protocol**: `openai-chatkit` — production chat UI backend
- **Tool protocol**: MCP (`mcp` SDK) — stateless tools exposed to AI agents
- **Rate limiting**: SlowAPI + Redis
- **Scheduling**: APScheduler (conversation cleanup job, daily 2 AM UTC)

## Project Structure
```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point, lifespan, scheduler setup
│   ├── config.py            # Pydantic settings (all env vars)
│   ├── database.py          # Async SQLAlchemy engine + session factory
│   ├── api/                 # Route handlers
│   │   ├── health.py        # GET /api/v1/health
│   │   ├── auth.py          # Auth endpoints
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   ├── chat.py          # Conversation REST endpoints
│   │   └── chatkit.py       # ChatKit protocol endpoints (streaming)
│   ├── auth/                # Authentication helpers
│   │   ├── jwt.py           # JWT create / verify (HS256)
│   │   └── dependencies.py  # get_current_user() FastAPI dependency
│   ├── models/              # SQLModel database models
│   │   ├── user.py          # User (string ID, Better Auth compatible)
│   │   ├── task.py          # Task (CRUD, priority, recurrence)
│   │   ├── conversation.py  # Conversation (chat session, 3-per-user limit)
│   │   ├── message.py       # Message (user/assistant/system roles, tool_calls JSONB)
│   │   └── tool_execution.py# ToolExecution (audit trail, undo support)
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── task.py          # Task schemas
│   │   └── conversation.py  # Conversation / message schemas
│   ├── services/            # Business logic
│   │   ├── task_service.py          # Task CRUD operations
│   │   ├── conversation_service.py  # Conversation CRUD
│   │   ├── ai_agent_service.py      # OpenAI Agents SDK integration
│   │   ├── chatkit_server.py        # ChatKit server with 7 task tools
│   │   ├── chatkit_store.py         # SQLAlchemy-backed ChatKit Store
│   │   ├── recurrence_service.py    # Auto-generate next recurring task
│   │   └── cleanup_service.py       # 30-day conversation retention cleanup
│   ├── middleware/
│   │   └── rate_limit.py    # SlowAPI rate limiter config
│   └── mcp/                 # Model Context Protocol
│       ├── todo_server.py   # Stateless task tool implementations
│       ├── utils.py         # MCP utility functions
│       └── __main__.py      # MCP server entry point
├── alembic/                 # Database migrations
│   ├── versions/
│   │   ├── 001_...py        # User ID string migration
│   │   └── 002_...py        # Conversations / messages / tool_executions tables
│   └── env.py
├── tests/                   # Unit + integration tests (pytest + pytest-asyncio)
├── pyproject.toml           # uv project config + all dependencies
├── .env.example             # Environment variable template
└── Dockerfile               # Python 3.12-slim, uv install, alembic upgrade + uvicorn
```

## API Conventions
- All routes under `/api/v1/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- Chat endpoints are rate-limited (SlowAPI, per-user, configurable RPM)

## Database
- Use SQLModel for all database operations
- Async sessions via SQLAlchemy `AsyncSession`
- Connection string from environment variable: `DATABASE_URL`
- Run migrations before first start: `uv run alembic upgrade head`

## Environment Variables
Copy `backend/.env.example` to `backend/.env` and fill in values:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Secret for JWT signing (min 32 chars) |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL (default 30) |
| `FRONTEND_URL` | CORS origin (default `http://localhost:3000`) |
| `ENVIRONMENT` | `development` / `production` / `test` |
| `OPENAI_API_KEY` | OpenAI API key (required for chat) |
| `AI_MODEL` | Model name, e.g. `gpt-4-turbo` |
| `REDIS_URL` | Redis connection for rate limiting |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | Per-user chat RPM (default 10) |
| `CONVERSATION_RETENTION_DAYS` | Auto-delete age (default 30) |
| `MAX_ACTIVE_CONVERSATIONS_PER_USER` | Concurrent conversation cap (default 3) |

## Running
```bash
# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Start server (dev)
uv run uvicorn src.main:app --reload --port 8000

# Tests
uv run pytest
uv run pytest -v --cov=src
```
