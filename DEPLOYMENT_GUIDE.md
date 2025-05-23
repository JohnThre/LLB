# LLB Deployment Guide

## 🎯 Overview

This guide will help you deploy the LLB (爱学伴) sexual health education system locally on your Ubuntu 22 LTS WSL2 environment with Windows 11 Pro.

## 📋 Prerequisites

### Hardware Requirements
- **Minimum**: Intel 8th gen mobile i7, 16GB RAM
- **Recommended**: Intel 9th gen desktop i7, 32GB RAM, NVIDIA RTX 3060 12GB
- **Your System**: Intel 9th gen desktop i7, 32GB DDR4, RTX 3060 OC 12GB ✅

### Software Requirements
- Ubuntu 22 LTS WSL2 ✅
- Python 3.11 ✅
- CUDA 12.8 and cuDNN ✅
- Git

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)

```bash
# Make deployment script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

### Option 2: Manual Deployment

Follow the step-by-step instructions below.

## 📝 Step-by-Step Manual Deployment

### 1. Environment Setup

```bash
# Check Python version
python3.11 --version

# Check CUDA
nvidia-smi

# Check GPU memory
nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install core dependencies
pip install -r requirements.txt

# Install PyTorch with CUDA 12.1 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install optional dependencies
pip install SpeechRecognition pyttsx3 PyPDF2 pdfplumber

cd ..
```

### 4. Test Prompt System

```bash
# Test the prompt engineering system
python test_prompt_system.py
```

Expected output:
```
✓ Successfully imported prompt engine
✓ Engine initialized successfully
✓ English request processed successfully
✓ Chinese request processed successfully
✓ Henan dialect request processed successfully
✓ Safety assessment working
✓ Document analysis working
🎉 LLB Prompt Engineering System is working correctly!
```

### 5. Create Necessary Directories

```bash
mkdir -p logs static uploads models
```

### 6. Start the System

```bash
# Start backend server
cd backend
python main.py
```

## 🌐 Accessing the System

Once deployed, you can access:

- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Backend configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Model configuration
MODEL_NAME=google/gemma-3-1b
MAX_LENGTH=2048
MAX_NEW_TOKENS=512

# GPU configuration
CUDA_VISIBLE_DEVICES=0
TORCH_DTYPE=float16

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/llb.log
```

### Model Configuration

The system will automatically download the Gemma 3 1B model on first run. For your RTX 3060 12GB:

```python
# Optimized settings for RTX 3060 12GB
model_kwargs = {
    "torch_dtype": torch.float16,
    "device_map": "auto",
    "low_cpu_mem_usage": True,
    "use_cache": True,
}

generation_config = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "do_sample": True,
}
```

## 🧪 Testing the Deployment

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "supported_languages": ["en", "zh-CN", "zh-CN-henan"],
  "available_topics": ["basic_education", "safety", "contraception", "anatomy", "relationship", "sti", "consent"]
}
```

### 2. Chat API Test

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is sexual health?",
    "language": "en"
  }'
```

### 3. Multilingual Test

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "什么是性健康？",
    "cultural_context": "chinese"
  }'
```

## 🔄 Service Management

### Using systemd (Linux)

```bash
# Copy service file
sudo cp llb.service /etc/systemd/system/

# Enable service
sudo systemctl enable llb

# Start service
sudo systemctl start llb

# Check status
sudo systemctl status llb

# View logs
sudo journalctl -u llb -f
```

### Manual Start/Stop

```bash
# Start
./start_llb.sh

# Stop (Ctrl+C or)
pkill -f "python main.py"
```

## 📊 Performance Optimization

### For RTX 3060 12GB

1. **Memory Optimization**:
   ```python
   # Enable gradient checkpointing
   model.gradient_checkpointing_enable()
   
   # Use mixed precision
   torch.backends.cudnn.benchmark = True
   ```

2. **Batch Processing**:
   ```python
   # Optimize batch size for 12GB VRAM
   batch_size = 4  # Adjust based on sequence length
   ```

3. **Model Compilation** (PyTorch 2.0+):
   ```python
   # Compile model for faster inference
   model = torch.compile(model)
   ```

### CPU Fallback

If GPU is not available:
```bash
# Install CPU-only PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## 🛡️ Security Considerations

### Local Deployment Security

1. **Network Access**:
   - System runs on localhost by default
   - No external network access required
   - All data processed locally

2. **Data Privacy**:
   - No user data sent to external services
   - All conversations processed locally
   - Optional audio/document processing

3. **Content Filtering**:
   - Built-in safety assessment
   - Age-appropriate content filtering
   - Medical advice boundaries

## 🔍 Troubleshooting

### Common Issues

1. **CUDA Out of Memory**:
   ```bash
   # Reduce model precision
   export TORCH_DTYPE=float16
   
   # Reduce batch size
   export MAX_NEW_TOKENS=256
   ```

2. **Model Download Issues**:
   ```bash
   # Clear cache and retry
   rm -rf ~/.cache/huggingface/
   python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('google/gemma-3-1b')"
   ```

3. **Audio Dependencies**:
   ```bash
   # Install system dependencies
   sudo apt-get install portaudio19-dev python3-pyaudio
   pip install pyaudio
   ```

4. **PDF Processing Issues**:
   ```bash
   # Install system dependencies
   sudo apt-get install poppler-utils
   ```

### Log Analysis

```bash
# View application logs
tail -f logs/llb.log

# Check system resources
htop
nvidia-smi -l 1
```

## 📈 Monitoring

### System Metrics

```bash
# GPU monitoring
watch -n 1 nvidia-smi

# Memory usage
free -h

# Disk usage
df -h
```

### Application Metrics

Access metrics at: http://localhost:8000/health

Monitor:
- Model loading status
- Response times
- Memory usage
- Error rates

## 🔄 Updates and Maintenance

### Updating the System

```bash
# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r backend/requirements.txt --upgrade

# Restart service
sudo systemctl restart llb
```

### Model Updates

```bash
# Clear model cache
rm -rf ~/.cache/huggingface/transformers/

# Restart to download latest model
sudo systemctl restart llb
```

## 🎯 Production Considerations

### For Production Deployment

1. **Reverse Proxy** (nginx):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. **SSL/TLS**:
   ```bash
   # Use Let's Encrypt
   sudo certbot --nginx -d your-domain.com
   ```

3. **Process Management**:
   ```bash
   # Use supervisor or systemd
   # Monitor with tools like Prometheus/Grafana
   ```

## 📞 Support

### Getting Help

1. **Check Logs**: `tail -f logs/llb.log`
2. **Health Check**: http://localhost:8000/health
3. **Test System**: `python test_prompt_system.py`

### Common Commands

```bash
# Full restart
sudo systemctl restart llb

# Check status
curl http://localhost:8000/health

# View logs
sudo journalctl -u llb -f

# Test prompt system
python test_prompt_system.py
```

## ✅ Deployment Checklist

- [ ] Python 3.11 installed
- [ ] CUDA 12.8 available
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Prompt system tested
- [ ] Model downloaded
- [ ] Service configured
- [ ] Health check passing
- [ ] API endpoints working
- [ ] Multilingual support tested

## 🎉 Success!

Your LLB sexual health education system is now deployed and ready to provide safe, accurate, and culturally appropriate education to users in mainland China.

**Access Points**:
- Main App: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

**Features Available**:
- ✅ Text-based chat in English, Chinese, and Henan dialect
- ✅ Voice input support (optional)
- ✅ PDF document analysis (optional)
- ✅ Cultural sensitivity and safety filtering
- ✅ Local processing with Gemma 3 1B model
- ✅ GPU acceleration on RTX 3060 