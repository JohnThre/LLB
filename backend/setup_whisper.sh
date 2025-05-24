#!/bin/bash
# Setup script for Whisper integration in LLB Backend

set -e

echo "🎤 Setting up Whisper integration for LLB Backend..."

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "llb-env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv llb-env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source llb-env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install PyTorch first (for better compatibility)
echo "🔥 Installing PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install Whisper and dependencies
echo "🎵 Installing OpenAI Whisper..."
pip install openai-whisper

# Install other audio dependencies
echo "📢 Installing audio processing libraries..."
pip install SpeechRecognition pyttsx3 edge-tts

# Install other requirements
echo "📋 Installing other requirements..."
pip install -r requirements.txt

# Test Whisper installation
echo "🧪 Testing Whisper installation..."
python3 -c "
import whisper
import torch
print('✅ Whisper imported successfully')
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')

# Test model loading
print('📥 Testing model download...')
model = whisper.load_model('tiny')
print('✅ Whisper tiny model loaded successfully')
"

# Create whisper models directory
echo "📁 Creating Whisper models directory..."
mkdir -p ../ai/models/whisper

# Test the audio service
echo "🎯 Testing audio service integration..."
if [ -f "test_whisper_integration.py" ]; then
    python3 test_whisper_integration.py
else
    echo "⚠️ Test script not found, skipping integration test"
fi

echo ""
echo "🎉 Whisper integration setup complete!"
echo ""
echo "📋 Summary:"
echo "  ✅ Virtual environment: llb-env"
echo "  ✅ PyTorch installed"
echo "  ✅ OpenAI Whisper installed"
echo "  ✅ Audio processing libraries installed"
echo "  ✅ Models directory created"
echo ""
echo "🚀 To start the backend with Whisper support:"
echo "  1. source llb-env/bin/activate"
echo "  2. python3 -m app.main"
echo ""
echo "🎤 Supported audio formats: WAV, MP3, M4A, OGG, FLAC, AAC"
echo "🌍 Supported languages: Chinese (zh), English (en), Auto-detect"
echo "" 