# Testing Documentation

## Overview

This document describes the comprehensive testing strategy implemented for the Deepcast Post project. The test suite covers all major functionality including unit tests, CLI tests, and integration tests.

## Test Structure

### Test Files

- **`tests/test_core.py`** - Unit tests for the `DeepcastGenerator` class
- **`tests/test_cli.py`** - Tests for the command-line interface
- **`tests/test_integration.py`** - Integration tests for the complete workflow
- **`tests/conftest.py`** - Shared test fixtures and configuration

### Test Configuration

- **`pytest.ini`** - Pytest configuration with coverage reporting
- **`pyproject.toml`** - Development dependencies including pytest and coverage tools

## Test Coverage

The test suite achieves **99% code coverage** across all modules:

- **`deepcast_post/core.py`**: 100% coverage (50 statements)
- **`deepcast_post/cli.py`**: 97% coverage (30 statements, 1 missed)
- **`deepcast_post/__init__.py`**: 100% coverage (0 statements)

## Running Tests

### Prerequisites

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Basic Test Execution

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_core.py

# Run specific test class
poetry run pytest tests/test_core.py::TestDeepcastGenerator

# Run specific test method
poetry run pytest tests/test_core.py::TestDeepcastGenerator::test_init_with_api_key
```

### Coverage Reports

```bash
# Generate coverage report in terminal
poetry run pytest --cov=deepcast_post --cov-report=term-missing

# Generate HTML coverage report
poetry run pytest --cov=deepcast_post --cov-report=html

# Generate XML coverage report (for CI/CD)
poetry run pytest --cov=deepcast_post --cov-report=xml
```

### Test Categories

```bash
# Run only unit tests
poetry run pytest tests/test_core.py

# Run only CLI tests
poetry run pytest tests/test_cli.py

# Run only integration tests
poetry run pytest tests/test_integration.py

# Run tests with specific markers
poetry run pytest -m "integration"
poetry run pytest -m "not slow"
```

## Test Types

### 1. Unit Tests (`test_core.py`)

Tests individual methods and functionality of the `DeepcastGenerator` class:

- **Initialization tests**: API key validation, parameter handling, environment overrides
- **File I/O tests**: Transcript loading, error handling, file operations
- **Prompt building tests**: Content validation, length handling
- **API interaction tests**: OpenAI client mocking, error handling
- **Workflow tests**: Complete breakdown generation with mocked dependencies

**Key Features:**

- Comprehensive mocking of external dependencies (OpenAI API, file system)
- Edge case testing (file not found, encoding errors, API failures)
- Parameter validation and environment variable handling

### 2. CLI Tests (`test_cli.py`)

Tests the command-line interface functionality:

- **Argument parsing**: All CLI options and flags
- **Environment validation**: API key checking
- **Error handling**: Graceful failure with user-friendly messages
- **Integration**: CLI-to-core class communication

**Key Features:**

- Mocked `DeepcastGenerator` to avoid actual execution
- Argument validation testing
- Error message verification
- Exit code validation

### 3. Integration Tests (`test_integration.py`)

Tests the complete workflow from transcript input to output generation:

- **End-to-end workflow**: Complete deepcast generation process
- **File handling**: Input/output file management
- **API integration**: Mocked OpenAI API calls
- **Output validation**: Markdown format verification

**Key Features:**

- Real file system operations with cleanup
- Mocked external APIs
- Workflow validation
- Output format verification

### 4. Test Fixtures (`conftest.py`)

Shared test utilities and fixtures:

- **Sample data**: Transcript content, expected outputs
- **File management**: Temporary file creation and cleanup
- **Environment mocking**: API keys and configuration
- **Mock objects**: OpenAI client, console output

## Mocking Strategy

### External Dependencies

- **OpenAI API**: Mocked to avoid actual API calls during testing
- **File System**: Mocked where appropriate, real operations for integration tests
- **Console Output**: Mocked for verification without cluttering test output

### Mock Patterns

```python
# Mock OpenAI client
with patch('openai.OpenAI') as mock_openai:
    mock_client = mock_openai.return_value
    mock_response = mock_client.chat.completions.create.return_value
    mock_response.choices[0].message.content = "Mocked response"

# Mock file operations
with patch('builtins.open', mock_open()) as mock_file:
    # Test file operations

# Mock environment variables
with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
    # Test with specific environment
```

## Test Data

### Sample Transcripts

```python
sample_transcript = """[00:00:00] Speaker A: Welcome to the podcast everyone.
[00:00:05] Speaker B: Thanks for having us.
[00:00:10] Speaker A: Today we're discussing AI and its impact on society."""
```

### Expected Outputs

```python
sample_deepcast_output = """# Deepcast Breakdown

## Main Themes
- **AI Ethics:** Discussion of responsible AI development
- **Societal Impact:** How AI affects different communities

## Speaker Notes
**Speaker A:** Host with technical background
**Speaker B:** Guest expert, provides industry insights

## Executive Summary
- AI ethics crucial for responsible development
- Societal impact requires careful consideration"""
```

## Best Practices

### Test Organization

1. **Descriptive names**: Test methods clearly describe what they're testing
2. **Single responsibility**: Each test focuses on one specific behavior
3. **Setup/teardown**: Proper cleanup of test resources
4. **Mock isolation**: Tests don't interfere with each other

### Assertion Patterns

```python
# Verify method calls
mock_generator.generate_breakdown.assert_called_once_with(
    transcript_path="input.txt",
    output_path="output.md"
)

# Verify content
assert "expected content" in actual_content

# Verify error conditions
with pytest.raises(ValueError, match="expected error message"):
    function_that_should_fail()
```

### Error Handling

- **Graceful failures**: Tests verify that errors are handled properly
- **User-friendly messages**: Error messages are clear and actionable
- **Proper exit codes**: CLI tools exit with appropriate status codes

## Continuous Integration

The test suite is designed to work in CI/CD environments:

- **Fast execution**: Tests complete in under 1 second
- **No external dependencies**: All external services are mocked
- **Deterministic results**: Tests produce consistent results
- **Coverage reporting**: XML coverage reports for CI tools

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure virtual environment is activated
2. **Mock failures**: Check that mocks are applied at the correct level
3. **File permission errors**: Ensure test files can be created/deleted
4. **Coverage gaps**: Add tests for uncovered code paths

### Debug Mode

```bash
# Run tests with debug output
poetry run pytest -v -s

# Run specific failing test
poetry run pytest tests/test_core.py::TestDeepcastGenerator::test_specific_method -v -s
```

## Future Enhancements

### Potential Improvements

1. **Performance tests**: Measure execution time for large transcripts
2. **Stress tests**: Test with very long or malformed input
3. **Security tests**: Validate input sanitization
4. **Compatibility tests**: Test with different Python versions

### Test Maintenance

- **Regular updates**: Keep tests in sync with code changes
- **Coverage monitoring**: Track coverage trends over time
- **Performance monitoring**: Ensure tests remain fast
- **Documentation updates**: Keep this document current

## Conclusion

The comprehensive test suite provides confidence in the codebase quality and enables safe refactoring and feature development. With 99% code coverage and thorough testing of all major functionality, the Deepcast Post project has a solid foundation for continued development.
