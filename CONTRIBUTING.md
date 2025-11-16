# Contributing to Resume Chatbot Website

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other contributors

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Screenshots** if applicable

**Example:**
```
Title: Chat endpoint returns 500 error with special characters

Steps to reproduce:
1. Navigate to AI Assistant tab
2. Enter message with emoji: "What's your experience? 😊"
3. Click Send

Expected: Normal response from AI
Actual: 500 Internal Server Error

Environment:
- OS: Windows 11
- Python: 3.11.5
- Browser: Chrome 119
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear description** of the enhancement
- **Use case** - why is this needed?
- **Possible implementation** approach
- **Alternative solutions** considered

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```powershell
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation

4. **Test your changes**
   ```powershell
   pytest
   ```

5. **Commit with clear messages**
   ```powershell
   git commit -m "Add feature: amazing new capability"
   ```

6. **Push to your fork**
   ```powershell
   git push origin feature/amazing-feature
   ```

7. **Create Pull Request**
   - Use PR template if available
   - Reference related issues
   - Describe changes clearly

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use meaningful variable and function names

**Good:**
```python
def calculate_user_experience_years(experiences: List[Experience]) -> float:
    """Calculate total years of experience from experience list."""
    total_years = 0.0
    for exp in experiences:
        # Calculate duration...
    return total_years
```

**Bad:**
```python
def calc(e):
    t = 0
    for x in e:
        # ...
    return t
```

### Type Hints

Always use type hints:

```python
from typing import List, Optional

def process_skills(skills: List[Skill]) -> dict[str, List[str]]:
    """Group skills by category."""
    result: dict[str, List[str]] = {}
    # Implementation...
    return result
```

### Documentation

- Add docstrings to all functions, classes, and modules
- Use Google-style docstrings
- Keep README.md updated with new features

**Example:**
```python
def validate_resume_data(resume: Resume) -> bool:
    """
    Validate resume data completeness.
    
    Args:
        resume: Resume object to validate
        
    Returns:
        True if resume has all required fields, False otherwise
        
    Raises:
        ValidationError: If resume data is malformed
        
    Example:
        >>> resume = get_resume_data()
        >>> is_valid = validate_resume_data(resume)
    """
    # Implementation...
```

### Testing

#### Writing Tests

- Test file naming: `test_*.py`
- Test class naming: `Test*`
- Test function naming: `test_*`
- Aim for 80%+ code coverage

**Example:**
```python
class TestResumeValidation:
    """Tests for resume validation."""
    
    def test_valid_resume_passes(self):
        """Test that valid resume passes validation."""
        resume = Resume(
            name="Test User",
            title="Developer",
            summary="Summary",
            contact=ContactInfo()
        )
        assert validate_resume_data(resume) is True
    
    def test_invalid_resume_fails(self):
        """Test that invalid resume fails validation."""
        with pytest.raises(ValidationError):
            Resume(name="")  # Empty name should fail
```

#### Running Tests

```powershell
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_models.py::TestSkillModel::test_valid_skill
```

### Security

- Never commit sensitive data (API keys, passwords)
- Validate all user inputs
- Use parameterized queries if adding database
- Keep dependencies updated
- Report security issues privately

### Performance

- Optimize database queries (if applicable)
- Use async/await for I/O operations
- Cache expensive computations
- Profile before optimizing

## Project Structure

```
shreyansh-resume-chatbot-website/
├── main.py                 # FastAPI application
├── models.py               # Pydantic models
├── ollama_service.py       # AI service integration
├── resume_data.py          # Resume data
├── config.py               # Configuration
├── static/                 # Frontend files
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── tests/                  # Test suite
│   ├── test_models.py
│   ├── test_api.py
│   ├── test_ollama_service.py
│   └── test_resume_data.py
└── docs/                   # Documentation
```

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Test additions or changes
- **chore**: Build process or auxiliary tool changes

### Examples

```
feat(chat): add support for voice input

- Implemented Web Speech API integration
- Added microphone permission handling
- Updated UI with voice button

Closes #123
```

```
fix(security): prevent prompt injection in chat

Fixed vulnerability where users could inject system prompts
by sanitizing input more thoroughly.

Fixes #456
```

## Branch Naming

- Feature: `feature/short-description`
- Bug fix: `fix/short-description`
- Documentation: `docs/short-description`
- Refactor: `refactor/short-description`

**Examples:**
- `feature/add-voice-chat`
- `fix/rate-limit-bypass`
- `docs/update-deployment-guide`

## Review Process

### For Contributors

- Be responsive to feedback
- Make requested changes promptly
- Keep PRs focused and small
- Update PR description if scope changes

### For Reviewers

- Review code thoroughly but kindly
- Provide specific, actionable feedback
- Approve when ready, request changes when needed
- Thank contributors for their work

## Getting Help

- **Documentation**: Check README.md, QUICKSTART.md
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to maintainers

## Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Thanked in the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Quick Checklist for PRs

- [ ] Code follows style guidelines
- [ ] Self-reviewed my code
- [ ] Commented complex code sections
- [ ] Updated documentation
- [ ] Added tests for new features
- [ ] All tests pass locally
- [ ] No merge conflicts
- [ ] PR description is clear

---

Thank you for contributing to Resume Chatbot Website! 🎉
