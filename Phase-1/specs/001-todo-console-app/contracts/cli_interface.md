# CLI Interface Contract

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Component**: CLI layer (user interaction)
**Purpose**: Define console interaction patterns and display formatting

---

## Overview

The CLI layer provides the user-facing console interface for the Todo application. It handles:
- Menu display and option selection
- User input collection and validation
- Output formatting and display
- Error message presentation

The CLI interacts with TaskManager exclusively through its public interface and contains NO business logic.

---

## Menu System

### Main Menu Display

```
=== Todo Application ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter choice (1-7):
```

**Behavior**:
- Menu displayed after every completed action
- User selects option by entering number 1-7
- Invalid input (non-numeric, out of range) re-prompts with error message
- Exit option (7) terminates application cleanly

---

## Input Patterns

### Integer Input Validation

**Function**: `get_integer_input(prompt: str) -> int`

```python
def get_integer_input(prompt: str) -> int:
    """Get validated integer input from user.

    Args:
        prompt: Message to display to user

    Returns:
        int: Validated integer value

    Behavior:
        - Displays prompt and waits for input
        - Attempts to convert input to integer
        - If conversion fails, displays "Invalid input. Please enter a number."
        - Re-prompts until valid integer provided
        - Never raises exception (loops until valid)
    """
```

**Example Interaction**:
```
Enter task ID: abc
Invalid input. Please enter a number.
Enter task ID: 1
(continues with ID 1)
```

### String Input Validation

**Function**: `get_string_input(prompt: str, allow_empty: bool = False, max_length: Optional[int] = None) -> str`

```python
def get_string_input(prompt: str, allow_empty: bool = False,
                     max_length: Optional[int] = None) -> str:
    """Get validated string input from user.

    Args:
        prompt: Message to display to user
        allow_empty: Whether empty string is valid (default False)
        max_length: Maximum allowed length (None = no limit)

    Returns:
        str: Validated string (whitespace stripped)

    Behavior:
        - Displays prompt and waits for input
        - Strips leading/trailing whitespace
        - If empty and allow_empty=False, displays "Input cannot be empty."
        - If exceeds max_length, displays "Input exceeds maximum length of {max_length}."
        - Re-prompts until valid input provided
    """
```

**Example Interaction**:
```
Enter title:
Input cannot be empty.
Enter title: Buy groceries
(continues with "Buy groceries")
```

---

## Command Flows

### 1. Add Task

**Prompt Sequence**:
```
Enter title: [user input]
Enter description (optional, press Enter to skip): [user input]
```

**Success Output**:
```
✓ Task created successfully! ID: 1
```

**Error Outputs**:
```
✗ Error: Title cannot be empty
✗ Error: Title exceeds maximum length of 200 characters
✗ Error: Description exceeds maximum length of 1000 characters
```

**Implementation Notes**:
- Use `get_string_input("Enter title: ", allow_empty=False, max_length=200)`
- Use `get_string_input("Enter description (optional, press Enter to skip): ", allow_empty=True, max_length=1000)`
- Call `manager.add_task(title, description)`
- Catch `ValueError` and display as error output

---

### 2. View All Tasks

**No Input Required**

**Output (Tasks Exist)**:
```
=== Task List ===
[1] ☐ Buy groceries
    Description: Milk, eggs, bread
[2] ☑ Complete project
    Description: Finish implementation
[3] ☐ Write report
    Description:
=== End of List ===
```

**Output (No Tasks)**:
```
=== Task List ===
No tasks found. Add a task to get started!
=== End of List ===
```

**Display Format Rules**:
- Incomplete tasks: `[ID] ☐ Title`
- Complete tasks: `[ID] ☑ Title`
- Description line indented with 4 spaces
- If description is empty, still show "Description:" line but leave it blank
- Tasks ordered by ID (ascending)

**Implementation Notes**:
- Call `manager.get_all_tasks()`
- Use `format_task_list(tasks)` helper function to generate output string
- Print formatted string

---

### 3. Update Task

**Prompt Sequence**:
```
Enter task ID: [user input]
Enter new title (leave empty to keep current): [user input]
Enter new description (leave empty to keep current): [user input]
```

**Success Output**:
```
✓ Task updated successfully!
```

**Error Outputs**:
```
✗ Error: Task not found: 5
✗ Error: Title cannot be empty
✗ Error: Title exceeds maximum length of 200 characters
✗ Error: Description exceeds maximum length of 1000 characters
```

**Implementation Notes**:
- Use `get_integer_input("Enter task ID: ")`
- Use `get_string_input("Enter new title (leave empty to keep current): ", allow_empty=True, max_length=200)`
- Use `get_string_input("Enter new description (leave empty to keep current): ", allow_empty=True, max_length=1000)`
- If user input is empty string, pass `None` to `manager.update_task()` (no change)
- If user input is non-empty, pass the value to `manager.update_task()`
- Catch `ValueError` and display as error output

---

### 4. Delete Task

**Prompt Sequence**:
```
Enter task ID: [user input]
```

**Success Output**:
```
✓ Task deleted successfully!
```

**Error Output (Task Not Found)**:
```
✗ Error: Task not found: 5
```

**Implementation Notes**:
- Use `get_integer_input("Enter task ID: ")`
- Call `deleted = manager.delete_task(task_id)`
- If `deleted` is False, display error message
- If `deleted` is True, display success message

---

### 5. Mark Task Complete

**Prompt Sequence**:
```
Enter task ID: [user input]
```

**Success Output**:
```
✓ Task marked as complete!
```

**Error Output**:
```
✗ Error: Task not found: 5
```

**Implementation Notes**:
- Use `get_integer_input("Enter task ID: ")`
- Call `manager.mark_complete(task_id, True)`
- Catch `ValueError` and display as error output

---

### 6. Mark Task Incomplete

**Prompt Sequence**:
```
Enter task ID: [user input]
```

**Success Output**:
```
✓ Task marked as incomplete!
```

**Error Output**:
```
✗ Error: Task not found: 5
```

**Implementation Notes**:
- Use `get_integer_input("Enter task ID: ")`
- Call `manager.mark_complete(task_id, False)`
- Catch `ValueError` and display as error output

---

### 7. Exit

**Output**:
```
Goodbye!
```

**Behavior**:
- Displays exit message
- Terminates application (exits main loop)
- No data saved (in-memory only per FR-003)

---

## Display Formatting Helpers

### format_task_list()

```python
def format_task_list(tasks: List[Task]) -> str:
    """Format task list for console display.

    Args:
        tasks: List of Task objects to format

    Returns:
        str: Formatted string ready for printing

    Format:
        === Task List ===
        [1] ☐ Title
            Description: text
        [2] ☑ Title
            Description: text
        === End of List ===

        Or if empty:
        === Task List ===
        No tasks found. Add a task to get started!
        === End of List ===
    """
```

### format_status_indicator()

```python
def format_status_indicator(is_complete: bool) -> str:
    """Get status indicator symbol.

    Args:
        is_complete: Task completion status

    Returns:
        str: "☑" if complete, "☐" if incomplete
    """
```

---

## Error Handling

### User-Facing Error Messages

**All errors from TaskManager** (ValueError exceptions):
- Displayed with `✗ Error:` prefix
- Shown in red text if terminal supports ANSI color codes (optional enhancement)
- Never crash the application
- Return to main menu after error display

**Input Validation Errors** (invalid format):
- Displayed immediately after bad input
- Re-prompt for valid input
- No menu return (stay in input loop)

### Error Display Pattern

```python
try:
    # Call TaskManager method
    result = manager.some_method(args)
    print("✓ Success message")
except ValueError as e:
    print(f"✗ Error: {e}")
```

---

## Application Entry Point

### main() Function

```python
def main() -> None:
    """Main application entry point.

    Behavior:
        - Create TaskManager instance
        - Display welcome message
        - Enter main menu loop
        - Handle user commands
        - Exit cleanly on option 7
    """
```

**Application Flow**:
1. Initialize TaskManager
2. Display main menu
3. Get user choice (1-7)
4. Execute corresponding command function
5. Display result (success/error)
6. Repeat from step 2 (unless option 7 selected)
7. Display "Goodbye!" and exit

---

## File Structure

```
src/cli/
├── __init__.py
├── app.py           # main() function, application entry point
├── menu.py          # Menu display, option selection, command dispatching
└── display.py       # Output formatting (format_task_list, status indicators)
```

**Module Responsibilities**:

- `app.py`: Application lifecycle (create TaskManager, main loop, exit)
- `menu.py`: User interaction (get_integer_input, get_string_input, command functions)
- `display.py`: Output formatting (format_task_list, format_status_indicator)

---

## Testing Contract

### Manual Testing Checklist

✅ All menu options (1-7) accessible and functional
✅ Invalid menu choices re-prompt without crashing
✅ Empty title rejected on add task
✅ Empty description allowed on add task
✅ Task list displays correctly with multiple tasks
✅ Status indicators (☐ ☑) clearly distinguish complete/incomplete
✅ Update with only title changes title, keeps description
✅ Update with only description changes description, keeps title
✅ Delete removes task from list
✅ Mark complete/incomplete toggles status correctly
✅ Non-existent task IDs show clear error messages
✅ Exit option terminates cleanly

### Integration Testing

✅ Full workflow (add → view → update → mark complete → delete) completes without errors
✅ Error messages match TaskManager ValueError messages exactly
✅ Input validation prevents crashes on invalid input
✅ Application recovers gracefully from all error conditions

---

**Status**: CLI contract defined, ready for implementation in `src/cli/`.
