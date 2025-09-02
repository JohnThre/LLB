#!/bin/bash
# Setup script for LLB AI Providers

echo "🚀 Setting up LLB with AI Providers..."

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ]; then
    echo "❌ Please run this script from the LLB project root directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "backend/llb-env" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3.11 -m venv llb-env
    cd ..
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source backend/llb-env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
echo "📚 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "🎨 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Copy environment files if they don't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️ Please edit .env and add your AI provider API keys"
fi

if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/.env.example backend/.env
    echo "⚠️ Please edit backend/.env and add your AI provider API keys"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/uploads
mkdir -p ai/cache
mkdir -p ai/temp

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env and backend/.env with your AI provider API keys"
echo "2. Configure at least one AI provider:"
echo "   - OpenAI: OPENAI_API_KEY=your_key"
echo "   - Claude: ANTHROPIC_API_KEY=your_key"
echo "   - Gemini: GOOGLE_API_KEY=your_key"
echo "   - Ollama: OLLAMA_ENABLED=true (requires Ollama installed)"
echo "3. Run 'make dev' to start the application"
echo ""
echo "🔗 Get API keys:"
echo "   - OpenAI: https://platform.openai.com/api-keys"
echo "   - Claude: https://console.anthropic.com/"
echo "   - Gemini: https://makersuite.google.com/app/apikey"
echo "   - Ollama: https://ollama.ai/ (local, no API key needed)"
echo ""
echo "🎉 Happy coding!"