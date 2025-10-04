# Contributing to MultiProdigy

Thank you for your interest in contributing to MultiProdigy! We welcome contributions from developers of all skill levels. This guide will help you get started and ensure your contributions are successful.

## Table of Contents

- [Getting Started](#getting-started)
- [Contribution Levels](#contribution-levels)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)
- [Recognition](#recognition)

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of multi-agent systems (helpful but not required)

### Quick Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/Abhay-Cerberus/MultiProdigy.git
   cd MultiProdigy
   ```

2. **Set up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pytest black isort flake8 mypy pre-commit
   ```

3. **Set up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

4. **Verify Setup**
   ```bash
   python -m pytest tests/ -v
   ```

## Contribution Levels

We welcome contributors at all levels! Here's how to find issues that match your experience:

### 🌟 Beginner (Good First Issues)
- **Labels**: `good first issue`, `beginner-friendly`
- **Time**: 1-4 hours
- **Skills**: Basic Python, willingness to learn
- **Examples**: Documentation fixes, simple bug fixes, adding tests

### 🔧 Intermediate
- **Labels**: `help wanted`, `intermediate`
- **Time**: 4-12 hours
- **Skills**: Python, understanding of async programming, testing
- **Examples**: Feature implementations, refactoring, integration work

### 🚀 Advanced
- **Labels**: `advanced`, `architecture`
- **Time**: 1-4 weeks
- **Skills**: Advanced Python, system design, performance optimization
- **Examples**: Major features, architectural changes, performance improvements

## Development Setup

### Environment Configuration

1. **Copy Configuration Files**
   ```bash
   cp .env.example .env
   cp config.yaml.example config.yaml
   ```

2. **Configure API Keys** (Optional for basic development)
   ```bash
   # Edit .env file with your API keys
   OPENAI_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   ```

3. **Set Python Path**
   ```bash
   # Linux/Mac
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   
   # Windows PowerShell
   $env:PYTHONPATH = "$(pwd);$env:PYTHONPATH"
   ```

### Development Tools

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

Run all checks:
```bash
# Format code
black .
isort .

# Check code quality
flake8 .
mypy MultiProdigy/

# Run tests
pytest tests/ -v
```

## Contribution Workflow

### Branching Strategy

| Branch Type | Purpose | Example |
|-------------|---------|---------|
| `main` | Stable, production-ready code | - |
| `develop` | Integration branch for features | - |
| `feature/*` | New features | `feature/multimodal-agents` |
| `fix/*` | Bug fixes | `fix/memory-leak-agents` |
| `docs/*` | Documentation updates | `docs/api-reference` |
| `refactor/*` | Code refactoring | `refactor/agent-architecture` |

### Step-by-Step Process

1. **Find or Create an Issue**
   - Browse [existing issues](https://github.com/Abhay-Cerberus/MultiProdigy/issues)
   - Use appropriate issue templates
   - Comment on issues you want to work on

2. **Create a Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write code following our standards
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Run full test suite
   pytest tests/ -v
   
   # Run specific tests
   pytest tests/test_agents.py -v
   
   # Check coverage
   pytest --cov=MultiProdigy tests/
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add multimodal agent support"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Standards

### Python Style Guide

We follow PEP 8 with some specific conventions:

```python
# Good: Clear, descriptive names
class MultimodalAgent(BaseAgent):
    def process_message(self, message: MultimodalMessage) -> AgentResponse:
        """Process a multimodal message and return response."""
        pass

# Good: Type hints
async def send_message(
    self, 
    recipient: str, 
    content: Union[str, MultimodalContent]
) -> bool:
    """Send message to recipient."""
    pass

# Good: Docstrings
def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Similarity score between 0.0 and 1.0
        
    Raises:
        ValueError: If either text is empty
    """
    pass
```

### Architecture Principles

1. **Modularity**: Keep components loosely coupled
2. **Async-First**: Use async/await for I/O operations
3. **Type Safety**: Use type hints throughout
4. **Error Handling**: Graceful error handling and recovery
5. **Observability**: Include logging and metrics

### File Organization

```
MultiProdigy/
├── agents/          # Agent implementations
├── llm/            # LLM integrations
├── observability/  # Monitoring and logging
├── utils/          # Utility functions
└── schemas/        # Data models and schemas
```

## Testing Guidelines

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from MultiProdigy.agents import BaseAgent

class TestBaseAgent:
    """Test suite for BaseAgent class."""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent instance."""
        return BaseAgent(name="test_agent", bus=Mock())
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.name == "test_agent"
        assert agent.bus is not None
    
    @pytest.mark.asyncio
    async def test_message_processing(self, agent):
        """Test agent can process messages."""
        message = Mock()
        response = await agent.process_message(message)
        assert response is not None
```

### Test Categories

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test performance characteristics

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_agents.py

# Specific test
pytest tests/test_agents.py::TestBaseAgent::test_initialization

# With coverage
pytest --cov=MultiProdigy --cov-report=html

# Performance tests
pytest tests/performance/ -v
```

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings and comments
2. **API Documentation**: Auto-generated from docstrings
3. **User Guides**: How-to guides and tutorials
4. **Architecture Documentation**: System design and patterns

### Writing Guidelines

- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting

### Documentation Structure

```
docs/
├── getting_started.md    # Quick start guide
├── architecture.md       # System architecture
├── api/                 # API documentation
├── tutorials/           # Step-by-step guides
└── examples/            # Code examples
```

## Issue Guidelines

### Before Creating an Issue

1. **Search Existing Issues**: Check if the issue already exists
2. **Check Documentation**: Ensure it's not a documentation issue
3. **Reproduce the Problem**: For bugs, provide reproduction steps
4. **Choose the Right Template**: Use appropriate issue template

### Issue Templates

- **Bug Report**: For reporting bugs
- **Feature Request**: For suggesting new features
- **Good First Issue**: For beginner-friendly tasks
- **Documentation**: For documentation issues
- **Question**: For asking questions

### Writing Good Issues

```markdown
## Clear Title
Use descriptive titles like "Agent fails to process multimodal messages"

## Detailed Description
Provide context and explain the problem or feature request clearly.

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. Expected vs actual behavior

## Environment Information
- OS: Ubuntu 22.04
- Python: 3.11.5
- MultiProdigy: 1.2.3
```

## Pull Request Process

### PR Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow conventional commits
- [ ] PR description explains changes
- [ ] Related issue linked

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

### Review Process

1. **Automated Checks**: CI/CD runs automatically
2. **Code Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: Get approval from maintainers
5. **Merge**: Maintainers merge approved PRs

## Community Guidelines

### Code of Conduct

We follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please read and follow it.

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions and reviews

### Getting Help

- **Documentation**: Check our [comprehensive docs](docs/README.md)
- **Issues**: Search [existing issues](https://github.com/Abhay-Cerberus/MultiProdigy/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/Abhay-Cerberus/MultiProdigy/discussions)
- **Contribution System**: See [automated workflows](docs/community/contribution_system.md)

## Recognition

We value all contributions! Contributors are recognized through:

- **Contributors List**: Listed in README.md
- **Release Notes**: Contributions mentioned in releases
- **GitHub Profile**: Contributions show on your GitHub profile
- **Community Recognition**: Highlighted in community updates

### Contribution Types

We recognize various types of contributions:

- 💻 Code contributions
- 📖 Documentation improvements
- 🐛 Bug reports and testing
- 💡 Ideas and feature suggestions
- 🎨 Design and UX improvements
- 🌍 Translations and localization
- 📢 Community building and outreach

## Getting Started Checklist

Ready to contribute? Here's your checklist:

- [ ] Read this contributing guide
- [ ] Set up development environment
- [ ] Run tests to verify setup
- [ ] Find a good first issue
- [ ] Comment on the issue to claim it
- [ ] Create a branch and start coding
- [ ] Submit your first PR

## Questions?

If you have questions about contributing:

1. Check our [comprehensive documentation](docs/README.md)
2. Search [existing issues](https://github.com/Abhay-Cerberus/MultiProdigy/issues)
3. Ask in [GitHub Discussions](https://github.com/Abhay-Cerberus/MultiProdigy/discussions)
4. Read our [contribution system guide](docs/community/contribution_system.md)

Thank you for contributing to MultiProdigy! Your contributions help make this project better for everyone. 🚀

