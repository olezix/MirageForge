# Contributing to MirageForge

Thank you for your interest in contributing to MirageForge! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct (see CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs
1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Screenshots if applicable

### Suggesting Features
1. Check existing issues and discussions
2. Use the feature request template
3. Explain the use case
4. Describe proposed solution
5. Consider alternatives

### Submitting Code
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Follow code style guidelines
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mirageforge.git
cd mirageforge

# Install dependencies
make setup

# Run tests
make test

# Run linters
make lint
```

## Code Style

- Use type hints for all functions
- Write docstrings for public functions
- Follow PEP 8 (enforced by ruff)
- Maximum line length: 100 characters
- Use descriptive variable names

## Testing

- Write unit tests for new functions
- Write integration tests for new features
- Ensure all tests pass before submitting
- Aim for reasonable coverage (not 100%)

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update docs/ for new features
- Keep documentation accurate and honest

## Pull Request Process

1. Update documentation
2. Add tests
3. Ensure CI passes
4. Request review
5. Address feedback
6. Merge when approved

## Ethical Considerations

- Respect participant privacy
- Follow ethical guidelines
- Be transparent about limitations
- Never overclaim results
- Mark synthetic data clearly

## Questions?

Open an issue or discussion on GitHub.

---

Thank you for contributing!
