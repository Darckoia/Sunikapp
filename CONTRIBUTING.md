# Contributing to SUNIKFLOW

Thank you for your interest in contributing to SUNIKFLOW! We welcome contributions from the community.

## Code of Conduct

Please be respectful and constructive in your interactions with other contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Sunikapp.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Install development dependencies: `uv sync`
5. Make your changes
6. Test your changes
7. Push to your fork
8. Create a Pull Request

## Development Setup

```bash
# Install dependencies
uv sync

# Run the development server
python -m uvicorn backend.main:app --reload

# The app will be available at http://localhost:8000
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions
- Keep functions small and focused

## Testing

When adding new features, please include tests:

```bash
# Run tests (coming soon)
pytest
```

## Pull Request Process

1. Ensure your code follows the style guide
2. Update documentation as needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Provide a clear description of your changes
6. Link any related issues

## Reporting Issues

When reporting bugs, please include:

- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- System information (OS, Python version, etc.)

## Feature Requests

Feature requests are welcome! Please provide:

- A clear description of the feature
- Use cases and benefits
- Potential implementation ideas (optional)

## Questions?

Feel free to open an issue or discussion for any questions.

Thank you for contributing! 🎵
