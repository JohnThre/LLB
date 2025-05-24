# Whisper Integration Documentation

## Overview

The LLB (爱学伴) project now includes complete Whisper integration for advanced speech-to-text functionality. This implementation provides high-quality audio transcription supporting both Chinese and English languages, optimized for sexual health education conversations.

## Features

### 🎤 **Core Capabilities**
- **Multi-language Support**: Chinese (Simplified), English (US/UK), Auto-detection
- **High Accuracy**: OpenAI Whisper models with confidence scoring
- **Multiple Formats**: WAV, MP3, M4A, OGG, FLAC, AAC
- **GPU Acceleration**: Automatic CUDA detection and utilization
- **Async Processing**: Non-blocking transcription with FastAPI integration

### 🔧 **Technical Features**
- **Model Flexibility**: Configurable model sizes (tiny, base, small, medium, large)
- **Segment Analysis**: Detailed transcription with timestamps and confidence scores
- **Error Handling**: Comprehensive validation and error recovery
- **Memory Management**: Automatic cleanup and CUDA cache management
- **File Validation**: Audio format and size validation

## Architecture

### Backend Components

#### 1. **Audio Service** (`backend/app/services/audio_service.py`)
```python
class AudioService:
    """Service for audio processing operations using Whisper."""
    
    def __init__(self, model_size: str = "base")
    async def initialize()
    async def transcribe_audio(audio_data: bytes, language: str, task: str)
    async def transcribe_upload_file(file: UploadFile, language: str)
    async def cleanup()
```

**Key Methods:**
- `transcribe_audio()`: Core transcription from audio bytes
- `transcribe_upload_file()`: FastAPI file upload transcription
- `get_capabilities()`: Service capability information
- `get_model_info()`: Model status and configuration

#### 2. **API Endpoints** (`backend/app/api/ai.py`)
```python
@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    audio_service: AudioService = Depends(deps.get_audio_service),
)
```

#### 3. **Response Models**
```python
class TranscriptionResponse(BaseModel):
    text: str                    # Transcribed text
    language: str               # Detected/specified language
    confidence: float           # Transcription confidence (0-1)
    duration: float            # Audio duration in seconds
    segments: List[Dict]       # Detailed segments with timestamps
    filename: Optional[str]    # Original filename
```

### Frontend Integration

#### **VoiceInput Component** (`frontend/src/components/common/VoiceInput.tsx`)
- **MediaRecorder API**: Browser-based audio recording
- **Real-time UI**: Recording status and processing indicators
- **Error Handling**: Microphone permissions and network errors
- **Integration**: Seamless chat interface integration

## Installation & Setup

### 1. **Automatic Setup**
```bash
cd backend
./setup_whisper.sh
```

### 2. **Manual Setup**
```bash
# Create virtual environment
python3 -m venv llb-env
source llb-env/bin/activate

# Install dependencies
pip install torch torchvision torchaudio
pip install openai-whisper
pip install -r requirements.txt

# Test installation
python3 test_whisper_integration.py
```

### 3. **Dependencies**
```txt
# Core Whisper
openai-whisper>=20231117
torch>=2.1.0
numpy<2.0.0

# Audio processing
SpeechRecognition==3.10.0
pyttsx3==2.90

# FastAPI integration
fastapi==0.104.1
python-multipart==0.0.6
```

## Configuration

### **Model Sizes**
| Model | Size | VRAM | Speed | Accuracy |
|-------|------|------|-------|----------|
| tiny  | 39MB | ~1GB | Fastest | Good |
| base  | 74MB | ~1GB | Fast | Better |
| small | 244MB | ~2GB | Medium | Good |
| medium| 769MB | ~5GB | Slow | Better |
| large | 1550MB | ~10GB | Slowest | Best |

### **Environment Variables**
```bash
# Model configuration
WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=auto  # auto, cpu, cuda
WHISPER_LANGUAGE=auto  # auto-detect or specific

# File limits
MAX_FILE_SIZE=50MB
UPLOAD_DIR=uploads

# Performance
USE_GPU=true
CUDA_MEMORY_FRACTION=0.8
```

### **Backend Configuration** (`backend/app/config.py`)
```python
class Settings(BaseSettings):
    whisper_model_path: str = "../ai/models/whisper"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_file_types: List[str] = [
        "audio/wav", "audio/mp3", "audio/mpeg",
        "audio/m4a", "audio/ogg", "audio/flac"
    ]
```

## Usage Examples

### **API Usage**
```bash
# Transcribe audio file
curl -X POST "http://localhost:8000/api/ai/transcribe" \
  -F "file=@audio.wav" \
  -F "language=zh"

# Response
{
  "text": "你好，我想了解性健康教育",
  "language": "zh",
  "confidence": 0.95,
  "duration": 3.2,
  "segments": [
    {
      "start": 0.0,
      "end": 3.2,
      "text": "你好，我想了解性健康教育",
      "confidence": 0.95
    }
  ],
  "filename": "audio.wav"
}
```

### **Frontend Integration**
```typescript
// VoiceInput component usage
<VoiceInput
  onTranscriptionComplete={(text) => handleMessage(text)}
  language="zh"
  disabled={isLoading}
/>

// Chat integration
const handleVoiceTranscription = (text: string) => {
  setInput(text);
  handleSend(text);
};
```

### **Python Service Usage**
```python
# Initialize service
audio_service = AudioService(model_size="base")
await audio_service.initialize()

# Transcribe audio
with open("audio.wav", "rb") as f:
    audio_data = f.read()

result = await audio_service.transcribe_audio(
    audio_data, 
    language="zh",
    task="transcribe"
)

print(f"Transcription: {result['text']}")
print(f"Confidence: {result['confidence']:.2f}")
```

## Performance Optimization

### **GPU Optimization**
```python
# Automatic GPU detection
device = "cuda" if torch.cuda.is_available() else "cpu"

# FP16 precision for speed
options = {
    "fp16": device == "cuda",
    "task": "transcribe"
}

# Memory management
if torch.cuda.is_available():
    torch.cuda.empty_cache()
```

### **Model Caching**
- Models are cached after first download
- Automatic model reuse across sessions
- Configurable cache directory

### **Async Processing**
```python
# Non-blocking transcription
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(
    None, self._transcribe_file, file_path, language
)
```

## Error Handling

### **Common Errors & Solutions**

#### 1. **Model Download Issues**
```bash
# Clear cache and retry
rm -rf ~/.cache/whisper
python3 -c "import whisper; whisper.load_model('base')"
```

#### 2. **CUDA Out of Memory**
```python
# Use smaller model
audio_service = AudioService(model_size="tiny")

# Or force CPU
audio_service = AudioService(model_size="base")
audio_service.device = "cpu"
```

#### 3. **Audio Format Issues**
```python
# Supported formats
valid_extensions = {'.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac'}

# Convert if needed
ffmpeg -i input.mp4 -acodec pcm_s16le -ar 16000 output.wav
```

### **Error Response Format**
```json
{
  "error": "Transcription failed",
  "detail": "Unsupported file type: .txt",
  "status_code": 400
}
```

## Testing

### **Integration Tests**
```bash
# Run comprehensive tests
cd backend
python3 test_whisper_integration.py

# Test specific functionality
python3 -c "
from app.services.audio_service import AudioService
import asyncio

async def test():
    service = AudioService('tiny')
    await service.initialize()
    print('✅ Service ready')
    
asyncio.run(test())
"
```

### **Performance Benchmarks**
| Model | File Size | Duration | Processing Time | Memory |
|-------|-----------|----------|----------------|---------|
| tiny  | 1MB WAV   | 30s      | ~2s           | ~500MB  |
| base  | 1MB WAV   | 30s      | ~3s           | ~800MB  |
| small | 1MB WAV   | 30s      | ~5s           | ~1.5GB  |

## Troubleshooting

### **Common Issues**

#### 1. **Service Not Ready**
```python
# Check service status
if not audio_service.is_ready():
    await audio_service.initialize()
```

#### 2. **Language Detection Issues**
```python
# Force specific language
result = await audio_service.transcribe_audio(
    audio_data, 
    language="zh"  # Don't use "auto"
)
```

#### 3. **File Size Limits**
```python
# Check file size
if len(audio_data) > settings.max_file_size:
    raise ValueError("File too large")
```

### **Debug Mode**
```python
# Enable detailed logging
import logging
logging.getLogger("whisper").setLevel(logging.DEBUG)

# Check model info
model_info = audio_service.get_model_info()
print(f"Model loaded: {model_info['is_loaded']}")
print(f"Device: {model_info['device']}")
```

## Security Considerations

### **File Validation**
- File type validation by extension and MIME type
- File size limits (default 50MB)
- Temporary file cleanup
- Input sanitization

### **Privacy**
- Audio files processed locally (no external API calls)
- Temporary files automatically deleted
- No audio data persistence
- GDPR compliant processing

## Future Enhancements

### **Planned Features**
1. **Real-time Streaming**: WebRTC integration for live transcription
2. **Voice Activity Detection**: Automatic speech detection
3. **Speaker Diarization**: Multiple speaker identification
4. **Custom Models**: Fine-tuned models for sexual health terminology
5. **Audio Preprocessing**: Noise reduction and enhancement

### **Performance Improvements**
1. **Model Quantization**: INT8 quantization for faster inference
2. **Batch Processing**: Multiple file transcription
3. **Caching**: Intelligent result caching
4. **Compression**: Audio compression for faster uploads

## Support

### **Documentation**
- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyTorch Documentation](https://pytorch.org/docs/)

### **Community**
- GitHub Issues: Report bugs and feature requests
- Discussions: Technical questions and improvements
- Wiki: Additional examples and tutorials

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Compatibility**: Python 3.8+, PyTorch 2.1+, Whisper 20231117+ 