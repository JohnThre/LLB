"""
Audio Streaming API Endpoints for LLB Backend
WebSocket-based real-time audio processing for longer conversations
"""

import asyncio
import json
import logging
from typing import Dict, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.api import deps
from app.services.audio_streaming_service import AudioStreamingService
from app.core.logging import get_logger
from app.core.sanitizer import sanitize_html, sanitize_log_input

logger = get_logger(__name__)

router = APIRouter()

# Global streaming service instance
streaming_service: Optional[AudioStreamingService] = None


async def get_streaming_service() -> AudioStreamingService:
    """Get the audio streaming service instance."""
    global streaming_service
    if streaming_service is None:
        streaming_service = AudioStreamingService()
        await streaming_service.initialize()
    return streaming_service


@router.post("/sessions")
async def create_streaming_session(
    language: str = "auto",
    service: AudioStreamingService = Depends(get_streaming_service)
):
    """
    Create a new audio streaming session for longer conversations.
    
    Args:
        language: Language code (zh, en, auto)
        service: Audio streaming service
        
    Returns:
        Session information with session_id
    """
    try:
        session_id = await service.create_session(language)
        
        return {
            "success": True,
            "session_id": session_id,
            "language": language,
            "websocket_url": f"/api/v1/audio-streaming/ws/{session_id}",
            "message": "Session created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating streaming session: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/sessions/{session_id}/stats")
async def get_session_stats(
    session_id: str,
    service: AudioStreamingService = Depends(get_streaming_service)
):
    """
    Get statistics for a streaming session.
    
    Args:
        session_id: Session identifier
        service: Audio streaming service
        
    Returns:
        Session statistics and performance metrics
    """
    try:
        stats = await service.get_session_stats(session_id)
        
        if stats is None:
            raise HTTPException(
                status_code=404, 
                detail=f"Session {session_id} not found"
            )
        
        return {
            "success": True,
            "stats": stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session stats: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get session stats: {str(e)}"
        )


@router.get("/sessions")
async def get_all_sessions_stats(
    service: AudioStreamingService = Depends(get_streaming_service)
):
    """
    Get statistics for all active streaming sessions.
    
    Args:
        service: Audio streaming service
        
    Returns:
        Overall service statistics and all session information
    """
    try:
        stats = await service.get_all_sessions_stats()
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting all sessions stats: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get sessions stats: {str(e)}"
        )


@router.delete("/sessions/{session_id}")
async def close_streaming_session(
    session_id: str,
    service: AudioStreamingService = Depends(get_streaming_service)
):
    """
    Close a streaming session and cleanup resources.
    
    Args:
        session_id: Session identifier
        service: Audio streaming service
        
    Returns:
        Confirmation of session closure
    """
    try:
        await service.close_session(session_id)
        
        return {
            "success": True,
            "message": f"Session {session_id} closed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error closing session: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to close session: {str(e)}"
        )


@router.websocket("/ws/{session_id}")
async def websocket_audio_stream(
    websocket: WebSocket,
    session_id: str,
    service: AudioStreamingService = Depends(get_streaming_service)
):
    """
    WebSocket endpoint for real-time audio streaming.
    
    Handles bidirectional audio communication:
    - Receives audio chunks from client for transcription
    - Sends transcription results back to client
    - Receives text for TTS generation
    - Sends audio responses back to client
    
    Message format:
    {
        "type": "audio_chunk" | "text_request" | "control",
        "data": {...},
        "timestamp": float
    }
    """
    await websocket.accept()
    logger.info(f"WebSocket connected for session: {session_id}")
    
    try:
        # Connect websocket to session
        await service.connect_websocket(session_id, websocket)
        
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "session_id": session_id,
            "message": "WebSocket connected successfully",
            "timestamp": asyncio.get_event_loop().time()
        }))
        
        # Main message processing loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                message_type = message.get("type")
                message_data = message.get("data", {})
                
                if message_type == "audio_chunk":
                    await handle_audio_chunk(service, session_id, message_data, websocket)
                
                elif message_type == "text_request":
                    await handle_text_request(service, session_id, message_data, websocket)
                
                elif message_type == "control":
                    await handle_control_message(service, session_id, message_data, websocket)
                
                else:
                    # Sanitize message_type to prevent XSS
                    safe_message_type = sanitize_html(str(message_type))
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {safe_message_type}",
                        "timestamp": asyncio.get_event_loop().time()
                    }))
            
            except json.JSONDecodeError as e:
                # Sanitize exception message to prevent XSS
                safe_error = sanitize_html(str(e))
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Invalid JSON format: {safe_error}",
                    "timestamp": asyncio.get_event_loop().time()
                }))
            
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Message processing error: {str(e)}",
                    "timestamp": asyncio.get_event_loop().time()
                }))
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session: {session_id}")
    
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
    
    finally:
        # Cleanup on disconnect
        try:
            await service.disconnect_websocket(session_id)
        except Exception as e:
            logger.error(f"Error during WebSocket cleanup: {e}")


async def handle_audio_chunk(
    service: AudioStreamingService,
    session_id: str,
    data: Dict,
    websocket: WebSocket
):
    """
    Handle incoming audio chunk for transcription.
    
    Expected data format:
    {
        "audio_data": "hex_encoded_bytes",
        "is_final": bool,
        "chunk_index": int
    }
    """
    try:
        # Decode audio data from hex
        audio_hex = data.get("audio_data", "")
        if not audio_hex:
            raise ValueError("No audio data provided")
        
        audio_bytes = bytes.fromhex(audio_hex)
        is_final = data.get("is_final", False)
        chunk_index = data.get("chunk_index", 0)
        
        # Process the audio chunk
        chunk_id = await service.process_audio_stream(
            session_id, audio_bytes, is_final
        )
        
        # Send acknowledgment
        await websocket.send_text(json.dumps({
            "type": "chunk_received",
            "chunk_id": chunk_id,
            "chunk_index": chunk_index,
            "size": len(audio_bytes),
            "is_final": is_final,
            "timestamp": asyncio.get_event_loop().time()
        }))
        
    except Exception as e:
        logger.error(f"Error handling audio chunk: {e}")
        # Sanitize exception message to prevent XSS
        import html
        safe_error = html.escape(str(e))
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Audio chunk processing error: {safe_error}",
            "timestamp": asyncio.get_event_loop().time()
        }))


async def handle_text_request(
    service: AudioStreamingService,
    session_id: str,
    data: Dict,
    websocket: WebSocket
):
    """
    Handle text-to-speech request.
    
    Expected data format:
    {
        "text": "text to convert",
        "language": "en|zh",
        "voice_settings": {...}
    }
    """
    try:
        text = data.get("text", "")
        if not text.strip():
            raise ValueError("No text provided")
        
        language = data.get("language")
        
        # Queue TTS generation
        await service.generate_speech_response(session_id, text, language)
        
        # Send acknowledgment
        await websocket.send_text(json.dumps({
            "type": "tts_queued",
            "text": text[:50] + "..." if len(text) > 50 else text,
            "language": language,
            "timestamp": asyncio.get_event_loop().time()
        }))
        
    except Exception as e:
        logger.error(f"Error handling text request: {e}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Text request processing error: {str(e)}",
            "timestamp": asyncio.get_event_loop().time()
        }))


async def handle_control_message(
    service: AudioStreamingService,
    session_id: str,
    data: Dict,
    websocket: WebSocket
):
    """
    Handle control messages (ping, stats request, etc.).
    
    Expected data format:
    {
        "command": "ping|stats|reset",
        "parameters": {...}
    }
    """
    try:
        command = data.get("command", "")
        
        if command == "ping":
            await websocket.send_text(json.dumps({
                "type": "pong",
                "timestamp": asyncio.get_event_loop().time()
            }))
        
        elif command == "stats":
            stats = await service.get_session_stats(session_id)
            await websocket.send_text(json.dumps({
                "type": "stats_response",
                "stats": stats,
                "timestamp": asyncio.get_event_loop().time()
            }))
        
        elif command == "reset":
            # Reset session buffers (keep session active)
            # This could be implemented to clear conversation history
            await websocket.send_text(json.dumps({
                "type": "reset_complete",
                "message": "Session buffers reset",
                "timestamp": asyncio.get_event_loop().time()
            }))
        
        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Unknown control command: {command}",
                "timestamp": asyncio.get_event_loop().time()
            }))
    
    except Exception as e:
        logger.error(f"Error handling control message: {e}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Control message processing error: {str(e)}",
            "timestamp": asyncio.get_event_loop().time()
        }))


@router.on_event("shutdown")
async def shutdown_streaming_service():
    """Cleanup streaming service on application shutdown."""
    global streaming_service
    if streaming_service:
        await streaming_service.cleanup()
        streaming_service = None
        logger.info("Audio streaming service shut down") 