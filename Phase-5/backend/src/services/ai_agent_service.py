"""AI agent service for conversational task management.

This service uses OpenAI Agents SDK to interpret user intent and call appropriate MCP tools.
"""
from dataclasses import dataclass
from typing import Optional

from agents import Agent, Runner, function_tool, RunContextWrapper

from src.config import settings
from src.mcp import todo_server


# Define context for passing user_id to tools
@dataclass
class UserContext:
    """Context containing authenticated user information."""
    user_id: str


# Define tool wrappers for OpenAI Agents SDK
# These bridge the Agents SDK to our MCP tool functions


@function_tool
async def add_task_tool(
    ctx: RunContextWrapper[UserContext],
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
    # Get user_id from context
    user_id = ctx.context.user_id

    # Call the MCP tool function
    result = await todo_server.add_task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        category=category,
        due_date=due_date
    )

    return result.text


# Define task management agent with UserContext type
task_agent = Agent[UserContext](
    name="Task Manager",
    instructions="""
    You are a helpful task management assistant.
    Help users manage their todo tasks through natural conversation.

    Use the provided tools to perform task operations:
    - add_task_tool: Create new tasks from user requests

    Always:
    - Confirm actions with clear, conversational responses
    - Ask clarifying questions when user intent is ambiguous
    - Extract task details from natural language (title, priority, dates, etc.)
    - Be friendly and helpful
    - Explain what you're doing in natural language

    When adding tasks:
    - Parse priority from words like "urgent", "high priority", "important" → high
    - Parse dates from natural language like "tomorrow", "next Friday", "by Monday"
    - Extract categories from context when mentioned
    """,
    tools=[add_task_tool],
    model=settings.ai_model
)


async def process_message(
    user_id: str,
    message: str,
    conversation_history: list
) -> dict:
    """Process user message and return agent response.

    Args:
        user_id: Authenticated user's ID
        message: User's input message
        conversation_history: Previous messages in the conversation (list of dicts with 'role' and 'content')

    Returns:
        dict with:
        - 'message': Agent's response text
        - 'tool_calls': List of tools executed (dicts with 'tool_name', 'parameters', 'result')
    """
    try:
        # Create user context
        user_ctx = UserContext(user_id=user_id)

        # Run agent with user context
        result = await Runner.run(
            starting_agent=task_agent,
            input=message,
            context=user_ctx
        )

        # Extract tool call information from result
        tool_calls = []
        if hasattr(result, 'tool_calls') and result.tool_calls:
            for tool_call in result.tool_calls:
                tool_calls.append({
                    "tool_name": tool_call.name if hasattr(tool_call, 'name') else "unknown",
                    "parameters": tool_call.arguments if hasattr(tool_call, 'arguments') else {},
                    "result": tool_call.result if hasattr(tool_call, 'result') else None
                })

        return {
            "message": result.final_output if hasattr(result, 'final_output') else str(result),
            "tool_calls": tool_calls
        }

    except Exception as e:
        return {
            "message": f"I encountered an error: {str(e)}",
            "tool_calls": []
        }
