# Research: Python Best Practices for Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Purpose**: Document Python 3.13+ patterns, TDD workflows, and console I/O best practices for implementation

---

## 1. Python 3.13+ Dataclass Usage

### Recommended Pattern: `@dataclass` with type hints

```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str = ""  # Default value for optional field
    is_complete: bool = False
```

**Benefits**:
- Auto-generates `__init__`, `__repr__`, `__eq__` methods
- Type hints provide IDE support and static analysis
- Default values handle optional fields cleanly
- Immutable variant available with `frozen=True` if needed

**Why Not NamedTuple**:
- NamedTuple is immutable, making updates cumbersome
- Task needs mutability for status changes (mark_complete)
- Dataclass provides better balance of convenience and flexibility

**Type Hints for Collections**:
```python
from typing import Dict, List, Optional

tasks: Dict[int, Task] = {}  # ID to Task mapping
all_tasks: List[Task] = []   # Ordered list
task: Optional[Task] = None  # May be None
```

---

## 2. Pytest Fixtures and Test Organization

### Fixture Pattern for Test Isolation

```python
import pytest
from src.services.task_manager import TaskManager

@pytest.fixture
def empty_manager():
    """Provide fresh TaskManager for each test."""
    return TaskManager()

@pytest.fixture
def manager_with_tasks():
    """Provide TaskManager pre-populated with sample tasks."""
    manager = TaskManager()
    manager.add_task("Task 1", "Description 1")
    manager.add_task("Task 2", "Description 2")
    return manager

def test_add_task(empty_manager):
    task = empty_manager.add_task("Test", "Desc")
    assert task.id == 1
    assert task.title == "Test"
```

**Benefits**:
- Each test gets fresh instance (no test pollution)
- Pre-populated fixtures reduce test setup duplication
- Clear test intent (fixture name describes state)

### Parameterized Testing for Edge Cases

```python
@pytest.mark.parametrize("title,description,expected_error", [
    ("", "Valid desc", "Title cannot be empty"),
    ("A" * 201, "Valid desc", "Title exceeds maximum length"),
    ("Valid", "B" * 1001, "Description exceeds maximum length"),
])
def test_add_task_validation(empty_manager, title, description, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        empty_manager.add_task(title, description)
```

**Benefits**:
- Tests multiple edge cases with single test function
- Easy to add new cases without duplicating test code
- Clear tabular view of test scenarios

---

## 3. Console I/O Best Practices

### Input Validation Pattern

```python
def get_integer_input(prompt: str) -> int:
    """Get validated integer input from user.

    Keeps prompting until valid integer provided.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_string_input(prompt: str, allow_empty: bool = False,
                     max_length: Optional[int] = None) -> str:
    """Get validated string input from user."""
    while True:
        value = input(prompt).strip()

        if not allow_empty and not value:
            print("Input cannot be empty.")
            continue

        if max_length and len(value) > max_length:
            print(f"Input exceeds maximum length of {max_length}.")
            continue

        return value
```

**Benefits**:
- User-friendly error recovery (re-prompt instead of crash)
- Centralized validation logic
- Consistent UX across all input points

### Display Formatting Pattern

```python
def format_task_list(tasks: List[Task]) -> str:
    """Format task list for console display."""
    if not tasks:
        return "No tasks found. Add a task to get started!"

    lines = ["=== Task List ==="]
    for task in tasks:
        status = "☑" if task.is_complete else "☐"
        lines.append(f"[{task.id}] {status} {task.title}")
        if task.description:
            lines.append(f"    Description: {task.description}")
    lines.append("=== End of List ===")
    return "\n".join(lines)
```

**Benefits**:
- Separation of formatting from display logic
- Testable (returns string, doesn't print directly)
- Clear visual structure with status indicators

---

## 4. TDD Workflow in Python

### Red-Green-Refactor Cycle

**Red Phase**: Write failing test first

```python
# tests/unit/test_task_manager.py
def test_add_task_assigns_sequential_ids(empty_manager):
    task1 = empty_manager.add_task("First", "")
    task2 = empty_manager.add_task("Second", "")
    assert task1.id == 1
    assert task2.id == 2
```

Run: `uv run pytest tests/unit/test_task_manager.py::test_add_task_assigns_sequential_ids`
Result: **FAIL** (method not implemented)

**Green Phase**: Write minimal code to pass

```python
# src/services/task_manager.py
class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(id=self.next_id, title=title,
                    description=description, is_complete=False)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task
```

Run: `uv run pytest tests/unit/test_task_manager.py::test_add_task_assigns_sequential_ids`
Result: **PASS**

**Refactor Phase**: Improve code while keeping tests green

- Extract magic numbers to constants
- Improve naming if needed
- Add type hints if missing
- Re-run tests after each change to ensure still passing

### Integration Test Pattern

```python
# tests/integration/test_workflows.py
def test_full_task_workflow():
    """Test complete user story: add → view → mark complete → delete."""
    manager = TaskManager()

    # Add task
    task = manager.add_task("Buy groceries", "Milk, eggs, bread")
    assert task.id == 1
    assert not task.is_complete

    # View tasks
    tasks = manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy groceries"

    # Mark complete
    updated = manager.mark_complete(task.id, True)
    assert updated.is_complete is True

    # Delete task
    result = manager.delete_task(task.id)
    assert result is True
    assert len(manager.get_all_tasks()) == 0
```

**Benefits**:
- Validates end-to-end user scenarios
- Catches integration issues between components
- Maps directly to acceptance criteria from spec.md

---

## 5. Error Handling Strategy

### Exception-Based Error Propagation

```python
class TaskManager:
    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> Task:
        """Update task, raising ValueError for invalid inputs."""
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")

        if title is not None and not title.strip():
            raise ValueError("Title cannot be empty")

        if title and len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title exceeds maximum length of {MAX_TITLE_LENGTH}")

        # Update task...
```

**CLI Error Handling**:

```python
def update_task_command(manager: TaskManager):
    """Handle update task user command with error recovery."""
    try:
        task_id = get_integer_input("Enter task ID: ")
        title = get_string_input("New title (empty to skip): ", allow_empty=True)
        description = get_string_input("New description (empty to skip): ", allow_empty=True)

        updated = manager.update_task(
            task_id,
            title if title else None,
            description if description else None
        )
        print(f"✓ Task updated successfully!")

    except ValueError as e:
        print(f"✗ Error: {e}")
```

**Benefits**:
- Clear separation: Services raise exceptions, CLI catches and displays
- User-friendly error messages per FR-011
- No silent failures

---

## 6. Project Setup with `uv`

### Creating Project

```bash
# Initialize uv project
uv init todo-app
cd todo-app

# Add pytest as dev dependency
uv add --dev pytest

# Create directory structure
mkdir -p src/models src/services src/cli
mkdir -p tests/unit tests/integration

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/cli/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

### `pyproject.toml` Configuration

```toml
[project]
name = "todo-app"
version = "0.1.0"
description = "In-memory Todo console application"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### Running Commands

```bash
# Run tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_task_manager.py

# Run with verbose output
uv run pytest -v

# Run application
uv run python src/cli/app.py
```

---

## 7. Recommended Constants

```python
# src/models/task.py or src/services/task_manager.py
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
DEFAULT_DESCRIPTION = ""
INITIAL_TASK_ID = 1
```

**Benefits**:
- No magic numbers in code
- Easy to adjust limits if requirements change
- Self-documenting

---

## Key Takeaways for Implementation

1. **Use `@dataclass`** for Task model with type hints and default values
2. **Pytest fixtures** provide test isolation; parameterized tests cover edge cases efficiently
3. **Separate input validation** into reusable functions; keep validation out of business logic
4. **TDD discipline**: Write test → verify FAIL → implement → verify PASS → refactor
5. **Exception-based errors**: Services raise ValueError, CLI catches and displays user-friendly messages
6. **uv for project management**: Simple setup, clear dependency management, easy test execution
7. **Constants over magic numbers**: Define MAX_TITLE_LENGTH, etc., in one place

---

## Answers to Key Questions

| Question | Answer |
|----------|--------|
| How to structure pytest fixtures for TaskManager test isolation? | Use `@pytest.fixture` with function scope (default); create `empty_manager` and `manager_with_tasks` fixtures |
| What's the best pattern for console menu systems in Python? | While-loop with match/case (Python 3.10+) or if/elif chain; separate menu display from command execution |
| How to handle user input validation cleanly? | Create `get_integer_input()` and `get_string_input()` helper functions with re-prompt loops |
| Dataclass vs NamedTuple for Task entity? | Dataclass (mutable, better for updates); NamedTuple is immutable and awkward for status changes |
| Type hints for optional description field? | Use default value `description: str = ""` in dataclass; method params use `Optional[str]` |

---

**Status**: Research complete, ready for Phase 1 design and implementation.
