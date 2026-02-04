"""Cleanup service for conversation retention policy."""
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import Conversation


async def cleanup_old_conversations(session: AsyncSession) -> dict:
    """Delete conversations older than retention period (30 days by default).

    Args:
        session: Database session

    Returns:
        dict with cleanup results (deleted_count, cutoff_date)
    """
    # Calculate cutoff date
    cutoff_date = datetime.utcnow() - timedelta(days=settings.conversation_retention_days)

    # Find old conversations
    stmt = select(Conversation).where(Conversation.updated_at < cutoff_date)
    result = await session.execute(stmt)
    old_conversations = list(result.scalars())

    deleted_count = 0
    for conversation in old_conversations:
        await session.delete(conversation)
        deleted_count += 1

    await session.commit()

    return {
        "deleted_count": deleted_count,
        "cutoff_date": cutoff_date.isoformat(),
        "retention_days": settings.conversation_retention_days
    }
