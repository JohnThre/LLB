#!/bin/bash

# LLB Test Runner Script
# Runs comprehensive tests for both backend and frontend

set -e

echo "🧪 LLB Comprehensive Test Suite"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the LLB project root directory"
    exit 1
fi

# Backend Tests
print_status "Running Backend Tests..."
cd backend

# Check if virtual environment exists
if [ ! -d "llb-env" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3.11 -m venv llb-env
fi

# Activate virtual environment
source llb-env/bin/activate

# Install test dependencies
print_status "Installing test dependencies..."
pip install -r requirements/test.txt > /dev/null 2>&1

# Run backend tests
print_status "Executing backend test suite..."
python -m pytest tests/ \
    --verbose \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --junit-xml=test-results.xml

BACKEND_EXIT_CODE=$?

if [ $BACKEND_EXIT_CODE -eq 0 ]; then
    print_status "✅ Backend tests passed!"
else
    print_error "❌ Backend tests failed!"
fi

# Deactivate virtual environment
deactivate

cd ..

# Frontend Tests
print_status "Running Frontend Tests..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_warning "Node modules not found. Installing..."
    npm install
fi

# Run frontend tests
print_status "Executing frontend test suite..."
npm test -- --run --coverage

FRONTEND_EXIT_CODE=$?

if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
    print_status "✅ Frontend tests passed!"
else
    print_error "❌ Frontend tests failed!"
fi

cd ..

# Summary
echo ""
echo "📊 Test Summary"
echo "==============="

if [ $BACKEND_EXIT_CODE -eq 0 ]; then
    echo -e "Backend:  ${GREEN}✅ PASSED${NC}"
else
    echo -e "Backend:  ${RED}❌ FAILED${NC}"
fi

if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
    echo -e "Frontend: ${GREEN}✅ PASSED${NC}"
else
    echo -e "Frontend: ${RED}❌ FAILED${NC}"
fi

# Overall result
if [ $BACKEND_EXIT_CODE -eq 0 ] && [ $FRONTEND_EXIT_CODE -eq 0 ]; then
    print_status "🎉 All tests passed successfully!"
    echo ""
    echo "Coverage reports:"
    echo "- Backend: backend/htmlcov/index.html"
    echo "- Frontend: frontend/coverage/index.html"
    exit 0
else
    print_error "💥 Some tests failed. Please check the output above."
    exit 1
fi