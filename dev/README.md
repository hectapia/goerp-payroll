# Development Scripts

This directory contains scripts to help with development and testing workflows.

## Linting and Code Quality

### lint.sh - Full Code Quality Validation

**Introduced in v1.0.6**

Runs the complete local validation stack to ensure code quality and correctness before pushing changes.

**Features:**
- Runs `black` for code formatting
- Runs `ruff` for fast linting
- Runs `flake8` for style checking
- Runs `pylint` for comprehensive static analysis
- Runs `mypy` for type checking
- Runs full test suite (regular + validation tests)

**Usage:**
```bash
./dev/lint.sh
```

**Best for:**
- Pre-push validation
- Ensuring CI will pass
- Comprehensive code quality checks
- Aligning with project standards

**Note:** This script runs all quality tools in sequence. If any step fails, the script continues to show all issues. This matches the CI pipeline configuration.

## Test Scripts

### test_fast.sh - Quick Feedback Testing

Fast test execution for rapid development feedback.

**Features:**
- Runs tests in parallel using all available CPU cores
- Excludes validation tests (which are slower)
- Fails fast on first error for quick feedback
- No coverage collection for maximum speed

**Usage:**
```bash
./dev/test_fast.sh

# Run specific test file
./dev/test_fast.sh tests/test_app.py

# Run specific test
./dev/test_fast.sh tests/test_app.py::test_create_app
```

**Best for:**
- Quick validation during development
- Pre-commit checks
- Finding the first failing test quickly

### test_full.sh - Comprehensive Testing

Full test suite execution with coverage reporting.

**Features:**
- Runs all tests including validation tests
- Parallel execution for speed
- Generates code coverage reports
- Verbose output with detailed results

**Usage:**
```bash
./dev/test_full.sh

# Run with specific pytest options
./dev/test_full.sh --verbose
```

**Best for:**
- Pre-push validation
- Coverage analysis
- Full system validation
- CI/CD pipeline locally

## Performance Improvements

The test suite has been optimized for speed:

- **Parallel Execution**: Tests run in parallel using pytest-xdist
- **Session-Scoped Fixtures**: Shared fixtures across tests reduce setup overhead
- **Baseline**: 21.04 seconds
- **Optimized**: 14.44 seconds
- **Improvement**: ~31% faster (6.6 seconds saved)

## Tips

1. Use `test_fast.sh` during active development for quick feedback loops
2. Use `test_full.sh` before committing to ensure nothing is broken
3. The CI pipeline automatically uses parallel execution
4. You can pass any pytest options to either script
