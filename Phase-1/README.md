# Todo In-Memory Python Console App

A simple console-based todo application built with Python 3.13+ that stores all data in memory.

## Features

- Add tasks with title and description
- View all tasks with status indicators
- Mark tasks as complete or incomplete
- Update task details (title/description)
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

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

All data is stored in memory only. When you exit the application, all tasks are lost.

## Development

This project follows Test-Driven Development (TDD) principles:
- Tests are written first (Red-Green-Refactor cycle)
- All tests pass before implementation is considered complete
- Code is refactored while keeping tests green

### Code Quality Standards

- **Type Safety**: Full type hints with mypy strict mode
- **Code Style**: PEP 8 compliant, enforced with ruff
- **Test Coverage**: 36 tests covering unit and integration scenarios
- **Documentation**: Comprehensive docstrings for all public APIs

### Performance Characteristics

- Startup time: < 1ms
- Add 100 tasks: ~0.3ms
- Display 100 tasks: ~3ms
- All operations complete in under 1 second

## License

MIT
