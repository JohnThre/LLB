# LLB - 爱学伴 (AI Sexual Health Education)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

A privacy-first, local AI-driven sexual health education system powered by a configurable health-tuned model based on Google Gemma 4. Answers are limited to English and Simplified Chinese and are backed by reviewable literature.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (optional, SQLite for development)
- Redis 7+ (optional, in-memory cache for development)

### Installation

1. **Clone and setup environment:**
   ```bash
   git clone <repository>
   cd LLB
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Install dependencies:**
   ```bash
   # Backend
   cd backend
   python3.11 -m venv llb-env
   source llb-env/bin/activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

   **Apple Silicon (M1/M2/M3/M4) Users:**
   ```bash
   cd backend && ./setup_whisper.sh
   cd ../frontend && npm install
   ```

3. **Start development servers:**
   ```bash
   make dev
   ```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Alternative Docs**: http://localhost:8000/redoc

## ✨ Features

- 🔒 **Privacy-First**: Local AI processing, no data leaves your system
- 🌍 **Supported Languages**: English and Simplified Chinese
- 📚 **Source-Backed Answers**: Inline citations and a literature review workflow
- 🎤 **Voice Input**: Speech recognition with Whisper
- 📄 **Document Analysis**: PDF processing and knowledge extraction
- 🎨 **Modern UI**: Bauhaus-inspired design system
- 🔐 **Secure**: JWT authentication, role-based access control
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 🧪 **Well-Tested**: Comprehensive test coverage (>70%)

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
- `make test-desktop` - Run Electron helper and release-signing tests
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

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - System architecture and design
- [API Documentation](docs/API.md) - REST API reference
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Contributing Guide](CONTRIBUTING.md) - Development guidelines

## 🛠 Technology Stack

### Frontend
- **React 18** with TypeScript
- **Material-UI (MUI)** for components
- **Redux Toolkit** for state management
- **Vite** for build tooling
- **Vitest** for testing

### Backend
- **FastAPI** with Python 3.11+
- **PostgreSQL** with SQLAlchemy ORM
- **Redis** for caching and sessions
- **JWT** for authentication
- **Pytest** for testing

### AI & ML
- **Google Gemma 4 health-tuned model** (configurable local artifact)
- **OpenAI Whisper** for speech recognition
- **Transformers** library
- **PyTorch** for model inference

## 🚢 Deployment

### Docker (Recommended)
```bash
# Production deployment
docker-compose up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up
```

### Manual Deployment
```bash
# Build frontend
cd frontend && npm run build

# Start backend
cd ../backend && source llb-env/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔧 Configuration

### Environment Variables
```bash
# Database (optional for development)
DATABASE_URL=postgresql://user:pass@localhost:5432/llb_db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret

# AI Providers (optional)
AI_PROVIDER_ORDER=ollama,github,openai,anthropic,gemini,mistral
GITHUB_MODELS_TOKEN=github_pat_with_models_read
GITHUB_MODELS_MODELS=openai/gpt-5.2
GITHUB_MODELS_API_VERSION=2026-03-10
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.2
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-opus-4-7
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-3-pro-preview
MISTRAL_API_KEY=...
MISTRAL_MODEL=mistral-medium-3.5
OLLAMA_ENABLED=false
OLLAMA_MODEL=llama3.2
```

Provider fallback is free-first by default: Ollama/local models, GitHub Models,
then direct OpenAI, Anthropic, Gemini, and Mistral API keys. GitHub Models requires a
GitHub token with `models:read` permission and uses GitHub's free, rate-limited
Models API for prototyping. See GitHub's Models REST API docs:
https://docs.github.com/en/rest/models/inference.

### Desktop Packaging

The Electron desktop scaffold lives in `desktop/`. It is designed to start the
FastAPI backend as an internal local process so users do not manage a separate
server.

Release artifacts must be signed with detached GPG signatures:

```bash
scripts/sign_release_artifacts.sh desktop/dist
```

macOS release builds should also use Apple Developer ID signing and
notarization through `electron-builder` credentials supplied outside the repo.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `make test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google for the Gemma model family
- OpenAI for Whisper speech recognition
- The open-source community for the amazing tools and libraries

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Last Updated**: September 2, 2025  
**Version**: 0.1.0  
**Status**: Active Development
