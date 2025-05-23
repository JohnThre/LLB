#!/bin/bash

# Run backend server for LLB application

# Activate virtual environment if not already activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Activating virtual environment..."
    source llb-env/bin/activate
fi

# Set environment variables
export PYTHONPATH="$(pwd)"

# Run the FastAPI server
echo "Starting LLB backend server..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo "Server stopped." 