# Contributing to AAW Master Chatbot

Thank you for your interest in contributing to AAW Master Chatbot! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/ketsar28/aaw-chatbot-with-python/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with the `enhancement` label
3. Describe the feature, its benefits, and potential implementation

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following our coding standards
4. Write tests for new functionality
5. Ensure all tests pass: `pytest`
6. Update documentation if needed
7. Commit with clear messages: `git commit -m "Add feature: description"`
8. Push to your fork: `git push origin feature/your-feature-name`
9. Create a Pull Request with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/aaw-chatbot-with-python.git
cd aaw-chatbot-with-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install black isort flake8 mypy pytest pytest-cov

# Run tests
pytest
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use Black for formatting: `black src/ tests/`
- Use isort for imports: `isort src/ tests/`
- Maximum line length: 100 characters

### Type Hints

- Add type hints to all functions
- Use Pydantic for data validation

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update README.md for user-facing changes

### Testing

- Write unit tests for all new functionality
- Maintain >80% code coverage
- Test edge cases and error handling

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Reference issues: "Fix #123: Description"

Example:
```
Add support for custom system prompts

- Add system_prompt field to settings
- Update UI to allow editing system prompt
- Add tests for custom prompts

Fixes #45
```

## Questions?

Feel free to ask questions in [GitHub Discussions](https://github.com/ketsar28/aaw-chatbot-with-python/discussions).

Thank you for contributing!
