"""Database connection and session management."""
from typing import AsyncGenerator
from urllib.parse import urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from src.config import settings

# Create async engine
# Convert postgresql:// to postgresql+asyncpg://
database_url = settings.database_url.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Remove query parameters from URL (like sslmode, channel_binding)
# asyncpg handles SSL differently
parsed = urlparse(database_url)
clean_url = urlunparse((
    parsed.scheme,
    parsed.netloc,
    parsed.path,
    parsed.params,
    '',  # Remove query string
    parsed.fragment
))

# Configure SSL for Neon (or other cloud PostgreSQL providers)
connect_args = {}
if 'sslmode=require' in settings.database_url:
    connect_args['ssl'] = 'require'

engine = create_async_engine(
    clean_url,
    echo=settings.environment == "development",
    future=True,
    connect_args=connect_args,
)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency for FastAPI."""
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
