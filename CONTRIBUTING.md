# Contributing to Paper Collector

Thank you for your interest in contributing to Paper Collector! This document provides guidelines for contributing to the project.

## Code of Conduct

This is an academic project built on principles of scientific rigor and collaboration. We expect all contributors to:

- Prioritize correctness and reproducibility over speed
- Provide clear documentation and justification for design decisions
- Write tests for new functionality
- Follow the existing code style and conventions

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/Paper-collector.git`
3. Install dependencies: `poetry install`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

Examples:
```
feat: add SPECTER2 embedding integration
fix: correct section boundary detection in parser
docs: update API documentation for Paper model
test: add integration tests for PDF ingestion
```

## Pull Request Process

1. Ensure all tests pass: `poetry run pytest`
2. Update documentation if needed
3. Write clear PR description explaining the changes
4. Reference any related issues

## Testing

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use mocking for external dependencies
- Test edge cases and error conditions

## Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Format code with Black: `poetry run black src/`
- Lint with Ruff: `poetry run ruff check src/`

## Questions?

Open an issue for discussion before starting major changes.
