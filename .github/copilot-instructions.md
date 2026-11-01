# Copilot Coding Agent Instructions for GoERP Payroll

## Project Overview

- **GoERP Payroll** is a jurisdiction-agnostic, highly configurable payroll engine. All payroll logic (earnings, deductions, benefits, taxes) is defined via configuration, not hardcoded.
- The system is modular: main logic in `goerp_payroll/`, with submodules for formula, payroll, vacation, reporting, RBAC, queue, and more.
- **No legal rules are hardcoded**. Implementers must configure all payroll concepts and rules.

## Key Architectural Patterns

- **Formula Engine** (`goerp_payroll/formula_engine/`): Uses AST and Visitor patterns for safe, dynamic formula evaluation. All calculation logic is schema-driven.
- **Payroll Engine** (`goerp_payroll/nomina_engine/`): Orchestrates payroll execution using domain, validator, calculator, processor, repository, and service layers. Follows clear separation of concerns.
- **RBAC** (`goerp_payroll/rbac.py`): Role-based access control with Admin, HR, and Audit roles.
- **Queue System** (`goerp_payroll/queue/`): Supports Dramatiq+Redis for background processing. If Redis is unavailable, uses NoopQueueDriver (synchronous execution).
- **Internationalization**: All user-facing text is translatable via `goerp_payroll/translations/`.
- **Configuration**: Environment variables control DB, queue, and other settings. See README for details.

## Developer Workflows

- **Run app**: `flask --debug run` (default port 5000)
- **CLI admin**: Use `payrollctl` (or `flask`) for system/db/user/cache/maintenance/debug tasks. See README for command list.
- **Tests**: Run with `pytest`. All tests use in-memory SQLite and are fully isolated. See `tests/README.md` for patterns and troubleshooting.
- **Docs**: Build/serve with MkDocs (`pip install -r docs.txt && mkdocs serve`).
- **Linting**: Use `flake8` and `ruff` for code quality checks.
- **Formatting**: Use `black` for consistent code style and `prettier` for html/CSS/JS.

## Project-Specific Conventions

- **No shared state in tests**: Each test creates its own data, uses rollback, and is parallel-safe.
- **Factories**: All test data is created via explicit factory functions (see `tests/factories/`).
- **Helpers**: Use helpers for auth, assertions, and HTTP in tests (see `tests/helpers/`).
- **Naming**: Test files/functions: `test_*.py`/`test_*`; Factories: `*_factory.py`/`create_*`.
- **All configuration is explicit**: No magic defaults for payroll logic—everything must be defined by the implementer.

## Integration Points

- **Database**: Supports SQLite (dev), PostgreSQL/MySQL (prod). DB engine is selected via `DATABASE_URL`.
- **Queue**: Background processing for large payrolls; backend auto-selected.
- **RBAC**: All sensitive actions are role-guarded.
- **Reporting**: Custom reports with role-based permissions and audit trail.
- **Vacation**: Fully configurable vacation policies and audit.

## Key Files/Directories

- `app.py`: Entrypoint
- `goerp_payroll/`: Main logic
  - `formula_engine/`, `nomina_engine/`, `vacation_service.py`, `rbac.py`, `report_engine.py`, `queue/`, `templates/`, `translations/`
- `tests/`: Test infra, factories, helpers, patterns (`tests/README.md`)
- `docs/`: Full documentation, guides, and reference
- `README.md`, `SOCIAL_CONTRACT.md`: Project scope, philosophy, and legal disclaimers

## Examples

- To add a new payroll concept: define it in configuration, not code.
- To add a test: use a factory to create data, ensure no shared state, and verify both HTTP and DB results.
- To run a background payroll: ensure `QUEUE_ENABLED=1` and Redis is configured and available.

---

For more, see `README.md`, `tests/README.md`, and `docs/`.
