# Contributing to Meteora Pool Screening Bot

We love your input! We want to make contributing to this project as easy and transparent as possible.

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

---

## 🐛 Found a Bug?

Before creating bug reports, check the issue list as you might find out that you don't need to create one. When creating a bug report, include as many details as possible:

**How to Submit a (Good) Bug Report**

1. Use a clear and descriptive title
2. Describe the exact steps which reproduce the problem
3. Provide specific examples to demonstrate the steps
4. Describe the behavior you observed and what the problem was
5. Explain which behavior you expected to see instead and why
6. Include screenshots/logs if possible
7. Mention your environment (OS, Python version, etc.)

---

## 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**How to Submit a (Good) Enhancement Suggestion**

1. Use a clear and descriptive title
2. Provide a step-by-step description of the suggested enhancement
3. Provide specific examples to demonstrate the steps
4. Describe the current behavior and expected behavior
5. Explain why this enhancement would be useful

---

## 🔧 Pull Requests

- Follow the PEP 8 code style
- Add tests for new functionality
- Update documentation
- End all files with a newline character

### Pull Request Process

1. Fork the repository
2. Create a branch with a descriptive name (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `pytest`
5. Format code: `black .`
6. Check style: `flake8 .`
7. Commit with clear messages: `git commit -m 'Add amazing feature'`
8. Push to the branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

---

## 🎨 Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/meteora-pool-bot.git
cd meteora-pool-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Check style
flake8 .
```

---

## 📝 Code Style

We use PEP 8 with Black formatting. Key points:

- Maximum line length: 88 characters
- 4 spaces for indentation
- Use type hints where possible
- Write docstrings for all public functions

Example:

```python
def analyze_pool(self, pool: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a pool and return score/analysis.
    
    Args:
        pool: Pool data dictionary
        
    Returns:
        Analysis result with score
    """
    analysis = {}
    # ... implementation
    return analysis
```

---

## ✅ Testing

Write tests for new features:

```python
# tests/test_pool_analyzer.py
import pytest
from pool_analyzer import PoolAnalyzer

def test_liquidity_check():
    """Test liquidity checking logic"""
    analyzer = PoolAnalyzer(config)
    result = analyzer._check_liquidity({
        'liquidity_usd': 50000
    })
    assert result['passed'] == True
    assert result['score'] == 25
```

Run tests:
```bash
pytest                    # Run all tests
pytest tests/test_file.py # Run specific file
pytest -v               # Verbose output
pytest --cov           # With coverage report
```

---

## 📚 Documentation

- Update README.md if changing user-facing functionality
- Update .env.example if adding new configuration options
- Add docstrings to new functions/classes
- Update WORKFLOW.md if changing core logic

---

## 🏷️ Commit Messages

Use clear, descriptive commit messages:

```
✓ Good:
  - "Add pool age filtering logic"
  - "Fix Telegram rate limit handling"
  - "Update API documentation"

✗ Avoid:
  - "fix bug"
  - "update stuff"
  - "WIP"
```

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

---

## 🚀 Release Process

Releases follow semantic versioning (v1.0.0):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

---

## 📞 Questions?

Feel free to open an issue with the `question` label.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under its MIT License.

---

## 🙏 Thank You!

Your contributions make this project better for everyone!
