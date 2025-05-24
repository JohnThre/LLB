"""
LLB Backend API - Main FastAPI application
Provides REST API endpoints for sexual health education with Gemma 3 1B
"""

import os
import sys
import asyncio
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import logging

# Add AI directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai'))

from prompt_engine import PromptEngine, PromptRequest, InputType
from services.model_service import ModelService
from services.audio_service import AudioService
from services.document_service import DocumentService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global services
model_service = None
prompt_engine = None
audio_service = None
document_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    global model_service, prompt_engine, audio_service, document_service
    
    print("🚀 Starting LLB Backend...")
    
    # Initialize services
    prompt_engine = PromptEngine()
    model_service = ModelService()
    audio_service = AudioService()
    document_service = DocumentService()
    
    # Load model
    await model_service.load_model()
    
    print("✅ LLB Backend started successfully!")
    
    yield
    
    print("🛑 Shutting down LLB Backend...")
    if model_service:
        await model_service.cleanup()


# Create FastAPI app
app = FastAPI(
    title="LLB Sexual Health Education API",
    description="Local AI-driven sexual health education system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = None
    cultural_context: Optional[str] = None
    user_age_group: Optional[str] = "adult"
    safety_level: str = "standard"


class ChatResponse(BaseModel):
    response: str
    language_detected: str
    topic: str
    safety_flags: List[str]
    confidence_score: float
    metadata: Dict[str, Any]


class HealthCheck(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    status: str
    version: str
    model_loaded: bool
    supported_languages: List[str]
    available_topics: List[str]


# API Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LLB - 爱学伴</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .status { background: #e8f5e8; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>LLB - 爱学伴</h1>
                <p>Local AI-Driven Sexual Health Education</p>
            </div>
            <div class="status">
                <h3>✅ System Status: Online</h3>
                <p>The LLB backend is running successfully.</p>
                <p><strong>API Documentation:</strong> <a href="/docs">/docs</a></p>
                <p><strong>Health Check:</strong> <a href="/health">/health</a></p>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    global model_service, prompt_engine
    
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        model_loaded=model_service.is_loaded() if model_service else False,
        supported_languages=prompt_engine.get_supported_languages() if prompt_engine else [],
        available_topics=prompt_engine.get_available_topics() if prompt_engine else []
    )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint for sexual health education."""
    logger.info(f"📝 Received chat request: {request.message[:50]}...")
    
    # Create prompt request
    prompt_request = PromptRequest(
        content=request.message,
        input_type=InputType.TEXT,
        language=request.language,
        cultural_context=request.cultural_context,
        user_age_group=request.user_age_group,
        safety_level=request.safety_level
    )
    
    # Process with prompt engine
    result = prompt_engine.process_request(prompt_request)
    
    # Generate response with model service, passing topic information
    response = await model_service.generate_response_with_topic(
        result.formatted_prompt, 
        topic=result.metadata.get("topic", "basic_education")
    )
    
    return ChatResponse(
        response=response,
        language_detected=result.language_detected,
        topic=result.metadata.get("topic", "basic_education"),
        safety_flags=result.safety_flags,
        confidence_score=result.confidence_score,
        metadata=result.metadata
    )


@app.post("/api/voice")
async def voice_chat(audio: UploadFile = File(...)):
    """Voice input endpoint."""
    global audio_service
    
    if not audio_service:
        raise HTTPException(status_code=503, detail="Audio service not available")
    
    try:
        # Process audio file
        text = await audio_service.speech_to_text(audio)
        
        # Process as regular chat
        chat_request = ChatRequest(message=text)
        return await chat(chat_request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@app.post("/api/document")
async def analyze_document(file: UploadFile = File(...)):
    """Document analysis endpoint."""
    global document_service, prompt_engine
    
    if not document_service:
        raise HTTPException(status_code=503, detail="Document service not available")
    
    try:
        # Extract text from document
        text_content = await document_service.extract_text(file)
        
        # Create document analysis request
        prompt_request = PromptRequest(
            content=text_content,
            input_type=InputType.DOCUMENT
        )
        
        # Process with prompt engine
        prompt_response = prompt_engine.process_request(prompt_request)
        
        return {
            "analysis": prompt_response.formatted_prompt,
            "language_detected": prompt_response.language_detected,
            "safety_flags": prompt_response.safety_flags,
            "metadata": prompt_response.metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")


@app.get("/api/languages")
async def get_supported_languages():
    """Get supported languages."""
    global prompt_engine
    
    if not prompt_engine:
        raise HTTPException(status_code=503, detail="Prompt engine not available")
    
    return {
        "languages": prompt_engine.get_supported_languages(),
        "topics": prompt_engine.get_available_topics()
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 