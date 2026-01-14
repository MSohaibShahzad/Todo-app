# Todo In-Memory Python Console App - Phase 1

A feature-rich console-based todo application built with Python 3.13+ that stores all data in memory.

## Features

### Phase-1 Advanced Features (Intermediate & Advanced)

#### Task Organization
- **Priority Levels**: Assign low/medium/high priority with color-coded display (Red/Yellow/Blue)
- **Categories**: Organize tasks into custom categories (Work, Personal, Shopping, etc.)
- **Due Dates**: Set due dates with smart reminders and visual indicators
- **Recurring Tasks**: Create daily/weekly/monthly recurring tasks that auto-regenerate

#### Search & Filter
- **Keyword Search**: Find tasks by title or description (case-insensitive)
- **Multi-Criteria Filtering**: Filter by status, priority, and category simultaneously (AND logic)
- **Advanced Sorting**: Sort by ID, priority, title, or due date

#### Smart Notifications
- **Startup Reminders**: Automatic alerts for overdue, due today, and tomorrow's tasks
- **Visual Indicators**: Color-coded OVERDUE (red/bold) and DUE TODAY (yellow/bold) badges
- **Due Date Display**: Clear date formatting for upcoming tasks

### Phase-1 Basic Features (CRUD Operations)

- Add tasks with title and description
- View all tasks with status indicators
- Mark tasks as complete or incomplete
- Update task details (title/description/priority/category/due date/recurrence)
- Delete tasks by ID

## Prerequisites

- Python 3.13 or later
- uv package manager

## Installation

```bash
# Install dependencies
uv sync

# Run the application
uv run python -m src.cli.app
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/test_task_manager.py

# Run manual workflow tests
uv run python test_manual.py

# Run performance tests
uv run python test_performance.py

# Type checking
uv run mypy src/ --strict

# Code quality check
uv run ruff check src/ tests/
```

## Project Structure

```
src/
├── models/          # Task data structures
├── services/        # Business logic (task management)
└── cli/             # Console interface and user interaction

tests/
├── unit/            # Unit tests for services and models
└── integration/     # Integration tests for full workflows
```

## Usage

The application provides a menu-based interface with the following options:

1. **Add Task** - Create tasks with priority, category, due date, and recurrence
2. **View All Tasks** - See all tasks with color-coded priorities and due date indicators
3. **Update Task** - Modify any task details
4. **Delete Task** - Remove tasks permanently
5. **Mark Task Complete** - Complete tasks (recurring tasks auto-regenerate with next due date!)
6. **Mark Task Incomplete** - Revert task to incomplete status
7. **Search Tasks** - Find tasks by keyword in title or description
8. **Filter Tasks** - Filter by status, priority, and/or category
9. **Exit** - Close the application

All data is stored in memory only. When you exit the application, all tasks are lost.

## Development

This project follows Test-Driven Development (TDD) principles:
- Tests are written first (Red-Green-Refactor cycle)
- All tests pass before implementation is considered complete
- Code is refactored while keeping tests green

### Code Quality Standards

- **Type Safety**: Full type hints with mypy strict mode
- **Code Style**: PEP 8 compliant, enforced with ruff
- **Test Coverage**: 100 unit tests with 99% coverage on service/model layers
- **Documentation**: Comprehensive docstrings for all public APIs
- **TDD Approach**: All features implemented using Red-Green-Refactor cycle

### Performance Characteristics

- Startup time: < 1ms
- Add 100 tasks: ~0.3ms
- Display 100 tasks: ~3ms
- All operations complete in under 1 second

## License

MIT
