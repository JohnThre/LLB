# LLB - AI Sexual Health Education

## Setup

1. Get API keys from at least one provider:
   - OpenAI: https://platform.openai.com/api-keys
   - Claude: https://console.anthropic.com/
   - Gemini: https://makersuite.google.com/app/apikey
   - Ollama: https://ollama.ai/ (local)

2. Install dependencies:
   ```bash
   cd backend && python3.11 -m venv llb-env && source llb-env/bin/activate && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

   **Apple Silicon (M1/M2/M3) Users:**
   ```bash
   # Use the optimized setup script for Apple Silicon
   cd backend && ./setup_whisper.sh
   cd ../frontend && npm install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Start:
   ```bash
   make dev
   ```

## Usage

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

## Commands

### Development
- `make dev` - Start development servers
- `make dev-arm64` - Start development on Apple Silicon

### Testing
- `make test` - Run comprehensive test suite
- `make test-backend` - Run backend tests only
- `make test-frontend` - Run frontend tests only
- `make test-watch` - Run tests in watch mode
- `make test-coverage` - Generate coverage reports
- `./scripts/run_tests.sh` - Run full test suite with detailed output

### Building
- `make build` - Build for production
- `make build-arm64` - Build for Apple Silicon (ARM64)
- `make clean` - Clean build artifacts

## Testing

The project includes comprehensive test coverage:

### Backend Tests
- **Unit Tests**: Service layer, API endpoints, core functionality
- **Integration Tests**: Full workflow testing
- **Coverage**: Minimum 70% code coverage required
- **Location**: `backend/tests/`

### Frontend Tests
- **Component Tests**: React component testing with React Testing Library
- **Hook Tests**: Custom hook testing
- **Store Tests**: Redux slice testing
- **Service Tests**: API service testing
- **Location**: `frontend/src/test/`

### Running Tests

```bash
# Run all tests
make test

# Run with coverage reports
make test-coverage

# Run backend tests only
cd backend && source llb-env/bin/activate && pytest tests/ -v

# Run frontend tests only
cd frontend && npm test

# Watch mode for development
make test-watch
```

### Coverage Reports
After running tests with coverage:
- Backend: `backend/htmlcov/index.html`
- Frontend: `frontend/coverage/index.html`