# Contributing to LLB (爱学伴)

Thank you for your interest in contributing to LLB! This document provides guidelines and information for contributors.

## 🌟 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful** and inclusive to all contributors
- **Be constructive** in discussions and feedback
- **Focus on the mission** of improving sexual health education
- **Maintain privacy** and security standards
- **Follow professional standards** appropriate for educational content

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.11+
- Node.js 18+
- Git
- Basic understanding of FastAPI and React
- Familiarity with AI/ML concepts (for AI-related contributions)

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/llb.git
   cd llb
   ```

2. **Run Setup**
   ```bash
   ./scripts/setup/setup_project.sh
   ```

3. **Verify Installation**
   ```bash
   make status
   make test
   ```

## 📋 Types of Contributions

We welcome various types of contributions:

### 🐛 Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Include relevant logs

### ✨ Feature Requests
- Use the feature request template
- Explain the use case
- Consider privacy implications
- Discuss implementation approach

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test improvements

### 📚 Documentation
- API documentation
- User guides
- Developer documentation
- Code comments
- README improvements

### 🌍 Localization
- Translation improvements
- Cultural context adaptations
- Language-specific features
- Regional compliance

## 🛠️ Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
# or
git checkout -b docs/documentation-update
```

### 2. Make Changes

Follow our coding standards:

#### Python (Backend)
- Follow PEP 8
- Use type hints
- Maximum line length: 80 characters
- Use descriptive variable names
- Add docstrings to functions and classes

#### TypeScript/JavaScript (Frontend)
- Follow ESLint configuration
- Use TypeScript for type safety
- Maximum line length: 80 characters
- Use camelCase for variables
- Use PascalCase for components

#### General Guidelines
- Maximum file length: 500 lines
- Write clean, readable code
- Add comments for complex logic
- Follow existing patterns

### 3. Testing

Ensure all tests pass:

```bash
# Run all tests
make test

# Run specific tests
make test-backend
make test-frontend
make test-ai

# Run linting
make lint

# Format code
make format
```

### 4. Commit Changes

Use conventional commit messages:

```bash
# Format: type(scope): description
git commit -m "feat(api): add voice processing endpoint"
git commit -m "fix(ui): resolve chat input validation"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(backend): add health check tests"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
git push origin your-branch-name
```

Create a Pull Request with:
- Clear title and description
- Reference related issues
- Include screenshots for UI changes
- List breaking changes
- Update documentation if needed

## 🧪 Testing Guidelines

### Backend Testing
- Write unit tests for all new functions
- Include integration tests for API endpoints
- Test error handling and edge cases
- Mock external dependencies
- Aim for >80% code coverage

### Frontend Testing
- Write component tests
- Test user interactions
- Include accessibility tests
- Test responsive design
- Mock API calls

### AI Testing
- Test model loading and inference
- Validate prompt engineering
- Test safety filters
- Verify multi-language support
- Test performance benchmarks

## 📖 Documentation Standards

### Code Documentation
- Add docstrings to all public functions
- Include parameter and return type information
- Provide usage examples
- Document complex algorithms

### API Documentation
- Use OpenAPI/Swagger annotations
- Include request/response examples
- Document error codes
- Provide authentication details

### User Documentation
- Write clear, step-by-step instructions
- Include screenshots and examples
- Consider different user skill levels
- Test documentation with real users

## 🔒 Security Guidelines

### Privacy Considerations
- Never log sensitive user data
- Ensure all processing remains local
- Validate all user inputs
- Follow data minimization principles

### Security Best Practices
- Use secure coding practices
- Validate and sanitize inputs
- Handle errors gracefully
- Keep dependencies updated
- Follow OWASP guidelines

### AI Safety
- Implement content filtering
- Test for bias and fairness
- Validate educational accuracy
- Ensure age-appropriate responses

## 🌍 Internationalization

### Adding New Languages
1. Add language code to configuration
2. Create translation files
3. Update language detection
4. Test cultural appropriateness
5. Validate with native speakers

### Cultural Considerations
- Respect cultural differences
- Adapt content for local contexts
- Consider legal and regulatory requirements
- Ensure inclusive language

## 📊 Performance Guidelines

### Backend Performance
- Optimize database queries
- Use async/await properly
- Implement caching where appropriate
- Monitor memory usage
- Profile critical paths

### Frontend Performance
- Optimize bundle size
- Use lazy loading
- Implement proper caching
- Optimize images and assets
- Monitor Core Web Vitals

### AI Performance
- Optimize model loading
- Implement efficient inference
- Use GPU acceleration when available
- Cache model outputs appropriately
- Monitor resource usage

## 🚀 Release Process

### Version Numbering
We follow Semantic Versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers bumped
- [ ] Security review completed
- [ ] Performance benchmarks run

## 🤝 Community

### Getting Help
- 💬 [GitHub Discussions](https://github.com/your-username/llb/discussions)
- 🐛 [GitHub Issues](https://github.com/your-username/llb/issues)
- 📧 Email: dev@llb-project.com

### Communication Channels
- Use GitHub for technical discussions
- Be respectful and professional
- Help other contributors
- Share knowledge and best practices

## 📝 License

By contributing to LLB, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- Annual contributor highlights

---

Thank you for contributing to LLB and helping improve sexual health education through technology! 🌟 