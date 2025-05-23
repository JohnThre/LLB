"""
LLB Backend API - Main FastAPI application
Provides REST API endpoints for sexual health education with Gemma 3 1B
"""

import sys
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

# Add AI directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "ai"))

from app.config import settings
from app.core.logging import get_logger, setup_logging
from app.core.exceptions import LLBException, LLBHTTPException
from app.api.v1 import health
from app.api.v1.endpoints import chat
from app.api import deps
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.document_service import DocumentService

# Initialize logging
logger = get_logger(__name__)

# Global services
ai_service = None
audio_service = None
document_service = None

# Create placeholder routers for missing endpoints
voice_router = APIRouter()
documents_router = APIRouter()

@voice_router.post("/voice/transcribe")
async def transcribe_voice():
    """Placeholder for voice transcription endpoint."""
    return {"message": "Voice transcription endpoint - coming soon"}

@documents_router.post("/documents/analyze")
async def analyze_document():
    """Placeholder for document analysis endpoint."""
    return {"message": "Document analysis endpoint - coming soon"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    global ai_service, audio_service, document_service
    
    logger.info("🚀 Starting LLB Backend...")
    
    try:
        # Initialize services
        ai_service = AIService()
        audio_service = AudioService()
        document_service = DocumentService()
        
        # Set services in deps module
        deps.set_services(ai_service, audio_service, document_service)
        
        # Initialize all services
        await ai_service.initialize()
        await audio_service.initialize()
        await document_service.initialize()
        
        logger.info("✅ LLB Backend started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to start LLB Backend: {e}")
        raise
    
    yield
    
    logger.info("🛑 Shutting down LLB Backend...")
    
    # Cleanup services
    if ai_service:
        await ai_service.cleanup()
    if audio_service:
        await audio_service.cleanup()
    if document_service:
        await document_service.cleanup()
    
    logger.info("✅ LLB Backend shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        description="Local AI-driven sexual health education system",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Serve static files
    static_path = Path(settings.upload_dir).parent / "static"
    static_path.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    # Include API routers
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
    app.include_router(voice_router, prefix="/api/v1", tags=["voice"])
    app.include_router(documents_router, prefix="/api/v1", tags=["documents"])
    
    # Add legacy health endpoint for backward compatibility
    @app.get("/health")
    async def legacy_health_check():
        """Legacy health check endpoint - redirects to API health."""
        return RedirectResponse(url="/api/v1/health")
    
    # Exception handlers
    @app.exception_handler(LLBException)
    async def llb_exception_handler(request, exc: LLBException):
        """Handle custom LLB exceptions."""
        logger.error(f"LLB Exception: {exc.message}", extra={"details": exc.details})
        return JSONResponse(
            status_code=500,
            content={"error": exc.message, "details": exc.details}
        )
    
    @app.exception_handler(LLBHTTPException)
    async def llb_http_exception_handler(request, exc: LLBHTTPException):
        """Handle custom LLB HTTP exceptions."""
        logger.error(f"LLB HTTP Exception: {exc.detail}")
        raise exc
    
    # Root endpoint
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
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                .header { 
                    text-align: center; 
                    margin-bottom: 40px; 
                }
                .header h1 {
                    font-size: 3em;
                    margin: 0;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                .header p {
                    font-size: 1.2em;
                    opacity: 0.9;
                    margin: 10px 0;
                }
                .status { 
                    background: rgba(255, 255, 255, 0.2); 
                    padding: 30px; 
                    border-radius: 15px; 
                    margin: 20px 0;
                }
                .status h3 {
                    margin-top: 0;
                    color: #4ade80;
                }
                .links {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-top: 30px;
                }
                .link-card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    transition: transform 0.3s ease;
                }
                .link-card:hover {
                    transform: translateY(-5px);
                }
                .link-card a {
                    color: white;
                    text-decoration: none;
                    font-weight: bold;
                }
                .features {
                    margin-top: 40px;
                }
                .features ul {
                    list-style: none;
                    padding: 0;
                }
                .features li {
                    padding: 10px 0;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }
                .features li:before {
                    content: "✨ ";
                    margin-right: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>LLB - 爱学伴</h1>
                    <p>Local AI-Driven Sexual Health Education</p>
                    <p>Powered by Google's Gemma 3 1B Model</p>
                </div>
                
                <div class="status">
                    <h3>✅ System Status: Online</h3>
                    <p>The LLB backend is running successfully and ready to serve requests.</p>
                </div>
                
                <div class="links">
                    <div class="link-card">
                        <h4>📚 API Documentation</h4>
                        <a href="/docs">Interactive API Docs</a>
                    </div>
                    <div class="link-card">
                        <h4>🔍 Health Check</h4>
                        <a href="/api/v1/health">System Health</a>
                    </div>
                    <div class="link-card">
                        <h4>🌐 Alternative Docs</h4>
                        <a href="/redoc">ReDoc Documentation</a>
                    </div>
                </div>
                
                <div class="features">
                    <h3>🚀 Features</h3>
                    <ul>
                        <li>Multi-language support (Chinese, English)</li>
                        <li>Voice input and processing</li>
                        <li>PDF document analysis</li>
                        <li>Local AI processing for privacy</li>
                        <li>Cultural context awareness</li>
                        <li>Safety-first content filtering</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    
    return app


# Create the FastAPI app
app = create_app()

if __name__ == "__main__":
    import uvicorn
    print("Starting LLB API server in development mode...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    ) 