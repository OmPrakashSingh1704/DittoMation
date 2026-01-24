# Contributing to DittoMation

Thank you for your interest in contributing to DittoMation! We appreciate your help in making this Android automation framework better.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior vs. actual behavior
- Your environment (Python version, OS, Android device/emulator details)
- Any relevant logs or error messages

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:

- A clear description of the enhancement
- Why this feature would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards (see below)
3. **Add tests** if you're adding functionality
4. **Ensure all tests pass** before submitting
5. **Update documentation** if you're changing behavior
6. **Write clear commit messages** describing what and why
7. **Submit a pull request** with a clear description

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/OmPrakashSingh1704/DittoMation.git
cd DittoMation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # Install development dependencies
```

4. Connect an Android device or start an emulator:
```bash
adb devices  # Should show your device
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use type hints for function parameters and return values
- Use descriptive variable and function names

### Code Quality

- **Type hints**: Add type hints to all function signatures
- **Docstrings**: Document all public functions and classes using Google-style docstrings
- **Error handling**: 
  - Use specific exception types, never bare `except:`
  - Always log exceptions with context
  - Provide helpful error messages
- **Logging**: Use the `logging_config` module, not `print()` statements
- **Constants**: Define magic numbers as named constants

### Example of Good Code

```python
from typing import Optional
from core.logging_config import get_logger

logger = get_logger(__name__)

# Constants
MAX_TEXT_LENGTH = 5000
DEFAULT_TIMEOUT = 30

def input_text(text: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """
    Input text into the current field on the Android device.
    
    Args:
        text: Text to input (max 5000 characters)
        timeout: Maximum time to wait in seconds
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If text exceeds maximum length
        TimeoutError: If operation times out
    """
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Text length {len(text)} exceeds maximum of {MAX_TEXT_LENGTH}")
    
    try:
        # Implementation here
        logger.info(f"Inputting text of length {len(text)}")
        return True
    except TimeoutError as e:
        logger.error(f"Text input timed out after {timeout}s: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to input text: {e}")
        return False
```

### Testing

- Write unit tests for new functionality
- Place tests in the `tests/` directory
- Use pytest for testing
- Aim for good test coverage of critical paths

Run tests with:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html tests/
```

### Linting

Before submitting, run linting tools:

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy .
```

## Project Structure

```
DittoMation/
├── core/              # Core utilities (CLI, config, exceptions, logging)
├── recorder/          # Recording workflow functionality
├── replayer/          # Replaying workflow functionality
├── config/            # Configuration files
├── docs/              # Documentation
└── tests/             # Test files
```

## Git Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit regularly:
```bash
git add .
git commit -m "Add feature: description of what you did"
```

3. Keep your branch updated:
```bash
git fetch origin
git rebase origin/main
```

4. Push your changes:
```bash
git push origin feature/your-feature-name
```

5. Create a pull request on GitHub

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

Examples:
```
Add support for scroll gestures in natural language runner

Fix IndexError in gesture execution when coordinate list is empty

Improve error handling in ADB wrapper with specific exceptions
```

## Documentation

- Update README.md if you change user-facing features
- Add docstrings to all public APIs
- Update docs/ folder for major changes
- Include code examples where helpful

## Questions?

Feel free to:
- Create an issue for questions
- Ask in pull request comments
- Reach out to the maintainers

Thank you for contributing to DittoMation! 🎉
