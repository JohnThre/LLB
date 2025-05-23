# LLB (爱学伴) - Local AI-Driven Sexual Health Education

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)

## 🌟 Overview

LLB (爱学伴) is a comprehensive, privacy-focused sexual health education web application that leverages Google's Gemma 3 1B AI model for local processing. The application provides multi-modal educational content through text, voice, and document analysis while maintaining complete privacy through local AI processing.

### ✨ Key Features

- 🤖 **Local AI Processing** - Powered by Google's Gemma 3 1B model
- 🗣️ **Multi-modal Input** - Text, voice, and PDF document support
- 🌍 **Multi-language Support** - Simplified Chinese, Henan Dialect, American/British English
- 🔒 **Privacy-First** - All processing done locally, no data transmission
- 🚀 **GPU Acceleration** - Optimized for NVIDIA RTX 3060+ GPUs
- 📱 **Progressive Web App** - Modern, responsive design
- 🛡️ **Safety-First** - Built-in content filtering and safety guidelines

## 🏗️ Architecture

```
LLB/
├── backend/           # FastAPI backend with AI services
├── frontend/          # React frontend application
├── ai/               # AI models and processing logic
├── docs/             # Comprehensive documentation
├── scripts/          # Build and deployment scripts
└── config/           # Configuration files
```

## 🚀 Quick Start

### Prerequisites

- **OS**: Windows 11 Pro with WSL2 (Ubuntu 22.04 LTS)
- **Python**: 3.11+
- **Node.js**: 18+
- **GPU**: NVIDIA RTX 3060+ (recommended)
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: 256GB SSD minimum

### 🔧 Automated Setup

Run the automated setup script:

```bash
# Clone the repository
git clone https://github.com/your-username/llb.git
cd llb

# Run the setup script
./scripts/setup/setup_project.sh
```

### 🛠️ Manual Setup

1. **Install Dependencies**
   ```bash
   make install
   ```

2. **Setup Environment**
   ```bash
   make setup
   ```

3. **Start Development**
   ```bash
   # Start both backend and frontend
   make dev

   # Or start individually
   make dev-backend  # Backend only
   make dev-frontend # Frontend only
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📋 Available Commands

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

## 🏛️ Project Structure

### Backend (`backend/`)
- **FastAPI** web framework with async support
- **Pydantic** for data validation and settings
- **SQLAlchemy** for database operations
- **Structured logging** with file rotation
- **Custom exception handling**
- **Comprehensive health checks**

### Frontend (`frontend/`)
- **React 18** with TypeScript
- **Material-UI** for modern UI components
- **Redux Toolkit** for state management
- **React Router** for navigation
- **Internationalization** support

### AI (`ai/`)
- **Gemma 3 1B** model integration
- **Whisper** for speech-to-text
- **Custom prompt engineering**
- **Multi-language processing**
- **Safety and content filtering**

## 🔧 Configuration

### Environment Variables

Copy and configure environment files:

```bash
# Backend configuration
cp backend/.env.example backend/.env

# Frontend configuration  
cp frontend/.env.example frontend/.env
```

Key configuration options:
- `LLB_ENVIRONMENT`: development/production
- `LLB_DEBUG`: Enable debug mode
- `LLB_CORS_ORIGINS`: Allowed CORS origins
- `LLB_SUPPORTED_LANGUAGES`: Supported languages
- `CUDA_VISIBLE_DEVICES`: GPU configuration

## 🧪 Testing

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

## 📚 Documentation

- **API Documentation**: Available at `/docs` when running
- **Architecture**: See `docs/architecture/`
- **Development Guide**: See `docs/development/`
- **Deployment Guide**: See `docs/deployment/`
- **User Guide**: See `docs/user/`

## 🚀 Deployment

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

## 🤝 Contributing

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

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 8th Gen Intel Mobile i7
- **RAM**: 16GB
- **Storage**: 256GB SSD
- **GPU**: Integrated Graphics
- **OS**: Windows 11 Pro with WSL2

### Recommended Requirements
- **CPU**: 9th Gen Intel Desktop i7+
- **RAM**: 32GB+
- **Storage**: 512GB SSD+
- **GPU**: NVIDIA RTX 3060 OC 12GB+
- **OS**: Windows 11 Pro with WSL2

## 🔒 Security & Privacy

- **Local Processing**: All AI processing happens locally
- **No Data Transmission**: User data never leaves the device
- **Content Filtering**: Built-in safety mechanisms
- **Secure Configuration**: Environment-based secrets management

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google** for the Gemma 3 1B AI model
- **FastAPI** for the excellent web framework
- **React** for the frontend framework
- **Material-UI** for beautiful UI components
- **NVIDIA** for CUDA support

## 📞 Support

For support and questions:

- 📧 **Email**: support@llb-project.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/llb/issues)
- 📖 **Documentation**: [Project Wiki](https://github.com/your-username/llb/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/llb/discussions)

---

<div align="center">
  <strong>Built with ❤️ for sexual health education</strong>
  <br>
  <em>Privacy-first • Local AI • Multi-language • Open Source</em>
</div> 