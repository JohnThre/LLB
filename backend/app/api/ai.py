"""
FastAPI routes for AI functionality in the LLB application.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
import logging
logger = logging.getLogger(__name__)
from pydantic import BaseModel, Field

from app.api import deps
from app.services.audio_service import AudioService
from app.core.exceptions import (
    AudioFormatException,
    AudioServiceUnavailableException,
    AudioTranscriptionException,
    AudioTTSException,
)

# Create router
router = APIRouter(prefix="/api/ai", tags=["AI"])

# Placeholder for AI functionality
def get_ai_service():
    """
    Placeholder for AI service.
    
    Returns:
        dict: Mock AI service
    """
    return {"status": "mock"}


# === Models for requests and responses ===


class TextGenerationRequest(BaseModel):
    """Request model for text generation."""

    prompt: str = Field(..., description="The prompt for text generation")
    max_length: int = Field(
        512, description="Maximum length of the generated text"
    )
    temperature: float = Field(0.7, description="Temperature for sampling")
    top_p: float = Field(0.95, description="Nucleus sampling parameter")
    top_k: int = Field(50, description="Top-k sampling parameter")


class TextGenerationResponse(BaseModel):
    """Response model for text generation."""

    generated_text: str = Field(..., description="Generated text")


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat completion."""

    messages: List[ChatMessage] = Field(..., description="Chat messages")
    max_length: int = Field(1024, description="Maximum length of the response")
    temperature: float = Field(0.7, description="Temperature for sampling")


class ChatResponse(BaseModel):
    """Response model for chat completion."""

    response: str = Field(..., description="Chat response")


class LanguageDetectionRequest(BaseModel):
    """Request model for language detection."""

    text: str = Field(..., description="Text to detect language from")


class LanguageDetectionResponse(BaseModel):
    """Response model for language detection."""

    language: str = Field(..., description="Detected language code")
    confidence: float = Field(..., description="Detection confidence")
    supported: bool = Field(
        ..., description="Whether the language is supported"
    )


class TranscriptionResponse(BaseModel):
    """Response model for transcription."""

    text: str = Field(..., description="Transcribed text")
    language: str = Field(..., description="Detected or specified language")
    confidence: float = Field(..., description="Transcription confidence score")
    duration: float = Field(..., description="Audio duration in seconds")
    segments: List[Dict[str, Any]] = Field(default=[], description="Transcription segments")
    filename: Optional[str] = Field(None, description="Original filename")


class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech."""

    text: str = Field(..., description="Text to convert to speech")
    language: Optional[str] = Field("en", description="Language code (zh, en)")
    voice_settings: Optional[Dict[str, Any]] = Field(None, description="Voice configuration")


class TextToSpeechResponse(BaseModel):
    """Response model for text-to-speech."""

    success: bool = Field(..., description="Whether TTS was successful")
    audio_url: Optional[str] = Field(None, description="URL to download audio file")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    language: str = Field(..., description="Language used for TTS")


class DocumentProcessingResponse(BaseModel):
    """Response model for document processing."""

    title: str = Field(..., description="Document title")
    author: str = Field(..., description="Document author")
    num_pages: int = Field(..., description="Number of pages")
    pages: List[Dict[str, Any]] = Field(
        ..., description="Extracted pages content"
    )


class ModelStatusResponse(BaseModel):
    """Response model for model status."""

    status: str = Field(..., description="Model status (loading, ready, error)")
    modelName: str = Field(..., description="Name of the AI model")
    lastUpdated: Optional[str] = Field(None, description="Last update timestamp")


class ModelSettingsRequest(BaseModel):
    """Request model for model settings."""

    temperature: float = Field(0.7, description="Temperature for sampling")
    maxTokens: int = Field(2048, description="Maximum tokens to generate")
    topP: float = Field(0.95, description="Top-p sampling parameter")
    topK: int = Field(40, description="Top-k sampling parameter")
    useQuantization: bool = Field(True, description="Whether to use quantization")


class ModelSettingsResponse(BaseModel):
    """Response model for model settings."""

    temperature: float = Field(..., description="Temperature for sampling")
    maxTokens: int = Field(..., description="Maximum tokens to generate")
    topP: float = Field(..., description="Top-p sampling parameter")
    topK: int = Field(..., description="Top-k sampling parameter")
    useQuantization: bool = Field(..., description="Whether to use quantization")


# === API Routes ===


@router.get("/model/status", response_model=ModelStatusResponse)
async def get_model_status():
    """
    Get the current status of the AI model.

    Returns:
        ModelStatusResponse: The model status information
    """
    try:
        # Return mock status for now
        return ModelStatusResponse(
            status="ready",
            modelName="Gemma 3 1B",
            lastUpdated=None
        )
    except Exception as e:
        logger.error(f"Model status check error: {str(e)}")
        return ModelStatusResponse(
            status="error",
            modelName="Gemma 3 1B",
            lastUpdated=None
        )


@router.get("/model/settings", response_model=ModelSettingsResponse)
async def get_model_settings():
    """
    Get the current model settings.

    Returns:
        ModelSettingsResponse: The current model settings
    """
    try:
        # Return default settings for now
        return ModelSettingsResponse(
            temperature=0.7,
            maxTokens=2048,
            topP=0.95,
            topK=40,
            useQuantization=True
        )
    except Exception as e:
        logger.error(f"Model settings fetch error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch model settings: {str(e)}"
        )


@router.post("/model/settings", response_model=ModelSettingsResponse)
async def update_model_settings(
    request: ModelSettingsRequest
):
    """
    Update the model settings.

    Args:
        request: Model settings to update

    Returns:
        ModelSettingsResponse: The updated model settings
    """
    try:
        # For now, just return the settings that were sent
        # In a real implementation, these would be saved and applied to the model
        return ModelSettingsResponse(
            temperature=request.temperature,
            maxTokens=request.maxTokens,
            topP=request.topP,
            topK=request.topK,
            useQuantization=request.useQuantization
        )
    except Exception as e:
        logger.error(f"Model settings update error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update model settings: {str(e)}"
        )


@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(
    request: TextGenerationRequest,
):
    """
    Generate text based on the provided prompt.

    Args:
        request: Text generation parameters

    Returns:
        TextGenerationResponse: The generated text
    """
    try:
        # Mock response for now
        generated_text = f"Mock response to: {request.prompt[:50]}..."
        return TextGenerationResponse(generated_text=generated_text)

    except Exception as e:
        logger.error(f"Text generation error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Text generation failed: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest
):
    """
    Generate a response in a conversational context.

    Args:
        request: Chat parameters

    Returns:
        ChatResponse: The generated response
    """
    try:
        # Mock response for now
        last_message = request.messages[-1].content if request.messages else "Hello"
        response = f"Mock AI response to: {last_message[:50]}..."

        return ChatResponse(response=response)

    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Chat completion failed: {str(e)}"
        )


@router.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(
    request: LanguageDetectionRequest,
):
    """
    Detect the language of the provided text.

    Args:
        request: Language detection parameters

    Returns:
        LanguageDetectionResponse: The detected language
    """
    try:
        # Mock language detection
        return LanguageDetectionResponse(
            language="en",
            confidence=0.95,
            supported=True,
        )

    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Language detection failed: {str(e)}"
        )


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    audio_service: AudioService = Depends(deps.get_audio_service),
):
    """
    Transcribe audio from an uploaded file using Whisper.

    Args:
        file: Audio file (wav, mp3, m4a, ogg, flac, aac)
        language: Optional language code (zh, en, auto)
        audio_service: Audio service dependency

    Returns:
        TranscriptionResponse: The transcription result with confidence and segments
    """
    try:
        logger.info(f"Transcribing audio file: {file.filename}")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
            
        # Check if audio service is ready
        if not audio_service.is_ready():
            raise HTTPException(
                status_code=503, 
                detail="Audio service not ready. Please try again later."
            )
        
        # Use the audio service's file transcription method
        result = await audio_service.transcribe_upload_file(file, language)
        
        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            confidence=result["confidence"],
            duration=result["duration"],
            segments=result["segments"],
            filename=result.get("filename")
        )

    except AudioFormatException as e:
        logger.warning(f"Audio format error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except AudioServiceUnavailableException as e:
        logger.error(f"Audio service unavailable: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))
    except AudioTranscriptionException as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected transcription error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Transcription failed: {str(e)}"
        )


@router.post("/text-to-speech", response_model=TextToSpeechResponse)
async def text_to_speech(
    request: TextToSpeechRequest,
    audio_service: AudioService = Depends(deps.get_audio_service),
):
    """
    Convert text to speech using TTS engine.

    Args:
        request: Text-to-speech parameters
        audio_service: Audio service dependency

    Returns:
        TextToSpeechResponse: The TTS result with audio URL
    """
    try:
        logger.info(f"Converting text to speech: {request.text[:50]}...")
        
        # Check if TTS service is ready
        if not audio_service.is_tts_ready():
            raise HTTPException(
                status_code=503, 
                detail="Text-to-speech service not ready. Please try again later."
            )
        
        # Generate speech audio
        audio_bytes = await audio_service.text_to_speech(
            request.text, 
            request.language,
            request.voice_settings
        )
        
        # Save audio to temporary file and create URL
        import uuid
        audio_id = str(uuid.uuid4())
        audio_filename = f"tts_{audio_id}.wav"
        
        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads/audio")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        audio_path = uploads_dir / audio_filename
        with open(audio_path, 'wb') as f:
            f.write(audio_bytes)
        
        # Calculate duration (rough estimate)
        duration = len(audio_bytes) / (16000 * 2)  # Assuming 16kHz, 16-bit
        
        return TextToSpeechResponse(
            success=True,
            audio_url=f"/static/audio/{audio_filename}",
            duration=duration,
            language=request.language or "en"
        )

    except AudioTTSException as e:
        logger.warning(f"TTS error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except AudioServiceUnavailableException as e:
        logger.error(f"TTS service unavailable: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected TTS error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Text-to-speech failed: {str(e)}"
        )


@router.get("/voices", response_model=List[Dict[str, str]])
async def get_available_voices(
    audio_service: AudioService = Depends(deps.get_audio_service),
):
    """
    Get list of available TTS voices.

    Args:
        audio_service: Audio service dependency

    Returns:
        List of available voices with their information
    """
    try:
        if not audio_service.is_tts_ready():
            return []
        
        voices = audio_service.get_available_voices()
        return voices

    except Exception as e:
        logger.error(f"Error getting voices: {str(e)}")
        return []


@router.post("/process-document", response_model=DocumentProcessingResponse)
async def process_document(
    file: UploadFile = File(...),
):
    """
    Process a PDF document.

    Args:
        file: PDF file

    Returns:
        DocumentProcessingResponse: The extracted content
    """
    try:
        # Check file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400, detail="Only PDF files are supported"
            )

        # Read the file
        pdf_bytes = await file.read()

        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Empty file")

        # Mock document processing
        return DocumentProcessingResponse(
            title="Mock Document Title",
            author="Mock Author",
            num_pages=1,
            pages=[{"page": 1, "content": "Mock document content"}],
        )

    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Document processing failed: {str(e)}"
        )


# Cleanup function for background tasks
def cleanup_resources():
    """Clean up AI resources when the application shuts down."""
    global _ai_factory
    if _ai_factory:
        logger.info("Cleaning up AI resources")
        _ai_factory.shutdown()
        _ai_factory = None
