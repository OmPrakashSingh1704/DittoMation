# Contributing to DittoMation

Thank you for your interest in contributing to DittoMation! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Android SDK with ADB (Android Debug Bridge)
- Git

### Installation

1. Fork and clone the repository:

```bash
git clone https://github.com/OmPrakashSingh1704/DittoMation.git
cd DittoMation
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -e .[dev]
```

4. Install pre-commit hooks:

```bash
pre-commit install
```

## Code Style

### Formatting

We use **Black** for code formatting with a line length of 100 characters:

```bash
black .
```

### Linting

We use **Ruff** for linting:

```bash
ruff check .
ruff check --fix .  # Auto-fix issues
```

### Type Checking

We use **MyPy** for static type checking:

```bash
mypy core recorder replayer
```

### Pre-commit

All style checks run automatically on commit via pre-commit hooks. To run manually:

```bash
pre-commit run --all-files
```

## Testing

### Running Tests

Run the test suite with pytest:

```bash
pytest
```

With coverage:

```bash
pytest --cov=core --cov=recorder --cov=replayer --cov-report=term-missing
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Include both positive and negative test cases
- Mock external dependencies (ADB, device connections)

Example:

```python
def test_tap_with_valid_coordinates_executes_successfully():
    """Test that tap executes with valid coordinates."""
    # Arrange
    executor = GestureExecutor()

    # Act
    result = executor.tap(100, 200)

    # Assert
    assert result.success
```

## Pull Request Process

### Before Submitting

1. **Create a branch** from `main`:

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** following the code style guidelines

3. **Write or update tests** for your changes

4. **Run the test suite** to ensure all tests pass:

```bash
pytest
```

5. **Run pre-commit hooks**:

```bash
pre-commit run --all-files
```

6. **Update documentation** if needed

### Submitting

1. Push your branch to your fork
2. Open a Pull Request against the `main` branch
3. Fill out the PR template with:
   - Description of changes
   - Related issues (if any)
   - Testing performed
4. Wait for CI checks to pass
5. Address any review feedback

### PR Guidelines

- Keep PRs focused and reasonably sized
- One feature or fix per PR
- Write clear commit messages
- Reference related issues using `#issue_number`
- Update CHANGELOG.md for user-facing changes

## Project Structure

```
DittoMation/
├── core/               # Core functionality
│   ├── android.py      # Main Android API
│   ├── automation.py   # Automation runner
│   ├── cli.py          # CLI commands
│   ├── config_manager.py
│   ├── exceptions.py   # Exception hierarchy
│   └── ...
├── recorder/           # Recording functionality
│   ├── interactive_recorder.py
│   ├── workflow.py
│   └── ...
├── replayer/           # Replay functionality
│   ├── executor.py
│   ├── locator.py
│   ├── nl_runner.py
│   └── ...
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Example scripts
```

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Android device/emulator details
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or error messages

## Getting Help

- Open an issue for bugs or feature requests
- Use discussions for questions and ideas
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
