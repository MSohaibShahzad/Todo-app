"""ChatKit server implementation for task management."""
from datetime import datetime
from typing import Any, AsyncIterator, Optional, List

import openai
from agents import Agent, Runner, function_tool, RunContextWrapper
from chatkit.server import ChatKitServer
from chatkit.types import ThreadMetadata, UserMessageItem, ThreadStreamEvent
from chatkit.agents import AgentContext, stream_agent_response, simple_to_agent_input
from chatkit.store import Store, AttachmentStore

from src.mcp import todo_server
from src.config import settings


# Define tool wrappers that extract user_id from AgentContext

@function_tool
async def add_task_tool(
    ctx: RunContextWrapper[AgentContext],
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    category: Optional[str] = None,
    due_date: Optional[str] = None
) -> str:
    """Add a new task to the user's todo list.

    Args:
        title: Task title (required)
        description: Optional task description
        priority: Task priority (low, medium, high). Default: medium
        category: Optional category for organization
        due_date: Optional due date in ISO 8601 format (e.g., "2026-01-16T14:00:00Z")

    Returns:
        Success message with task ID
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.add_task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        category=category,
        due_date=due_date
    )
    return result.text


@function_tool
async def list_tasks_tool(
    ctx: RunContextWrapper[AgentContext],
    filter_completed: Optional[bool] = None,
    filter_priority: Optional[str] = None,
    filter_category: Optional[str] = None,
    limit: int = 50
) -> str:
    """List user's tasks with optional filters.

    Args:
        filter_completed: Filter by completion status (True/False/None for all)
        filter_priority: Filter by priority (low, medium, high)
        filter_category: Filter by category name
        limit: Maximum number of tasks to return (default: 50)

    Returns:
        Formatted list of tasks
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.list_tasks(
        user_id=user_id,
        filter_completed=filter_completed,
        filter_priority=filter_priority,
        filter_category=filter_category,
        limit=limit
    )
    return result.text


@function_tool
async def update_task_tool(
    ctx: RunContextWrapper[AgentContext],
    task_identifier: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
) -> str:
    """Update an existing task.

    Args:
        task_identifier: Task ID (number like "5") or task title (text) to identify the task
        title: New title (optional)
        description: New description (optional)
        priority: New priority (low, medium, high) (optional)
        category: New category (optional)
        due_date: New due date in ISO 8601 format (optional)
        completed: New completion status (optional)

    Returns:
        Success message
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.update_task(
        user_id=user_id,
        task_identifier=task_identifier,
        title=title,
        description=description,
        priority=priority,
        category=category,
        due_date=due_date,
        completed=completed
    )
    return result.text


@function_tool
async def delete_task_tool(
    ctx: RunContextWrapper[AgentContext],
    task_identifier: str
) -> str:
    """Delete a task.

    Args:
        task_identifier: Task ID (number like "5") or task title (text) to identify the task

    Returns:
        Success message
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.delete_task(
        user_id=user_id,
        task_identifier=task_identifier
    )
    return result.text


@function_tool
async def mark_task_complete_tool(
    ctx: RunContextWrapper[AgentContext],
    task_identifier: str,
    completed: bool = True
) -> str:
    """Mark a task as complete or incomplete.

    Args:
        task_identifier: Task ID (number like "5") or task title (text) to identify the task
        completed: Completion status (default: True)

    Returns:
        Success message
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.mark_task_complete(
        user_id=user_id,
        task_identifier=task_identifier,
        completed=completed
    )
    return result.text


@function_tool
async def search_tasks_tool(
    ctx: RunContextWrapper[AgentContext],
    query: str,
    limit: int = 20
) -> str:
    """Search tasks by keyword in title or description.

    Args:
        query: Search query string
        limit: Maximum number of results (default: 20)

    Returns:
        Search results
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.search_tasks(
        user_id=user_id,
        query=query,
        limit=limit
    )
    return result.text


@function_tool
async def bulk_delete_tasks_tool(
    ctx: RunContextWrapper[AgentContext],
    task_ids: List[int]
) -> str:
    """Delete multiple tasks at once.

    Args:
        task_ids: List of task IDs to delete

    Returns:
        Summary of deleted tasks
    """
    user_id = ctx.context.request_context.get("user_id")
    if not user_id:
        raise ValueError("User ID not found in request context")

    result = await todo_server.bulk_delete_tasks(
        user_id=user_id,
        task_ids=task_ids
    )
    return result.text


class TaskManagementChatKitServer(ChatKitServer):
    """ChatKit server for task management using OpenAI Agents SDK."""

    def __init__(
        self,
        data_store: Store,
        attachment_store: Optional[AttachmentStore] = None
    ):
        """Initialize the ChatKit server.

        Args:
            data_store: Store for thread/message persistence
            attachment_store: Optional store for file attachments
        """
        super().__init__(data_store, attachment_store)

    # Define the task management agent with AgentContext type
    task_agent = Agent[AgentContext](
        model=settings.ai_model,
        name="Task Assistant",
        instructions="""
        You are a helpful task management assistant.
        Help users manage their todo tasks through natural conversation.

        Use the provided tools to perform task operations:
        - add_task_tool: Create new tasks from user requests
        - list_tasks_tool: View all tasks or filtered subsets
        - update_task_tool: Modify existing task attributes
        - delete_task_tool: Remove a single task
        - mark_task_complete_tool: Mark tasks as complete or incomplete
        - search_tasks_tool: Search tasks by keyword
        - bulk_delete_tasks_tool: Delete multiple tasks at once

        Always:
        - Confirm actions with clear, conversational responses
        - Ask clarifying questions when user intent is ambiguous
        - Extract task details from natural language (title, priority, dates, etc.)
        - Be friendly and helpful
        - Explain what you're doing in natural language
        - After creating, updating, or deleting tasks, confirm what was done

        When working with tasks:
        - Parse priority from words like "urgent", "high priority", "important" → high
        - Parse dates from natural language like "tomorrow", "next Friday", "by Monday"
        - Extract categories from context when mentioned
        - For viewing tasks, ask which filters to apply if unclear (completed, priority, category)
        - For updating/deleting/completing tasks, users can specify either:
          * Task ID (e.g., "5", "task 5") - shown in brackets like [5] when listing tasks
          * Task title (e.g., "buy groceries") - will find matching task
        - If multiple tasks match a title, ask user to specify the task ID
        - For deletions, ask for confirmation if it seems like an important task

        Natural language examples:
        - "add task to buy groceries" → use add_task_tool
        - "show my tasks" → use list_tasks_tool
        - "what do I need to do today?" → use list_tasks_tool with appropriate filters
        - "mark task 5 as done" → use mark_task_complete_tool with task_identifier="5"
        - "mark 'buy groceries' as done" → use mark_task_complete_tool with task_identifier="buy groceries"
        - "change the due date for task 3" → use update_task_tool with task_identifier="3"
        - "update my shopping task" → use update_task_tool with task_identifier="shopping"
        - "delete task 7" → use delete_task_tool with task_identifier="7"
        - "delete the groceries task" → use delete_task_tool with task_identifier="groceries"
        - "find tasks about groceries" → use search_tasks_tool
        """,
        tools=[
            add_task_tool,
            list_tasks_tool,
            update_task_tool,
            delete_task_tool,
            mark_task_complete_tool,
            search_tasks_tool,
            bulk_delete_tasks_tool,
        ],
    )

    async def respond(
        self,
        thread: ThreadMetadata,
        input: Optional[UserMessageItem],
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Process user message and stream response events.

        Args:
            thread: Thread metadata containing conversation context
            input: User's message input (can be None for thread initialization)
            context: Request context (can contain user auth info, etc.)

        Yields:
            ThreadStreamEvent: ChatKit events for streaming to client
        """
        # Create agent context with thread and store
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Load conversation history from the thread
        conversation_history = []
        if thread.id:
            try:
                page = await self.store.load_thread_items(
                    thread_id=thread.id,
                    after=None,
                    limit=20,
                    order="asc",
                    context=context,
                )
                conversation_history = await simple_to_agent_input(page.data)
            except Exception as e:
                print(f"[ChatKit] Warning: Failed to load conversation history: {e}")

        # Convert current ChatKit input to Agents SDK format
        current_input = await simple_to_agent_input(input) if input else []

        # Generate title IMMEDIATELY for first message (before streaming)
        # This ensures the title is set when ChatKit loads the thread list
        if not conversation_history and input and thread.id:
            await self._generate_thread_title_sync(thread, input, context)

        # Combine conversation history with current input
        agent_input = conversation_history + current_input

        # Run agent in streaming mode
        result = Runner.run_streamed(
            self.task_agent,
            agent_input,
            context=agent_context,
        )

        # Stream agent response events back to ChatKit
        async for event in stream_agent_response(agent_context, result):
            yield event

    async def _generate_thread_title_sync(
        self,
        thread: ThreadMetadata,
        user_message: UserMessageItem,
        context: Any,
    ) -> None:
        """Generate a simple title immediately from the first user message.

        Creates title from first 40 characters of message. This happens
        BEFORE streaming starts so the title is available immediately.

        Args:
            thread: Thread metadata to update
            user_message: First user message in the thread
            context: Request context
        """
        try:
            # Extract user message text
            message_text = ""
            if hasattr(user_message, 'content') and isinstance(user_message.content, list):
                for part in user_message.content:
                    if hasattr(part, 'text'):
                        message_text = str(part.text).strip()
                        break

            if not message_text:
                print("[ChatKit] No message text for title")
                return

            # Generate simple title from message text
            # Take first 40 chars, capitalize first letter
            generated_title = message_text[:40]
            if len(message_text) > 40:
                # Find last space to avoid cutting words
                last_space = generated_title.rfind(' ')
                if last_space > 20:  # Only if we have at least 20 chars
                    generated_title = generated_title[:last_space]
                generated_title += "..."

            # Capitalize first letter
            if generated_title:
                generated_title = generated_title[0].upper() + generated_title[1:]

            print(f"[ChatKit] Generated title for thread {thread.id}: '{generated_title}'")

            # Update title in thread metadata (for current request)
            thread.metadata["title"] = generated_title

            # Save to database immediately using context session
            session = context.get("session")
            if not session:
                print("[ChatKit] ❌ No session in context")
                return

            from sqlalchemy import update as sql_update
            from src.models.conversation import Conversation

            # Update the conversation directly
            stmt = (
                sql_update(Conversation)
                .where(Conversation.id == thread.id)
                .values(title=generated_title, updated_at=datetime.utcnow())
            )
            await session.execute(stmt)
            await session.commit()

            print(f"[ChatKit] ✅ Title saved: '{generated_title}' for thread {thread.id}")

        except Exception as e:
            print(f"[ChatKit] ❌ Error generating title: {e}")
            import traceback
            traceback.print_exc()
