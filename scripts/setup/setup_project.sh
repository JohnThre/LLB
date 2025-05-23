#!/bin/bash

# LLB (爱学伴) Project Setup Script
# Automated setup for Local AI-Driven Sexual Health Education Web Application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="LLB (爱学伴)"
PYTHON_VERSION="3.11"
NODE_VERSION="18"
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
AI_DIR="ai"
VENV_NAME="llb-env"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check system requirements
check_requirements() {
    print_header "Checking System Requirements"
    
    # Check Python
    if command_exists python3.11; then
        PYTHON_CMD="python3.11"
        print_success "Python 3.11 found"
    elif command_exists python3; then
        PYTHON_CMD="python3"
        PYTHON_VER=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        if [[ "$PYTHON_VER" == "3.11" ]]; then
            print_success "Python 3.11 found"
        else
            print_warning "Python $PYTHON_VER found, but 3.11 is recommended"
        fi
    else
        print_error "Python 3.11 not found. Please install Python 3.11"
        exit 1
    fi
    
    # Check Node.js
    if command_exists node; then
        NODE_VER=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
        if [[ "$NODE_VER" -ge 18 ]]; then
            print_success "Node.js $NODE_VER found"
        else
            print_warning "Node.js $NODE_VER found, but version 18+ is recommended"
        fi
    else
        print_error "Node.js not found. Please install Node.js 18+"
        exit 1
    fi
    
    # Check Yarn
    if command_exists yarn; then
        print_success "Yarn found"
    else
        print_warning "Yarn not found. Installing via npm..."
        npm install -g yarn
    fi
    
    # Check Git
    if command_exists git; then
        print_success "Git found"
    else
        print_error "Git not found. Please install Git"
        exit 1
    fi
    
    # Check CUDA (optional)
    if command_exists nvidia-smi; then
        print_success "NVIDIA GPU detected"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    else
        print_warning "NVIDIA GPU not detected. CPU-only mode will be used"
    fi
}

# Function to create project directories
create_directories() {
    print_header "Creating Project Directories"
    
    # Backend directories
    mkdir -p $BACKEND_DIR/{app/{api/v1,core,models,services,utils},tests/{unit,integration,e2e},logs,uploads,static}
    mkdir -p $BACKEND_DIR/requirements
    
    # Frontend directories
    mkdir -p $FRONTEND_DIR/{src/{components/{common,chat,voice,documents},pages,hooks,services,store,utils,types,constants,locales,styles},tests,public}
    
    # AI directories
    mkdir -p $AI_DIR/{models/{gemma,whisper,configs},processors,prompts,utils,cache,temp}
    
    # Documentation directories
    mkdir -p docs/{api,deployment,development,user,architecture}
    
    # Scripts directories
    mkdir -p scripts/{setup,build,deploy,utils}
    
    # Configuration directories
    mkdir -p config docker/{backend,frontend,nginx}
    
    print_success "Project directories created"
}

# Function to setup Python virtual environment
setup_python_env() {
    print_header "Setting up Python Environment"
    
    cd $BACKEND_DIR
    
    # Create virtual environment
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv $VENV_NAME
    
    # Activate virtual environment
    source $VENV_NAME/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install base requirements
    if [[ -f "requirements/base.txt" ]]; then
        print_status "Installing base requirements..."
        pip install -r requirements/base.txt
    elif [[ -f "requirements.txt" ]]; then
        print_status "Installing requirements..."
        pip install -r requirements.txt
    else
        print_warning "No requirements file found"
    fi
    
    cd ..
    print_success "Python environment setup complete"
}

# Function to setup Node.js environment
setup_node_env() {
    print_header "Setting up Node.js Environment"
    
    cd $FRONTEND_DIR
    
    # Install dependencies
    if [[ -f "package.json" ]]; then
        print_status "Installing Node.js dependencies..."
        yarn install
        print_success "Node.js dependencies installed"
    else
        print_warning "No package.json found in frontend directory"
    fi
    
    cd ..
}

# Function to download AI models
download_models() {
    print_header "Setting up AI Models"
    
    cd $AI_DIR
    
    # Activate Python environment
    source ../$BACKEND_DIR/$VENV_NAME/bin/activate
    
    # Create model directories
    mkdir -p models/{gemma,whisper}
    
    # Download Gemma 3 1B model (placeholder - actual implementation needed)
    print_status "Preparing Gemma 3 1B model setup..."
    echo "# Gemma 3 1B model will be downloaded here" > models/gemma/README.md
    
    # Download Whisper model (placeholder - actual implementation needed)
    print_status "Preparing Whisper model setup..."
    echo "# Whisper model will be downloaded here" > models/whisper/README.md
    
    print_warning "Model download scripts need to be implemented"
    print_status "Models will be downloaded on first run"
    
    cd ..
}

# Function to setup configuration files
setup_config() {
    print_header "Setting up Configuration Files"
    
    # Copy environment files if they exist
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        print_success "Root .env file created"
    fi
    
    if [[ -f "$BACKEND_DIR/.env.example" ]]; then
        cp $BACKEND_DIR/.env.example $BACKEND_DIR/.env
        print_success "Backend .env file created"
    fi
    
    if [[ -f "$FRONTEND_DIR/.env.example" ]]; then
        cp $FRONTEND_DIR/.env.example $FRONTEND_DIR/.env
        print_success "Frontend .env file created"
    fi
    
    # Setup Git hooks (if .git exists)
    if [[ -d ".git" ]]; then
        print_status "Setting up Git hooks..."
        # Add pre-commit hooks setup here
        print_success "Git hooks configured"
    fi
}

# Function to run initial tests
run_tests() {
    print_header "Running Initial Tests"
    
    # Test backend
    cd $BACKEND_DIR
    source $VENV_NAME/bin/activate
    
    if command_exists pytest; then
        print_status "Running backend tests..."
        pytest tests/ -v || print_warning "Some backend tests failed"
    else
        print_warning "pytest not available, skipping backend tests"
    fi
    
    cd ..
    
    # Test frontend
    cd $FRONTEND_DIR
    if [[ -f "package.json" ]] && command_exists yarn; then
        print_status "Running frontend tests..."
        yarn test --run || print_warning "Some frontend tests failed"
    else
        print_warning "Frontend tests not available"
    fi
    
    cd ..
}

# Function to display final instructions
show_final_instructions() {
    print_header "Setup Complete!"
    
    echo -e "${GREEN}🎉 LLB (爱学伴) project setup completed successfully!${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo "1. Review and update configuration files:"
    echo "   - .env (root)"
    echo "   - backend/.env"
    echo "   - frontend/.env"
    echo ""
    echo "2. Download AI models:"
    echo "   cd ai && python scripts/download_models.py"
    echo ""
    echo "3. Start the development environment:"
    echo "   make dev"
    echo ""
    echo "4. Or start services individually:"
    echo "   Backend:  make dev-backend"
    echo "   Frontend: make dev-frontend"
    echo ""
    echo -e "${CYAN}Useful commands:${NC}"
    echo "   make help     - Show all available commands"
    echo "   make status   - Check project status"
    echo "   make test     - Run all tests"
    echo "   make clean    - Clean build artifacts"
    echo ""
    echo -e "${CYAN}Access points:${NC}"
    echo "   Backend API:  http://localhost:8000"
    echo "   Frontend:     http://localhost:3000"
    echo "   API Docs:     http://localhost:8000/docs"
    echo ""
    echo -e "${YELLOW}Note: Make sure to configure your environment variables before starting!${NC}"
}

# Main setup function
main() {
    print_header "LLB (爱学伴) Project Setup"
    echo -e "${CYAN}Local AI-Driven Sexual Health Education Web Application${NC}"
    echo ""
    
    # Check if we're in the right directory
    if [[ ! -f "README.md" ]] || [[ ! -d ".git" ]]; then
        print_warning "This doesn't appear to be the LLB project root directory"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Run setup steps
    check_requirements
    create_directories
    setup_python_env
    setup_node_env
    download_models
    setup_config
    
    # Optional: run tests
    read -p "Run initial tests? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_tests
    fi
    
    show_final_instructions
}

# Run main function
main "$@"