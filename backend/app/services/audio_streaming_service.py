"""
Audio Streaming Service for LLB Backend
Optimized for longer conversations with real-time streaming capabilities
"""

import asyncio
import io
import os
import tempfile
import time
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple
from pathlib import Path
import json

import torch
import whisper
import numpy as np
from fastapi import WebSocket
import wave

# Text-to-speech imports
try:
    import pyttsx3
    import edge_tts
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

from app.core.logging import get_logger
from app.core.sanitizer import sanitize_log_input
from app.config import settings
from app.core.exceptions import (
    AudioProcessingException,
    AudioFormatException,
    AudioServiceUnavailableException,
    AudioTranscriptionException,
    AudioTTSException,
)

logger = get_logger(__name__)


class AudioChunk:
    """Represents a chunk of audio data for streaming processing."""
    
    def __init__(self, data: bytes, chunk_id: str, timestamp: float, 
                 is_final: bool = False, metadata: Optional[Dict] = None):
        self.data = data
        self.chunk_id = chunk_id
        self.timestamp = timestamp
        self.is_final = is_final
        self.metadata = metadata or {}
        self.processed = False
        self.result: Optional[Dict[str, Any]] = None


class AudioBuffer:
    """Manages audio buffers for streaming processing."""
    
    def __init__(self, max_size: int = 10 * 1024 * 1024):  # 10MB default
        self.max_size = max_size
        self.chunks: List[AudioChunk] = []
        self.total_size = 0
        self._lock = asyncio.Lock()
    
    async def add_chunk(self, chunk: AudioChunk) -> bool:
        """Add a chunk to the buffer. Returns False if buffer is full."""
        async with self._lock:
            chunk_size = len(chunk.data)
            if self.total_size + chunk_size > self.max_size:
                # Remove oldest chunks to make space
                await self._cleanup_old_chunks(chunk_size)
            
            self.chunks.append(chunk)
            self.total_size += chunk_size
            return True
    
    async def get_unprocessed_chunks(self) -> List[AudioChunk]:
        """Get all unprocessed chunks."""
        async with self._lock:
            return [chunk for chunk in self.chunks if not chunk.processed]
    
    async def mark_processed(self, chunk_id: str):
        """Mark a chunk as processed."""
        async with self._lock:
            for chunk in self.chunks:
                if chunk.chunk_id == chunk_id:
                    chunk.processed = True
                    break
    
    async def _cleanup_old_chunks(self, needed_space: int):
        """Remove old processed chunks to free space."""
        removed_size = 0
        chunks_to_remove = []
        
        for chunk in self.chunks:
            if chunk.processed and removed_size < needed_space:
                chunks_to_remove.append(chunk)
                removed_size += len(chunk.data)
        
        for chunk in chunks_to_remove:
            self.chunks.remove(chunk)
            self.total_size -= len(chunk.data)
        
        logger.debug(f"Cleaned up {sanitize_log_input(len(chunks_to_remove))} chunks, freed {sanitize_log_input(removed_size)} bytes")


class ConversationSession:
    """Manages a streaming conversation session."""
    
    def __init__(self, session_id: str, language: str = "auto"):
        self.session_id = session_id
        self.language = language
        self.created_at = time.time()
        self.last_activity = time.time()
        self.audio_buffer = AudioBuffer()
        self.conversation_history: List[Dict[str, Any]] = []
        self.is_active = True
        self.websocket: Optional[WebSocket] = None
        self.processing_queue = asyncio.Queue()
        self.response_queue = asyncio.Queue()
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = time.time()
    
    def is_expired(self, timeout: int = 3600) -> bool:
        """Check if session has expired (default 1 hour)."""
        return time.time() - self.last_activity > timeout
    
    async def add_audio_chunk(self, data: bytes, is_final: bool = False) -> str:
        """Add audio chunk to the session."""
        chunk_id = str(uuid.uuid4())
        chunk = AudioChunk(
            data=data,
            chunk_id=chunk_id,
            timestamp=time.time(),
            is_final=is_final,
            metadata={"language": self.language}
        )
        
        await self.audio_buffer.add_chunk(chunk)
        await self.processing_queue.put(chunk)
        self.update_activity()
        
        return chunk_id
    
    async def add_conversation_entry(self, entry: Dict[str, Any]):
        """Add entry to conversation history."""
        entry["timestamp"] = time.time()
        self.conversation_history.append(entry)
        
        # Keep only last 50 entries to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]


class AudioStreamingService:
    """Enhanced audio service with streaming capabilities for longer conversations."""
    
    def __init__(self, model_size: str = "base"):
        """Initialize streaming audio service."""
        self.whisper_model = None
        self.tts_engine = None
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_initialized = False
        self.tts_initialized = False
        
        # Streaming configuration
        self.chunk_duration = 2.0  # seconds
        self.overlap_duration = 0.5  # seconds
        self.max_chunk_size = 1024 * 1024  # 1MB
        self.sample_rate = 16000
        
        # Session management
        self.active_sessions: Dict[str, ConversationSession] = {}
        self.session_cleanup_task = None
        
        # Processing queues
        self.transcription_workers = []
        self.tts_workers = []
        
        logger.info(f"Audio Streaming Service initialized with model size: {model_size}")
    
    async def initialize(self, num_workers: int = 2):
        """Initialize streaming audio service with worker processes."""
        try:
            logger.info(f"Initializing Audio Streaming Service on {self.device}...")
            
            # Load Whisper model
            loop = asyncio.get_event_loop()
            self.whisper_model = await loop.run_in_executor(
                None, self._load_whisper_model
            )
            
            # Initialize TTS engine
            if TTS_AVAILABLE:
                await loop.run_in_executor(None, self._initialize_tts)
                self.tts_initialized = True
                logger.info("✅ TTS engine initialized")
            
            # Start worker processes
            await self._start_workers(num_workers)
            
            # Start session cleanup task
            self.session_cleanup_task = asyncio.create_task(self._session_cleanup_loop())
            
            self.is_initialized = True
            logger.info("✅ Audio Streaming Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize audio streaming service: {e}")
            raise
    
    def _load_whisper_model(self):
        """Load Whisper model (blocking operation)."""
        try:
            model = whisper.load_model(
                self.model_size,
                device=self.device,
                download_root=settings.whisper_model_path
            )
            logger.info(f"Whisper {self.model_size} model loaded on {self.device}")
            return model
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            raise
    
    def _initialize_tts(self):
        """Initialize TTS engine (blocking operation)."""
        try:
            if not TTS_AVAILABLE:
                raise RuntimeError("TTS libraries not available")
            
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
            # Configure voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if any(keyword in voice.name.lower() 
                          for keyword in ['female', 'woman', 'zira', 'hazel']):
                        self.tts_engine.setProperty('voice', voice.id)
                        logger.info(f"Selected TTS voice: {voice.name}")
                        break
            
            logger.info("TTS engine configured successfully")
            
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {str(e)}")
            raise
    
    async def _start_workers(self, num_workers: int):
        """Start background worker processes."""
        # Start transcription workers
        for i in range(num_workers):
            worker = asyncio.create_task(self._transcription_worker(f"transcription-{i}"))
            self.transcription_workers.append(worker)
        
        # Start TTS workers
        if self.tts_initialized:
            for i in range(num_workers):
                worker = asyncio.create_task(self._tts_worker(f"tts-{i}"))
                self.tts_workers.append(worker)
        
        logger.info(f"Started {num_workers} transcription and TTS workers")
    
    async def _transcription_worker(self, worker_id: str):
        """Background worker for processing transcription chunks."""
        logger.info(f"Transcription worker {worker_id} started")
        
        while True:
            try:
                # Process chunks from all active sessions
                for session in list(self.active_sessions.values()):
                    if not session.is_active:
                        continue
                    
                    try:
                        chunk = await asyncio.wait_for(
                            session.processing_queue.get(), timeout=0.1
                        )
                        
                        # Process the chunk
                        result = await self._process_audio_chunk(chunk, session)
                        chunk.result = result
                        
                        # Mark as processed
                        await session.audio_buffer.mark_processed(chunk.chunk_id)
                        
                        # Send result if websocket is connected
                        if session.websocket and result:
                            await self._send_transcription_result(session, result)
                        
                        # Add to conversation history
                        if result and result.get("text"):
                            await session.add_conversation_entry({
                                "type": "transcription",
                                "chunk_id": chunk.chunk_id,
                                "text": result["text"],
                                "confidence": result.get("confidence", 0.0),
                                "language": result.get("language", "unknown")
                            })
                    
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Error in transcription worker {sanitize_log_input(worker_id)}: {sanitize_log_input(e)}")
                
                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logger.error(f"Critical error in transcription worker {worker_id}: {e}")
                await asyncio.sleep(1)
    
    async def _tts_worker(self, worker_id: str):
        """Background worker for processing TTS requests."""
        logger.info(f"TTS worker {worker_id} started")
        
        while True:
            try:
                # Process TTS requests from all active sessions
                for session in list(self.active_sessions.values()):
                    if not session.is_active:
                        continue
                    
                    try:
                        request = await asyncio.wait_for(
                            session.response_queue.get(), timeout=0.1
                        )
                        
                        # Generate speech
                        audio_data = await self._generate_speech_chunk(
                            request["text"], 
                            request.get("language", "en")
                        )
                        
                        # Send audio data if websocket is connected
                        if session.websocket and audio_data:
                            await self._send_audio_chunk(session, audio_data, request)
                        
                        # Add to conversation history
                        await session.add_conversation_entry({
                            "type": "tts_response",
                            "text": request["text"],
                            "language": request.get("language", "en"),
                            "audio_size": len(audio_data) if audio_data else 0
                        })
                    
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Error in TTS worker {worker_id}: {e}")
                
                await asyncio.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Critical error in TTS worker {worker_id}: {e}")
                await asyncio.sleep(1)
    
    async def _session_cleanup_loop(self):
        """Background task to clean up expired sessions."""
        while True:
            try:
                current_time = time.time()
                expired_sessions = []
                
                for session_id, session in self.active_sessions.items():
                    if session.is_expired():
                        expired_sessions.append(session_id)
                
                for session_id in expired_sessions:
                    await self.close_session(session_id)
                    logger.info(f"Cleaned up expired session: {session_id}")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in session cleanup: {e}")
                await asyncio.sleep(60)
    
    async def create_session(self, language: str = "auto") -> str:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())
        session = ConversationSession(session_id, language)
        self.active_sessions[session_id] = session
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    async def connect_websocket(self, session_id: str, websocket: WebSocket):
        """Connect a websocket to a session."""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        session.websocket = websocket
        session.update_activity()
        
        logger.info(f"WebSocket connected to session: {session_id}")
    
    async def disconnect_websocket(self, session_id: str):
        """Disconnect websocket from a session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.websocket = None
            logger.info(f"WebSocket disconnected from session: {session_id}")
    
    async def close_session(self, session_id: str):
        """Close and cleanup a session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.is_active = False
            
            if session.websocket:
                try:
                    await session.websocket.close()
                except:
                    pass
            
            del self.active_sessions[session_id]
            logger.info(f"Closed session: {session_id}")
    
    async def process_audio_stream(self, session_id: str, audio_data: bytes, 
                                 is_final: bool = False) -> str:
        """Process streaming audio data."""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        chunk_id = await session.add_audio_chunk(audio_data, is_final)
        
        return chunk_id
    
    async def generate_speech_response(self, session_id: str, text: str, 
                                     language: Optional[str] = None):
        """Queue a text-to-speech response for a session."""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        request = {
            "text": text,
            "language": language or session.language,
            "timestamp": time.time()
        }
        
        await session.response_queue.put(request)
        session.update_activity()
    
    async def _process_audio_chunk(self, chunk: AudioChunk, 
                                 session: ConversationSession) -> Optional[Dict[str, Any]]:
        """Process a single audio chunk."""
        try:
            if not self.whisper_model:
                return None
            
            # Create temporary file for the chunk
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(chunk.data)
                temp_path = temp_file.name
            
            try:
                # Transcribe the chunk
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, self._transcribe_chunk_file, temp_path, session.language
                )
                
                return result
                
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        except Exception as e:
            logger.error(f"Error processing audio chunk {chunk.chunk_id}: {e}")
            return None
    
    def _transcribe_chunk_file(self, file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Transcribe audio chunk file (blocking operation)."""
        try:
            # Use Whisper to transcribe
            result = self.whisper_model.transcribe(
                file_path,
                language=language if language != "auto" else None,
                task="transcribe",
                fp16=torch.cuda.is_available()
            )
            
            # Calculate confidence score
            confidence = self._calculate_confidence(result)
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "confidence": confidence,
                "duration": result.get("duration", 0.0),
                "segments": result.get("segments", [])
            }
            
        except Exception as e:
            logger.error(f"Error transcribing chunk: {e}")
            return {
                "text": "",
                "language": "unknown",
                "confidence": 0.0,
                "duration": 0.0,
                "segments": []
            }
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score from Whisper result."""
        try:
            segments = result.get("segments", [])
            if not segments:
                return 0.0
            
            # Average confidence from segments
            total_confidence = sum(
                segment.get("avg_logprob", 0.0) for segment in segments
            )
            avg_confidence = total_confidence / len(segments)
            
            # Convert log probability to confidence (0-1)
            confidence = max(0.0, min(1.0, (avg_confidence + 1.0) / 2.0))
            return confidence
            
        except Exception:
            return 0.0
    
    async def _generate_speech_chunk(self, text: str, language: str = "en") -> Optional[bytes]:
        """Generate speech for a text chunk."""
        try:
            if not self.tts_initialized or not self.tts_engine:
                return None
            
            loop = asyncio.get_event_loop()
            audio_data = await loop.run_in_executor(
                None, self._generate_speech_blocking, text, language
            )
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Error generating speech chunk: {e}")
            return None
    
    def _generate_speech_blocking(self, text: str, language: str) -> bytes:
        """Generate speech (blocking operation)."""
        try:
            # Set voice for language
            self._set_voice_for_language_blocking(language)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                # Generate speech
                self.tts_engine.save_to_file(text, temp_path)
                self.tts_engine.runAndWait()
                
                # Read audio data
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()
                
                return audio_data
                
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        except Exception as e:
            logger.error(f"Error in blocking speech generation: {e}")
            return b""
    
    def _set_voice_for_language_blocking(self, language: str):
        """Set voice for language (blocking operation)."""
        try:
            voices = self.tts_engine.getProperty('voices')
            if not voices:
                return
            
            if language.startswith('zh'):
                for voice in voices:
                    if any(keyword in voice.name.lower() 
                          for keyword in ['chinese', 'mandarin', 'zh']):
                        self.tts_engine.setProperty('voice', voice.id)
                        return
            elif language.startswith('en'):
                for voice in voices:
                    if any(keyword in voice.name.lower() 
                          for keyword in ['english', 'en', 'us', 'uk']):
                        self.tts_engine.setProperty('voice', voice.id)
                        return
        
        except Exception as e:
            logger.warning(f"Could not set voice for language {language}: {e}")
    
    async def _send_transcription_result(self, session: ConversationSession, 
                                       result: Dict[str, Any]):
        """Send transcription result via WebSocket."""
        try:
            if session.websocket:
                message = {
                    "type": "transcription",
                    "data": result,
                    "session_id": session.session_id,
                    "timestamp": time.time()
                }
                await session.websocket.send_text(json.dumps(message))
        
        except Exception as e:
            logger.error(f"Error sending transcription result: {e}")
    
    async def _send_audio_chunk(self, session: ConversationSession, 
                              audio_data: bytes, request: Dict[str, Any]):
        """Send audio chunk via WebSocket."""
        try:
            if session.websocket:
                message = {
                    "type": "audio_response",
                    "data": {
                        "audio_data": audio_data.hex(),  # Convert to hex for JSON
                        "text": request["text"],
                        "language": request["language"],
                        "size": len(audio_data)
                    },
                    "session_id": session.session_id,
                    "timestamp": time.time()
                }
                await session.websocket.send_text(json.dumps(message))
        
        except Exception as e:
            logger.error(f"Error sending audio chunk: {e}")
    
    async def get_session_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a session."""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "is_active": session.is_active,
            "language": session.language,
            "conversation_entries": len(session.conversation_history),
            "buffer_chunks": len(session.audio_buffer.chunks),
            "buffer_size": session.audio_buffer.total_size,
            "pending_transcriptions": session.processing_queue.qsize(),
            "pending_responses": session.response_queue.qsize()
        }
    
    async def get_all_sessions_stats(self) -> Dict[str, Any]:
        """Get statistics for all sessions."""
        return {
            "total_sessions": len(self.active_sessions),
            "active_sessions": [
                session_id for session_id, session in self.active_sessions.items()
                if session.is_active
            ],
            "service_status": {
                "is_initialized": self.is_initialized,
                "tts_initialized": self.tts_initialized,
                "model_size": self.model_size,
                "device": self.device,
                "transcription_workers": len(self.transcription_workers),
                "tts_workers": len(self.tts_workers)
            }
        }
    
    async def cleanup(self):
        """Cleanup streaming service resources."""
        logger.info("Cleaning up Audio Streaming Service...")
        
        # Close all sessions
        for session_id in list(self.active_sessions.keys()):
            await self.close_session(session_id)
        
        # Cancel workers
        for worker in self.transcription_workers + self.tts_workers:
            worker.cancel()
        
        # Cancel cleanup task
        if self.session_cleanup_task:
            self.session_cleanup_task.cancel()
        
        # Cleanup models
        if self.whisper_model is not None:
            del self.whisper_model
            self.whisper_model = None
        
        if self.tts_engine is not None:
            try:
                self.tts_engine.stop()
            except:
                pass
            self.tts_engine = None
        
        # Clear CUDA cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.is_initialized = False
        self.tts_initialized = False
        logger.info("✅ Audio Streaming Service cleanup complete") 