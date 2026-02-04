# Tasks: Conversational AI Integration

**Input**: Design documents from `/specs/004-conversational-ai/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are included per the spec requirement for comprehensive testing strategy.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/src/`, `frontend/src/`
- Backend tests: `backend/tests/`
- Frontend tests: `frontend/__tests__/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [ ] T001 Install Python dependencies (openai, swarm-py, mcp, redis, slowapi, apscheduler) in backend/requirements.txt
- [ ] T002 [P] Install NPM dependency (@openai/chatkit) in frontend/package.json
- [ ] T003 [P] Configure Redis connection in backend/src/config.py
- [ ] T004 [P] Add environment variables to backend/.env.example (OPENAI_API_KEY, AI_MODEL, REDIS_URL, rate limits)
- [ ] T005 Create conversation history directories: history/prompts/004-conversational-ai/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Schema

- [ ] T006 Create Alembic migration 002_add_conversations.py in backend/alembic/versions/
- [ ] T007 Define conversations table schema (id, user_id, title, is_active, created_at, updated_at) in migration
- [ ] T008 [P] Define messages table schema (id, conversation_id, role, content, tool_calls, created_at) in migration
- [ ] T009 [P] Define tool_executions table schema (id, message_id, conversation_id, tool_name, parameters, result, status, error_message, created_at, completed_at) in migration
- [ ] T010 Add indexes (user_id, updated_at, conversation_id, status) in migration
- [ ] T011 Run Alembic migration to create tables

### SQLModel Models

- [ ] T012 Create Conversation model in backend/src/models/conversation.py with relationships
- [ ] T013 [P] Create MessageRole enum in backend/src/models/message.py
- [ ] T014 [P] Create Message model in backend/src/models/message.py with relationships
- [ ] T015 [P] Create ToolExecutionStatus enum in backend/src/models/tool_execution.py
- [ ] T016 [P] Create ToolExecution model in backend/src/models/tool_execution.py with relationships
- [ ] T017 Update backend/src/models/__init__.py to export new models

### MCP Server Foundation

- [ ] T018 Create MCP server structure in backend/src/mcp/todo_server.py
- [ ] T019 Initialize MCP Server instance with name "todo-mcp-server"
- [ ] T020 Create backend/src/mcp/__main__.py entry point for MCP server
- [ ] T021 [P] Add database session helper for MCP tools in backend/src/mcp/utils.py

### AI Agent Foundation

- [ ] T022 Create AI agent service structure in backend/src/services/ai_agent_service.py
- [ ] T023 Initialize OpenAI Agents SDK client
- [ ] T024 Define task_agent with instructions in ai_agent_service.py
- [ ] T025 [P] Create conversation service for CRUD operations in backend/src/services/conversation_service.py

### API Foundation

- [ ] T026 Create chat router structure in backend/src/api/chat.py
- [ ] T027 Register chat router in backend/src/api/__init__.py with /conversations prefix
- [ ] T028 [P] Create rate limiting middleware in backend/src/middleware/rate_limit.py
- [ ] T029 [P] Configure SlowAPI limiter with Redis backend in rate_limit.py

### Cleanup & Retention

- [ ] T030 Create cleanup service in backend/src/services/cleanup_service.py
- [ ] T031 Implement cleanup_old_conversations() function (30-day cutoff)
- [ ] T032 Add APScheduler job to backend/src/main.py (daily at 2 AM)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Quick Task Creation via Chat (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks by typing natural language messages like "remind me to call John tomorrow at 2pm"

**Independent Test**: Send chat message "add task: buy groceries", verify task created in database with correct title, confirm conversational response

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T033 [P] [US1] Unit test for add_task MCP tool in backend/tests/unit/test_mcp_add_task.py
- [ ] T034 [P] [US1] Integration test for task creation conversation flow in backend/tests/integration/test_chat_add_task.py

### MCP Tool Implementation

- [ ] T035 [US1] Implement add_task MCP tool in backend/src/mcp/todo_server.py
- [ ] T036 [US1] Add parameter validation for add_task (title required, priority enum, date format)
- [ ] T037 [US1] Implement database insert logic using existing TaskService
- [ ] T038 [US1] Return structured success response with task_id

### AI Agent Integration

- [ ] T039 [US1] Register add_task tool with task_agent in ai_agent_service.py
- [ ] T040 [US1] Add agent instructions for task creation intent recognition
- [ ] T041 [US1] Implement process_message() function to handle user input

### API Endpoint

- [ ] T042 [US1] Implement POST /conversations endpoint in backend/src/api/chat.py
- [ ] T043 [US1] Add validation for initial_message and title parameters
- [ ] T044 [US1] Check active conversation limit (max 3) before creation
- [ ] T045 [US1] Implement POST /conversations/{id}/messages endpoint
- [ ] T046 [US1] Load conversation history from database (last 20 messages)
- [ ] T047 [US1] Call ai_agent_service.process_message() with user input
- [ ] T048 [US1] Persist user message and assistant response to messages table
- [ ] T049 [US1] Log tool execution to tool_executions table
- [ ] T050 [US1] Apply rate limiting (10 req/min) to message endpoint

### Frontend UI

- [ ] T051 [P] [US1] Create conversation page at frontend/app/chat/page.tsx
- [ ] T052 [P] [US1] Install and configure OpenAI ChatKit components
- [ ] T053 [US1] Implement ChatContainer with MessageList and MessageInput
- [ ] T054 [US1] Add handleSendMessage function to call backend API
- [ ] T055 [US1] Display user and assistant messages in MessageList
- [ ] T056 [US1] Add conversation creation UI (new chat button)
- [ ] T057 [US1] Update frontend/lib/api.ts with createConversation() and sendMessage() methods
- [ ] T058 [US1] Add "Chat" navigation link to frontend/app/layout.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via conversation

---

## Phase 4: User Story 2 - View and Search Tasks via Chat (Priority: P2)

**Goal**: Enable users to check tasks by asking questions like "what do I need to do today?" or "show me my high priority tasks"

**Independent Test**: Pre-populate tasks via UI, then query "what's due today?" through chat, verify filtered tasks returned in conversational format

### Tests for User Story 2

- [ ] T059 [P] [US2] Unit test for list_tasks MCP tool in backend/tests/unit/test_mcp_list_tasks.py
- [ ] T060 [P] [US2] Unit test for search_tasks MCP tool in backend/tests/unit/test_mcp_search_tasks.py
- [ ] T061 [P] [US2] Integration test for task query conversation flow in backend/tests/integration/test_chat_list_tasks.py

### MCP Tool Implementation

- [ ] T062 [P] [US2] Implement list_tasks MCP tool with filtering in backend/src/mcp/todo_server.py
- [ ] T063 [P] [US2] Add filter parameters (completed, priority, category, due_date_start, due_date_end, limit, offset)
- [ ] T064 [P] [US2] Implement search_tasks MCP tool with keyword search in backend/src/mcp/todo_server.py
- [ ] T065 [US2] Return structured task list with total_count

### AI Agent Integration

- [ ] T066 [US2] Register list_tasks and search_tasks tools with task_agent
- [ ] T067 [US2] Add agent instructions for query and search intent recognition
- [ ] T068 [US2] Handle natural language date parsing (today, tomorrow, this week)

### Frontend Enhancement

- [ ] T069 [US2] Update MessageList to render task lists in readable format
- [ ] T070 [US2] Add formatting for task attributes (priority, due date, category)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Tasks via Conversation (Priority: P3)

**Goal**: Enable users to modify tasks by saying "mark groceries as done" or "change the due date for report to next Monday"

**Independent Test**: Create task via UI/chat, then send "mark [task] as complete" through chat, verify task status updated

### Tests for User Story 3

- [ ] T071 [P] [US3] Unit test for update_task MCP tool in backend/tests/unit/test_mcp_update_task.py
- [ ] T072 [P] [US3] Unit test for mark_task_complete MCP tool in backend/tests/unit/test_mcp_mark_complete.py
- [ ] T073 [P] [US3] Integration test for task update conversation flow in backend/tests/integration/test_chat_update_task.py

### MCP Tool Implementation

- [ ] T074 [P] [US3] Implement update_task MCP tool in backend/src/mcp/todo_server.py
- [ ] T075 [P] [US3] Add parameter validation for update_task (task_id required, optional fields)
- [ ] T076 [P] [US3] Implement mark_task_complete MCP tool in backend/src/mcp/todo_server.py
- [ ] T077 [US3] Handle task not found errors gracefully

### AI Agent Integration

- [ ] T078 [US3] Register update_task and mark_task_complete tools with task_agent
- [ ] T079 [US3] Add agent instructions for update and completion intent recognition
- [ ] T080 [US3] Handle ambiguous task references (multiple matches → ask for clarification)

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks via Chat (Priority: P4)

**Goal**: Enable users to remove tasks by saying "delete the grocery task" or "remove all completed tasks"

**Independent Test**: Create task via UI/chat, then send "delete [task name]" through chat, verify task deleted from database

### Tests for User Story 4

- [ ] T081 [P] [US4] Unit test for delete_task MCP tool in backend/tests/unit/test_mcp_delete_task.py
- [ ] T082 [P] [US4] Unit test for bulk_delete_tasks MCP tool in backend/tests/unit/test_mcp_bulk_delete.py
- [ ] T083 [P] [US4] Integration test for task deletion conversation flow in backend/tests/integration/test_chat_delete_task.py

### MCP Tool Implementation

- [ ] T084 [P] [US4] Implement delete_task MCP tool in backend/src/mcp/todo_server.py
- [ ] T085 [P] [US4] Implement bulk_delete_tasks MCP tool with filters in backend/src/mcp/todo_server.py
- [ ] T086 [US4] Handle task not found and authorization errors

### AI Agent Integration

- [ ] T087 [US4] Register delete_task and bulk_delete_tasks tools with task_agent
- [ ] T088 [US4] Add agent instructions for delete intent recognition
- [ ] T089 [US4] Implement confirmation prompt for destructive operations (bulk delete)

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Advanced Filtering and Sorting via Chat (Priority: P5)

**Goal**: Enable users to perform complex queries like "show my high priority work tasks due this week sorted by date"

**Independent Test**: Pre-populate diverse task set, then query with multiple filters ("high priority work tasks this week"), verify correct filtering and sorting

### Tests for User Story 5

- [ ] T090 [P] [US5] Unit test for complex filtering in list_tasks tool in backend/tests/unit/test_mcp_complex_filters.py
- [ ] T091 [P] [US5] Integration test for advanced query conversation flow in backend/tests/integration/test_chat_advanced_queries.py

### MCP Tool Enhancement

- [ ] T092 [US5] Add sorting parameters to list_tasks tool (sort_by, sort_order)
- [ ] T093 [US5] Implement date range parsing helpers (this week, next month, etc.)
- [ ] T094 [US5] Add combined filter logic (priority AND category AND date range)

### AI Agent Integration

- [ ] T095 [US5] Add agent instructions for complex query intent recognition
- [ ] T096 [US5] Handle query simplification prompts when intent too complex

**Checkpoint**: All user stories (1-5) should now be independently functional

---

## Phase 8: Undo Functionality (Cross-Cutting)

**Goal**: Allow users to reverse last AI action to recover from misinterpretations

**Independent Test**: Create task via chat, then send "undo last action", verify task deleted and confirmation message received

### Implementation

- [ ] T097 Create undo service in backend/src/services/undo_service.py
- [ ] T098 Implement get_last_tool_execution() to find most recent SUCCESS status
- [ ] T099 Implement undo_tool_execution() with inverse tool mapping logic
- [ ] T100 Handle inverse operations (add_task → delete_task, update_task → restore previous state)
- [ ] T101 Implement POST /conversations/{id}/undo endpoint in backend/src/api/chat.py
- [ ] T102 Add undo button to frontend chat UI in frontend/app/chat/page.tsx
- [ ] T103 Update frontend/lib/api.ts with undoLastAction() method

### Tests

- [ ] T104 [P] Unit test for undo service in backend/tests/unit/test_undo_service.py
- [ ] T105 [P] Integration test for undo conversation flow in backend/tests/integration/test_chat_undo.py

---

## Phase 9: Conversation Management (Cross-Cutting)

**Goal**: Enable users to manage multiple conversations (list, archive, delete)

### Implementation

- [ ] T106 Implement GET /conversations endpoint in backend/src/api/chat.py
- [ ] T107 Add filtering by is_active status
- [ ] T108 Implement PATCH /conversations/{id} endpoint for updating title and is_active
- [ ] T109 Implement DELETE /conversations/{id} endpoint with cascade delete
- [ ] T110 Implement GET /conversations/{id} endpoint with message history
- [ ] T111 Create ConversationList component in frontend/components/ConversationList.tsx
- [ ] T112 Add conversation sidebar to chat page
- [ ] T113 Implement conversation switching in frontend
- [ ] T114 Add archive/delete buttons to conversation list
- [ ] T115 Update frontend/lib/api.ts with conversation management methods

### Tests

- [ ] T116 [P] Unit test for conversation service CRUD operations in backend/tests/unit/test_conversation_service.py
- [ ] T117 [P] Integration test for conversation management API in backend/tests/integration/test_chat_conversations.py

---

## Phase 10: Streaming Responses (Enhancement)

**Goal**: Stream AI responses in real-time for better perceived performance

### Implementation

- [ ] T118 Implement POST /conversations/{id}/stream endpoint in backend/src/api/chat.py
- [ ] T119 Configure Server-Sent Events (SSE) response format
- [ ] T120 Stream OpenAI Agents SDK response tokens incrementally
- [ ] T121 Send tool call events (started, completed status)
- [ ] T122 Update frontend ChatInterface to handle streaming responses
- [ ] T123 Add loading indicators and typing animation

### Tests

- [ ] T124 [P] Integration test for streaming endpoint in backend/tests/integration/test_chat_streaming.py

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [ ] T125 [P] Add comprehensive error handling to all MCP tools
- [ ] T126 [P] Add logging for all AI agent interactions
- [ ] T127 [P] Implement graceful degradation for OpenAI API unavailability
- [ ] T128 [P] Add input sanitization for prompt injection protection
- [ ] T129 [P] Update API documentation in backend/src/api/chat.py docstrings
- [ ] T130 [P] Add loading states and error messages to frontend UI
- [ ] T131 [P] Implement retry logic for transient database errors
- [ ] T132 [P] Add cost monitoring dashboard for OpenAI API usage
- [ ] T133 Performance optimization: Add Redis caching for user context
- [ ] T134 Performance optimization: Implement database connection pooling
- [ ] T135 Security: Add JWT token validation to all chat endpoints
- [ ] T136 Security: Implement user isolation in all MCP tools (filter by user_id)
- [ ] T137 Run quickstart.md validation workflow
- [ ] T138 Update CLAUDE.md with conversation features
- [ ] T139 Create deployment guide in specs/004-conversational-ai/deployment.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Undo (Phase 8)**: Can start after any user story completes (recommended after US1)
- **Conversation Management (Phase 9)**: Can start after Foundational (independent of user stories)
- **Streaming (Phase 10)**: Can start after US1 completes
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent of US1-3
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Builds on US2 (list_tasks enhancement)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- MCP tools before AI agent registration
- Backend API before frontend UI
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T002, T003, T004 can run in parallel
- **Foundational Phase**:
  - T008, T009 (table schemas) in parallel
  - T013, T014, T015, T016 (models) in parallel after T012
  - T021, T025, T028, T029 (services/middleware) in parallel
- **Within Each User Story**:
  - Tests marked [P] can run in parallel
  - MCP tools with [P] can be developed in parallel
- **Cross-Story Parallelism**: After Foundational phase, different developers can work on US1, US2, US3, US4, US5 simultaneously

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T033: "Unit test for add_task MCP tool"
Task T034: "Integration test for task creation conversation flow"

# Launch all frontend tasks in parallel with backend API tasks (different codebases):
Task T045-T050: "Backend API endpoints"
Task T051-T058: "Frontend UI components"
```

## Parallel Example: User Story 2

```bash
# Launch all MCP tools for User Story 2 together:
Task T062: "Implement list_tasks MCP tool"
Task T064: "Implement search_tasks MCP tool"

# Launch all tests in parallel:
Task T059: "Unit test for list_tasks"
Task T060: "Unit test for search_tasks"
Task T061: "Integration test for task query"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T032) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T033-T058)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - users can now create tasks via conversation!

**Estimated Time**: 1.5-2 weeks for MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (now can create + view)
4. Add User Story 3 → Test independently → Deploy/Demo (now can create + view + update)
5. Add Undo Functionality (Phase 8) → Test → Deploy (safety net added)
6. Add User Story 4 → Test independently → Deploy/Demo (full CRUD via chat)
7. Add User Story 5 → Test independently → Deploy/Demo (power user features)
8. Add Conversation Management (Phase 9) → Deploy (multi-conversation support)
9. Add Streaming (Phase 10) → Deploy (better UX)
10. Polish (Phase 11) → Final release

**Estimated Time**: 3-4 weeks for full feature set

### Parallel Team Strategy

With multiple developers:

1. **Week 1**: Team completes Setup + Foundational together (critical path)
2. **Week 2-3**: Once Foundational is done, parallel work:
   - Developer A: User Story 1 (task creation)
   - Developer B: User Story 2 (task viewing)
   - Developer C: User Story 3 (task updating)
3. **Week 3**: Integration and undo functionality
4. **Week 4**: User Stories 4-5, conversation management, streaming, polish

---

## Task Summary

**Total Tasks**: 139 tasks

**Task Count by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 27 tasks (BLOCKING)
- Phase 3 (US1 - Task Creation): 26 tasks
- Phase 4 (US2 - Task Viewing): 12 tasks
- Phase 5 (US3 - Task Updating): 10 tasks
- Phase 6 (US4 - Task Deletion): 9 tasks
- Phase 7 (US5 - Advanced Filtering): 7 tasks
- Phase 8 (Undo): 9 tasks
- Phase 9 (Conversation Management): 12 tasks
- Phase 10 (Streaming): 7 tasks
- Phase 11 (Polish): 15 tasks

**Parallel Opportunities Identified**:
- 68 tasks marked [P] for parallel execution
- 5 user stories can run in parallel after Foundational phase
- Multiple tests within each story can run in parallel

**Independent Test Criteria**:
- US1: Create task via chat, verify in database
- US2: Query tasks via chat, verify correct filtering
- US3: Update task via chat, verify changes persisted
- US4: Delete task via chat, verify removed from database
- US5: Complex query via chat, verify correct multi-filter results

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 58 tasks

---

## Notes

- [P] tasks = different files, no dependencies - safe to parallelize
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **Use Context7 MCP server during implementation** for up-to-date library documentation
- Verify tests fail before implementing (Red → Green → Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution compliance verified: stateless design, MCP architecture, database-backed state ✓
