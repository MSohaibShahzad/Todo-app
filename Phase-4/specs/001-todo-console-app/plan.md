# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

## Summary

Implement a Python 3.13+ console application that provides complete task management capabilities (add, view, update, delete, mark complete/incomplete) with in-memory storage only. The application follows strict TDD principles, clean code standards, and separation of concerns with models, services, and CLI layers clearly delineated.

**Technical Approach**: Use Python dataclasses for the Task model, implement a TaskManager service class for business logic, and provide a console-based menu interface for user interaction. All data stored in-memory using Python dict/list structures with sequential integer IDs starting from 1.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: pytest (testing only - no runtime dependencies beyond Python standard library)
**Storage**: In-memory only (Python dict mapping task ID to Task object)
**Testing**: pytest for unit and integration tests
**Target Platform**: Console/terminal applications (cross-platform via Python)
**Project Type**: Single project (console application)
**Performance Goals**:
- Task operations complete within 3 seconds (SC-001)
- Application startup under 1 second (SC-009)
- Handle 100 tasks with clear display (SC-002)
**Constraints**:
- No external dependencies except pytest
- No file I/O or database access
- Console-only interaction
- In-memory storage only
**Scale/Scope**:
- Single-user, single-session operation
- ~200 character title limit, ~1000 character description limit
- Sequential task IDs (1, 2, 3, ...)

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

### I. Simplicity First ✅

- ✅ No over-engineering: Using standard Python dict for storage, not introducing database abstractions
- ✅ No external frameworks: Only Python standard library for runtime (pytest dev-only)
- ✅ No persistence: Explicit in-memory-only storage per FR-003
- ✅ No auth/multi-user: Single-user console application per FR-012
- ✅ Console-only: No GUI, web, or API components per FR-012

### II. Clean Code ✅

- ✅ Descriptive naming: TaskManager, Task, add_task(), mark_complete(), etc.
- ✅ Single Responsibility: Task (data), TaskManager (logic), CLI (interaction)
- ✅ PEP 8 compliance: Will use black/ruff for formatting
- ✅ Named constants: MAX_TITLE_LENGTH = 200, MAX_DESCRIPTION_LENGTH = 1000
- ✅ Self-documenting: Type hints and clear function signatures

### III. Test-Driven Development (TDD) ✅

- ✅ Red-Green-Refactor cycle: Tests written first for each user story
- ✅ pytest framework: Using pytest for all test execution
- ✅ Test organization: Unit tests (models, services) and integration tests (full workflows)
- ✅ Behavior-focused: Testing user scenarios from spec.md acceptance criteria

### IV. Separation of Concerns ✅

- ✅ Models layer: `src/models/task.py` - Task dataclass only
- ✅ Services layer: `src/services/task_manager.py` - Business logic only
- ✅ CLI layer: `src/cli/` - User interaction and display only
- ✅ No business logic in CLI: CLI calls TaskManager methods, doesn't manipulate tasks directly
- ✅ No UI in services: TaskManager returns data, never prints or reads input

### V. Python Best Practices ✅

- ✅ Type hints: All function signatures include parameter and return types
- ✅ Dataclasses: Task entity as `@dataclass` with typed attributes
- ✅ List comprehensions: For filtering/transforming task lists where appropriate
- ✅ Explicit over implicit: Clear error handling, no silent failures
- ✅ Virtual environment: Managed via `uv` per constitution

**Constitution Compliance**: PASS - All principles satisfied with no violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # User requirements and acceptance criteria
├── research.md          # Phase 0 output (Python best practices, TDD patterns)
├── data-model.md        # Phase 1 output (Task entity design)
├── quickstart.md        # Phase 1 output (User guide for running app)
├── contracts/           # Phase 1 output (Interface definitions)
│   ├── task_manager_interface.md
│   └── cli_interface.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py              # Task dataclass with id, title, description, is_complete
├── services/
│   ├── __init__.py
│   └── task_manager.py      # TaskManager class: add, update, delete, list, mark_complete
└── cli/
    ├── __init__.py
    ├── app.py               # Main application entry point
    ├── menu.py              # Menu display and user input handling
    └── display.py           # Task list formatting and output

tests/
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py       # Task dataclass validation tests
│   └── test_task_manager.py     # TaskManager business logic tests
└── integration/
    ├── __init__.py
    └── test_workflows.py        # End-to-end user story tests

pyproject.toml               # uv project configuration
README.md                    # Project overview and setup instructions
```

**Structure Decision**: Selected "Single project" structure because this is a standalone console application with no frontend/backend split or multi-platform requirements. The src/ directory organizes code by layer (models, services, cli) following Separation of Concerns principle. Tests mirror the source structure with unit/ for isolated component tests and integration/ for full workflow validation.

## Complexity Tracking

> **No violations** - All constitution principles satisfied without exceptions.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                |

---

## Phase 0: Research & Technical Validation

**Purpose**: Validate technical approach and document Python best practices for TDD, dataclasses, and console I/O.

**Output**: `research.md` covering:
- Python 3.13+ dataclass usage patterns
- pytest fixtures and parameterized testing
- Console I/O best practices (input validation, clear display formatting)
- Type hinting strategies for collections and optional values
- TDD workflow in Python (Red-Green-Refactor cycle with pytest)

**Key Questions to Answer**:
1. How to structure pytest fixtures for TaskManager test isolation?
2. What's the best pattern for console menu systems in Python?
3. How to handle user input validation cleanly (empty strings, invalid IDs)?
4. Dataclass vs NamedTuple for Task entity?
5. Type hints for optional description field?

**Deliverables**:
- Research findings documented in `research.md`
- Recommended patterns for implementation
- Example code snippets for key patterns

---

## Phase 1: Design & Contracts

**Purpose**: Define data model, interfaces, and user interaction flow before implementation.

### 1.1 Data Model Design

**Output**: `data-model.md`

**Task Entity**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    is_complete: bool
```

**Attributes**:
- `id`: Sequential integer starting from 1, auto-assigned by TaskManager
- `title`: Required string, max 200 characters (validated on input)
- `description`: Optional string (empty string allowed), max 1000 characters
- `is_complete`: Boolean, defaults to False on creation

**Validation Rules**:
- Title cannot be empty (FR-014)
- Title max length: 200 characters (assumption from spec)
- Description max length: 1000 characters (assumption from spec)
- ID uniqueness enforced by TaskManager (sequential allocation)

**Storage Approach**:
- TaskManager maintains: `Dict[int, Task]` for O(1) lookup by ID
- TaskManager tracks: `next_id: int` counter starting at 1
- No persistence: Dict cleared on application restart (FR-003)

### 1.2 Service Interface Design

**Output**: `contracts/task_manager_interface.md`

**TaskManager Public Methods**:

```python
def add_task(title: str, description: str = "") -> Task:
    """Add new task with title and optional description.

    Returns: Created Task with assigned ID
    Raises: ValueError if title empty or exceeds length limits
    """

def get_all_tasks() -> List[Task]:
    """Get all tasks in creation order (sorted by ID).

    Returns: List of Task objects (empty list if no tasks)
    """

def get_task(task_id: int) -> Optional[Task]:
    """Get single task by ID.

    Returns: Task if found, None otherwise
    """

def update_task(task_id: int, title: Optional[str] = None,
                description: Optional[str] = None) -> Task:
    """Update task title and/or description.

    Args:
        task_id: ID of task to update
        title: New title (if provided)
        description: New description (if provided)

    Returns: Updated Task
    Raises: ValueError if task_id not found or validation fails
    """

def delete_task(task_id: int) -> bool:
    """Delete task by ID.

    Returns: True if deleted, False if task_id not found
    """

def mark_complete(task_id: int, is_complete: bool) -> Task:
    """Mark task as complete or incomplete.

    Args:
        task_id: ID of task to update
        is_complete: True for complete, False for incomplete

    Returns: Updated Task
    Raises: ValueError if task_id not found
    """
```

**Error Handling Strategy**:
- Invalid task ID: Raise ValueError with message "Task not found: {task_id}"
- Empty title: Raise ValueError with message "Title cannot be empty"
- Length violations: Raise ValueError with message "Title/Description exceeds maximum length"

### 1.3 CLI Interface Design

**Output**: `contracts/cli_interface.md`

**Menu Options**:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

**Interaction Flows**:

**Add Task Flow**:
```
Enter title: [user input]
Enter description (optional): [user input]
→ Task created successfully! ID: 1
```

**View Tasks Flow**:
```
=== Task List ===
[1] ☐ Buy groceries
    Description: Milk, eggs, bread
[2] ☑ Complete project
    Description: Finish implementation
=== End of List ===
```

**Update Task Flow**:
```
Enter task ID: [user input]
Enter new title (leave empty to keep current): [user input]
Enter new description (leave empty to keep current): [user input]
→ Task updated successfully!
```

**Display Format**:
- Incomplete tasks: `[ID] ☐ Title`
- Complete tasks: `[ID] ☑ Title`
- Description indented below title
- Empty list message: "No tasks found. Add a task to get started!"

**Input Validation**:
- Numeric ID validation: Reject non-numeric input with "Invalid ID format"
- Task not found: Display "Task ID {id} not found"
- Empty title on add: Display "Title cannot be empty"

### 1.4 Quickstart Guide

**Output**: `quickstart.md`

**Content**:
- Prerequisites (Python 3.13+, uv)
- Installation steps (uv sync)
- Running the application (uv run python src/cli/app.py)
- Running tests (uv run pytest)
- Example usage walkthrough (add task → view → mark complete → delete)
- Troubleshooting common issues

---

## Phase 2: Task Breakdown

**Purpose**: Generate detailed, testable tasks organized by user story priority.

**Output**: `tasks.md` (generated by `/sp.tasks` command)

**Expected Task Organization**:
- Phase 1: Project setup (uv init, directory structure, pytest config)
- Phase 2: Foundational (Task model, basic TaskManager structure)
- Phase 3: User Story 1 - Add and View Tasks (P1 MVP)
- Phase 4: User Story 2 - Mark Complete/Incomplete (P2)
- Phase 5: User Story 3 - Update Task Details (P3)
- Phase 6: User Story 4 - Delete Tasks (P4)
- Phase 7: Polish (error handling, input validation, display formatting)

**TDD Task Pattern** (per user story):
1. Write contract tests (verify interface behavior)
2. Write integration tests (verify user scenario end-to-end)
3. **Verify tests FAIL** (Red phase)
4. Implement minimum code to pass tests (Green phase)
5. Refactor while keeping tests green (Refactor phase)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. **Setup**: Create project structure with uv, configure pytest
2. **Foundational**: Implement Task dataclass and TaskManager skeleton
3. **P1 Implementation**:
   - Write tests for add_task() and get_all_tasks()
   - Implement TaskManager.add_task() and get_all_tasks()
   - Write tests for CLI add/view commands
   - Implement CLI add/view functionality
   - **STOP and VALIDATE**: Run full workflow manually
4. **Demo**: User can add tasks and view list

### Incremental Delivery (By Priority)

1. **Foundation** → Task model + TaskManager structure complete
2. **P1: Add/View** → Test independently → Basic MVP functional
3. **P2: Mark Complete** → Test independently → Status management working
4. **P3: Update Details** → Test independently → Edit capabilities added
5. **P4: Delete** → Test independently → Full CRUD complete
6. **Polish** → Input validation, error messages, display formatting

Each priority level delivers independently testable value.

### TDD Workflow Example (User Story 1)

**Red Phase**:
```python
# tests/unit/test_task_manager.py
def test_add_task_creates_task_with_id_1():
    manager = TaskManager()
    task = manager.add_task("Buy groceries", "Milk, eggs")
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.is_complete is False
```

Run: `uv run pytest` → **FAIL** (add_task not implemented)

**Green Phase**:
```python
# src/services/task_manager.py
def add_task(self, title: str, description: str = "") -> Task:
    task = Task(id=self.next_id, title=title,
                description=description, is_complete=False)
    self.tasks[self.next_id] = task
    self.next_id += 1
    return task
```

Run: `uv run pytest` → **PASS**

**Refactor Phase**:
- Extract validation logic if needed
- Improve naming if clarity can be enhanced
- Keep tests passing throughout

---

## Risk Analysis

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Console input parsing errors | Medium | Comprehensive input validation with clear error messages (FR-011) |
| Large task lists display poorly | Low | Tested with 100 tasks per SC-002; pagination not needed for in-memory scope |
| ID collision on edge cases | Low | Sequential ID allocation prevents collisions; validated in tests |
| Type hint complexity for Python 3.13 | Low | Research phase validates type hint patterns; standard library sufficient |

### Process Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Skipping TDD discipline | High | Constitution requires TDD (Principle III); enforce in code reviews |
| Over-engineering storage | Medium | Constitution Simplicity First prevents; use plain dict/list only |
| Mixing concerns (UI in services) | Medium | Code review checklist includes Separation of Concerns validation |

### Acceptance Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Console UX unclear | Medium | Quickstart guide with examples; manual testing per user story |
| Error messages insufficient | Low | FR-011 requires clear messages; integration tests validate |

---

## Success Validation

### Definition of Done (Per User Story)

- [ ] All acceptance scenarios from spec.md have passing integration tests
- [ ] Unit tests cover TaskManager and Task model behavior
- [ ] PEP 8 compliance verified (can use `ruff check`)
- [ ] Type hints present on all functions
- [ ] Manual testing confirms console UX is clear
- [ ] Code review confirms Separation of Concerns maintained

### Overall Feature Completion

- [ ] All 4 user stories (P1-P4) implemented and tested
- [ ] All 15 functional requirements (FR-001 to FR-015) satisfied
- [ ] All 10 success criteria (SC-001 to SC-010) validated
- [ ] Constitution compliance verified (no violations)
- [ ] Quickstart guide tested by running through steps
- [ ] Application runs with `uv run python src/cli/app.py`

---

## Next Steps

1. **Run `/sp.tasks`** to generate detailed task breakdown from this plan
2. **Execute Phase 0**: Create research.md documenting Python patterns
3. **Execute Phase 1**: Create data-model.md, contracts/, and quickstart.md
4. **Begin Implementation**: Start with User Story 1 (P1) using TDD workflow
5. **Validate MVP**: Manually test add/view functionality before proceeding to P2

---

## Notes

- All implementation must follow Red-Green-Refactor TDD cycle per Constitution Principle III
- No external dependencies allowed except pytest (dev-only)
- Keep functions small and focused (Clean Code principle)
- Validate Constitution Check passes before each user story implementation
- Defer polish/edge cases to final phase (Simplicity First - solve core problem first)
