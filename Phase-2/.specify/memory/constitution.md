<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0 (Phase-2 expansion - backward-incompatible scope changes)
- Modified principles:
  - Simplicity First → Updated to allow measured complexity for organization features
  - Separation of Concerns → Clarified to accommodate filtering and display enhancements
- Added sections:
  - Phase Evolution Strategy (new governance section)
  - Incremental Complexity principle
  - Organization & Filtering capabilities to In Scope
- Removed from Out of Scope:
  - Task prioritization, due dates, tags (now allowed in Phase-2)
- Templates requiring updates:
  ✅ Updated: plan-template.md (Constitution Check section updated)
  ✅ Updated: spec-template.md (Requirements expanded for Phase-2)
  ✅ Updated: tasks-template.md (Task categorization expanded)
- Follow-up TODOs: None (all placeholders filled)
-->

# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Simplicity First

The codebase MUST remain simple and maintainable. Every design decision should favor the simplest viable solution that meets the requirement. Complexity is allowed ONLY when it delivers clear user value and is properly justified.

**Rules**:
- No over-engineering or premature abstraction
- External libraries allowed ONLY for terminal enhancements (colorama, rich) - no web frameworks
- No persistence layers (in-memory storage only, all phases)
- No authentication, authorization, or user management
- Console-based interaction only—no GUI, web interface, or REST API
- New complexity MUST be justified in the Complexity Tracking table during planning

**Rationale**: The app evolves through phases (Basic → Intermediate → Advanced). Each phase adds measured complexity to deliver organization, usability, and intelligent features while maintaining the console-first philosophy.

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

### VI. Incremental Complexity

Features MUST be added incrementally, building on previous phases without breaking existing functionality. Each phase delivers independent user value.

**Rules**:
- Phase-1 (Basic): Core CRUD operations
- Phase-2 (Intermediate): Organization and usability (categories, priorities, filtering, enhanced display)
- Phase-3 (Advanced): Intelligent behaviors (analytics, patterns, recommendations)
- All phases maintain backward compatibility with previous phase features
- Each phase MUST have complete test coverage before moving to the next
- Refactoring is continuous but MUST keep tests green

**Rationale**: Incremental delivery reduces risk, enables early feedback, and ensures a stable foundation for advanced features.

## Functional Scope

### Phase-1 (Basic) - COMPLETED

- Adding tasks with title and description
- Viewing all tasks with clear status indicators
- Updating task title and description
- Deleting tasks by unique ID
- Marking tasks as complete or incomplete

### Phase-2 (Intermediate) - In Scope

- **Organization**: Categories/projects, priority levels (Low/Medium/High), tags, due dates
- **Filtering & Search**: Filter by status/category/priority, search by keyword, sort options
- **Enhanced Display**: Color-coded priorities, grouped views, task statistics, overdue indicators
- **Bulk Operations**: Mark multiple complete, batch delete, clear completed tasks
- **Usability**: Command history, input validation improvements, better error messages

### Phase-3 (Advanced) - Future Scope

- Task analytics and productivity insights
- Smart recommendations based on patterns
- Recurring tasks and reminders
- Task dependencies and subtasks
- Export/import capabilities (CSV, JSON)

### Out of Scope (All Phases)

- Persistence (database, file storage) - in-memory ONLY
- Authentication or user accounts
- GUI, web interface, or REST API
- Multi-user support or collaboration features
- External integrations (calendar, email, etc.)
- Cloud sync or mobile apps

## Development Standards

### Project Structure

The project MUST use a proper Python project structure with clear separation:

```
src/
├── models/          # Data structures (Task, Category, Priority, etc.)
├── services/        # Business logic (task management, filtering, search)
├── cli/             # Console interface and user interaction
└── utils/           # Shared utilities (validators, formatters, date helpers)

tests/
├── unit/            # Unit tests for services and models
└── integration/     # Integration tests for full workflows

specs/               # Feature specifications organized by feature number
└── <NNN>-<feature-name>/
    ├── spec.md      # Requirements and acceptance criteria
    ├── plan.md      # Architecture and design decisions
    ├── tasks.md     # Implementation task breakdown
    └── contracts/   # Interface definitions
```

### Technology Constraints

- **Python Version**: 3.13+
- **Package Manager**: `uv` (for project and dependency management)
- **Testing Framework**: pytest
- **Storage**: In-memory only (no databases or files, all phases)
- **Interaction**: Console/terminal only
- **Allowed Libraries**:
  - Standard library (unlimited use)
  - Terminal enhancements: colorama, rich (for colors and formatting)
  - Date/time: datetime, dateutil (for due date handling)
  - Testing: pytest, pytest-cov, pytest-mock
- **Forbidden**: Web frameworks, ORMs, authentication libraries, cloud SDKs

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

### Phase Evolution Strategy

Each phase builds on the previous phase without breaking existing functionality:

1. **Phase Completion Criteria**:
   - All user stories implemented and tested
   - Test coverage ≥ 80% for new code
   - No regressions in previous phase features
   - Documentation updated (specs, README, quickstart)

2. **Phase Transition Process**:
   - Complete current phase (all acceptance criteria met)
   - Update constitution if needed (scope, principles)
   - Create new feature spec for next phase
   - Plan architecture with backward compatibility in mind
   - Implement incrementally with continuous testing

3. **Backward Compatibility**:
   - Existing features MUST continue to work unchanged
   - New features are additive, not replacements
   - CLI commands can be extended but not removed
   - Data models can be extended with optional fields only

### Compliance Review

- All feature planning (`/sp.plan`) MUST include a Constitution Check section
- Violations of principles MUST be justified in the Complexity Tracking table
- Code reviews MUST verify adherence to core principles
- Unjustified complexity is grounds for rejection
- Phase transitions require explicit constitution review

**Version**: 2.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-06
