"""Utility functions for MCP tools."""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker


@asynccontextmanager
async def get_db_session():
    """Get database session for MCP tools.

    Usage:
        async with get_db_session() as session:
            # Perform database operations
            pass
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
