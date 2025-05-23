"""
FastAPI routes for AI functionality in the LLB application.
"""

import os
import json
from typing import List, Dict, Any, Optional
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from loguru import logger

# Import AI factory and models
from ai.factory import AIFactory

# Create router
router = APIRouter(prefix="/api/ai", tags=["AI"])

# Global AI factory instance
_ai_factory = None


def get_ai_factory():
    """
    Get or create the global AI factory instance.
    
    Returns:
        AIFactory: The global AIFactory instance
    """
    global _ai_factory
    if _ai_factory is None:
        logger.info("Creating new AIFactory")
        _ai_factory = AIFactory()
    return _ai_factory


# === Models for requests and responses ===

class TextGenerationRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="The prompt for text generation")
    max_length: int = Field(512, description="Maximum length of the generated text")
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
    supported: bool = Field(..., description="Whether the language is supported")


class TranscriptionResponse(BaseModel):
    """Response model for transcription."""
    text: str = Field(..., description="Transcribed text")
    language: str = Field(..., description="Detected or specified language")


class DocumentProcessingResponse(BaseModel):
    """Response model for document processing."""
    title: str = Field(..., description="Document title")
    author: str = Field(..., description="Document author")
    num_pages: int = Field(..., description="Number of pages")
    pages: List[Dict[str, Any]] = Field(..., description="Extracted pages content")


# === API Routes ===

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(
    request: TextGenerationRequest,
    ai_factory: AIFactory = Depends(get_ai_factory)
):
    """
    Generate text based on the provided prompt.
    
    Args:
        request: Text generation parameters
        ai_factory: AIFactory instance
        
    Returns:
        TextGenerationResponse: The generated text
    """
    try:
        generated_text = ai_factory.generate_text(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
        )
        
        return TextGenerationResponse(generated_text=generated_text)
    
    except Exception as e:
        logger.error(f"Text generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    ai_factory: AIFactory = Depends(get_ai_factory)
):
    """
    Generate a response in a conversational context.
    
    Args:
        request: Chat parameters
        ai_factory: AIFactory instance
        
    Returns:
        ChatResponse: The generated response
    """
    try:
        # Convert messages to the format expected by the AI factory
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        response = ai_factory.chat(
            messages=messages,
            max_length=request.max_length,
            temperature=request.temperature,
        )
        
        return ChatResponse(response=response)
    
    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")


@router.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(
    request: LanguageDetectionRequest,
    ai_factory: AIFactory = Depends(get_ai_factory)
):
    """
    Detect the language of the provided text.
    
    Args:
        request: Language detection parameters
        ai_factory: AIFactory instance
        
    Returns:
        LanguageDetectionResponse: The detected language
    """
    try:
        result = ai_factory.detect_language(request.text)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return LanguageDetectionResponse(
            language=result["language"],
            confidence=result.get("confidence", 0.0),
            supported=result.get("supported", False),
        )
    
    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    ai_factory: AIFactory = Depends(get_ai_factory)
):
    """
    Transcribe audio from an uploaded file.
    
    Args:
        file: Audio file
        language: Optional language code
        ai_factory: AIFactory instance
        
    Returns:
        TranscriptionResponse: The transcription result
    """
    try:
        # Read the file
        audio_bytes = await file.read()
        
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Process the audio
        result = ai_factory.transcribe_audio(
            audio_data=audio_bytes,
            is_file_path=False,
            language=language,
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return TranscriptionResponse(
            text=result.get("text", ""),
            language=result.get("language", "unknown"),
        )
    
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/process-document", response_model=DocumentProcessingResponse)
async def process_document(
    file: UploadFile = File(...),
    ai_factory: AIFactory = Depends(get_ai_factory)
):
    """
    Process a PDF document.
    
    Args:
        file: PDF file
        ai_factory: AIFactory instance
        
    Returns:
        DocumentProcessingResponse: The extracted content
    """
    try:
        # Check file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read the file
        pdf_bytes = await file.read()
        
        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Process the document
        result = ai_factory.process_document(
            document_data=pdf_bytes,
            is_file_path=False,
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return DocumentProcessingResponse(
            title=result.get("title", "Untitled"),
            author=result.get("author", "Unknown"),
            num_pages=result.get("num_pages", 0),
            pages=result.get("pages", []),
        )
    
    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")


# Cleanup function for background tasks
def cleanup_resources():
    """Clean up AI resources when the application shuts down."""
    global _ai_factory
    if _ai_factory:
        logger.info("Cleaning up AI resources")
        _ai_factory.shutdown()
        _ai_factory = None 