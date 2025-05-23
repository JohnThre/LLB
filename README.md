# LLB (爱学伴) - Local AI-Driven Sexual Health Education

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)

## 🧑‍🏫 Beginner Tutorial: How to Deploy and Use LLB (爱学伴)

Welcome! This guide will help anyone (even with no technical background) set up and use the LLB (爱学伴) sexual health education app on their own computer.

---

### 📝 What is LLB?
LLB (爱学伴) is a private, local web app that answers sexual health questions in English and Chinese (including Henan dialect). It works with text, voice, and PDF files—all on your own computer, with no data sent to the internet.

---

### 🖥️ What You Need
- **A computer with:**
  - Windows 11 Pro
  - At least 16GB RAM (32GB recommended)
  - Intel i7 8th gen or newer
  - (Optional) NVIDIA RTX 3060 or better for faster AI
- **Software:**
  - [Google Chrome](https://www.google.com/chrome/)
  - [WSL2 with Ubuntu 22.04](https://learn.microsoft.com/en-us/windows/wsl/install)
  - [Python 3.11](https://www.python.org/downloads/release/python-3110/)
  - [Node.js 18+](https://nodejs.org/)
  - (Optional) Latest NVIDIA driver for your GPU

---

### 🚀 Step 1: Download LLB
1. Go to the [LLB GitHub page](https://github.com/your-username/llb).
2. Click **Code > Download ZIP** (or use Git if you know how).
3. Unzip the file to a folder (e.g., `C:\LLB` or your home directory in Ubuntu).

---

### ⚡ Step 2: One-Click Setup (Easiest Way)
1. Open **Ubuntu 22.04** (WSL2) on your computer.
2. Change to the LLB folder. For example:
   ```bash
   cd ~/LLB
   ```
3. Make the setup script executable:
   ```bash
   chmod +x scripts/setup/setup_project.sh
   ```
4. Run the setup script:
   ```bash
   ./scripts/setup/setup_project.sh
   ```
5. **Wait**: The script will check your system, install everything, and set up the app. This may take 10–30 minutes (internet required).

---

### 🟢 Step 3: Start the App
1. In Ubuntu, start the app:
   ```bash
   ./start_llb.sh
   ```
2. When you see "🚀 Starting LLB System...", open **Google Chrome** and go to:
   - [http://localhost:3000](http://localhost:3000) (main app)
   - [http://localhost:8000/docs](http://localhost:8000/docs) (API docs)

---

### 💬 Step 4: Using LLB
- **Text Chat:** Type your question and press send.
- **Voice Input:** Click the microphone button and speak (first time, allow browser microphone access).
- **PDF Upload:** Click the upload button and select a PDF to analyze.
- **Language:** You can ask questions in English, Simplified Chinese, or Henan dialect. The app will detect the language automatically.

---

### 🛑 Step 5: Stopping and Restarting
- To **stop** the app: Press `Ctrl+C` in the Ubuntu window.
- To **restart**: Run `./start_llb.sh` again.

---

### 🆘 Troubleshooting
- If you see errors, check the file `TROUBLESHOOTING.md` in the LLB folder.
- For common problems (like missing Python, Node.js, or GPU issues), the setup script will give hints.
- If you get stuck, email: **support@llb-project.com** or open an issue on [GitHub Issues](https://github.com/your-username/llb/issues).

---

### ❓ FAQ
- **Is my data private?** Yes! All processing is local. Nothing is sent to the internet.
- **Can I use LLB offline?** Yes, after setup, no internet is needed.
- **Do I need a GPU?** No, but it will be faster with an NVIDIA GPU.
- **Can I use it on Mac or other Linux?** Not officially supported, but advanced users may try.

---

Enjoy learning with LLB (爱学伴)! If you have feedback, please let us know.

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