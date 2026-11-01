# Test Infrastructure Documentation

## Overview

This test infrastructure is designed for independent, parallel-safe testing with SQLite in-memory databases. Each test is completely isolated and can run sequentially or in parallel using pytest-xdist.

## Architecture Principles

### Core Design Rules

1. **Complete Independence**: Each test is fully independent and creates its own data
2. **No Shared State**: No test depends on state left by another test
3. **Automatic Rollback**: Each test runs in a transaction that is rolled back after completion
4. **Parallel-Safe**: Tests can run in parallel using `pytest -n auto`
5. **Sequential-Safe**: Tests can also run sequentially without any issues
6. **In-Memory Database**: All tests use SQLite in-memory databases for speed and isolation

## Directory Structure

```
tests/
├── conftest.py              # Pytest fixtures (app, db_session, client, admin_user)
├── factories/               # Data creation functions
│   ├── __init__.py
│   ├── user_factory.py      # create_user()
│   ├── employee_factory.py  # create_employee()
│   └── company_factory.py   # create_company()
├── helpers/                 # Helper functions
│   ├── __init__.py
│   ├── auth.py             # login_user(), logout_user()
│   ├── assertions.py       # assert_user_exists(), assert_redirected_to()
│   └── http.py             # follow_redirects_once()
├── test_auth/              # Authentication tests
│   └── test_login.py
├── test_users/             # User management tests
│   └── test_user_creation.py
├── test_basic/             # Basic application tests
│   └── test_app_initialization.py
└── README.md               # This file
```

## Fixtures

### `app` (function scope)
- Creates a fresh Flask application for each test
- Configured with TESTING=True and SQLite in-memory database
- CSRF protection disabled for easier testing
- Uses filesystem session storage to avoid conflicts

### `db_session` (function scope)
- Provides a database session wrapped in a transaction
- Transaction is automatically rolled back after each test
- Ensures complete isolation between tests

### `client` (function scope)
- Flask test client for making HTTP requests
- Allows testing without running a real server

### `admin_user` (function scope)
- Creates an admin user only when explicitly requested
- Tests that don't need an admin don't create one

## Factories

Factories are simple functions that create data. They:
- Accept explicit parameters
- Have no hidden side effects
- Don't create related data implicitly
- Return the created entity

Example:
```python
from tests.factories import create_user

def test_something(app, db_session):
    with app.app_context():
        user = create_user(
            db_session,
            usuario="testuser",
            password="password",
            nombre="John",
            apellido="Doe"
        )
        assert user.usuario == "testuser"
```

## Helpers

Helpers reduce duplication without hiding behavior:

### Authentication Helpers
- `login_user(client, username, password)` - Log in via HTTP
- `logout_user(client)` - Log out

### Assertion Helpers
- `assert_user_exists(db_session, usuario)` - Verify user exists in DB
- `assert_redirected_to(response, expected_location)` - Verify redirect

### HTTP Helpers
- `follow_redirects_once(client, response)` - Follow one redirect

## Writing Tests

### Test Structure

Each test should follow this pattern:

```python
def test_description(client, app, db_session):
    """
    Brief description of what is being tested.
    
    Setup:
        - What data is created
    
    Action:
        - What HTTP request is made
    
    Verification:
        - What is checked (HTTP response and DB state)
    """
    with app.app_context():
        # 1. Setup: Create minimal data needed
        user = create_user(db_session, "testuser", "password")
        
        # 2. Action: Perform HTTP request
        response = login_user(client, "testuser", "password")
        
        # 3. Verification: Check HTTP response
        assert response.status_code == 302
        
        # 4. Verification: Check database state
        found = assert_user_exists(db_session, "testuser")
        assert found.activo is True
```

### Naming Conventions

- **Test files**: `test_*.py`
- **Test functions**: `test_*`
- **Factory files**: `*_factory.py`
- **Factory functions**: `create_*`

### Do's and Don'ts

✅ **DO:**
- Create only the data your test needs
- Use explicit factory calls
- Verify both HTTP response and database state
- Make tests readable and self-documenting
- Use fixtures when appropriate

❌ **DON'T:**
- Depend on the order of test execution
- Share state between tests
- Create unnecessary data
- Use "magic" fixtures that hide complexity
- Manually clean up (rollback is automatic)

## Running Tests

### Run all tests in parallel (default)
```bash
pytest
# or explicitly:
pytest -n auto
```

### Run all tests sequentially
```bash
pytest -o addopts=""
```

### Run specific test file
```bash
pytest tests/test_auth/test_login.py
```

### Run specific test
```bash
pytest tests/test_auth/test_login.py::test_successful_admin_login
```

### Run with coverage
```bash
pytest --cov=goerp_payroll --cov-report=term-missing
```

### Run validation tests only
```bash
pytest -m validation
```

### Run excluding validation tests
```bash
pytest -m "not validation"
```

## CI/CD Integration

The test infrastructure is designed to work seamlessly with GitHub Actions. The workflow:

1. **Lint with flake8** - Check for syntax errors and style issues
2. **Lint with ruff** - Additional code quality checks
3. **Test with pytest (regular)** - Run main test suite in parallel
4. **Test with pytest (validation)** - Run end-to-end validation tests
5. **Coverage reporting** - Generate and upload coverage reports

All tests use SQLite in-memory databases and run in parallel for speed.

## Adding New Tests

1. Choose the appropriate directory (or create a new one)
2. Create a test file following naming conventions
3. Write tests following the structure above
4. Ensure tests are independent and can run in any order
5. Verify tests pass both sequentially and in parallel:
   ```bash
   pytest -o addopts="" tests/your_test.py
   pytest -n auto tests/your_test.py
   ```

## Troubleshooting

### Tests fail in parallel but pass sequentially
- Tests are sharing state somehow
- Check for global variables or singletons
- Ensure each test creates its own data

### Database locked errors
- SQLite connections not properly closed
- Check that db_session is being used correctly
- Verify check_same_thread=False is configured

### Fixture errors
- Make sure fixture scope is "function"
- Verify fixtures are properly imported
- Check fixture dependency order

## Best Practices

1. **Minimal Data**: Create only what the test needs
2. **Explicit Over Implicit**: Make data creation visible in the test
3. **Fast Tests**: Use in-memory database and avoid unnecessary operations
4. **Clear Intent**: Test names and docstrings should explain what's being tested
5. **Database Verification**: Always verify that database state matches expectations
6. **HTTP Testing**: Use Flask test client for all HTTP interactions
7. **Isolation**: Each test should work correctly even if run alone

## Performance

- In-memory SQLite provides fast test execution
- Parallel execution with pytest-xdist scales with CPU cores
- Transaction rollback is faster than database cleanup
- Typical test execution time: 2-6 seconds for 17 tests (parallel)

## Future Enhancements

Potential areas for expansion:
- Additional factories for complex entities (payrolls, loans, etc.)
- More helper functions for common assertions
- Integration tests for complete workflows
- Performance benchmarking with pytest-benchmark
- Additional validation tests for end-to-end scenarios
