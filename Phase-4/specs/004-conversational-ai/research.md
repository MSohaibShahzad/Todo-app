# Research: Conversational AI Integration

**Feature**: 004-conversational-ai
**Date**: 2026-01-15
**Status**: Complete

## Overview

This document consolidates research findings for integrating conversational AI into the Todo application. The system will enable users to manage tasks through natural language conversation while maintaining a stateless, database-backed architecture.

## Technology Decisions

### 1. AI Agent Framework

**Decision**: OpenAI Agents SDK

**Rationale**:
- Lightweight, orchestration-focused framework from OpenAI
- Designed for stateless agent workflows with handoffs between specialized agents
- Native integration with OpenAI function calling for tool execution
- Simple pattern: Agents interpret intent → call appropriate tools → return responses
- Better suited for our stateless requirement than complex frameworks like LangChain

**Alternatives Considered**:
- **LangChain**: More complex, opinionated, includes memory/state management we explicitly don't want
- **Anthropic Claude SDK**: Strong for complex reasoning but heavier weight, less tool-focused
- **Custom implementation**: Would require building intent parsing, tool orchestration from scratch

**Integration Pattern**:
```python
from openai import OpenAI

client = OpenAI()

# Define task management agent
task_agent = {
    "name": "Task Manager",
    "instructions": "You help users manage their todo tasks through conversation",
    "tools": [add_task_tool, list_tasks_tool, update_task_tool, delete_task_tool, mark_complete_tool]
}

# Process user message
response = client.agents.run(
    agent=task_agent,
    messages=conversation_history,
    context_variables={"user_id": user_id}
)
```

### 2. MCP Server SDK

**Decision**: Official Model Context Protocol (MCP) SDK for Python

**Rationale**:
- Official SDK ensures compatibility and future support
- Provides standardized tool definition format
- Clean separation between tool interface and implementation
- Supports structured parameters and return types
- Works with multiple AI frameworks (not locked to OpenAI)

**MCP Tool Pattern**:
```python
from mcp.server import Server, Tool
from mcp.types import TextContent

server = Server("todo-mcp-server")

@server.tool()
async def add_task(
    user_id: str,
    title: str,
    description: str = None,
    priority: str = "medium",
    category: str = None,
    due_date: str = None
) -> TextContent:
    """Add a new task to the user's todo list."""
    # Database operation
    task = await create_task_in_db(user_id, title, description, priority, category, due_date)
    return TextContent(
        type="text",
        text=f"Task created: {task.id} - {task.title}"
    )
```

**Alternatives Considered**:
- **Custom REST API**: Already exists, but MCP provides standardized tool interface for AI agents
- **Direct function exposure**: No standardization, harder for AI to discover and call correctly
- **LangChain Tools**: Tied to LangChain ecosystem, not framework-agnostic

### 3. Frontend Chat Interface

**Decision**: OpenAI ChatKit (React component library)

**Rationale**:
- Official OpenAI component library for chat interfaces
- Pre-built components: message list, input field, typing indicators
- Handles common chat UX patterns (scrolling, formatting, loading states)
- Integrates well with Next.js 14 App Router
- Reduces custom UI development time

**Component Structure**:
```tsx
import { ChatContainer, MessageList, MessageInput } from '@openai/chatkit'

export default function ConversationPage() {
  const [messages, setMessages] = useState([])

  const handleSendMessage = async (content: string) => {
    // Send to backend chat endpoint
    const response = await fetch('/api/v1/chat', {
      method: 'POST',
      body: JSON.stringify({ message: content, conversation_id })
    })
    // Update messages with response
  }

  return (
    <ChatContainer>
      <MessageList messages={messages} />
      <MessageInput onSend={handleSendMessage} />
    </ChatContainer>
  )
}
```

**Alternatives Considered**:
- **Custom React components**: More work, reinventing chat UX patterns
- **react-chatbot-kit**: Less actively maintained, not from OpenAI
- **Vercel AI SDK UI**: Good alternative, but ChatKit more focused on conversational UX

### 4. Conversation State Storage

**Decision**: PostgreSQL tables for conversations and messages

**Rationale**:
- Already using PostgreSQL (Neon) for task storage
- ACID compliance ensures conversation history consistency
- Supports efficient queries for conversation retrieval
- Enables 30-day retention policy with scheduled cleanup
- Allows concurrent conversation tracking per user

**Schema Design**:
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tool_calls JSONB,  -- Store tool execution details
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
```

**Alternatives Considered**:
- **Redis**: Fast but requires separate infrastructure, persistence complexity
- **In-memory storage**: Violates stateless requirement, lost on restart
- **File-based storage**: Harder to query, no concurrent access support

### 5. Rate Limiting Strategy

**Decision**: Per-user token bucket with Redis backing

**Rationale**:
- Token bucket algorithm allows burst requests while maintaining average rate
- Redis provides distributed rate limiting across backend instances
- Per-user limits ensure fair resource distribution
- Configurable limits without code changes

**Implementation Pattern**:
```python
from redis import Redis
from datetime import datetime

redis_client = Redis.from_url(settings.redis_url)

async def check_rate_limit(user_id: str, limit: int = 10, window: int = 60):
    """Check if user is within rate limit (10 requests per 60 seconds)."""
    key = f"rate_limit:{user_id}"
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, window)
    return current <= limit
```

**Alternatives Considered**:
- **Database-based**: Slower, adds load to primary database
- **In-memory**: Doesn't work across multiple backend instances
- **API Gateway rate limiting**: Would limit all requests, not just AI endpoints

### 6. AI Model Selection

**Decision**: OpenAI GPT-4 Turbo

**Rationale**:
- Balance of quality and cost for task management domain
- Strong function calling capabilities for tool selection
- 128K context window supports long conversation histories
- Reliable availability and performance
- Cost management through usage quotas ($100/month initial limit)

**Cost Estimation**:
- Input: ~$0.01 per 1K tokens
- Output: ~$0.03 per 1K tokens
- Average conversation: ~500 tokens (input) + 200 tokens (output) = $0.011 per exchange
- Monthly budget supports ~9,000 conversational exchanges
- Per-user quota: 300 requests/month

**Alternatives Considered**:
- **GPT-3.5 Turbo**: Cheaper but less reliable for intent parsing and tool selection
- **Claude 3**: Excellent quality but higher cost, requires Anthropic SDK
- **Open-source models (Llama, Mistral)**: Infrastructure overhead, quality variability

## Integration Architecture

### Request Flow

```
User Message (Frontend)
    ↓
Chat API Endpoint (Backend)
    ↓
Load Conversation Context (Database)
    ↓
Send to AI Agent (OpenAI Agents SDK)
    ↓
Agent Selects Tools (MCP Server)
    ↓
Execute Tool → Database Operation
    ↓
Return Results to Agent
    ↓
Agent Generates Response
    ↓
Persist Message + Tool Calls (Database)
    ↓
Return Response to Frontend
```

### Stateless Guarantee

**Backend Endpoint**: No session storage, reconstructs state per request
```python
@router.post("/chat")
async def chat(
    message: str,
    conversation_id: int,
    user: User = Depends(get_current_user)
):
    # 1. Load conversation history from database
    messages = await get_conversation_messages(conversation_id, user.id)

    # 2. Add new user message
    messages.append({"role": "user", "content": message})

    # 3. Send to AI agent (stateless)
    response = await client.agents.run(
        agent=task_agent,
        messages=messages,
        context_variables={"user_id": user.id}
    )

    # 4. Persist new messages to database
    await save_messages(conversation_id, response.messages)

    # 5. Return response
    return {"message": response.messages[-1]}
```

**AI Agent**: No internal state, context passed per request
```python
def task_agent_instructions(context_variables):
    user_id = context_variables["user_id"]
    return f"""
    You are a helpful task management assistant.
    User ID: {user_id}

    Help the user manage their tasks through natural conversation.
    Use the provided tools to perform task operations.
    Always confirm actions with clear, conversational responses.
    """
```

**MCP Tools**: Pure functions, all state in database
```python
@server.tool()
async def add_task(user_id: str, title: str, **kwargs) -> TextContent:
    """Stateless tool - reads/writes only to database."""
    async with get_db_session() as session:
        task = Task(user_id=user_id, title=title, **kwargs)
        session.add(task)
        await session.commit()
        return TextContent(type="text", text=f"Created task: {task.id}")
```

## Performance Considerations

### Latency Targets

- **Chat endpoint response**: < 2 seconds (p95)
- **Database query**: < 100ms (conversation retrieval)
- **AI inference**: 1-1.5 seconds (GPT-4 Turbo average)
- **Tool execution**: < 50ms per tool call

### Optimization Strategies

1. **Conversation History Truncation**: Keep last 20 messages in context to reduce token costs
2. **Database Connection Pooling**: Reuse connections for conversation queries
3. **Async Operations**: Non-blocking I/O for database and AI API calls
4. **Caching**: Cache user context (name, preferences) in Redis for 5 minutes
5. **Streaming Responses**: Stream AI responses to frontend for perceived performance

### Scalability Limits

- **Concurrent Users**: 100 (OpenAI API rate limits)
- **Conversations per User**: 3 active, unlimited archived
- **Messages per Conversation**: 1000 (truncate older in context)
- **Database Storage**: ~1MB per user per month (conversation + tasks)

## Security Considerations

### Authentication & Authorization

- **JWT Verification**: All chat endpoints verify JWT tokens from Better-Auth
- **User Isolation**: Tools filter operations by authenticated user_id
- **Conversation Ownership**: Users can only access their own conversations

### Input Validation

- **Message Length**: Limit to 2000 characters to prevent abuse
- **Rate Limiting**: 10 requests per minute per user
- **Prompt Injection Protection**: Sanitize user input before sending to AI

### Data Privacy

- **Conversation Retention**: Auto-delete after 30 days
- **PII Handling**: Don't log conversation content in application logs
- **OpenAI Data**: Use zero data retention policy (enterprise tier)

## Error Handling Strategies

### AI Misinterpretation

- **User-Initiated Undo**: "undo last action" command rolls back last tool execution
- **Clarification Prompts**: Agent asks follow-up questions for ambiguous intent
- **Confirmation for Destructive Actions**: "Are you sure?" for bulk deletes

### Tool Execution Failures

- **Graceful Degradation**: Agent acknowledges failure, suggests alternative
- **Retry Logic**: Automatic retry for transient database errors (max 3 attempts)
- **Fallback Responses**: Pre-defined responses for common failure scenarios

### API Availability

- **OpenAI Outage**: Return friendly error message, suggest using traditional UI
- **Database Unavailable**: Queue requests temporarily (Redis), process when available
- **Rate Limit Exceeded**: Queue request, notify user of wait time

## Testing Strategy

### Unit Tests
- MCP tool functions (mocked database)
- Intent parsing accuracy (sample conversations)
- Rate limiting logic
- Conversation retrieval and persistence

### Integration Tests
- End-to-end conversation flows (user message → tool execution → response)
- Multi-turn conversations with context retention
- Error scenarios (invalid input, tool failures)
- Concurrent conversation handling

### Load Tests
- 50 concurrent users sending messages
- 1000 messages per minute across all users
- Database query performance under load

## Migration Path

### Phase 1: Foundation (Week 1)
- Set up MCP server with basic tools (add, list, update, delete, complete)
- Implement conversation storage schema
- Create stateless chat API endpoint
- Integrate OpenAI Agents SDK agent

### Phase 2: Frontend Integration (Week 2)
- Add OpenAI ChatKit to Next.js frontend
- Implement conversation UI page
- Connect to backend chat endpoint
- Add conversation list/management

### Phase 3: Enhancement (Week 3)
- Add rate limiting and cost controls
- Implement undo functionality
- Add conversation retention policy
- Performance optimization

### Phase 4: Refinement (Week 4)
- Error handling improvements
- User feedback collection
- Intent parsing accuracy improvements
- Documentation and deployment

## Open Questions & Risks

### Questions Resolved
- ✅ Which AI model to use? → GPT-4 Turbo (cost/quality balance)
- ✅ How to handle conversation history? → Database with 30-day retention
- ✅ Rate limiting strategy? → Per-user token bucket with queuing
- ✅ Concurrent conversation limit? → 3 active conversations per user
- ✅ Misinterpretation recovery? → Undo + clarification prompts

### Remaining Risks

1. **AI API Costs**: GPT-4 Turbo costs could exceed budget with high usage
   - **Mitigation**: Strict per-user quotas, monitor usage daily, downgrade to GPT-3.5 if needed

2. **Intent Parsing Accuracy**: AI may misinterpret complex or ambiguous requests
   - **Mitigation**: Extensive testing with sample conversations, clarification prompts, undo capability

3. **Performance Degradation**: AI inference latency may exceed 2-second target
   - **Mitigation**: Streaming responses, conversation truncation, caching strategies

4. **Database Growth**: Conversation storage could grow rapidly with adoption
   - **Mitigation**: 30-day auto-deletion, archival strategy for old conversations

5. **OpenAI Dependency**: System unusable if OpenAI API is unavailable
   - **Mitigation**: Clear error messaging, fallback to traditional UI, consider multi-provider strategy

## References

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI ChatKit](https://github.com/openai/chatkit)
- [GPT-4 Turbo Pricing](https://openai.com/pricing)
- [FastAPI Async Patterns](https://fastapi.tiangolo.com/async/)
- [Better-Auth JWT Integration](https://www.better-auth.com/)
