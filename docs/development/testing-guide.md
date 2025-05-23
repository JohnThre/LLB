# Testing Guide for LLB (爱学伴)

This guide covers the comprehensive testing infrastructure for LLB, including unit tests, integration tests, end-to-end tests, and performance testing.

## 📋 Testing Overview

LLB uses a multi-layered testing approach:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Test system performance and scalability
- **AI Model Tests**: Test AI functionality and accuracy

## 🏗️ Testing Infrastructure

### Backend Testing (Python)

**Framework**: pytest with additional plugins
- `pytest`: Core testing framework
- `pytest-asyncio`: Async test support
- `pytest-cov`: Code coverage
- `pytest-mock`: Mocking utilities
- `httpx`: HTTP client for API testing
- `factory-boy`: Test data factories

**Configuration**: `backend/pytest.ini`
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=app
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
```

### Frontend Testing (TypeScript/React)

**Framework**: Vitest with React Testing Library
- `vitest`: Fast test runner
- `@testing-library/react`: React component testing
- `@testing-library/jest-dom`: DOM matchers
- `jsdom`: DOM environment for tests

**Configuration**: `frontend/vitest.config.ts`
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/coverage/**'
      ]
    }
  },
})
```

### AI Module Testing (Python)

**Framework**: pytest with AI-specific fixtures
- Model loading tests
- Response quality tests
- Performance benchmarks
- Multilingual capability tests

## 🚀 Running Tests

### Quick Commands

```bash
# Run all tests
make test

# Run specific test suites
make test-backend     # Backend tests only
make test-frontend    # Frontend tests only
make test-ai          # AI module tests only

# Generate coverage reports
make coverage

# Run tests with specific markers
make test-unit        # Unit tests only
make test-integration # Integration tests only
make test-e2e         # End-to-end tests only
```

### Detailed Commands

#### Backend Tests
```bash
cd backend
source llb-env/bin/activate

# Run all backend tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/unit/test_health.py

# Run tests with specific marker
python -m pytest -m unit
python -m pytest -m integration

# Run tests in parallel
python -m pytest -n auto

# Run tests with verbose output
python -m pytest -v --tb=long
```

#### Frontend Tests
```bash
cd frontend

# Run all frontend tests
yarn test

# Run with coverage
yarn test --coverage

# Run specific test file
yarn test src/components/common/Button.test.tsx

# Run tests in watch mode
yarn test --watch

# Run tests with UI
yarn test --ui
```

#### AI Module Tests
```bash
cd ai

# Run all AI tests
python -m pytest tests/

# Run specific AI test categories
python -m pytest tests/test_gemma_integration.py
python -m pytest tests/test_whisper_integration.py
python -m pytest tests/test_multilingual.py

# Run performance benchmarks
python -m pytest tests/test_performance.py -m slow
```

## 📝 Writing Tests

### Backend Unit Tests

**Example**: Testing a service function
```python
# tests/unit/test_chat_service.py
import pytest
from app.services.chat_service import ChatService
from app.models.chat import ChatRequest, ChatResponse

class TestChatService:
    def test_process_message_basic(self):
        """Test basic message processing."""
        service = ChatService()
        request = ChatRequest(
            message="What is sexual health?",
            language="en"
        )
        
        response = service.process_message(request)
        
        assert isinstance(response, ChatResponse)
        assert response.message is not None
        assert response.language == "en"
        assert len(response.message) > 0

    def test_process_message_chinese(self):
        """Test Chinese message processing."""
        service = ChatService()
        request = ChatRequest(
            message="什么是性健康？",
            language="zh-CN"
        )
        
        response = service.process_message(request)
        
        assert response.language in ["zh-CN", "zh"]
        assert response.message is not None

    @pytest.mark.asyncio
    async def test_process_message_async(self):
        """Test async message processing."""
        service = ChatService()
        request = ChatRequest(
            message="Tell me about contraception",
            language="en"
        )
        
        response = await service.process_message_async(request)
        
        assert response is not None
        assert "contraception" in response.message.lower()
```

### Backend Integration Tests

**Example**: Testing API endpoints
```python
# tests/integration/test_chat_api.py
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestChatAPI:
    def test_chat_endpoint_basic(self, client: TestClient):
        """Test basic chat endpoint functionality."""
        payload = {
            "message": "What is sexual health?",
            "language": "en",
            "cultural_context": "western"
        }
        
        response = client.post("/api/v1/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "language_detected" in data
        assert data["language_detected"] == "en"

    def test_chat_endpoint_multilingual(self, client: TestClient):
        """Test multilingual support."""
        test_cases = [
            {
                "message": "什么是性健康？",
                "expected_lang": "zh-CN"
            },
            {
                "message": "What is contraception?",
                "expected_lang": "en"
            }
        ]
        
        for case in test_cases:
            response = client.post("/api/v1/chat", json={
                "message": case["message"]
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["language_detected"] in [case["expected_lang"], case["expected_lang"][:2]]

    def test_chat_endpoint_validation(self, client: TestClient):
        """Test input validation."""
        # Test empty message
        response = client.post("/api/v1/chat", json={"message": ""})
        assert response.status_code == 422
        
        # Test missing message
        response = client.post("/api/v1/chat", json={})
        assert response.status_code == 422
        
        # Test invalid language
        response = client.post("/api/v1/chat", json={
            "message": "test",
            "language": "invalid"
        })
        assert response.status_code == 422
```

### Frontend Component Tests

**Example**: Testing React components
```typescript
// src/components/common/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import Button from './Button'

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveTextContent('Click me')
  })

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('applies custom className', () => {
    render(<Button className="custom-class">Button</Button>)
    expect(screen.getByRole('button')).toHaveClass('custom-class')
  })

  it('disables button when disabled prop is true', () => {
    render(<Button disabled>Disabled Button</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('shows loading state', () => {
    render(<Button loading>Loading Button</Button>)
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true')
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument()
  })
})
```

### Frontend Integration Tests

**Example**: Testing component interactions
```typescript
// src/components/chat/ChatInterface.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import ChatInterface from './ChatInterface'
import { ChatProvider } from '../../contexts/ChatContext'

// Mock API calls
vi.mock('../../services/api', () => ({
  sendMessage: vi.fn().mockResolvedValue({
    response: 'This is a test response',
    language_detected: 'en'
  })
}))

describe('ChatInterface Integration', () => {
  const renderWithProvider = (component: React.ReactElement) => {
    return render(
      <ChatProvider>
        {component}
      </ChatProvider>
    )
  }

  it('sends message and displays response', async () => {
    renderWithProvider(<ChatInterface />)
    
    const input = screen.getByPlaceholderText('Type your question...')
    const sendButton = screen.getByRole('button', { name: /send/i })
    
    fireEvent.change(input, { target: { value: 'What is sexual health?' } })
    fireEvent.click(sendButton)
    
    await waitFor(() => {
      expect(screen.getByText('This is a test response')).toBeInTheDocument()
    })
  })

  it('handles voice input', async () => {
    renderWithProvider(<ChatInterface />)
    
    const voiceButton = screen.getByRole('button', { name: /voice input/i })
    fireEvent.click(voiceButton)
    
    await waitFor(() => {
      expect(screen.getByText(/listening/i)).toBeInTheDocument()
    })
  })
})
```

### AI Module Tests

**Example**: Testing AI functionality
```python
# ai/tests/test_gemma_integration.py
import pytest
from ai.models.gemma_client import GemmaClient
from ai.models.prompt_engine import PromptEngine

class TestGemmaIntegration:
    @pytest.fixture
    def gemma_client(self):
        """Create Gemma client for testing."""
        return GemmaClient(model_path="ai/models/gemma3-keras-gemma3_1b-v3")

    @pytest.fixture
    def prompt_engine(self):
        """Create prompt engine for testing."""
        return PromptEngine()

    def test_model_loading(self, gemma_client):
        """Test that the model loads successfully."""
        assert gemma_client.is_loaded()
        assert gemma_client.model is not None

    def test_basic_generation(self, gemma_client):
        """Test basic text generation."""
        prompt = "What is sexual health education?"
        response = gemma_client.generate(prompt, max_tokens=100)
        
        assert response is not None
        assert len(response) > 0
        assert isinstance(response, str)

    def test_multilingual_support(self, gemma_client, prompt_engine):
        """Test multilingual capabilities."""
        test_cases = [
            {
                "input": "What is contraception?",
                "language": "en"
            },
            {
                "input": "什么是避孕？",
                "language": "zh-CN"
            }
        ]
        
        for case in test_cases:
            prompt = prompt_engine.format_prompt(
                case["input"], 
                language=case["language"]
            )
            response = gemma_client.generate(prompt)
            
            assert response is not None
            assert len(response) > 10  # Reasonable response length

    @pytest.mark.slow
    def test_response_quality(self, gemma_client, prompt_engine):
        """Test response quality for sexual health topics."""
        topics = [
            "sexual health education",
            "contraception methods",
            "STI prevention",
            "reproductive health"
        ]
        
        for topic in topics:
            prompt = prompt_engine.format_educational_prompt(topic)
            response = gemma_client.generate(prompt, max_tokens=200)
            
            # Check response quality
            assert len(response) > 50
            assert topic.lower() in response.lower()
            assert not any(inappropriate in response.lower() 
                          for inappropriate in ["explicit", "graphic"])

    def test_performance_benchmark(self, gemma_client):
        """Test response time performance."""
        import time
        
        prompt = "Explain the importance of sexual health education."
        
        start_time = time.time()
        response = gemma_client.generate(prompt, max_tokens=100)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response is not None
        assert response_time < 30  # Should respond within 30 seconds
```

## 📊 Test Coverage

### Coverage Requirements

- **Backend**: Minimum 80% code coverage
- **Frontend**: Minimum 75% code coverage
- **AI Modules**: Minimum 70% code coverage

### Viewing Coverage Reports

```bash
# Backend coverage
cd backend
python -m pytest --cov=app --cov-report=html
open htmlcov/index.html

# Frontend coverage
cd frontend
yarn test --coverage
open coverage/index.html
```

### Coverage Exclusions

Files excluded from coverage:
- Configuration files
- Migration scripts
- Test files themselves
- Third-party integrations
- Development utilities

## 🔄 Continuous Integration

### Pre-commit Hooks

Automatically run tests before commits:
```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running pre-commit tests..."

# Backend tests
cd backend
source llb-env/bin/activate
python -m pytest tests/ --tb=short -q
if [ $? -ne 0 ]; then
    echo "Backend tests failed. Commit aborted."
    exit 1
fi
cd ..

# Frontend tests
cd frontend
yarn test --run --reporter=basic
if [ $? -ne 0 ]; then
    echo "Frontend tests failed. Commit aborted."
    exit 1
fi
cd ..

echo "All tests passed. Proceeding with commit."
```

### GitHub Actions (Future)

Example workflow for CI/CD:
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          python -m venv llb-env
          source llb-env/bin/activate
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          source llb-env/bin/activate
          python -m pytest --cov=app

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          yarn install
      - name: Run tests
        run: |
          cd frontend
          yarn test --coverage
```

## 🐛 Debugging Tests

### Common Issues

1. **Test Database Issues**:
   ```bash
   # Reset test database
   rm backend/test.db
   python -m pytest tests/conftest.py::setup_test_db
   ```

2. **Frontend Test Environment**:
   ```bash
   # Clear test cache
   yarn test --clearCache
   
   # Update snapshots
   yarn test --updateSnapshot
   ```

3. **AI Model Tests Failing**:
   ```bash
   # Verify model is available
   python scripts/verify_model.py
   
   # Check GPU availability
   python -c "import torch; print(torch.cuda.is_available())"
   ```

### Test Debugging Tools

```bash
# Run single test with debugging
python -m pytest tests/unit/test_specific.py::test_function -v -s

# Run tests with pdb debugger
python -m pytest --pdb tests/unit/test_specific.py

# Run tests with coverage and open browser
python -m pytest --cov=app --cov-report=html && open htmlcov/index.html
```

## 📈 Performance Testing

### Load Testing

```python
# tests/performance/test_load.py
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def test_concurrent_requests():
    """Test API under concurrent load."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):
            task = session.post(
                'http://localhost:8000/api/v1/chat',
                json={'message': f'Test message {i}'}
            )
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Verify all requests succeeded
        for response in responses:
            assert response.status == 200
        
        total_time = end_time - start_time
        requests_per_second = len(tasks) / total_time
        
        print(f"Processed {len(tasks)} requests in {total_time:.2f}s")
        print(f"Rate: {requests_per_second:.2f} requests/second")
        
        assert requests_per_second > 10  # Minimum performance requirement
```

### Memory Testing

```python
# tests/performance/test_memory.py
import psutil
import os
from ai.models.gemma_client import GemmaClient

def test_memory_usage():
    """Test memory usage during AI operations."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Load model
    client = GemmaClient()
    after_load_memory = process.memory_info().rss / 1024 / 1024
    
    # Generate responses
    for i in range(10):
        response = client.generate(f"Test prompt {i}")
    
    final_memory = process.memory_info().rss / 1024 / 1024
    
    print(f"Initial memory: {initial_memory:.2f} MB")
    print(f"After model load: {after_load_memory:.2f} MB")
    print(f"Final memory: {final_memory:.2f} MB")
    
    # Memory should not grow excessively
    memory_growth = final_memory - after_load_memory
    assert memory_growth < 500  # Less than 500MB growth
```

## 🎯 Best Practices

### Test Organization

1. **Group related tests** in classes
2. **Use descriptive test names** that explain what is being tested
3. **Keep tests independent** - each test should be able to run alone
4. **Use fixtures** for common setup code
5. **Mock external dependencies** to isolate units under test

### Test Data Management

1. **Use factories** for creating test data
2. **Clean up after tests** to avoid side effects
3. **Use realistic test data** that represents actual usage
4. **Avoid hardcoded values** - use constants or configuration

### Performance Considerations

1. **Mark slow tests** with `@pytest.mark.slow`
2. **Run fast tests first** in development
3. **Use parallel execution** for independent tests
4. **Cache expensive operations** when possible

## 🆘 Getting Help

- **Test failures**: Check the test output and logs
- **Coverage issues**: Review the coverage report
- **Performance problems**: Use profiling tools
- **CI/CD issues**: Check the workflow logs
- **Documentation**: See the testing framework docs

---

*This guide is part of the LLB (爱学伴) documentation. For more information, see the main README.md file.* 