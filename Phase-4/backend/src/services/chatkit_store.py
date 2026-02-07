"""SQLAlchemy-based Store implementation for ChatKit."""
import json
import uuid
from typing import Any, Dict, Literal, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from chatkit.store import Store
from chatkit.types import (
    ThreadMetadata, ThreadItem, Attachment, Page,
    UserMessageItem, AssistantMessageItem,
    UserMessageTextContent, AssistantMessageContent,
    InferenceOptions,
)

from src.models.conversation import Conversation
from src.models.message import Message, MessageRole


class SQLAlchemyStore(Store[Dict[str, Any]]):
    """Store implementation using SQLAlchemy with PostgreSQL.

    Maps ChatKit concepts to our existing database schema:
    - Thread -> Conversation
    - ThreadItem -> Message
    - TContext -> Dict with 'user_id' and 'session' keys
    """

    def __init__(self):
        """Initialize the store."""
        super().__init__()

    def generate_thread_id(self, context: Dict[str, Any]) -> str:
        """Generate a new thread ID using UUID."""
        return str(uuid.uuid4())

    # generate_item_id: use base class default (unique IDs like msg_a1b2c3d4)

    async def load_thread(self, thread_id: str, context: Dict[str, Any]) -> ThreadMetadata:
        """Load a thread by ID."""
        session: AsyncSession = context.get("session")
        user_id: str = context.get("user_id")

        if not session or not user_id:
            raise ValueError("Session and user_id required in context")

        result = await session.execute(
            select(Conversation).where(
                Conversation.id == thread_id,
                Conversation.user_id == user_id
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise ValueError(f"Thread {thread_id} not found")

        # Convert Conversation to ThreadMetadata
        return ThreadMetadata(
            id=str(conversation.id),
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            metadata={
                "title": conversation.title,
                "is_active": conversation.is_active,
                "user_id": conversation.user_id
            }
        )

    async def save_thread(self, thread: ThreadMetadata, context: Dict[str, Any]) -> None:
        """Save a thread."""
        session: AsyncSession = context.get("session")
        user_id: str = context.get("user_id")

        if not session or not user_id:
            raise ValueError("Session and user_id required in context")

        # Check if conversation exists
        result = await session.execute(
            select(Conversation).where(Conversation.id == thread.id)
        )
        conversation = result.scalar_one_or_none()

        if conversation:
            # Update existing conversation
            conversation.updated_at = datetime.utcnow()
            if "title" in thread.metadata:
                conversation.title = thread.metadata["title"]
            if "is_active" in thread.metadata:
                conversation.is_active = thread.metadata["is_active"]
        else:
            # Create new conversation with the UUID from thread.id
            conversation = Conversation(
                id=thread.id,
                user_id=user_id,
                title=thread.metadata.get("title", "Chat"),
                is_active=True,
                created_at=thread.created_at or datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conversation)

        await session.commit()

    async def load_thread_items(
        self,
        thread_id: str,
        after: Optional[str],
        limit: int,
        order: str,
        context: Dict[str, Any],
    ) -> Page[ThreadItem]:
        """Load thread items (messages)."""
        session: AsyncSession = context.get("session")

        if not session:
            raise ValueError("Session required in context")

        # Build query
        query = select(Message).where(Message.conversation_id == thread_id)

        # Order by id (auto-increment) for reliable insertion order
        if order == "desc":
            query = query.order_by(desc(Message.id))
        else:
            query = query.order_by(asc(Message.id))

        # Cursor-based pagination: direction depends on sort order
        if after:
            after_id = int(after)
            if order == "desc":
                query = query.where(Message.id < after_id)
            else:
                query = query.where(Message.id > after_id)

        # Apply limit
        query = query.limit(limit)

        result = await session.execute(query)
        messages = result.scalars().all()

        # Convert messages to proper ChatKit ThreadItem types
        items: list[ThreadItem] = []
        for msg in messages:
            if msg.role == MessageRole.USER:
                items.append(UserMessageItem(
                    id=str(msg.id),
                    thread_id=thread_id,
                    content=[UserMessageTextContent(text=msg.content)],
                    created_at=msg.created_at,
                    attachments=[],
                    inference_options=InferenceOptions(),
                ))
            elif msg.role == MessageRole.ASSISTANT:
                items.append(AssistantMessageItem(
                    id=str(msg.id),
                    thread_id=thread_id,
                    content=[AssistantMessageContent(text=msg.content)],
                    created_at=msg.created_at,
                ))
            # skip system messages

        has_more = len(messages) == limit
        next_cursor = str(messages[-1].id) if messages and has_more else None

        return Page(
            data=items,
            after=next_cursor,
            has_more=has_more,
        )

    async def add_thread_item(
        self, thread_id: str, item: ThreadItem, context: Dict[str, Any]
    ) -> None:
        """Add an item to a thread."""
        from chatkit.types import UserMessageItem, AssistantMessageItem

        session: AsyncSession = context.get("session")
        if not session:
            raise ValueError("Session required in context")

        # Determine role based on item type
        item_class_name = item.__class__.__name__
        print(f"[ChatKit Store] Item class: {item_class_name}", flush=True)

        if isinstance(item, AssistantMessageItem):
            role = MessageRole.ASSISTANT
            print(f"[ChatKit Store] Detected as AssistantMessageItem via isinstance", flush=True)
        elif isinstance(item, UserMessageItem):
            role = MessageRole.USER
            print(f"[ChatKit Store] Detected as UserMessageItem via isinstance", flush=True)
        else:
            # Fallback: check type string
            item_type = str(getattr(item, 'type', '')).lower()
            print(f"[ChatKit Store] Fallback check, item.type={item_type}", flush=True)
            if 'assistant' in item_type or 'output' in item_type:
                role = MessageRole.ASSISTANT
            else:
                role = MessageRole.USER

        # Extract text content
        content = ""
        if hasattr(item, 'content') and isinstance(item.content, list):
            # Extract text from content list
            content_parts = []
            for part in item.content:
                if hasattr(part, 'text'):
                    content_parts.append(str(part.text))
            content = " ".join(content_parts) if content_parts else str(item)
        elif hasattr(item, 'text'):
            content = str(item.text)
        else:
            content = str(item)

        print(f"[ChatKit Store] Final role={role.value}, content={content[:50]}", flush=True)

        message = Message(
            conversation_id=thread_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        await session.commit()

    async def save_item(
        self, thread_id: str, item: ThreadItem, context: Dict[str, Any]
    ) -> None:
        """Save/update an item."""
        # For now, treat as add (updates are rare in chat)
        await self.add_thread_item(thread_id, item, context)

    async def load_item(
        self, thread_id: str, item_id: str, context: Dict[str, Any]
    ) -> ThreadItem:
        """Load a specific item."""
        session: AsyncSession = context.get("session")

        if not session:
            raise ValueError("Session required in context")

        msg_id = int(item_id)

        result = await session.execute(
            select(Message).where(
                Message.id == msg_id,
                Message.conversation_id == thread_id
            )
        )
        message = result.scalar_one_or_none()

        if not message:
            raise ValueError(f"Item {item_id} not found in thread {thread_id}")

        if message.role == MessageRole.USER:
            return UserMessageItem(
                id=str(message.id),
                thread_id=thread_id,
                content=[UserMessageTextContent(text=message.content)],
                created_at=message.created_at,
                attachments=[],
                inference_options=InferenceOptions(),
            )
        else:
            return AssistantMessageItem(
                id=str(message.id),
                thread_id=thread_id,
                content=[AssistantMessageContent(text=message.content)],
                created_at=message.created_at,
            )

    async def delete_thread(self, thread_id: str, context: Dict[str, Any]) -> None:
        """Delete a thread."""
        session: AsyncSession = context.get("session")
        user_id: str = context.get("user_id")

        if not session or not user_id:
            raise ValueError("Session and user_id required in context")

        result = await session.execute(
            select(Conversation).where(
                Conversation.id == thread_id,
                Conversation.user_id == user_id
            )
        )
        conversation = result.scalar_one_or_none()

        if conversation:
            await session.delete(conversation)
            await session.commit()

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: Dict[str, Any]
    ) -> None:
        """Delete a thread item."""
        session: AsyncSession = context.get("session")

        if not session:
            raise ValueError("Session required in context")

        msg_id = int(item_id)

        result = await session.execute(
            select(Message).where(
                Message.id == msg_id,
                Message.conversation_id == thread_id
            )
        )
        message = result.scalar_one_or_none()

        if message:
            await session.delete(message)
            await session.commit()

    async def load_threads(
        self,
        limit: int,
        after: Optional[str],
        order: str,
        context: Dict[str, Any],
    ) -> Page[ThreadMetadata]:
        """Load threads for a user."""
        session: AsyncSession = context.get("session")
        user_id: str = context.get("user_id")

        if not session or not user_id:
            raise ValueError("Session and user_id required in context")

        # Build query
        query = select(Conversation).where(Conversation.user_id == user_id)

        # Apply ordering
        if order == "desc":
            query = query.order_by(desc(Conversation.updated_at))
        else:
            query = query.order_by(asc(Conversation.updated_at))

        # Apply cursor
        if after:
            after_id = int(after)
            query = query.where(Conversation.id > after_id)

        query = query.limit(limit)

        result = await session.execute(query)
        conversations = result.scalars().all()

        threads = [
            ThreadMetadata(
                id=str(conv.id),
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                metadata={
                    "title": conv.title,
                    "is_active": conv.is_active,
                    "user_id": conv.user_id
                }
            )
            for conv in conversations
        ]

        has_more = len(conversations) == limit
        next_cursor = str(conversations[-1].id) if conversations and has_more else None

        return Page(
            data=threads,
            after=next_cursor,
            has_more=has_more,
        )

    async def save_attachment(self, attachment: Attachment, context: Dict[str, Any]) -> None:
        """Save an attachment (not implemented)."""
        raise NotImplementedError("Attachment storage not implemented")

    async def load_attachment(self, attachment_id: str, context: Dict[str, Any]) -> Attachment:
        """Load an attachment (not implemented)."""
        raise NotImplementedError("Attachment storage not implemented")

    async def delete_attachment(self, attachment_id: str, context: Dict[str, Any]) -> None:
        """Delete an attachment (not implemented)."""
        raise NotImplementedError("Attachment storage not implemented")
