# Data Model: Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Purpose**: Define Task entity structure and storage patterns

---

## Task Entity

### Definition

The **Task** represents a single todo item with unique identifier, descriptive content, and completion status.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-assigned | Unique, sequential starting from 1 | Unique identifier for the task |
| `title` | `str` | Yes | None | Non-empty, max 200 chars | Short summary of the task |
| `description` | `str` | No | `""` (empty string) | Max 1000 chars | Detailed information about the task |
| `is_complete` | `bool` | Yes | `False` | N/A | Completion status (True = complete, False = incomplete) |

### Python Implementation

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential identifier
        title: Task summary (required, max 200 chars)
        description: Detailed task information (optional, max 1000 chars)
        is_complete: Completion status (False = incomplete, True = complete)
    """
    id: int
    title: str
    description: str = ""
    is_complete: bool = False
```

### Validation Rules

**On Creation**:
- `title` MUST NOT be empty (enforced by TaskManager, not Task itself)
- `title` MUST NOT exceed 200 characters
- `description` MAY be empty string (user can add title-only tasks)
- `description` MUST NOT exceed 1000 characters
- `is_complete` defaults to `False` (all new tasks start incomplete)

**On Update**:
- Same title/description constraints apply
- `id` is immutable (cannot be changed after creation)
- `is_complete` can toggle between True/False freely

### Invariants

1. **ID Uniqueness**: No two tasks can have the same ID (enforced by TaskManager)
2. **ID Immutability**: Task ID never changes after creation
3. **Sequential IDs**: IDs are assigned sequentially (1, 2, 3, ...) in creation order
4. **Non-null Title**: Title is always a string (may be empty only if validation bypassed, which shouldn't happen)
5. **Non-null Description**: Description is always a string (empty string is valid)
6. **Boolean Status**: `is_complete` is always exactly `True` or `False`

---

## Storage Model

### In-Memory Storage Structure

The TaskManager maintains task data using Python built-in collections:

```python
class TaskManager:
    """Manages in-memory task storage and operations."""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}  # ID -> Task mapping for O(1) lookup
        self.next_id: int = 1              # Counter for sequential ID assignment
```

### Storage Characteristics

**Data Structure**: `Dict[int, Task]`
- **Key**: Task ID (integer)
- **Value**: Task object
- **Rationale**: O(1) lookup by ID for get/update/delete operations

**ID Generation**: Sequential counter
- Starts at 1 (INITIAL_TASK_ID constant)
- Increments by 1 after each task creation
- Never decrements (deleted task IDs are not reused)

**Ordering**: Creation order
- `get_all_tasks()` returns tasks sorted by ID
- ID sequence reflects creation order (earlier tasks have lower IDs)

### Lifecycle

```
[Task Created] → assigned next_id → stored in dict → next_id incremented
       ↓
[Task Updated] → retrieved by ID → modified in place → same dict reference
       ↓
[Task Deleted] → removed from dict → ID not reused
       ↓
[App Terminates] → all data lost (in-memory only per FR-003)
```

---

## Example States

### Initial State (Empty Application)

```python
tasks = {}
next_id = 1
```

### After Adding First Task

```python
# User adds: title="Buy groceries", description="Milk, eggs, bread"

tasks = {
    1: Task(id=1, title="Buy groceries", description="Milk, eggs, bread", is_complete=False)
}
next_id = 2
```

### After Adding Second Task and Marking First Complete

```python
# User adds: title="Write report", description=""
# User marks task 1 as complete

tasks = {
    1: Task(id=1, title="Buy groceries", description="Milk, eggs, bread", is_complete=True),
    2: Task(id=2, title="Write report", description="", is_complete=False)
}
next_id = 3
```

### After Updating Task 2

```python
# User updates task 2: description="Q4 performance report"

tasks = {
    1: Task(id=1, title="Buy groceries", description="Milk, eggs, bread", is_complete=True),
    2: Task(id=2, title="Write report", description="Q4 performance report", is_complete=False)
}
next_id = 3  # Unchanged (no new task created)
```

### After Deleting Task 1

```python
# User deletes task 1

tasks = {
    2: Task(id=2, title="Write report", description="Q4 performance report", is_complete=False)
}
next_id = 3  # Still 3 (ID 1 not reused)
```

### After App Restart

```python
# Application terminates and restarts

tasks = {}
next_id = 1  # Resets to initial state
```

---

## Constraints Summary

| Constraint | Enforcement Point | Validation Method |
|------------|-------------------|-------------------|
| Title non-empty | TaskManager.add_task() | Raise ValueError if empty/whitespace-only |
| Title max length (200 chars) | TaskManager.add_task(), update_task() | Raise ValueError if len(title) > 200 |
| Description max length (1000 chars) | TaskManager.add_task(), update_task() | Raise ValueError if len(description) > 1000 |
| ID uniqueness | TaskManager (sequential assignment) | Automatic (counter-based, no duplicates possible) |
| ID immutability | Task dataclass (no setter), TaskManager | No update_task() parameter for ID |
| is_complete is boolean | Task dataclass type hint, mark_complete() | Type system + explicit parameter validation |

---

## Data Model Decisions

### Why Dict Over List?

**Dict[int, Task] chosen over List[Task]**:
- ✅ O(1) lookup by ID (get, update, delete operations)
- ✅ Natural mapping of ID to Task
- ✅ Deletion doesn't require shifting elements

**Tradeoff**: Slightly more memory overhead than list, but negligible for 100-task scale (SC-002)

### Why Sequential IDs Over UUIDs?

**Sequential integers chosen over UUIDs**:
- ✅ Simpler for console interaction (user types "1" not "550e8400-e29b-41d4-a716-446655440000")
- ✅ Predictable and easy to remember
- ✅ Aligns with in-memory, single-session context (no distributed ID collision risk)
- ✅ Satisfies Simplicity First principle (Constitution I)

**Tradeoff**: IDs reset on each app run, but this is expected behavior per FR-003

### Why Dataclass Over Regular Class?

**@dataclass chosen over manual `__init__`**:
- ✅ Auto-generates `__init__`, `__repr__`, `__eq__` boilerplate
- ✅ Type hints integrated natively
- ✅ Default values cleanly expressed
- ✅ Pythonic and follows Constitution V (Python Best Practices)

**Tradeoff**: None for this use case; dataclass fits requirements perfectly

---

## Mapping to Spec Requirements

| Spec Requirement | Data Model Support |
|------------------|-------------------|
| FR-001: Add task with title and description | Task has `title` (required) and `description` (optional) attributes |
| FR-002: Unique identifier | Task has `id` attribute, assigned sequentially by TaskManager |
| FR-003: In-memory storage only | Dict[int, Task] exists only in process memory, no persistence |
| FR-004: Display ID, title, description, status | All four attributes present in Task model |
| FR-005/FR-006: Update title/description | Task attributes are mutable (dataclass default) |
| FR-008/FR-009: Mark complete/incomplete | `is_complete` boolean attribute supports both states |
| FR-010: New tasks start incomplete | `is_complete=False` is default value |
| FR-013: Distinguish complete/incomplete | `is_complete` boolean enables clear differentiation |
| FR-014: Title required | Validation in TaskManager (not Task dataclass itself) |

---

**Status**: Data model design complete, ready for implementation in `src/models/task.py`.
