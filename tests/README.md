# GTR-Bench Tests

This directory contains the test suite for GTR-Bench.

## Structure

```
tests/
├── unit/             # Unit tests for individual components
├── integration/      # Integration tests for workflows
└── fixtures/         # Test data and fixtures
```

## Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest --cov=src/gtr_bench

# Run specific test file
pytest tests/unit/test_tasks.py
```

## Test Guidelines

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test complete workflows and pipelines  
3. **Fixtures**: Use shared test data and mock objects
4. **Coverage**: Aim for >90% code coverage
5. **Naming**: Use descriptive test names that explain what is being tested

## Adding New Tests

1. Create test files matching the source structure: `test_{module_name}.py`
2. Use pytest fixtures for reusable test data
3. Mock external dependencies (models, APIs)
4. Test both success and failure cases
5. Add integration tests for new workflows