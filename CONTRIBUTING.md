# Contributing to LLB

## Welcome Contributors! 🎉

Thank you for your interest in contributing to LLB (爱学伴). This guide will help you get started with contributing to our AI-driven sexual health education system.

## Code of Conduct

This project is committed to providing a safe, inclusive, and respectful environment for all contributors. We expect all participants to adhere to our code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Respect privacy and confidentiality
- Maintain professionalism in all interactions

## Getting Started

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/LLB.git
   cd LLB
   ```

2. **Set up the development environment:**
   ```bash
   # Backend setup
   cd backend
   python3.11 -m venv llb-env
   source llb-env/bin/activate
   pip install -r requirements/dev.txt
   
   # Frontend setup
   cd ../frontend
   npm install
   ```

3. **Run tests to ensure everything works:**
   ```bash
   make test
   ```

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes:**
   ```bash
   make test
   make test-coverage
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

5. **Push and create a Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8 with Black formatting
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings
- **Testing**: Minimum 70% code coverage required

```python
def process_user_input(text: str, language: str = "en") -> dict:
    """Process user input for AI analysis.
    
    Args:
        text: The input text to process
        language: Language code (default: "en")
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If text is empty or invalid
    """
    pass
```

### TypeScript (Frontend)

- **Style**: Use Prettier for formatting
- **Types**: Prefer interfaces over types
- **Components**: Use functional components with hooks
- **Testing**: Test all components and hooks

```typescript
interface UserProfile {
  id: number;
  email: string;
  username: string;
  role: UserRole;
}

const UserProfileComponent: React.FC<{ user: UserProfile }> = ({ user }) => {
  // Component implementation
};
```

### Commit Messages

Use conventional commits format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks

## Testing Guidelines

### Backend Testing

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test service interactions
- **API Tests**: Test endpoint functionality

```python
def test_ai_service_classification():
    """Test AI service text classification."""
    service = AIService()
    result = service.classify_text("test input", ["category1", "category2"])
    assert result["category"] in ["category1", "category2"]
    assert 0 <= result["confidence"] <= 1
```

### Frontend Testing

- **Component Tests**: Test React components
- **Hook Tests**: Test custom hooks
- **Integration Tests**: Test user workflows

```typescript
describe('ChatComponent', () => {
  it('should send message when form is submitted', async () => {
    render(<ChatComponent />);
    const input = screen.getByPlaceholderText('Type your message...');
    const button = screen.getByRole('button', { name: 'Send' });
    
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument();
    });
  });
});
```

## Documentation

### Code Documentation

- Document all public APIs
- Include usage examples
- Explain complex algorithms
- Update README for new features

### API Documentation

- Update OpenAPI schema for new endpoints
- Include request/response examples
- Document error codes and messages

## Security Guidelines

### Sensitive Content

- Never commit API keys or secrets
- Use environment variables for configuration
- Sanitize all user inputs
- Implement proper authentication checks

### Content Safety

- Ensure all AI responses are appropriate
- Implement content filtering
- Respect cultural sensitivities
- Maintain educational focus

## Performance Guidelines

### Backend Performance

- Use async/await for I/O operations
- Implement proper caching strategies
- Optimize database queries
- Monitor memory usage

### Frontend Performance

- Implement code splitting
- Optimize bundle size
- Use React.memo for expensive components
- Implement proper loading states

## Accessibility

- Follow WCAG 2.1 AA guidelines
- Ensure keyboard navigation works
- Provide proper ARIA labels
- Test with screen readers

## Internationalization

- Use i18next for translations
- Support RTL languages
- Consider cultural differences
- Test with different locales

## Pull Request Process

1. **Before submitting:**
   - Ensure all tests pass
   - Update documentation
   - Add changelog entry
   - Rebase on latest main

2. **PR Description:**
   - Describe what changes were made
   - Explain why the changes were necessary
   - Include screenshots for UI changes
   - Reference related issues

3. **Review Process:**
   - Address reviewer feedback
   - Keep discussions constructive
   - Be open to suggestions
   - Update PR as needed

## Issue Reporting

### Bug Reports

Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs
- Screenshots if applicable

### Feature Requests

Include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Mockups or examples if applicable

## Community

### Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in discussions
- Join our community channels

### Helping Others

- Answer questions in issues
- Review pull requests
- Improve documentation
- Share your experience

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Project documentation
- Community highlights

Thank you for contributing to LLB! Together, we're building a better, more accessible sexual health education system. 🚀