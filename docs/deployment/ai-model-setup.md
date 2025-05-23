# AI Model Setup Guide

This guide explains how to properly set up the AI models for LLB (爱学伴), including downloading the Gemma 3 1B model from Kaggle and configuring the system for optimal performance.

## 📋 Overview

LLB uses two main AI models:
- **Gemma 3 1B**: Primary language model for generating responses
- **Whisper**: Speech-to-text model for voice input (auto-downloaded)

## 🎯 Gemma 3 1B Model Setup

### Prerequisites

1. **Kaggle Account**: Create a free account at [kaggle.com](https://www.kaggle.com)
2. **Disk Space**: At least 5GB free space for the model
3. **Internet**: Stable connection for downloading (~2GB)

### Step 1: Download from Kaggle

1. **Navigate to the model page**:
   - Go to: https://www.kaggle.com/models/google/gemma/keras/gemma_1.1_instruct_2b_en
   - Or search for "Gemma Keras" on Kaggle

2. **Accept terms and download**:
   - Click "Download" button
   - Accept Google's terms of use
   - Select the **1B parameter version** (not 2B or 7B)
   - Download will be a ZIP file (~2GB)

3. **Alternative download methods**:
   ```bash
   # Using Kaggle API (if you have it configured)
   kaggle models download google/gemma/keras/gemma_1.1_instruct_2b_en
   ```

### Step 2: Extract and Place Model

1. **Create the model directory**:
   ```bash
   mkdir -p ai/models/gemma3-keras-gemma3_1b-v3
   ```

2. **Extract the downloaded ZIP**:
   ```bash
   # Extract to the correct location
   unzip gemma_1.1_instruct_2b_en.zip -d ai/models/gemma3-keras-gemma3_1b-v3/
   ```

3. **Verify file structure**:
   ```
   ai/models/gemma3-keras-gemma3_1b-v3/
   ├── config.json
   ├── metadata.json
   ├── model.weights.h5
   ├── preprocessor.json
   ├── task.json
   ├── tokenizer.json
   └── assets/
       └── (vocabulary files)
   ```

### Step 3: Verify Installation

Run the verification script:
```bash
./scripts/setup/setup_project.sh
```

Or manually verify:
```bash
python3 -c "
import os
model_path = 'ai/models/gemma3-keras-gemma3_1b-v3'
required_files = ['config.json', 'model.weights.h5', 'tokenizer.json', 'task.json', 'metadata.json', 'preprocessor.json']
missing = [f for f in required_files if not os.path.exists(f'{model_path}/{f}')]
if missing:
    print(f'Missing files: {missing}')
else:
    print('✅ All required files found!')
"
```

## 🎤 Whisper Model Setup

Whisper models are downloaded automatically when first used. No manual setup required.

### Configuration Options

In `backend/.env`:
```bash
# Whisper model size (tiny, base, small, medium, large)
WHISPER_MODEL_SIZE=base

# Supported languages
WHISPER_LANGUAGES=en,zh

# Cache directory
WHISPER_CACHE_DIR=ai/models/whisper
```

### Model Sizes and Performance

| Model | Size | Speed | Accuracy | Recommended For |
|-------|------|-------|----------|-----------------|
| tiny  | 39MB | Fastest | Good | Testing, low-end hardware |
| base  | 74MB | Fast | Better | **Default choice** |
| small | 244MB | Medium | Good | Better accuracy needed |
| medium| 769MB | Slow | Very Good | High accuracy required |
| large | 1550MB | Slowest | Best | Maximum accuracy |

## ⚙️ Configuration

### Backend Configuration

Edit `backend/.env`:
```bash
# Gemma Model Configuration
GEMMA_MODEL_PATH=ai/models/gemma3-keras-gemma3_1b-v3
GEMMA_MAX_TOKENS=512
GEMMA_TEMPERATURE=0.7
GEMMA_TOP_P=0.9

# Whisper Configuration
WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=auto  # auto, cpu, cuda
WHISPER_LANGUAGE=auto  # auto-detect or specific language

# Performance Settings
USE_GPU=true
GPU_MEMORY_FRACTION=0.8
BATCH_SIZE=1

# Supported Languages
SUPPORTED_LANGUAGES=en,zh-CN,zh-TW
DEFAULT_LANGUAGE=en
```

### Hardware-Specific Settings

#### For RTX 3060 12GB (Recommended)
```bash
USE_GPU=true
GPU_MEMORY_FRACTION=0.8
GEMMA_MAX_TOKENS=512
WHISPER_MODEL_SIZE=base
BATCH_SIZE=2
```

#### For 16GB RAM (Minimum)
```bash
USE_GPU=false
GEMMA_MAX_TOKENS=256
WHISPER_MODEL_SIZE=tiny
BATCH_SIZE=1
```

#### For 32GB RAM (Optimal)
```bash
USE_GPU=true
GPU_MEMORY_FRACTION=0.9
GEMMA_MAX_TOKENS=1024
WHISPER_MODEL_SIZE=small
BATCH_SIZE=4
```

## 🧪 Testing AI Models

### Basic Model Test

```bash
# Test Gemma model loading
cd backend
source llb-env/bin/activate
python -c "
from app.ai.gemma_client import GemmaClient
client = GemmaClient()
response = client.generate('What is sexual health?')
print(f'Response: {response}')
"
```

### Comprehensive AI Tests

```bash
# Run all AI module tests
make test-ai

# Run specific tests
cd ai
python -m pytest tests/test_gemma_integration.py -v
python -m pytest tests/test_whisper_integration.py -v
python -m pytest tests/test_multilingual.py -v
```

### Performance Benchmarks

```bash
# Run performance tests
python scripts/benchmark_ai.py

# Test memory usage
python scripts/monitor_memory.py

# Test response times
python scripts/benchmark_response_time.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Model not found" Error
```bash
# Check if model exists
ls -la ai/models/gemma3-keras-gemma3_1b-v3/

# Verify all files are present
python scripts/verify_model.py
```

#### 2. "Out of Memory" Error
```bash
# Reduce model parameters in backend/.env
GEMMA_MAX_TOKENS=256
GPU_MEMORY_FRACTION=0.6
BATCH_SIZE=1
```

#### 3. "CUDA not available" Warning
```bash
# Check CUDA installation
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"

# Force CPU mode if needed
USE_GPU=false
```

#### 4. Slow Response Times
```bash
# Optimize settings for your hardware
WHISPER_MODEL_SIZE=tiny
GEMMA_MAX_TOKENS=256
USE_GPU=true
```

#### 5. Model Loading Fails
```bash
# Check file permissions
chmod -R 755 ai/models/

# Verify file integrity
python scripts/verify_model_integrity.py
```

### Performance Optimization

#### For Development
```bash
# Fast startup, lower accuracy
WHISPER_MODEL_SIZE=tiny
GEMMA_MAX_TOKENS=128
GEMMA_TEMPERATURE=0.5
```

#### For Production
```bash
# Better accuracy, slower startup
WHISPER_MODEL_SIZE=base
GEMMA_MAX_TOKENS=512
GEMMA_TEMPERATURE=0.7
```

## 📊 Model Information

### Gemma 3 1B Specifications
- **Parameters**: 1 billion
- **Context Length**: 8192 tokens
- **Languages**: Primarily English, some multilingual capability
- **File Size**: ~2GB
- **Memory Requirements**: 4-6GB RAM minimum

### Whisper Specifications
- **Languages**: 99 languages supported
- **Input**: Audio files (WAV, MP3, etc.)
- **Output**: Text transcription with timestamps
- **Real-time**: Supports streaming transcription

## 🔄 Model Updates

### Updating Gemma Model
1. Download new version from Kaggle
2. Extract to temporary directory
3. Test with new model
4. Replace old model files
5. Update configuration if needed

### Updating Whisper Model
Whisper models update automatically through the OpenAI Whisper library.

## 📝 Best Practices

1. **Always verify model integrity** after download
2. **Test models** before deploying to production
3. **Monitor memory usage** during operation
4. **Keep backups** of working model configurations
5. **Document any custom modifications**

## 🆘 Getting Help

- **Model Issues**: Check the [Kaggle model page](https://www.kaggle.com/models/google/gemma)
- **Technical Support**: Open an issue in the project repository
- **Performance Questions**: See the performance optimization guide
- **Community**: Join our discussion forums

---

*This guide is part of the LLB (爱学伴) documentation. For more information, see the main README.md file.* 