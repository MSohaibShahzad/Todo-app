"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.api import api_router
from src.config import settings
from src.database import create_db_and_tables, async_session_maker
from src.middleware.rate_limit import limiter
from src.services.cleanup_service import cleanup_old_conversations

# Initialize scheduler
scheduler = AsyncIOScheduler()


async def run_cleanup_job():
    """Run conversation cleanup job."""
    async with async_session_maker() as session:
        result = await cleanup_old_conversations(session)
        print(f"[Cleanup] Deleted {result['deleted_count']} conversations older than {result['retention_days']} days")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await create_db_and_tables()

    # Schedule cleanup job (daily at 2 AM)
    scheduler.add_job(
        run_cleanup_job,
        'cron',
        hour=2,
        minute=0,
        id='cleanup_old_conversations'
    )
    scheduler.start()
    print("[Scheduler] Started conversation cleanup job (daily at 2 AM)")

    yield

    # Shutdown
    scheduler.shutdown()
    print("[Scheduler] Stopped")


app = FastAPI(
    title="Todo API",
    description="Backend API for Todo Web Application",
    version="1.0.0",
    lifespan=lifespan,
)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")
