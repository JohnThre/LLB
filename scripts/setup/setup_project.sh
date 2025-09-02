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

# Function to clean conflicting files
clean_conflicting_files() {
    print_header "Cleaning Conflicting Files"
    
    # Remove package-lock.json files to avoid conflicts with yarn
    if [[ -f "package-lock.json" ]]; then
        print_status "Removing root package-lock.json..."
        rm -f package-lock.json
        print_success "Root package-lock.json removed"
    fi
    
    if [[ -f "$FRONTEND_DIR/package-lock.json" ]]; then
        print_status "Removing frontend package-lock.json..."
        rm -f $FRONTEND_DIR/package-lock.json
        print_success "Frontend package-lock.json removed"
    fi
    
    # Remove Zone.Identifier files (Windows WSL artifacts)
    find . -name "*.Zone.Identifier" -type f -delete 2>/dev/null || true
    print_success "Zone.Identifier files cleaned"
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
    mkdir -p $AI_DIR/{models/{gemma,whisper,configs},processors,prompts,utils,cache,temp,tests}
    
    # Documentation directories
    mkdir -p docs/{api,deployment,development,user,architecture}
    
    # Scripts directories
    mkdir -p scripts/{setup,build,deploy,utils,tests}
    
    # Configuration directories
    mkdir -p config docker/{backend,frontend,nginx}
    
    # Test directories
    mkdir -p tests/{integration,e2e,performance}
    
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
    
    # Install testing dependencies
    print_status "Installing testing dependencies..."
    pip install pytest pytest-asyncio pytest-cov pytest-mock httpx factory-boy
    
    # Install development dependencies
    print_status "Installing development dependencies..."
    pip install black isort flake8 mypy pre-commit
    
    print_success "Python environment setup complete"
    cd ..
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

# Function to verify AI models
verify_ai_models() {
    print_header "Verifying AI Models"
    
    # Check for Gemma 3 1B model
    GEMMA_MODEL_PATH="$AI_DIR/models/gemma3-keras-gemma3_1b-v3"
    if [[ -d "$GEMMA_MODEL_PATH" ]]; then
        print_status "Checking Gemma 3 1B model..."
        
        # Check required files
        REQUIRED_FILES=("config.json" "model.weights.h5" "tokenizer.json" "task.json" "metadata.json" "preprocessor.json")
        MISSING_FILES=()
        
        for file in "${REQUIRED_FILES[@]}"; do
            if [[ ! -f "$GEMMA_MODEL_PATH/$file" ]]; then
                MISSING_FILES+=("$file")
            fi
        done
        
        if [[ ${#MISSING_FILES[@]} -eq 0 ]]; then
            print_success "Gemma 3 1B model verified successfully"
            
            # Check assets directory
            if [[ -d "$GEMMA_MODEL_PATH/assets" ]]; then
                print_success "Model assets directory found"
            else
                print_warning "Model assets directory not found"
            fi
        else
            print_error "Missing required model files: ${MISSING_FILES[*]}"
            print_error "Please ensure you have extracted the complete Gemma model from Kaggle"
            exit 1
        fi
    else
        print_error "Gemma 3 1B model not found at: $GEMMA_MODEL_PATH"
        print_error "Please download and extract the Gemma 3 1B model from Kaggle:"
        print_error "https://www.kaggle.com/models/google/gemma/keras/gemma_1.1_instruct_2b_en"
        print_error "Extract it to: $GEMMA_MODEL_PATH"
        exit 1
    fi
    
    # Create placeholder for Whisper model
    mkdir -p $AI_DIR/models/whisper
    if [[ ! -f "$AI_DIR/models/whisper/README.md" ]]; then
        cat > $AI_DIR/models/whisper/README.md << 'EOF'
# Whisper Model

Whisper models will be downloaded automatically when first used.
No manual setup required.

Supported models:
- tiny (39 MB)
- base (74 MB) 
- small (244 MB)
- medium (769 MB)
- large (1550 MB)

The default model is 'base' for optimal performance/size balance.
EOF
        print_success "Whisper model placeholder created"
    fi
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
        
        # Create pre-commit hook
        cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run tests before commit
echo "Running pre-commit tests..."

# Run backend tests
cd backend
source llb-env/bin/activate
python -m pytest tests/ --tb=short -q
if [ $? -ne 0 ]; then
    echo "Backend tests failed. Commit aborted."
    exit 1
fi
cd ..

# Run frontend tests
cd frontend
yarn test --run --reporter=basic
if [ $? -ne 0 ]; then
    echo "Frontend tests failed. Commit aborted."
    exit 1
fi
cd ..

echo "All tests passed. Proceeding with commit."
EOF
        chmod +x .git/hooks/pre-commit
        print_success "Git hooks configured"
    fi
}

# Function to create test files
create_test_files() {
    print_header "Setting up Test Infrastructure"
    
    # Backend test configuration
    cd $BACKEND_DIR
    
    # Create pytest.ini
    cat > pytest.ini << 'EOF'
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
EOF
    
    # Create conftest.py for shared test fixtures
    cat > tests/conftest.py << 'EOF'
"""Shared test fixtures for LLB backend tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base_class import Base
from app.core.config import get_settings

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db):
    """Create database session for tests."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client():
    """Create test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def settings():
    """Get test settings."""
    return get_settings()
EOF
    
    # Create sample unit test
    cat > tests/unit/test_health.py << 'EOF'
"""Unit tests for health endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_api_health_check(client: TestClient):
    """Test API health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
EOF
    
    # Create sample integration test
    cat > tests/integration/test_chat_api.py << 'EOF'
"""Integration tests for chat API."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_chat_endpoint(client: TestClient):
    """Test chat endpoint integration."""
    payload = {
        "message": "What is sexual health?",
        "language": "en"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "language_detected" in data


@pytest.mark.integration
def test_chat_multilingual(client: TestClient):
    """Test multilingual chat support."""
    # Test Chinese
    payload = {
        "message": "什么是性健康？",
        "cultural_context": "chinese"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language_detected"] in ["zh-CN", "zh"]
EOF
    
    cd ..
    
    # Frontend test setup
    cd $FRONTEND_DIR
    
    # Create vitest config if it doesn't exist
    if [[ ! -f "vitest.config.ts" ]]; then
        cat > vitest.config.ts << 'EOF'
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
EOF
    fi
    
    # Create test setup file
    mkdir -p src/test
    cat > src/test/setup.ts << 'EOF'
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock environment variables
vi.mock('../config/env', () => ({
  API_BASE_URL: 'http://localhost:8000',
  APP_NAME: 'LLB Test',
}))

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})
EOF
    
    # Create sample component test
    mkdir -p src/components/common
    cat > src/components/common/Button.test.tsx << 'EOF'
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
})
EOF
    
    cd ..
    
    # AI module tests
    cd $AI_DIR
    
    # Create AI test configuration
    cat > tests/conftest.py << 'EOF'
"""Shared test fixtures for AI module tests."""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "What is sexual health education?"


@pytest.fixture
def sample_chinese_text():
    """Sample Chinese text for testing."""
    return "什么是性健康教育？"


@pytest.fixture
def mock_model_path():
    """Mock model path for testing."""
    return "ai/models/gemma3-keras-gemma3_1b-v3"
EOF
    
    # Create AI module tests
    cat > tests/test_prompt_engine.py << 'EOF'
"""Tests for prompt engineering system."""

import pytest
from prompt_engine import PromptEngine, PromptRequest, InputType


def test_prompt_engine_initialization():
    """Test prompt engine can be initialized."""
    engine = PromptEngine()
    assert engine is not None
    assert hasattr(engine, 'process_request')


def test_basic_prompt_processing(sample_text):
    """Test basic prompt processing."""
    engine = PromptEngine()
    request = PromptRequest(
        content=sample_text,
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    assert response is not None
    assert hasattr(response, 'formatted_prompt')


def test_language_detection(sample_chinese_text):
    """Test language detection functionality."""
    engine = PromptEngine()
    request = PromptRequest(
        content=sample_chinese_text,
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    assert response.language_detected in ['zh-CN', 'zh']


def test_supported_languages():
    """Test getting supported languages."""
    engine = PromptEngine()
    languages = engine.get_supported_languages()
    assert 'en' in languages
    assert 'zh-CN' in languages


def test_available_topics():
    """Test getting available topics."""
    engine = PromptEngine()
    topics = engine.get_available_topics()
    assert 'basic_education' in topics
    assert 'safety' in topics
    assert 'contraception' in topics
EOF
    
    cd ..
    
    print_success "Test infrastructure created"
}

# Function to run comprehensive tests
run_tests() {
    print_header "Running Comprehensive Tests"
    
    # Test backend
    cd $BACKEND_DIR
    source $VENV_NAME/bin/activate
    
    if command_exists pytest; then
        print_status "Running backend unit tests..."
        python -m pytest tests/unit/ -v --tb=short
        
        print_status "Running backend integration tests..."
        python -m pytest tests/integration/ -v --tb=short -m integration
        
        print_status "Running backend test coverage..."
        python -m pytest tests/ --cov=app --cov-report=term-missing --tb=short
    else
        print_error "pytest not available after installation"
        exit 1
    fi
    
    cd ..
    
    # Test frontend
    cd $FRONTEND_DIR
    if [[ -f "package.json" ]] && command_exists yarn; then
        print_status "Running frontend tests..."
        yarn test --run --coverage
    else
        print_warning "Frontend tests not available"
    fi
    
    cd ..
    
    # Test AI modules
    cd $AI_DIR
    if [[ -f "../$BACKEND_DIR/$VENV_NAME/bin/activate" ]]; then
        # shellcheck source=/dev/null
        source "../$BACKEND_DIR/$VENV_NAME/bin/activate"
    else
        print_warning "Virtual environment not found for AI tests"
    fi
    
    if [[ -d "tests" ]]; then
        print_status "Running AI module tests..."
        python -m pytest tests/ -v --tb=short
    else
        print_warning "AI module tests not available"
    fi
    
    cd ..
    
    print_success "All tests completed"
}

# Function to display final instructions
show_final_instructions() {
    print_header "Setup Complete!"
    
    echo -e "${GREEN}🎉 LLB (爱学伴) project setup completed successfully!${NC}"
    echo ""
    echo -e "${CYAN}✅ What was set up:${NC}"
    echo "   - Python 3.11 virtual environment with all dependencies"
    echo "   - Node.js environment with Yarn package manager"
    echo "   - Comprehensive testing infrastructure (pytest, vitest)"
    echo "   - AI model verification (Gemma 3 1B found and verified)"
    echo "   - Git hooks for automated testing"
    echo "   - Development tools (linting, formatting, coverage)"
    echo ""
    echo -e "${CYAN}🚀 Next steps:${NC}"
    echo "1. Review and update configuration files:"
    echo "   - .env (root)"
    echo "   - backend/.env"
    echo "   - frontend/.env"
    echo ""
    echo "2. Start the development environment:"
    echo "   make dev"
    echo ""
    echo "3. Or start services individually:"
    echo "   Backend:  make dev-backend"
    echo "   Frontend: make dev-frontend"
    echo ""
    echo -e "${CYAN}🧪 Testing commands:${NC}"
    echo "   make test           - Run all tests"
    echo "   make test-backend   - Run backend tests only"
    echo "   make test-frontend  - Run frontend tests only"
    echo "   make test-ai        - Run AI module tests only"
    echo "   make coverage       - Generate test coverage reports"
    echo ""
    echo -e "${CYAN}🛠️ Development commands:${NC}"
    echo "   make lint          - Run code linting"
    echo "   make format        - Format code"
    echo "   make clean         - Clean build artifacts"
    echo "   make status        - Check project status"
    echo ""
    echo -e "${CYAN}🌐 Access points:${NC}"
    echo "   Backend API:  http://localhost:8000"
    echo "   Frontend:     http://localhost:3000"
    echo "   API Docs:     http://localhost:8000/docs"
    echo "   Test Coverage: backend/htmlcov/index.html"
    echo ""
    echo -e "${YELLOW}📋 Important notes:${NC}"
    echo "   - Gemma 3 1B model verified and ready to use"
    echo "   - All tests are configured and ready to run"
    echo "   - Git pre-commit hooks will run tests automatically"
    echo "   - Configure environment variables before starting"
    echo ""
    echo -e "${GREEN}🎯 Your LLB project is now fully configured and ready for development!${NC}"
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
    clean_conflicting_files
    create_directories
    setup_python_env
    setup_node_env
    verify_ai_models
    setup_config
    create_test_files
    
    # Optional: run tests
    read -p "Run comprehensive tests? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_tests
    fi
    
    show_final_instructions
}

# Run main function
main "$@"