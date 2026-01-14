# Quickstart Guide: Todo Console App

**Feature**: 001-todo-console-app
**Last Updated**: 2026-01-02

Welcome to the Todo In-Memory Python Console App! This guide will help you get started quickly.

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.13 or later** installed
  - Check version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

- **uv package manager** installed
  - Check if installed: `uv --version`
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Or via pip: `pip install uv`

---

## Installation

### 1. Clone/Navigate to Project Directory

```bash
cd /path/to/Todo-app
```

### 2. Install Dependencies

```bash
# Install project dependencies (pytest for testing)
uv sync
```

This command:
- Creates a virtual environment (if not already present)
- Installs pytest for testing
- Prepares the project for development

---

## Running the Application

### Start the Todo App

```bash
uv run python src/cli/app.py
```

You should see the main menu:

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

---

## Example Usage Walkthrough

### Step 1: Add Your First Task

1. Select option **1** (Add Task)
2. Enter title: `Buy groceries`
3. Enter description: `Milk, eggs, bread`
4. See confirmation: `✓ Task created successfully! ID: 1`

### Step 2: View Your Tasks

1. Select option **2** (View All Tasks)
2. See your task list:

```
=== Task List ===
[1] ☐ Buy groceries
    Description: Milk, eggs, bread
=== End of List ===
```

**Status Indicators**:
- `☐` = Incomplete task
- `☑` = Complete task

### Step 3: Mark Task as Complete

1. Select option **5** (Mark Task Complete)
2. Enter task ID: `1`
3. See confirmation: `✓ Task marked as complete!`
4. View tasks again (option 2) to see:

```
=== Task List ===
[1] ☑ Buy groceries
    Description: Milk, eggs, bread
=== End of List ===
```

### Step 4: Add Another Task

1. Select option **1** (Add Task)
2. Enter title: `Write report`
3. Enter description: *(leave empty and press Enter)*
4. See confirmation: `✓ Task created successfully! ID: 2`

### Step 5: Update a Task

1. Select option **3** (Update Task)
2. Enter task ID: `2`
3. Enter new title: *(leave empty to keep current)*
4. Enter new description: `Q4 performance summary`
5. See confirmation: `✓ Task updated successfully!`

### Step 6: Delete a Task

1. Select option **4** (Delete Task)
2. Enter task ID: `1`
3. See confirmation: `✓ Task deleted successfully!`
4. View tasks (option 2) to confirm:

```
=== Task List ===
[2] ☐ Write report
    Description: Q4 performance summary
=== End of List ===
```

### Step 7: Exit the Application

1. Select option **7** (Exit)
2. See message: `Goodbye!`
3. Application terminates

**Important**: All tasks are stored in memory only. When you exit, all data is lost.

---

## Running Tests

### Run All Tests

```bash
uv run pytest
```

Expected output:
```
===== test session starts =====
collected 20 items

tests/unit/test_task_model.py ....
tests/unit/test_task_manager.py ............
tests/integration/test_workflows.py ....

===== 20 passed in 0.50s =====
```

### Run Specific Test File

```bash
# Unit tests for TaskManager
uv run pytest tests/unit/test_task_manager.py

# Integration tests
uv run pytest tests/integration/test_workflows.py
```

### Run Tests with Verbose Output

```bash
uv run pytest -v
```

### Run Tests with Coverage (Optional)

```bash
# Install coverage tool
uv add --dev pytest-cov

# Run tests with coverage report
uv run pytest --cov=src --cov-report=term-missing
```

---

## Common Operations

### Add a Task (Title Only)

```
Enter title: Quick task
Enter description: (just press Enter)
```

Result: Task created with empty description

### Add a Task (Title + Description)

```
Enter title: Detailed task
Enter description: This task has more context and details
```

Result: Task created with both title and description

### Update Only Title

```
Enter task ID: 2
Enter new title: Updated title
Enter new description: (press Enter to skip)
```

Result: Title updated, description unchanged

### Update Only Description

```
Enter task ID: 2
Enter new title: (press Enter to skip)
Enter new description: New description text
```

Result: Description updated, title unchanged

### Handle Empty Task List

If you view tasks when none exist:
```
=== Task List ===
No tasks found. Add a task to get started!
=== End of List ===
```

---

## Troubleshooting

### Issue: "Command not found: uv"

**Solution**: Install uv package manager
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:
```bash
pip install uv
```

### Issue: "Python version too old"

**Solution**: Upgrade to Python 3.13+
- Check current version: `python --version`
- Download latest from: https://www.python.org/downloads/

### Issue: "Invalid input" when entering task ID

**Cause**: You entered text instead of a number

**Solution**: Enter only numeric task IDs (e.g., `1`, `2`, `3`)

### Issue: "Task not found: X"

**Cause**: Task with that ID doesn't exist or was deleted

**Solution**:
1. View all tasks (option 2) to see valid IDs
2. Use an ID from the displayed list

### Issue: "Title cannot be empty"

**Cause**: You pressed Enter without typing a title when adding a task

**Solution**: Enter at least one character for the title (titles are required)

### Issue: Tests fail with import errors

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Ensure dependencies are installed
uv sync

# Run tests with uv (automatically uses correct environment)
uv run pytest
```

---

## Data Persistence Notice

**IMPORTANT**: This application stores all data in memory only.

When you:
- Exit the application (option 7)
- Close the terminal
- Restart your computer

**All tasks are permanently lost**.

This is intentional Phase I behavior. Future versions may add file or database persistence.

---

## Keyboard Shortcuts

- **Ctrl+C**: Force quit (not recommended; use Exit option instead)
- **Ctrl+D**: EOF signal (may exit input prompts)

---

## Next Steps

After familiarizing yourself with the application:

1. **Explore edge cases**:
   - Try adding a task with a very long title
   - Attempt to delete a non-existent task ID
   - Mark an already-complete task as complete again

2. **Review the code**:
   - `src/models/task.py` - Task data structure
   - `src/services/task_manager.py` - Business logic
   - `src/cli/app.py` - Main application entry point

3. **Run tests**:
   - See how tests validate behavior
   - Understand TDD workflow (Red-Green-Refactor)

4. **Contribute**:
   - Add new features (tags, priorities, due dates)
   - Improve error messages
   - Enhance display formatting

---

## Support

For issues or questions:
- Check the specification: `specs/001-todo-console-app/spec.md`
- Review the implementation plan: `specs/001-todo-console-app/plan.md`
- Examine test cases: `tests/unit/` and `tests/integration/`

---

**Happy task managing!** 🎯
