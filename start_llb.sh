#!/bin/bash

# LLB Startup Script
echo "🚀 Starting LLB System..."

# Activate virtual environment
source llb-env/bin/activate

# Start backend
cd backend
echo "🔧 Starting backend server..."
python main.py 