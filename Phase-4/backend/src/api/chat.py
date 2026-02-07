"""Chat API endpoints for conversational AI."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_session
from src.middleware.rate_limit import limiter, get_rate_limit_key
from src.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    SendMessageResponse,
    MessageResponse,
    ToolExecutionResponse
)
from src.services import conversation_service
from src.services import ai_agent_service
from src.models.message import MessageRole, Message
from src.models.tool_execution import ToolExecution, ToolExecutionStatus

router = APIRouter(prefix="/conversations", tags=["chat"])


# Placeholder routes - will be implemented in Phase 3+ (User Story implementations)

@router.get("/")
async def list_conversations(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """List user's conversations.

    Implemented in Phase 9 (Conversation Management)
    """
    return {"conversations": [], "message": "Conversation management coming in Phase 9"}


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new conversation.

    Optionally send an initial message to start the conversation.

    Args:
        data: Conversation creation data (title, optional initial_message)
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Created conversation with messages if initial_message was provided

    Raises:
        HTTPException: If user has reached max active conversations limit
    """
    # Create conversation
    conversation = await conversation_service.ConversationService.create_conversation(
        user_id=user_id,
        title=data.title,
        session=session
    )

    # If initial message provided, process it
    if data.initial_message:
        # Create user message
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=data.initial_message
        )
        session.add(user_message)
        await session.flush()
        await session.refresh(user_message)

        # Process with AI agent
        agent_response = await ai_agent_service.process_message(
            user_id=user_id,
            message=data.initial_message,
            conversation_history=[]
        )

        # Create assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=agent_response["message"]
        )
        session.add(assistant_message)
        await session.flush()
        await session.refresh(assistant_message)

        # Save tool executions
        for tool_call in agent_response.get("tool_calls", []):
            tool_exec = ToolExecution(
                message_id=assistant_message.id,
                conversation_id=conversation.id,
                tool_name=tool_call["tool_name"],
                parameters=tool_call["parameters"],
                result=tool_call.get("result"),
                status=ToolExecutionStatus.SUCCESS if tool_call.get("result") else ToolExecutionStatus.FAILED
            )
            session.add(tool_exec)

        await session.commit()

        # Reload conversation with messages
        await session.refresh(conversation)
        conversation_messages = await conversation_service.ConversationService.get_conversation_messages(
            conversation_id=conversation.id,
            user_id=user_id,
            session=session,
            limit=10
        )

        response = ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            is_active=conversation.is_active,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[MessageResponse.model_validate(msg) for msg in conversation_messages]
        )
        return response

    # Return conversation without messages
    response = ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        is_active=conversation.is_active,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[]  # No messages when no initial_message provided
    )
    return response


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get conversation details with message history.

    Implemented in Phase 9 (Conversation Management)
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Conversation retrieval will be implemented in Phase 9"
    )


@router.post("/{conversation_id}/messages", response_model=SendMessageResponse)
@limiter.limit("10/minute", key_func=get_rate_limit_key)
async def send_message(
    request: Request,
    conversation_id: int,
    data: MessageCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Send a message and receive AI response.

    Rate limited to 10 requests per minute per user.

    Args:
        conversation_id: ID of the conversation
        data: Message content
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Both user and assistant messages with tool executions

    Raises:
        HTTPException: If conversation not found or not owned by user
        HTTPException: If rate limit exceeded (429)
    """
    # Verify conversation exists and belongs to user
    conversation = await conversation_service.ConversationService.get_conversation(
        conversation_id=conversation_id,
        user_id=user_id,
        session=session
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Get conversation history (last 20 messages)
    history_messages = await conversation_service.ConversationService.get_conversation_messages(
        conversation_id=conversation_id,
        user_id=user_id,
        session=session,
        limit=20
    )
    conversation_history = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history_messages
    ]

    # Create user message
    user_message = Message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=data.content
    )
    session.add(user_message)
    await session.flush()
    await session.refresh(user_message)

    # Process with AI agent
    agent_response = await ai_agent_service.process_message(
        user_id=user_id,
        message=data.content,
        conversation_history=conversation_history
    )

    # Create assistant message
    assistant_message = Message(
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
        content=agent_response["message"]
    )
    session.add(assistant_message)
    await session.flush()
    await session.refresh(assistant_message)

    # Save tool executions
    tool_executions = []
    for tool_call in agent_response.get("tool_calls", []):
        tool_exec = ToolExecution(
            message_id=assistant_message.id,
            conversation_id=conversation_id,
            tool_name=tool_call["tool_name"],
            parameters=tool_call["parameters"],
            result=tool_call.get("result"),
            status=ToolExecutionStatus.SUCCESS if tool_call.get("result") else ToolExecutionStatus.FAILED
        )
        session.add(tool_exec)
        await session.flush()
        await session.refresh(tool_exec)
        tool_executions.append(tool_exec)

    await session.commit()

    return SendMessageResponse(
        user_message=MessageResponse.model_validate(user_message),
        assistant_message=MessageResponse.model_validate(assistant_message),
        tool_executions=[ToolExecutionResponse.model_validate(te) for te in tool_executions]
    )


@router.post("/{conversation_id}/undo")
async def undo_last_action(
    conversation_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Undo last tool execution.

    Implemented in Phase 8 (Undo Functionality)
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Undo functionality will be implemented in Phase 8"
    )
