"""Conversation service for managing chat sessions."""
from datetime import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Conversation, Message, MessageRole
from src.config import settings


class ConversationService:
    """Service for conversation CRUD operations."""

    @staticmethod
    async def create_conversation(
        user_id: str,
        title: Optional[str],
        session: AsyncSession
    ) -> Conversation:
        """Create a new conversation.

        Args:
            user_id: User ID
            title: Optional conversation title
            session: Database session

        Returns:
            Created conversation

        Raises:
            ValueError: If user has reached max active conversations limit
        """
        # Check active conversation limit
        stmt = select(func.count()).where(
            Conversation.user_id == user_id,
            Conversation.is_active == True
        )
        count = await session.scalar(stmt)

        if count >= settings.max_active_conversations_per_user:
            raise ValueError(
                f"Maximum {settings.max_active_conversations_per_user} active conversations reached. "
                "Please archive an existing conversation first."
            )

        # Create conversation
        conversation = Conversation(
            user_id=user_id,
            title=title,
            is_active=True
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        return conversation

    @staticmethod
    async def get_conversation(
        conversation_id: int,
        user_id: str,
        session: AsyncSession
    ) -> Optional[Conversation]:
        """Get conversation by ID with ownership check.

        Args:
            conversation_id: Conversation ID
            user_id: User ID (for ownership check)
            session: Database session

        Returns:
            Conversation if found and owned by user, None otherwise
        """
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_conversation_messages(
        conversation_id: int,
        user_id: str,
        session: AsyncSession,
        limit: int = 20
    ) -> list[Message]:
        """Get last N messages for a conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User ID (for ownership check)
            limit: Number of recent messages to retrieve
            session: Database session

        Returns:
            List of messages in chronological order

        Raises:
            ValueError: If conversation not found or access denied
        """
        # Verify ownership
        conversation = await ConversationService.get_conversation(
            conversation_id, user_id, session
        )
        if not conversation:
            raise ValueError("Conversation not found or access denied")

        # Get messages
        stmt = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)

        result = await session.execute(stmt)
        messages = list(result.scalars())

        # Return in chronological order
        return list(reversed(messages))

    @staticmethod
    async def list_conversations(
        user_id: str,
        is_active: Optional[bool],
        limit: int,
        session: AsyncSession
    ) -> list[Conversation]:
        """List user's conversations.

        Args:
            user_id: User ID
            is_active: Filter by active status (None for all)
            limit: Maximum number of conversations
            session: Database session

        Returns:
            List of conversations ordered by updated_at desc
        """
        stmt = select(Conversation).where(Conversation.user_id == user_id)

        if is_active is not None:
            stmt = stmt.where(Conversation.is_active == is_active)

        stmt = stmt.order_by(Conversation.updated_at.desc()).limit(limit)

        result = await session.execute(stmt)
        return list(result.scalars())

    @staticmethod
    async def update_conversation(
        conversation_id: int,
        user_id: str,
        title: Optional[str],
        is_active: Optional[bool],
        session: AsyncSession
    ) -> Conversation:
        """Update conversation metadata.

        Args:
            conversation_id: Conversation ID
            user_id: User ID (for ownership check)
            title: New title (optional)
            is_active: New active status (optional)
            session: Database session

        Returns:
            Updated conversation

        Raises:
            ValueError: If conversation not found or access denied
        """
        conversation = await ConversationService.get_conversation(
            conversation_id, user_id, session
        )
        if not conversation:
            raise ValueError("Conversation not found or access denied")

        if title is not None:
            conversation.title = title
        if is_active is not None:
            conversation.is_active = is_active

        conversation.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(conversation)

        return conversation

    @staticmethod
    async def delete_conversation(
        conversation_id: int,
        user_id: str,
        session: AsyncSession
    ) -> None:
        """Delete a conversation (cascade deletes messages and tool executions).

        Args:
            conversation_id: Conversation ID
            user_id: User ID (for ownership check)
            session: Database session

        Raises:
            ValueError: If conversation not found or access denied
        """
        conversation = await ConversationService.get_conversation(
            conversation_id, user_id, session
        )
        if not conversation:
            raise ValueError("Conversation not found or access denied")

        await session.delete(conversation)
        await session.commit()
