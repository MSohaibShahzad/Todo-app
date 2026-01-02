# TaskManager Interface Contract

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Component**: TaskManager service layer
**Purpose**: Define public API for task management business logic

---

## Overview

The **TaskManager** class provides all business logic for managing tasks. It maintains in-memory storage and enforces validation rules. The CLI layer interacts with TaskManager exclusively through this public interface.

---

## Class Definition

```python
from typing import Dict, List, Optional
from src.models.task import Task

class TaskManager:
    """Manages in-memory task storage and operations.

    Responsibilities:
    - Store tasks in memory (Dict[int, Task])
    - Assign unique sequential IDs to tasks
    - Validate task data (title/description length, non-empty title)
    - Provide CRUD operations (Create, Read, Update, Delete)
    - Manage task completion status

    Storage:
    - tasks: Dict[int, Task] - ID to Task mapping
    - next_id: int - Counter for sequential ID assignment (starts at 1)
    """

    def __init__(self) -> None:
        """Initialize empty TaskManager with no tasks."""
```

---

## Public Methods

### 1. add_task()

**Purpose**: Create a new task with title and optional description.

**Signature**:
```python
def add_task(self, title: str, description: str = "") -> Task:
    """Add a new task to the manager.

    Args:
        title: Task summary (required, max 200 characters)
        description: Detailed information (optional, max 1000 characters)

    Returns:
        Task: Newly created task with assigned ID and is_complete=False

    Raises:
        ValueError: If title is empty/whitespace-only
        ValueError: If title exceeds 200 characters
        ValueError: If description exceeds 1000 characters

    Behavior:
        - Strips whitespace from title/description before validation
        - Assigns next available ID (sequential, starting from 1)
        - Sets is_complete=False automatically
        - Increments next_id counter after creation
        - Stores task in internal tasks dict

    Example:
        >>> manager = TaskManager()
        >>> task = manager.add_task("Buy groceries", "Milk, eggs, bread")
        >>> task.id
        1
        >>> task.is_complete
        False
    """
```

**Acceptance Criteria** (from spec.md User Story 1):
- ✅ Task created with unique sequential ID
- ✅ Initial status is incomplete
- ✅ Title and description stored correctly
- ✅ Empty description allowed
- ❌ Empty title rejected with ValueError

---

### 2. get_all_tasks()

**Purpose**: Retrieve all tasks in creation order.

**Signature**:
```python
def get_all_tasks(self) -> List[Task]:
    """Get all tasks sorted by ID (creation order).

    Returns:
        List[Task]: All tasks in ascending ID order (empty list if no tasks)

    Behavior:
        - Returns list sorted by task.id
        - Returns empty list [] if no tasks exist
        - Returns copies/references (Task objects are mutable)
        - Order is consistent (always sorted by ID)

    Example:
        >>> manager = TaskManager()
        >>> manager.add_task("First", "")
        >>> manager.add_task("Second", "")
        >>> tasks = manager.get_all_tasks()
        >>> [t.id for t in tasks]
        [1, 2]
    """
```

**Acceptance Criteria** (from spec.md User Story 1):
- ✅ Returns all tasks with ID, title, description, status
- ✅ Returns empty list if no tasks exist
- ✅ Tasks ordered by creation (ID sequence)

---

### 3. get_task()

**Purpose**: Retrieve a single task by ID.

**Signature**:
```python
def get_task(self, task_id: int) -> Optional[Task]:
    """Get task by ID.

    Args:
        task_id: Unique task identifier

    Returns:
        Task if found, None if task_id doesn't exist

    Behavior:
        - O(1) lookup in internal tasks dict
        - Returns None (not exception) for missing IDs
        - Returns actual Task object (mutable reference)

    Example:
        >>> manager = TaskManager()
        >>> task = manager.add_task("Test", "")
        >>> found = manager.get_task(1)
        >>> found.title
        'Test'
        >>> manager.get_task(999)
        None
    """
```

**Acceptance Criteria**:
- ✅ Returns Task if ID exists
- ✅ Returns None if ID not found
- ✅ No exception raised for missing ID

---

### 4. update_task()

**Purpose**: Update task title and/or description.

**Signature**:
```python
def update_task(self, task_id: int, title: Optional[str] = None,
                description: Optional[str] = None) -> Task:
    """Update task title and/or description.

    Args:
        task_id: ID of task to update
        title: New title (None = no change)
        description: New description (None = no change)

    Returns:
        Task: Updated task object

    Raises:
        ValueError: If task_id not found
        ValueError: If new title is empty/whitespace-only
        ValueError: If new title exceeds 200 characters
        ValueError: If new description exceeds 1000 characters

    Behavior:
        - Strips whitespace from title/description before validation
        - If both title and description are None, returns task unchanged
        - Partial updates allowed (title only, description only, or both)
        - Validates all provided values (even if only one field updating)
        - Modifies task in place (same object reference)

    Example:
        >>> manager = TaskManager()
        >>> task = manager.add_task("Old Title", "Old Desc")
        >>> updated = manager.update_task(1, title="New Title")
        >>> updated.title
        'New Title'
        >>> updated.description  # Unchanged
        'Old Desc'
    """
```

**Acceptance Criteria** (from spec.md User Story 3):
- ✅ Title updated when provided
- ✅ Description updated when provided
- ✅ Partial updates supported (title-only or description-only)
- ❌ ValueError raised for non-existent task_id
- ❌ ValueError raised for empty title

---

### 5. delete_task()

**Purpose**: Remove task by ID.

**Signature**:
```python
def delete_task(self, task_id: int) -> bool:
    """Delete task by ID.

    Args:
        task_id: ID of task to delete

    Returns:
        bool: True if task was deleted, False if task_id not found

    Behavior:
        - Removes task from internal tasks dict
        - Does NOT reuse deleted IDs (next_id counter never decrements)
        - Idempotent: calling twice with same ID returns False on second call
        - No exception raised for missing ID (returns False instead)

    Example:
        >>> manager = TaskManager()
        >>> task = manager.add_task("Test", "")
        >>> manager.delete_task(1)
        True
        >>> manager.delete_task(1)  # Already deleted
        False
        >>> manager.get_task(1)
        None
    """
```

**Acceptance Criteria** (from spec.md User Story 4):
- ✅ Task removed from storage
- ✅ Task no longer appears in get_all_tasks()
- ✅ Returns True if deleted
- ✅ Returns False (not exception) if task_id not found
- ✅ Other tasks unaffected by deletion

---

### 6. mark_complete()

**Purpose**: Mark task as complete or incomplete.

**Signature**:
```python
def mark_complete(self, task_id: int, is_complete: bool) -> Task:
    """Mark task as complete or incomplete.

    Args:
        task_id: ID of task to update
        is_complete: True for complete, False for incomplete

    Returns:
        Task: Updated task object

    Raises:
        ValueError: If task_id not found

    Behavior:
        - Updates task.is_complete to provided value
        - Idempotent: setting same status twice is allowed (no error)
        - Modifies task in place (same object reference)

    Example:
        >>> manager = TaskManager()
        >>> task = manager.add_task("Test", "")
        >>> updated = manager.mark_complete(1, True)
        >>> updated.is_complete
        True
        >>> manager.mark_complete(1, False)  # Toggle back
        >>> task.is_complete
        False
    """
```

**Acceptance Criteria** (from spec.md User Story 2):
- ✅ Status changes to complete when is_complete=True
- ✅ Status changes to incomplete when is_complete=False
- ✅ Changes reflected in get_all_tasks() and get_task()
- ❌ ValueError raised for non-existent task_id
- ✅ Idempotent (can mark complete task as complete again)

---

## Constants

```python
# Maximum lengths for validation
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Initial ID value
INITIAL_TASK_ID = 1
```

---

## Error Messages

**Standardized error messages for ValueError exceptions**:

| Condition | Error Message |
|-----------|--------------|
| Empty title | `"Title cannot be empty"` |
| Title too long | `"Title exceeds maximum length of 200 characters"` |
| Description too long | `"Description exceeds maximum length of 1000 characters"` |
| Task not found | `"Task not found: {task_id}"` |

---

## Invariants

The TaskManager MUST maintain these invariants at all times:

1. **ID Uniqueness**: No two tasks in `tasks` dict have the same ID
2. **Sequential IDs**: IDs are assigned as 1, 2, 3, ... in order
3. **ID Immutability**: Task IDs never change after assignment
4. **No ID Reuse**: Deleted task IDs are never reassigned to new tasks
5. **Non-negative next_id**: `next_id` is always >= 1
6. **Valid Task State**: All tasks in storage have valid title/description lengths

---

## Thread Safety

**NOT THREAD-SAFE**: TaskManager is designed for single-threaded console application only. No locks or synchronization mechanisms are provided.

---

## Testing Contract

**Unit tests MUST verify**:

✅ All public methods with valid inputs return expected results
✅ All ValueError conditions raise exceptions with correct messages
✅ ID assignment is sequential starting from 1
✅ IDs are not reused after deletion
✅ Empty list returned when no tasks exist
✅ Partial updates work correctly (title-only, description-only)
✅ Status toggles work bidirectionally (incomplete → complete → incomplete)

**Integration tests MUST verify**:

✅ Full workflow: add → view → update → mark complete → delete
✅ Multiple tasks can coexist and be managed independently
✅ Error messages are user-friendly and accurate

---

**Status**: Contract defined, ready for TDD implementation in `src/services/task_manager.py`.
