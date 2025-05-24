"""
Audio Service for LLB Backend
Handles audio processing and speech-to-text using Whisper
"""

import os
import tempfile
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
import io

import torch
import whisper
import numpy as np
from fastapi import UploadFile

# Text-to-speech imports
try:
    import pyttsx3
    import edge_tts
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

from app.core.logging import get_logger
from app.config import settings
from app.core.exceptions import (
    AudioProcessingException,
    AudioFormatException,
    AudioServiceUnavailableException,
    AudioTranscriptionException,
    AudioTTSException,
)

logger = get_logger(__name__)


class AudioService:
    """Service for audio processing operations using Whisper."""

    def __init__(self, model_size: str = "base"):
        """Initialize audio service."""
        self.whisper_model = None
        self.tts_engine = None
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_initialized = False
        self.tts_initialized = False
        self.supported_languages = [
            "zh",  # Chinese
            "en",  # English
            "auto"  # Auto-detect
        ]
        logger.info(f"Audio Service initialized with model size: {model_size}")

    async def initialize(self):
        """Initialize audio processing models."""
        try:
            logger.info(f"Initializing Whisper model ({self.model_size}) on {self.device}...")
            
            # Load Whisper model in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            self.whisper_model = await loop.run_in_executor(
                None, self._load_whisper_model
            )
            
            # Initialize TTS engine
            if TTS_AVAILABLE:
                logger.info("Initializing text-to-speech engine...")
                await loop.run_in_executor(None, self._initialize_tts)
                self.tts_initialized = True
                logger.info("✅ TTS engine initialized successfully")
            else:
                logger.warning("⚠️ TTS libraries not available")
            
            self.is_initialized = True
            logger.info("✅ Audio service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize audio service: {e}")
            self.is_initialized = False
            raise

    def _load_whisper_model(self):
        """Load the Whisper model (blocking operation)."""
        try:
            # Download and load Whisper model
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
        """Initialize text-to-speech engine (blocking operation)."""
        try:
            if not TTS_AVAILABLE:
                raise RuntimeError("TTS libraries not available")
            
            # Initialize pyttsx3 engine
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)  # Speed (words per minute)
            self.tts_engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
            
            # Try to set a better voice if available
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice for health education
                for voice in voices:
                    if any(keyword in voice.name.lower() for keyword in ['female', 'woman', 'zira', 'hazel']):
                        self.tts_engine.setProperty('voice', voice.id)
                        logger.info(f"Selected TTS voice: {voice.name}")
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
                    logger.info(f"Using default TTS voice: {voices[0].name}")
            
            logger.info("TTS engine configured successfully")
            
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {str(e)}")
            raise

    async def cleanup(self):
        """Cleanup audio resources."""
        logger.info("Cleaning up audio service...")
        
        if self.whisper_model is not None:
            # Clear model from memory
            del self.whisper_model
            self.whisper_model = None
            
            # Clear CUDA cache if using GPU
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        if self.tts_engine is not None:
            # Stop TTS engine
            try:
                self.tts_engine.stop()
            except:
                pass
            self.tts_engine = None
        
        self.is_initialized = False
        self.tts_initialized = False
        logger.info("✅ Audio service cleanup complete")

    async def transcribe_audio(
        self, 
        audio_data: bytes, 
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text using Whisper.
        
        Args:
            audio_data: Raw audio bytes
            language: Language code (zh, en, or auto for auto-detect)
            task: Task type ('transcribe' or 'translate')
            
        Returns:
            Transcription result with text, language, and metadata
        """
        if not self.is_initialized or self.whisper_model is None:
            raise AudioServiceUnavailableException(
                "Audio service not initialized",
                {"is_initialized": self.is_initialized, "model_loaded": self.whisper_model is not None}
            )

        if not audio_data or len(audio_data) == 0:
            raise AudioFormatException(
                "Empty audio data provided",
                {"data_size": len(audio_data)}
            )

        logger.info(f"Transcribing audio (language: {language or 'auto'}, task: {task})...")

        try:
            # Create temporary file for audio data
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name

            try:
                # Perform transcription in executor to avoid blocking
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, self._transcribe_file, temp_path, language, task
                )
                
                logger.info("✅ Audio transcription completed successfully")
                return result
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except AudioTranscriptionException:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"❌ Audio transcription failed: {str(e)}")
            raise AudioTranscriptionException(
                f"Transcription failed: {str(e)}",
                {"language": language, "task": task, "data_size": len(audio_data)}
            )

    def _transcribe_file(
        self, 
        file_path: str, 
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> Dict[str, Any]:
        """
        Perform actual transcription (blocking operation).
        
        Args:
            file_path: Path to audio file
            language: Language code
            task: Task type
            
        Returns:
            Transcription result
        """
        try:
            # Prepare transcription options
            options = {
                "task": task,
                "fp16": self.device == "cuda",  # Use FP16 on GPU for speed
            }
            
            # Set language if specified and not auto-detect
            if language and language != "auto":
                # Map language codes
                lang_map = {
                    "zh": "zh",
                    "zh-CN": "zh", 
                    "en": "en",
                    "en-US": "en",
                    "en-GB": "en"
                }
                options["language"] = lang_map.get(language, language)

            # Perform transcription
            result = self.whisper_model.transcribe(file_path, **options)
            
            # Extract relevant information
            transcription_result = {
                "text": result["text"].strip(),
                "language": result.get("language", language or "unknown"),
                "confidence": self._calculate_confidence(result),
                "duration": self._get_audio_duration(result),
                "segments": self._process_segments(result.get("segments", [])),
                "task": task
            }
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"Error in Whisper transcription: {str(e)}")
            raise AudioTranscriptionException(
                f"Whisper transcription failed: {str(e)}",
                {"file_path": file_path, "language": language, "task": task}
            )

    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate average confidence from segments."""
        segments = result.get("segments", [])
        if not segments:
            return 0.0
            
        # Calculate average confidence from segments
        confidences = []
        for segment in segments:
            if "avg_logprob" in segment:
                # Convert log probability to confidence (0-1)
                confidence = np.exp(segment["avg_logprob"])
                confidences.append(confidence)
        
        return float(np.mean(confidences)) if confidences else 0.8

    def _get_audio_duration(self, result: Dict[str, Any]) -> float:
        """Extract audio duration from result."""
        segments = result.get("segments", [])
        if segments:
            return float(segments[-1].get("end", 0.0))
        return 0.0

    def _process_segments(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and clean up segments data."""
        processed_segments = []
        for segment in segments:
            processed_segment = {
                "start": segment.get("start", 0.0),
                "end": segment.get("end", 0.0),
                "text": segment.get("text", "").strip(),
                "confidence": np.exp(segment.get("avg_logprob", -1.0))
            }
            processed_segments.append(processed_segment)
        return processed_segments

    async def transcribe_upload_file(
        self, 
        file: UploadFile, 
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe an uploaded audio file.
        
        Args:
            file: Uploaded audio file
            language: Language code
            
        Returns:
            Transcription result
        """
        try:
            # Validate file
            if not file.filename:
                raise AudioFormatException(
                    "No filename provided",
                    {"filename": file.filename}
                )
                
            # Check file size
            content = await file.read()
            if len(content) == 0:
                raise AudioFormatException(
                    "Empty file uploaded",
                    {"filename": file.filename, "size": len(content)}
                )
                
            if len(content) > settings.max_file_size:
                raise AudioFormatException(
                    f"File too large: {len(content)} bytes (max: {settings.max_file_size})",
                    {"filename": file.filename, "size": len(content), "max_size": settings.max_file_size}
                )
            
            # Validate file type
            if not self._is_valid_audio_file(file.filename):
                raise AudioFormatException(
                    f"Unsupported file type: {file.filename}",
                    {"filename": file.filename, "supported_formats": self.get_supported_formats()}
                )
            
            logger.info(f"Transcribing uploaded file: {file.filename}")
            
            # Transcribe audio
            result = await self.transcribe_audio(content, language)
            result["filename"] = file.filename
            
            return result
            
        except (AudioFormatException, AudioTranscriptionException, AudioServiceUnavailableException):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"Error transcribing uploaded file: {str(e)}")
            raise AudioProcessingException(
                f"File transcription failed: {str(e)}",
                {"filename": file.filename if file.filename else "unknown"}
            )

    def _is_valid_audio_file(self, filename: str) -> bool:
        """Check if file is a valid audio file."""
        if not filename:
            return False
            
        valid_extensions = {'.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac'}
        file_ext = Path(filename).suffix.lower()
        return file_ext in valid_extensions

    def is_ready(self) -> bool:
        """Check if audio service is ready."""
        return self.is_initialized and self.whisper_model is not None

    def is_healthy(self) -> bool:
        """Check if audio service is healthy."""
        try:
            return (
                self.is_initialized and 
                self.whisper_model is not None and
                torch.cuda.is_available() == (self.device == "cuda")
            )
        except Exception:
            return False

    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio formats."""
        return ["wav", "mp3", "ogg", "m4a", "flac", "aac"]

    def is_whisper_loaded(self) -> bool:
        """Check if Whisper model is loaded."""
        return self.is_initialized and self.whisper_model is not None

    def get_capabilities(self) -> Dict[str, Any]:
        """Get audio processing capabilities."""
        return {
            "transcription": True,
            "translation": True,
            "language_detection": True,
            "text_to_speech": self.tts_initialized,
            "real_time": False,
            "max_duration": 300,  # 5 minutes
            "supported_sample_rates": [16000, 22050, 44100, 48000],
            "supported_languages": self.supported_languages,
            "model_size": self.model_size,
            "device": self.device,
            "gpu_available": torch.cuda.is_available()
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_size": self.model_size,
            "device": self.device,
            "is_loaded": self.is_whisper_loaded(),
            "tts_available": self.tts_initialized,
            "gpu_available": torch.cuda.is_available(),
            "supported_languages": self.supported_languages
        }

    async def text_to_speech(
        self, 
        text: str, 
        language: Optional[str] = None,
        voice_settings: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Convert text to speech and return audio bytes.
        
        Args:
            text: Text to convert to speech
            language: Language code (zh, en)
            voice_settings: Optional voice configuration
            
        Returns:
            Audio bytes in WAV format
        """
        if not self.tts_initialized or self.tts_engine is None:
            raise AudioServiceUnavailableException(
                "TTS engine not initialized",
                {"tts_initialized": self.tts_initialized, "engine_available": self.tts_engine is not None}
            )

        if not text.strip():
            raise AudioTTSException(
                "Text cannot be empty",
                {"text_length": len(text)}
            )

        logger.info(f"Converting text to speech: {text[:50]}...")

        try:
            # Apply voice settings if provided
            if voice_settings:
                if 'rate' in voice_settings:
                    self.tts_engine.setProperty('rate', voice_settings['rate'])
                if 'volume' in voice_settings:
                    self.tts_engine.setProperty('volume', voice_settings['volume'])

            # Configure voice based on language
            if language:
                await self._set_voice_for_language(language)

            # Generate speech in executor to avoid blocking
            loop = asyncio.get_event_loop()
            audio_bytes = await loop.run_in_executor(
                None, self._generate_speech, text
            )

            logger.info("✅ Text-to-speech conversion completed")
            return audio_bytes

        except (AudioTTSException, AudioServiceUnavailableException):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"❌ Text-to-speech failed: {str(e)}")
            raise AudioTTSException(
                f"TTS generation failed: {str(e)}",
                {"text_length": len(text), "language": language}
            )

    def _generate_speech(self, text: str) -> bytes:
        """Generate speech from text (blocking operation)."""
        try:
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name

            try:
                # Save speech to file
                self.tts_engine.save_to_file(text, temp_path)
                self.tts_engine.runAndWait()

                # Read audio data
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()

                return audio_data

            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            raise AudioTTSException(
                f"Speech generation failed: {str(e)}",
                {"text_length": len(text)}
            )

    async def _set_voice_for_language(self, language: str):
        """Set appropriate voice for the specified language."""
        try:
            voices = self.tts_engine.getProperty('voices')
            if not voices:
                return

            # Language-specific voice selection
            if language.startswith('zh'):
                # Look for Chinese voices
                for voice in voices:
                    if any(keyword in voice.name.lower() for keyword in ['chinese', 'mandarin', 'zh']):
                        self.tts_engine.setProperty('voice', voice.id)
                        logger.info(f"Selected Chinese voice: {voice.name}")
                        return
            elif language.startswith('en'):
                # Look for English voices
                for voice in voices:
                    if any(keyword in voice.name.lower() for keyword in ['english', 'en', 'us', 'uk']):
                        self.tts_engine.setProperty('voice', voice.id)
                        logger.info(f"Selected English voice: {voice.name}")
                        return

        except Exception as e:
            logger.warning(f"Could not set voice for language {language}: {e}")

    async def text_to_speech_stream(
        self, 
        text: str, 
        language: Optional[str] = None
    ) -> io.BytesIO:
        """
        Convert text to speech and return as stream.
        
        Args:
            text: Text to convert
            language: Language code
            
        Returns:
            Audio stream
        """
        audio_bytes = await self.text_to_speech(text, language)
        return io.BytesIO(audio_bytes)

    def is_tts_ready(self) -> bool:
        """Check if text-to-speech is ready."""
        return self.tts_initialized and self.tts_engine is not None

    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available TTS voices."""
        if not self.tts_initialized or self.tts_engine is None:
            return []

        try:
            voices = self.tts_engine.getProperty('voices')
            if not voices:
                return []

            voice_list = []
            for voice in voices:
                voice_info = {
                    "id": voice.id,
                    "name": voice.name,
                    "language": getattr(voice, 'languages', ['unknown'])[0] if hasattr(voice, 'languages') else 'unknown'
                }
                voice_list.append(voice_info)

            return voice_list

        except Exception as e:
            logger.error(f"Error getting available voices: {e}")
            return []
