# LLB (爱学伴) - AI-Powered Sexual Health Education

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)

## Quick Start Guide

*This guide will help you set up and run LLB (爱学伴) on your computer with modern AI providers!*

### 📋 What You'll Need

Before starting, make sure your computer has:
- **Windows 11** with WSL2 (Ubuntu 22.04) or **Ubuntu 22.04** directly
- **At least 8GB RAM** (16GB recommended)
- **At least 10GB free disk space**
- **Internet connection** for AI API access
- **API keys** for at least one AI provider (see below)

### Step 1: Get AI Provider API Keys

**Choose at least one AI provider:**

1. **OpenAI (Recommended)**:
   - Go to: https://platform.openai.com/api-keys
   - Create account and get API key
   - Models: GPT-3.5-turbo, GPT-4

2. **Anthropic Claude**:
   - Go to: https://console.anthropic.com/
   - Create account and get API key
   - Models: Claude-3-haiku, Claude-3-sonnet

3. **Google Gemini**:
   - Go to: https://makersuite.google.com/app/apikey
   - Create account and get API key
   - Models: Gemini-pro, Gemini-pro-vision

4. **Ollama (Local AI)**:
   - Install Ollama: https://ollama.ai/
   - Run: `ollama pull llama2`
   - No API key needed

5. **Chrome Web AI (Experimental)**:
   - Requires Chrome Canary with experimental features
   - No API key needed

### Step 2: Install Required Software

1. **Install Python 3.11**:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3.11-dev
   ```

2. **Install Node.js 18+**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Install Yarn**:
   ```bash
   npm install -g yarn
   ```

4. **Install Git** (if not already installed):
   ```bash
   sudo apt install git
   ```

### Step 3: Set Up the Project

1. **Clone or navigate to the project folder**:
   ```bash
   cd /path/to/your/LLB/project
   ```

2. **Run the setup script**:
   ```bash
   chmod +x scripts/setup/setup_project.sh
   ./scripts/setup/setup_project.sh
   ```

### Step 4: Configure AI Providers

1. **Copy environment files**:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   ```

2. **Edit `.env` and `backend/.env`** with your API keys:
   ```bash
   # Add your API keys (at least one required)
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Enable local AI if desired
   OLLAMA_ENABLED=true
   CHROME_WEB_AI_ENABLED=false
   ```

### Step 5: Start the Application

1. **Start all services**:
   ```bash
   make dev
   ```

2. **Or start services individually**:
   ```bash
   # Backend only
   make dev-backend
   
   # Frontend only (in another terminal)
   make dev-frontend
   ```

3. **Manual startup (if make commands fail)**:
   ```bash
   # Activate virtual environment and start backend
   source backend/llb-env/bin/activate
   cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
   # In another terminal, start frontend
   cd frontend && npm run dev
   ```

### Step 6: Use the Application

1. **Open your web browser** and go to:
   - **Main app**: http://localhost:3000
   - **API documentation**: http://localhost:8000/docs

2. **Test the features**:
   - Type a question in English or Chinese
   - Try voice input (click microphone icon)
   - Upload a PDF document for analysis

### Step 7: Run Tests (Optional but Recommended)

**Test everything is working correctly**:

```bash
# Run all tests
make test

# Run specific test suites
make test-backend    # Backend API tests
make test-frontend   # Frontend component tests
make test-ai         # AI module tests

# Generate test coverage reports
make coverage
```

### Step 8: Stop the Application

When you're done:
```bash
# Stop all services
Ctrl+C (in the terminal where you ran make dev)

# Or if running in background
make stop
```

### Troubleshooting

**Common issues and solutions**:

1. **"No AI providers available" error**:
   - Make sure you have at least one valid API key configured
   - Check your internet connection
   - Verify API key format and permissions

2. **"Port already in use" error**:
   ```bash
   # Check what's using the ports
   lsof -ti:3000
   lsof -ti:8000
   
   # Kill processes on ports 3000 and 8000
   sudo lsof -ti:3000 | xargs kill -9
   sudo lsof -ti:8000 | xargs kill -9
   ```

3. **API key errors**:
   - Verify your API keys are correct
   - Check API usage limits and billing
   - Ensure API keys have proper permissions

4. **Ollama connection issues**:
   ```bash
   # Start Ollama service
   ollama serve
   
   # Pull a model
   ollama pull llama2
   
   # Test connection
   curl http://localhost:11434/api/tags
   ```

5. **Python/Node.js version issues**:
   - Make sure you have Python 3.11 and Node.js 18+
   - Run: `python3.11 --version` and `node --version`

### Getting Help

- **Check logs**: Look in `backend/logs/` for error messages
- **GitHub Issues**: Report bugs at [project repository]
- **Documentation**: See `docs/` folder for detailed guides

### You're All Set!

Congratulations! You now have LLB (爱学伴) running with modern AI providers. The app provides:
- ✅ Multiple AI provider support (OpenAI, Claude, Gemini, Ollama)
- ✅ AI-powered sexual health education
- ✅ Support for English and Chinese
- ✅ Voice interaction capabilities
- ✅ PDF document processing
- ✅ Culturally sensitive responses
- ✅ Automatic provider fallback

---

## Overview

LLB (爱学伴) is a comprehensive, privacy-focused sexual health education web application that leverages multiple AI providers for intelligent responses. The application provides multi-modal educational content through text, voice, and document analysis.

### ✨ Key Features

- **Multiple AI Providers** - OpenAI, Claude, Gemini, Ollama, Chrome Web AI
- **Automatic Fallback** - Switches providers if one fails
- **Multi-modal Input** - Text, voice, and PDF document support
- **Multi-language Support** - Simplified Chinese, Henan Dialect, American/British English
- **Privacy Options** - Use local AI (Ollama) for complete privacy
- **Progressive Web App** - Modern, responsive design
- **Safety-First** - Built-in content filtering and safety guidelines

## Architecture

```
LLB/
├── backend/           # FastAPI backend with AI services
├── frontend/          # React frontend application
├── ai/               # AI processing logic and prompts
├── docs/             # Comprehensive documentation
├── scripts/          # Build and deployment scripts
└── config/           # Configuration files
```

## AI Provider Support

### Cloud AI Providers
- **OpenAI**: GPT-3.5-turbo, GPT-4
- **Anthropic Claude**: Claude-3-haiku, Claude-3-sonnet
- **Google Gemini**: Gemini-pro, Gemini-pro-vision

### Local AI Providers
- **Ollama**: Run Llama2, Mistral, and other models locally
- **Chrome Web AI**: Experimental browser-based AI (Gemini Nano)

### Provider Features
- **Automatic Selection**: Uses the first available provider
- **Fallback Support**: Switches to backup providers on failure
- **Load Balancing**: Distributes requests across providers
- **Cost Optimization**: Prefers cheaper providers when available

## Quick Start

### Prerequisites

- **OS**: Windows 11 Pro with WSL2 (Ubuntu 22.04 LTS) or Ubuntu 22.04
- **Python**: 3.11+
- **Node.js**: 18+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB minimum
- **API Keys**: At least one AI provider

### Automated Setup

Run the automated setup script:

```bash
# Clone the repository
git clone https://github.com/your-username/llb.git
cd llb

# Run the setup script
./scripts/setup/setup_project.sh
```

### Manual Setup

1. **Install Dependencies**
   ```bash
   make install
   ```

2. **Setup Environment**
   ```bash
   make setup
   ```

3. **Configure API Keys**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start Development**
   ```bash
   # Start both backend and frontend
   make dev

   # Or start individually
   make dev-backend  # Backend only
   make dev-frontend # Frontend only
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Available Commands

Use the Makefile for common tasks:

```bash
make help          # Show all available commands
make install       # Install all dependencies
make setup         # Complete project setup
make dev           # Start development environment
make test          # Run all tests
make lint          # Run code linting
make format        # Format code
make build         # Build the application
make clean         # Clean build artifacts
make status        # Check project status
```

## Configuration

### Environment Variables

Configure AI providers in `.env`:

```bash
# AI Provider API Keys (configure at least one)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Local AI
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Chrome Web AI (experimental)
CHROME_WEB_AI_ENABLED=false
```

### AI Provider Priority

The system tries providers in this order:
1. OpenAI (if configured)
2. Claude (if configured)
3. Gemini (if configured)
4. Ollama (if enabled)
5. Chrome Web AI (if enabled)

## Testing

Run comprehensive tests:

```bash
# All tests
make test

# Backend tests only
make test-backend

# Frontend tests only
make test-frontend

# AI tests only
make test-ai
```

## Documentation

- **API Documentation**: Available at `/docs` when running
- **Architecture**: See `docs/architecture/`
- **Development Guide**: See `docs/development/`
- **Deployment Guide**: See `docs/deployment/`
- **User Guide**: See `docs/user/`

## Deployment

### Local Deployment
```bash
make deploy-local
```

### Production Deployment
```bash
make deploy-prod
```

### Docker Deployment
```bash
make docker-build
make docker-up
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python, ESLint for TypeScript
- **Line Length**: Maximum 80 characters
- **File Length**: Maximum 500 lines per file
- **Testing**: Write tests for new features
- **Documentation**: Update docs for API changes

## System Requirements

### Minimum Requirements
- **CPU**: 4-core processor
- **RAM**: 8GB
- **Storage**: 10GB SSD
- **Internet**: Broadband connection for AI APIs
- **OS**: Windows 11 Pro with WSL2 or Ubuntu 22.04

### Recommended Requirements
- **CPU**: 8-core processor
- **RAM**: 16GB+
- **Storage**: 20GB SSD+
- **Internet**: High-speed broadband
- **OS**: Ubuntu 22.04 LTS

## Security & Privacy

- **API Key Security**: Environment-based secrets management
- **Local Processing**: Use Ollama for complete privacy
- **Content Filtering**: Built-in safety mechanisms
- **Data Protection**: No user data stored by default

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.

## Recent Updates & Improvements

### **Latest Updates (September 2025)**
- **Multiple AI Providers**: Added support for OpenAI, Claude, Gemini, Ollama, Chrome Web AI
- **Automatic Fallback**: System switches providers if one fails
- **Removed Gemma**: Eliminated problematic local Gemma model integration
- **Simplified Setup**: No more complex model downloads
- **Better Performance**: Faster responses with cloud AI providers
- **Cost Optimization**: Choose providers based on cost and performance

### **Migration from Gemma**
- **No Model Downloads**: No need to manually download large AI models
- **API-Based**: All AI processing now uses reliable API services
- **Better Quality**: Higher quality responses from state-of-the-art models
- **Easier Setup**: Just add API keys and start using

## Acknowledgments

- **OpenAI** for GPT models and API
- **Anthropic** for Claude AI models
- **Google** for Gemini AI models
- **Ollama** for local AI model serving
- **FastAPI** for the excellent web framework
- **React** for the frontend framework
- **Material-UI** for beautiful UI components

## Support

For support and questions:

- **Email**: jnc@freew.org
- **Issues**: [GitHub Issues](https://github.com/your-username/llb/issues)
- **Documentation**: [Project Wiki](https://github.com/your-username/llb/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/llb/discussions)

---

<div align="center">
  <strong>Built with ❤️ for sexual health education</strong>
  <br>
  <em>Multiple AI Providers • Multi-language • Open Source • Privacy Options</em>
</div>