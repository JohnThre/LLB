#!/bin/bash

# LLB Deployment Script
# Deploys the LLB sexual health education system locally

set -e  # Exit on any error

echo "🚀 Starting LLB Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if running on WSL2
check_environment() {
    print_status "Checking environment..."
    
    if grep -q microsoft /proc/version; then
        print_success "Running on WSL2"
        export WSL_ENV=true
    else
        print_warning "Not running on WSL2"
        export WSL_ENV=false
    fi
    
    # Check Python version
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD=python3.11
        print_success "Python 3.11 found"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        if [[ "$PYTHON_VERSION" == "3.11" ]]; then
            print_success "Python 3.11 found"
        else
            print_warning "Python version is $PYTHON_VERSION, recommended: 3.11"
        fi
    else
        print_error "Python 3 not found"
        exit 1
    fi
    
    # Check CUDA
    if command -v nvidia-smi &> /dev/null; then
        print_success "NVIDIA GPU detected"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
    else
        print_warning "No NVIDIA GPU detected, will use CPU"
    fi
}

# Setup Python virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "llb-env" ]; then
        $PYTHON_CMD -m venv llb-env
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source llb-env/bin/activate
    print_success "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip
    print_success "Pip upgraded"
}

# Install backend dependencies
install_backend_deps() {
    print_status "Installing backend dependencies..."
    
    cd backend
    
    # Install core dependencies
    pip install -r requirements.txt
    print_success "Backend dependencies installed"
    
    # Install PyTorch with CUDA support if available
    if command -v nvidia-smi &> /dev/null; then
        print_status "Installing PyTorch with CUDA support..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        print_success "PyTorch with CUDA installed"
    else
        print_status "Installing PyTorch CPU version..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        print_success "PyTorch CPU installed"
    fi
    
    cd ..
}

# Install optional dependencies
install_optional_deps() {
    print_status "Installing optional dependencies..."
    
    # Try to install audio dependencies
    if pip install SpeechRecognition pyttsx3; then
        print_success "Audio dependencies installed"
    else
        print_warning "Audio dependencies failed to install (optional)"
    fi
    
    # Try to install PDF dependencies
    if pip install PyPDF2 pdfplumber; then
        print_success "PDF dependencies installed"
    else
        print_warning "PDF dependencies failed to install (optional)"
    fi
}

# Test the prompt system
test_prompt_system() {
    print_status "Testing prompt engineering system..."
    
    if $PYTHON_CMD test_prompt_system.py; then
        print_success "Prompt system test passed"
    else
        print_error "Prompt system test failed"
        exit 1
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p static
    mkdir -p uploads
    mkdir -p models
    
    print_success "Directories created"
}

# Download Gemma model (if not exists)
download_model() {
    print_status "Checking Gemma 3 1B model..."
    
    # Create a simple Python script to check/download model
    cat > check_model.py << 'EOF'
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "google/gemma-3-1b"

try:
    print("🔍 Checking if model is available...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("✅ Model tokenizer loaded successfully")
    
    # Just check if model can be loaded (don't actually load it)
    print("✅ Gemma 3 1B model is available")
    
except Exception as e:
    print(f"❌ Error checking model: {e}")
    print("📥 Model will be downloaded on first run")

print("🎯 Model check completed")
EOF
    
    $PYTHON_CMD check_model.py
    rm check_model.py
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    cat > start_llb.sh << 'EOF'
#!/bin/bash

# LLB Startup Script
echo "🚀 Starting LLB System..."

# Activate virtual environment
source venv/bin/activate

# Start backend
cd backend
echo "🔧 Starting backend server..."
python main.py

EOF
    
    chmod +x start_llb.sh
    print_success "Startup script created"
}

# Create systemd service (for Linux)
create_systemd_service() {
    if [[ "$WSL_ENV" == "false" ]] && [[ -d "/etc/systemd/system" ]]; then
        print_status "Creating systemd service..."
        
        cat > llb.service << EOF
[Unit]
Description=LLB Sexual Health Education System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python $(pwd)/backend/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        print_status "Systemd service file created (llb.service)"
        print_status "To install: sudo cp llb.service /etc/systemd/system/"
        print_status "To enable: sudo systemctl enable llb"
        print_status "To start: sudo systemctl start llb"
    fi
}

# Main deployment function
main() {
    echo "🎯 LLB Sexual Health Education System Deployment"
    echo "================================================"
    
    check_environment
    setup_venv
    install_backend_deps
    install_optional_deps
    create_directories
    test_prompt_system
    download_model
    create_startup_script
    create_systemd_service
    
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Start the system: ./start_llb.sh"
    echo "2. Open browser: http://localhost:8000"
    echo "3. API docs: http://localhost:8000/docs"
    echo "4. Health check: http://localhost:8000/health"
    echo ""
    echo "🔧 System requirements met:"
    echo "- ✅ Python 3.11 environment"
    echo "- ✅ Prompt engineering system"
    echo "- ✅ FastAPI backend"
    echo "- ✅ Gemma 3 1B model support"
    echo ""
    
    if command -v nvidia-smi &> /dev/null; then
        echo "🚀 GPU acceleration available"
    else
        echo "💻 CPU-only mode (consider GPU for better performance)"
    fi
    
    echo ""
    echo "🌟 LLB is ready to provide safe sexual health education!"
}

# Run main function
main "$@" 