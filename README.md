# LLB (爱学伴) - Local AI-Driven Sexual Health Education

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
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

## 📖 Complete Tutorial for Non-Technical Users

This comprehensive guide will help you set up and use LLB (爱学伴) even if you're not familiar with programming or command-line tools.

### 🎯 What You'll Need

Before starting, make sure your computer meets these requirements:

#### Minimum System Requirements
- **Computer**: Any laptop or desktop with Intel 8th generation i7 processor
- **Memory (RAM)**: 16GB
- **Storage**: 256GB free space on SSD
- **Operating System**: Windows 11 Pro
- **Graphics Card**: Any NVIDIA graphics card (optional but recommended)

#### Recommended System Requirements
- **Computer**: Desktop with Intel 9th generation i7 or newer
- **Memory (RAM)**: 32GB or more
- **Storage**: 512GB free space on SSD
- **Graphics Card**: NVIDIA RTX 3060 with 12GB memory or better

### 🔧 Step 1: Setting Up Your Computer

#### 1.1 Enable WSL2 (Windows Subsystem for Linux)

WSL2 allows you to run Linux on Windows, which is required for LLB.

1. **Open PowerShell as Administrator**:
   - Press `Windows + X`
   - Click "Windows PowerShell (Admin)" or "Terminal (Admin)"
   - Click "Yes" when prompted

2. **Install WSL2**:
   ```powershell
   wsl --install
   ```

3. **Restart your computer** when prompted

4. **Install Ubuntu 22.04**:
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

5. **Set up Ubuntu**:
   - When Ubuntu starts, create a username and password
   - Remember these credentials - you'll need them later

#### 1.2 Install Required Software

1. **Update Ubuntu**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python 3.11**:
   ```bash
   sudo apt install python3.11 python3.11-venv python3-pip -y
   ```

3. **Install Node.js 18**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

4. **Install Git**:
   ```bash
   sudo apt install git -y
   ```

### 🚀 Step 2: Download and Install LLB

#### 2.1 Download the Project

1. **Open Ubuntu terminal** (if not already open)

2. **Navigate to your home directory**:
   ```bash
   cd ~
   ```

3. **Download LLB**:
   ```bash
   git clone https://github.com/your-username/llb.git
   cd llb
   ```

#### 2.2 Automatic Installation (Recommended)

1. **Make the setup script executable**:
   ```bash
   chmod +x scripts/setup/setup_project.sh
   ```

2. **Run the automatic setup**:
   ```bash
   ./scripts/setup/setup_project.sh
   ```

3. **Wait for installation** (this may take 15-30 minutes):
   - The script will download and install all required components
   - You'll see progress messages during installation
   - Don't close the terminal window during this process

#### 2.3 Manual Installation (If Automatic Fails)

If the automatic installation doesn't work, follow these steps:

1. **Create a virtual environment**:
   ```bash
   python3.11 -m venv llb-env
   source llb-env/bin/activate
   ```

2. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Download AI models** (this will take some time):
   ```bash
   python scripts/download_models.py
   ```

### 🎮 Step 3: Starting LLB

#### 3.1 Quick Start

1. **Navigate to the LLB directory**:
   ```bash
   cd ~/llb
   ```

2. **Start the application**:
   ```bash
   ./start_llb.sh
   ```

3. **Wait for startup** (first time may take 2-3 minutes):
   - You'll see messages about loading models
   - Wait until you see "Application startup complete"

#### 3.2 Manual Start (Alternative Method)

If the quick start doesn't work:

1. **Start the backend** (in one terminal):
   ```bash
   cd ~/llb
   source llb-env/bin/activate
   cd backend
   python main.py
   ```

2. **Start the frontend** (in a new terminal):
   ```bash
   cd ~/llb/frontend
   npm start
   ```

### 🌐 Step 4: Using LLB

#### 4.1 Accessing the Application

1. **Open Google Chrome browser**

2. **Go to the application**:
   - Type in address bar: `http://localhost:3000`
   - Press Enter

3. **You should see the LLB welcome screen**

#### 4.2 Basic Usage

**Text Chat**:
1. Type your question in the chat box
2. Select your language (English, Chinese, or Henan dialect)
3. Click "Send" or press Enter
4. Wait for the AI response

**Voice Input**:
1. Click the microphone button
2. Speak your question clearly
3. Click stop when finished
4. The system will process your speech and respond

**Document Upload**:
1. Click the "Upload Document" button
2. Select a PDF file from your computer
3. Wait for the system to analyze the document
4. Ask questions about the document content

#### 4.3 Language Support

LLB supports multiple languages:
- **English**: American and British English
- **简体中文**: Simplified Chinese (Mandarin)
- **河南话**: Henan dialect

To change language:
1. Click the language selector in the top-right corner
2. Choose your preferred language
3. The interface and AI responses will switch to that language

### 🔧 Step 5: Troubleshooting Common Issues

#### 5.1 Application Won't Start

**Problem**: Error messages when starting LLB

**Solutions**:
1. **Check system requirements**: Ensure you have enough RAM and storage
2. **Restart WSL2**:
   ```bash
   wsl --shutdown
   # Wait 10 seconds, then restart Ubuntu
   ```
3. **Update dependencies**:
   ```bash
   cd ~/llb
   source llb-env/bin/activate
   pip install --upgrade -r backend/requirements.txt
   ```

#### 5.2 Slow Performance

**Problem**: LLB responds very slowly

**Solutions**:
1. **Check GPU usage**:
   ```bash
   nvidia-smi
   ```
2. **Close other applications** to free up memory
3. **Restart the application**:
   ```bash
   # Stop LLB (Ctrl+C in terminal)
   # Then restart with:
   ./start_llb.sh
   ```

#### 5.3 Can't Access the Website

**Problem**: Browser shows "This site can't be reached"

**Solutions**:
1. **Check if services are running**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:3000
   ```
2. **Restart the application**
3. **Check firewall settings** in Windows

#### 5.4 AI Not Responding

**Problem**: Chat messages don't get responses

**Solutions**:
1. **Check backend logs**:
   ```bash
   cd ~/llb/backend
   tail -f logs/llb.log
   ```
2. **Restart the backend service**
3. **Check model loading** in the logs

### 🛡️ Step 6: Safety and Privacy

#### 6.1 Privacy Features

- **Local Processing**: All your data stays on your computer
- **No Internet Required**: Once installed, works offline
- **No Data Collection**: Your conversations are not stored or transmitted

#### 6.2 Content Safety

- **Built-in Filters**: Inappropriate content is automatically filtered
- **Educational Focus**: Responses are focused on health education
- **Age-Appropriate**: Content is suitable for educational purposes

### 🔄 Step 7: Updating LLB

#### 7.1 Getting Updates

1. **Check for updates**:
   ```bash
   cd ~/llb
   git pull origin main
   ```

2. **Update dependencies**:
   ```bash
   source llb-env/bin/activate
   pip install --upgrade -r backend/requirements.txt
   cd frontend
   npm update
   cd ..
   ```

3. **Restart the application**

#### 7.2 Backup Your Settings

Before updating, backup your configuration:
```bash
cp backend/.env backend/.env.backup
cp frontend/.env frontend/.env.backup
```

### 📞 Step 8: Getting Help

#### 8.1 Self-Help Resources

1. **Check the logs** for error messages:
   ```bash
   cd ~/llb/backend
   cat logs/llb.log
   ```

2. **Visit the documentation**: See the `docs/` folder for detailed guides

3. **Check system status**:
   ```bash
   cd ~/llb
   make status
   ```

#### 8.2 Community Support

- **GitHub Issues**: Report bugs and get help
- **Documentation**: Comprehensive guides in the `docs/` folder
- **Community Forum**: Connect with other users

#### 8.3 Common Commands Reference

```bash
# Navigate to LLB directory
cd ~/llb

# Start the application
./start_llb.sh

# Stop the application (Ctrl+C in terminal)

# Check application status
make status

# View logs
tail -f backend/logs/llb.log

# Update the application
git pull origin main
make install

# Restart services
make restart
```

### 🎉 Congratulations!

You've successfully set up and learned how to use LLB! The application provides:

- **Private, local AI-powered sexual health education**
- **Multi-language support** for diverse users
- **Voice and text interaction** for accessibility
- **Document analysis** for educational materials
- **Complete privacy** with no data transmission

Remember: All processing happens on your computer, ensuring your privacy and data security.

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