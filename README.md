# LLB (爱学伴) - Local AI-Driven Sexual Health Education

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)

## 🚀 Quick Start Guide for Beginners

*This guide will help you set up and run LLB (爱学伴) on your computer, even if you're not a programmer!*

### 📋 What You'll Need

Before starting, make sure your computer has:
- **Windows 11** with WSL2 (Ubuntu 22.04) or **Ubuntu 22.04** directly
- **At least 16GB RAM** (32GB recommended)
- **At least 20GB free disk space**
- **Internet connection** for downloading dependencies

### 🎯 Step 1: Download the AI Model

**⚠️ Important: You must download the AI model manually before setup!**

1. **Create a Kaggle account** at [kaggle.com](https://www.kaggle.com) (free)
2. **Download the Gemma model**:
   - Go to: https://www.kaggle.com/models/google/gemma/keras/gemma_1.1_instruct_2b_en
   - Click "Download" (you may need to accept terms)
   - Download the **1B parameter version** (about 2GB)
3. **Extract the model**:
   - Create folder: `ai/models/gemma3-keras-gemma3_1b-v3/`
   - Extract all files from the download into this folder
   - You should see files like: `config.json`, `model.weights.h5`, `tokenizer.json`, etc.

### 🛠️ Step 2: Install Required Software

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

### 🏗️ Step 3: Set Up the Project

1. **Open terminal** and navigate to the project folder:
   ```bash
   cd /path/to/your/LLB/project
   ```

2. **Run the setup script**:
   ```bash
   chmod +x scripts/setup/setup_project.sh
   ./scripts/setup/setup_project.sh
   ```

3. **Follow the prompts**:
   - The script will check your system
   - Install all dependencies automatically
   - Verify your AI model is correctly placed
   - Set up testing infrastructure
   - When asked "Run comprehensive tests?", type `y` to verify everything works

### ⚙️ Step 4: Configure the Application

1. **Update environment files**:
   - Edit `.env` (main settings)
   - Edit `backend/.env` (backend settings)
   - Edit `frontend/.env` (frontend settings)

2. **Key settings to check**:
   ```bash
   # In backend/.env
   GEMMA_MODEL_PATH=ai/models/gemma3-keras-gemma3_1b-v3
   WHISPER_MODEL_SIZE=base
   SUPPORTED_LANGUAGES=en,zh-CN
   ```

### 🚀 Step 5: Start the Application

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

### 🌐 Step 6: Use the Application

1. **Open your web browser** and go to:
   - **Main app**: http://localhost:3000
   - **API documentation**: http://localhost:8000/docs

2. **Test the features**:
   - Type a question in English or Chinese
   - Try voice input (click microphone icon)
   - Upload a PDF document for analysis

### 🧪 Step 7: Run Tests (Optional but Recommended)

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

**View test results**:
- Coverage report: `backend/htmlcov/index.html`
- Test logs in terminal

### 🛑 Step 8: Stop the Application

When you're done:
```bash
# Stop all services
Ctrl+C (in the terminal where you ran make dev)

# Or if running in background
make stop
```

### 🔧 Troubleshooting

**Common issues and solutions**:

1. **"Gemma model not found" error**:
   - Make sure you downloaded and extracted the model correctly
   - Check the path: `ai/models/gemma3-keras-gemma3_1b-v3/`
   - Verify all required files are present

2. **"Port already in use" error**:
   ```bash
   # Kill processes on ports 3000 and 8000
   sudo lsof -ti:3000 | xargs kill -9
   sudo lsof -ti:8000 | xargs kill -9
   ```

3. **Python/Node.js version issues**:
   - Make sure you have Python 3.11 and Node.js 18+
   - Run: `python3.11 --version` and `node --version`

4. **Memory issues**:
   - Close other applications
   - Use smaller Whisper model: set `WHISPER_MODEL_SIZE=tiny` in backend/.env

5. **Tests failing**:
   ```bash
   # Clean and reinstall
   make clean
   ./scripts/setup/setup_project.sh
   ```

### 📞 Getting Help

- **Check logs**: Look in `backend/logs/` for error messages
- **GitHub Issues**: Report bugs at [project repository]
- **Documentation**: See `docs/` folder for detailed guides
- **Community**: Join our discussion forums

### 🎉 You're All Set!

Congratulations! You now have LLB (爱学伴) running on your computer. The app provides:
- ✅ AI-powered sexual health education
- ✅ Support for English and Chinese
- ✅ Voice interaction capabilities
- ✅ PDF document processing
- ✅ Culturally sensitive responses
- ✅ Complete privacy (everything runs locally)

---

## Overview

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

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.

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