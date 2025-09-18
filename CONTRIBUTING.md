# Contributing to GTR-Bench

Thank you for your interest in contributing to GTR-Bench! This document provides guidelines for contributors.

## 🤝 How to Contribute

### Getting Started
1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GTR-Bench.git
   cd GTR-Bench
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/X-Luffy/GTR-Bench.git
   ```

### Development Workflow
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** and test thoroughly
3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```
4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request** on GitHub

## 📝 Code Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Commit Messages
Use clear, descriptive commit messages:
- `Add: new feature description`
- `Fix: bug description`
- `Update: what was updated`
- `Remove: what was removed`
- `Refactor: what was refactored`

### Testing
- Test your changes thoroughly
- Ensure the application runs without errors
- Test with sample data if possible

## 🐛 Reporting Issues

When reporting issues, please include:
1. **Clear description** of the problem
2. **Steps to reproduce** the issue
3. **Expected vs actual behavior**
4. **System information** (OS, Python version, etc.)
5. **Screenshots** if applicable

## 🔄 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated if needed
- [ ] No merge conflicts

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
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏗️ Project Structure

```
GTR-Bench/
├── app.py                 # Main Streamlit application
├── utils/                 # Utility modules
├── components/            # UI components
├── data/                  # Assessment data
├── scripts/               # Utility scripts
└── docs/                  # Documentation
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
- [ ] Multi-language support

## 📞 Getting Help

- Open an issue for questions
- Check existing issues and discussions
- Review documentation and examples

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to GTR-Bench! 🎉
