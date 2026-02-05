# Contributing to ML-Scaler

Thank you for your interest in contributing to ML-Scaler! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

- Check if the issue already exists in the [issue tracker](../../issues)
- Use a clear and descriptive title
- Provide detailed steps to reproduce the issue
- Include relevant logs, error messages, and environment details

### Submitting Changes

1. **Fork the repository** and create your branch from `cli`
2. **Make your changes** with clear, descriptive commit messages
3. **Add tests** for any new functionality
4. **Ensure all tests pass** by running `pytest`
5. **Update documentation** if you're changing functionality
6. **Submit a pull request** with a clear description of changes

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/ML-Scaler.git
cd ML-Scaler

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .
pip install pytest pytest-cov

# Run tests
pytest
```

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when relevant

### Pull Request Process

1. Update the README.md with details of changes if applicable
2. Ensure your PR description clearly describes the problem and solution
3. Link any relevant issues in your PR description
4. Wait for review from maintainers
5. Address any feedback or requested changes

## Code of Conduct

Please note that this project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing!
