# Contributing to Human-Level Visual Reasoning Assessment System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or request features
- Provide detailed information about the issue, including:
  - Steps to reproduce
  - Expected vs. actual behavior
  - System information (OS, Python version, etc.)
  - Screenshots if applicable

### Suggesting Enhancements
- Use the GitHub issue tracker with the "enhancement" label
- Clearly describe the proposed feature
- Explain the use case and benefits
- Consider implementation complexity

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- pip or conda

### Setup Steps
1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/human-level-assessment.git
   cd human-level-assessment
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🧪 Testing

### Running Tests
```bash
pytest tests/
```

### Code Quality
- Run linting: `flake8 .`
- Format code: `black .`
- Type checking: `mypy .`

## 📝 Code Style Guidelines

### Python Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Streamlit Best Practices
- Use session state for maintaining application state
- Implement proper error handling
- Optimize for performance (cache expensive operations)
- Ensure responsive design

### Documentation
- Update README.md for significant changes
- Add docstrings for new functions/classes
- Include examples for new features

## 🏗️ Project Structure

```
human_level/
├── app.py                 # Main application
├── utils/                 # Utility modules
├── components/            # UI components
├── data/                  # Assessment data
├── tests/                 # Test files
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Add unit tests for core functionality
- [ ] Improve error handling and user feedback
- [ ] Add support for more video formats
- [ ] Implement data validation
- [ ] Add accessibility features

### Medium Priority
- [ ] Performance optimizations
- [ ] Additional scoring algorithms
- [ ] Export to more formats (JSON, Excel)
- [ ] Batch processing capabilities
- [ ] Configuration management

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional visualization options
- [ ] Plugin system for custom tasks
- [ ] Multi-language support

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**:
   - Operating System
   - Python version
   - Package versions (from `pip list`)

2. **Steps to Reproduce**:
   - Clear, numbered steps
   - Sample data if applicable

3. **Expected vs. Actual Behavior**:
   - What you expected to happen
   - What actually happened

4. **Additional Context**:
   - Screenshots or error messages
   - Relevant log output

## 💡 Feature Requests

When suggesting features, please include:

1. **Problem Description**:
   - What problem does this solve?
   - Who would benefit from this feature?

2. **Proposed Solution**:
   - How should this feature work?
   - Any design considerations?

3. **Alternatives Considered**:
   - Other ways to solve this problem
   - Why this approach is preferred

## 📄 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🏷️ Release Process

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release tag
4. Update documentation

## 📞 Getting Help

- Open an issue for questions
- Check existing issues and discussions
- Review documentation and examples

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to this project! 🎉
