# Contributing to DittoMation

Thank you for your interest in contributing to DittoMation! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're building an inclusive community where everyone feels welcome to contribute.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description** of the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, Android version, device type)
- **Logs or error messages** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description** of the feature
- **Use case** explaining why this would be useful
- **Possible implementation** if you have ideas

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write clear commit messages** describing what and why
6. **Submit a pull request** with a clear description

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DittoMation.git
   cd DittoMation
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up ADB and connect your Android device:
   ```bash
   adb devices  # Should show your device
   ```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate

### Code Quality

- **Write docstrings** for all public functions and classes
- **Handle errors explicitly** - avoid bare `except:` clauses
- **Add logging** for important operations (use the provided logger)
- **Validate inputs** especially for user-provided data
- **Use context managers** for resource management

### Security Best Practices

- **Never use shell=True** in subprocess calls
- **Always validate file paths** before operations
- **Use separate arguments** instead of string interpolation for commands
- **Add timeouts** to all subprocess operations
- **Handle sensitive data** (phone numbers, etc.) carefully

### Example: Good Code Pattern

```python
def execute_command(self, command: str, timeout: int = 30) -> str:
    """
    Execute ADB command safely.
    
    Args:
        command: Command to execute
        timeout: Timeout in seconds
        
    Returns:
        Command output
        
    Raises:
        ADBCommandError: If command fails
    """
    try:
        result = subprocess.run(
            ['adb', 'shell', command],  # Separate arguments
            capture_output=True,
            timeout=timeout,  # Always include timeout
            check=True
        )
        return result.stdout.decode('utf-8')
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out: {command}")
        raise ADBTimeoutError(f"Command timed out after {timeout}s") from e
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        raise ADBCommandError(f"Command failed: {e.stderr}") from e
```

## Testing

Currently, the project does not have a comprehensive test suite. We welcome contributions in this area!

If you add new functionality, consider adding tests:

```bash
# Run tests (when available)
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

## Commit Messages

Write clear, descriptive commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Example:
```
Fix command injection vulnerability in adb_wrapper

- Replace string interpolation with separate command arguments
- Add input validation for file paths
- Add comprehensive error handling

Fixes #123
```

## Documentation

- Update README.md if you add new features
- Add docstrings to new functions and classes
- Update examples if behavior changes
- Consider adding to docs/ folder for complex features

## Project Structure

```
DittoMation/
├── core/              # Core functionality (Android interface, config, logging)
├── recorder/          # Recording workflows (ADB, events, gestures)
├── replayer/          # Replaying workflows (locators, executors, NL)
├── docs/              # Technical documentation
└── tests/             # Test files (to be created)
```

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in the repository
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in release notes and the project README.

Thank you for contributing to DittoMation! 🎉
