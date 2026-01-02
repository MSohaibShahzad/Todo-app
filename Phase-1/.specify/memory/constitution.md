<!--
Sync Impact Report:
- Version change: [INITIAL] → 1.0.0 (Initial constitution establishment)
- New principles established: Simplicity First, Clean Code, Test-Driven Development, Separation of Concerns, Python Best Practices
- Templates requiring updates:
  ✅ Updated: plan-template.md (Constitution Check section aligns)
  ✅ Updated: spec-template.md (Requirements and Success Criteria align)
  ✅ Updated: tasks-template.md (Task categorization aligns with principles)
- Follow-up TODOs: None (all placeholders filled)
-->

# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Simplicity First

The codebase MUST remain simple and maintainable. Every design decision should favor the simplest viable solution that meets the requirement. YAGNI (You Aren't Gonna Need It) is strictly enforced.

**Rules**:
- No over-engineering or premature abstraction
- No external frameworks beyond the Python standard library
- No persistence layers (in-memory storage only)
- No authentication, authorization, or user management
- Console-based interaction only—no GUI, web interface, or REST API

**Rationale**: This is Phase I focusing on core Todo functionality. Complexity adds maintenance burden and learning curve without delivering user value.

### II. Clean Code

All code MUST follow clean code principles with clear, descriptive naming and simple, readable logic.

**Rules**:
- Functions and variables use clear, descriptive names (no abbreviations unless universally understood)
- Functions do one thing and do it well (Single Responsibility Principle)
- Logic is readable and self-documenting; comments only where necessary for complex algorithms
- Code follows PEP 8 style guidelines for Python
- No magic numbers; use named constants

**Rationale**: Readable code reduces bugs, accelerates onboarding, and enables confident refactoring.

### III. Test-Driven Development (TDD)

All features MUST be developed following the Red-Green-Refactor cycle. Tests are written FIRST, verified to FAIL, then implementation follows.

**Rules**:
- Write tests before implementation
- Verify tests fail (Red phase)
- Write minimal code to make tests pass (Green phase)
- Refactor while keeping tests green (Refactor phase)
- Use pytest as the testing framework
- Test coverage should focus on behavior, not implementation details

**Rationale**: TDD ensures correctness, reduces regressions, and produces testable, modular code from the start.

### IV. Separation of Concerns

The codebase MUST maintain clear separation between models (data), services (logic), and CLI (interaction).

**Rules**:
- Models: Define data structures (Task entity)
- Services: Implement business logic (add, update, delete, list, mark complete)
- CLI: Handle user interaction and display
- No business logic in CLI code
- No UI concerns in service code
- Models remain pure data structures with minimal behavior

**Rationale**: Separation of concerns enables independent testing, easier maintenance, and potential future migrations (e.g., adding a GUI layer).

### V. Python Best Practices

All code MUST follow Python 3.13+ best practices and idiomatic patterns.

**Rules**:
- Use type hints for function signatures and return types
- Use dataclasses or named tuples for structured data
- Prefer list comprehensions and generator expressions where appropriate
- Use context managers for resource handling (if needed)
- Follow Python's "Explicit is better than implicit" principle
- Use virtual environments (managed via `uv`)

**Rationale**: Modern Python features improve code clarity, catch errors earlier, and align with ecosystem standards.

## Functional Scope

### In Scope

- Adding tasks with title and description
- Viewing all tasks with clear status indicators
- Updating task title and description
- Deleting tasks by unique ID
- Marking tasks as complete or incomplete

### Out of Scope (Non-Goals)

- Persistence (database, file storage)
- Authentication or user accounts
- GUI, web interface, or REST API
- Multi-user support
- Task prioritization, due dates, tags, or advanced features
- External integrations

## Development Standards

### Project Structure

The project MUST use a proper Python project structure with clear separation:

```
src/
├── models/          # Task data structures
├── services/        # Business logic (task management)
└── cli/             # Console interface and user interaction

tests/
├── unit/            # Unit tests for services and models
└── integration/     # Integration tests for full workflows
```

### Technology Constraints

- **Python Version**: 3.13+
- **Package Manager**: `uv` (for project and dependency management)
- **Testing Framework**: pytest
- **Storage**: In-memory only (no databases or files)
- **Interaction**: Console/terminal only

### Quality Gates

All code changes MUST pass these gates before being considered complete:

1. **Tests First**: Tests written and verified to fail before implementation
2. **Tests Pass**: All tests pass (Red → Green achieved)
3. **Code Quality**: Follows PEP 8, uses type hints, has descriptive names
4. **No Over-Engineering**: Solution is the simplest viable approach
5. **Separation Maintained**: Models, services, and CLI remain distinct

## Governance

### Amendment Process

1. Proposed changes to this constitution MUST be documented with clear rationale
2. Impact on existing code and templates MUST be assessed
3. Version MUST be incremented following semantic versioning:
   - **MAJOR**: Backward-incompatible principle changes or removals
   - **MINOR**: New principles or expanded guidance
   - **PATCH**: Clarifications, wording fixes, non-semantic refinements
4. All dependent templates (plan, spec, tasks) MUST be reviewed for consistency
5. Amendments require explicit approval before implementation

### Versioning Policy

- This constitution follows semantic versioning (MAJOR.MINOR.PATCH)
- Version changes are recorded in the Sync Impact Report (HTML comment at top)
- Breaking changes require migration plan for existing code

### Compliance Review

- All feature planning (`/sp.plan`) MUST include a Constitution Check section
- Violations of principles MUST be justified in the Complexity Tracking table
- Code reviews MUST verify adherence to core principles
- Unjustified complexity is grounds for rejection

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
