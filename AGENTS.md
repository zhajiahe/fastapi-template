# Project Overview

This is a modern FastAPI backend template featuring asynchronous SQLAlchemy 2.0 ORM,
JWT authentication with access/refresh tokens, and layered architecture (Router → Service → Repository).
Built with Python 3.12+, using uv for dependency management, ruff for code quality,
ty for type checking (10x-100x faster than mypy), and pytest for testing.

## Repository Structure

- `app/` - Main application code
  - `api/` - FastAPI route handlers and endpoints
  - `core/` - Configuration, security, database setup, and exceptions
  - `models/` - SQLAlchemy ORM models and base classes
  - `repositories/` - Data access layer with generic CRUD operations
  - `schemas/` - Pydantic models for request/response validation
  - `services/` - Business logic layer
  - `middleware/` - Custom middleware (logging, etc.)
  - `utils/` - Utility functions and helpers
- `tests/` - Test suite with unit and integration tests
  - `unit/` - Unit tests for individual components
  - `integration/` - API integration tests
- `alembic/` - Database migration scripts and configuration
- `scripts/` - Utility scripts for development and deployment

## Setup & Dev Commands

```bash
# Install dependencies with uv (recommended Python package manager)
uv sync

# Start development server with hot reload
make dev
# Alternative: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Database setup
cp .env.example .env  # Configure environment variables
make db-upgrade       # Run database migrations

# View API documentation at http://localhost:8000/docs
```

## Testing Instructions

Tests use pytest with asyncio support. Run from project root.

```bash
# Run all tests
make test
# Alternative: uv run pytest tests/ -v

# Run specific test types
make test-unit       # Unit tests only
make test-integration # Integration tests only

# Run tests with coverage report
make test-cov
# Alternative: uv run pytest tests/ -v --cov=app --cov-report=html

# Run specific test file or class
uv run pytest tests/unit/test_security.py -v
uv run pytest tests/integration/test_user_route.py::TestAuthAPI -v
```

## Code Style & Conventions

Code formatting and quality enforced by ruff and ty.

```bash
# Run all code quality checks
make check
# Alternative: make lint-fix && make format && make type-check

# Individual commands
make lint-fix    # Fix linting issues automatically
make format      # Format code with ruff
make type-check  # Type checking with ty
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `snake_case.py`
- **Directories**: `snake_case/`

### Good/Bad Examples

```python
# ✅ Good: Explicit type hints, descriptive names
async def get_user_by_id(user_id: int) -> User | None:
    """Get user by ID with proper error handling."""
    if user_id <= 0:
        raise ValueError("User ID must be positive")
    return await self.user_repo.get_by_id(user_id)

# ❌ Bad: Implicit types, unclear logic
def get_user(id):  # No type hints
    return db.query(User).filter(User.id == id).first()  # No error handling
```

## PR & Git Workflow

### Branch Naming

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `refactor/component-name` - Code refactoring
- `docs/update-description` - Documentation updates

### Commit Message Format

Follow conventional commits:

```bash
feat: add user registration endpoint
fix: resolve password reset bug
refactor: simplify user service logic
docs: update API documentation
test: add integration tests for auth
```

### PR Requirements

All PRs must pass:
- `make check` - Code quality checks (lint, format, type check)
- `make test` - Test suite
- Manual review by at least one maintainer

## Security & Guardrails

### Secrets Management

- Never commit `.env` files to git
- Use `.env.example` as template for required environment variables
- Production secrets must be set via environment variables only
- Default JWT secrets in config are placeholders - **MUST** be changed in production

### Security Scanning

```bash
# TODO: Add security scanning commands when implemented
# make security-scan
```

### AI Agent Boundaries

**✅ Allowed Operations:**
- Read/modify application code in `app/`, `tests/`, `scripts/`
- Run tests, linting, formatting commands
- Update documentation in `*.md` files
- Create/modify database migrations
- Update configuration files (`.env.example`, `pyproject.toml`, etc.)

**⚠️ Ask Before:**
- Changing database schema or migrations
- Modifying security-related code (auth, JWT, password handling)
- Adding new dependencies
- Changing CI/CD pipeline configuration

**❌ Forbidden:**
- Committing secrets or sensitive data
- Modifying production environment variables
- Accessing external APIs or services without explicit permission
- Running code that could affect production systems

## Further Reading

- `README.md` - General project overview and setup
- `docs/` - TODO: Add documentation directory when created
- `ARCHITECTURE.md` - TODO: Add architecture documentation when created
- `alembic/README` - Database migration documentation