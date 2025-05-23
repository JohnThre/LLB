"""
Audio service for LLB application.
Handles speech-to-text and text-to-speech functionality.
"""

import os
import tempfile
import asyncio
from typing import Optional
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

try:
    import speech_recognition as sr
    import pyttsx3
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logger.warning("⚠️ Audio libraries not available. Install speech_recognition and pyttsx3 for audio support.")


class AudioService:
    """Service for handling audio input and output."""
    
    def __init__(self):
        self.recognizer = None
        self.tts_engine = None
        self._initialized = False
        
        if AUDIO_AVAILABLE:
            self._initialize_services()
    
    def _initialize_services(self):
        """Initialize speech recognition and TTS services."""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            
            # Initialize TTS engine
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
            
            # Try to set a better voice if available
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice for health education
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self._initialized = True
            logger.info("✅ Audio services initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize audio services: {e}")
            self._initialized = False
    
    async def speech_to_text(self, audio_file: UploadFile) -> str:
        """Convert speech to text from uploaded audio file."""
        if not self._initialized:
            raise RuntimeError("Audio service not initialized")
        
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                content = await audio_file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # Load audio file
                with sr.AudioFile(temp_file_path) as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source)
                    # Record the audio
                    audio_data = self.recognizer.record(source)
                
                # Try multiple recognition services
                text = await self._recognize_speech(audio_data)
                
                logger.info(f"✅ Speech recognized: {text[:50]}...")
                return text
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"❌ Speech recognition failed: {e}")
            raise
    
    async def _recognize_speech(self, audio_data) -> str:
        """Try multiple speech recognition services."""
        # Try Google Speech Recognition first (free tier)
        try:
            text = self.recognizer.recognize_google(audio_data, language='zh-CN')
            if text:
                return text
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.warning(f"Google Speech Recognition error: {e}")
        
        # Try Google Speech Recognition with English
        try:
            text = self.recognizer.recognize_google(audio_data, language='en-US')
            if text:
                return text
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition (EN) could not understand audio")
        except sr.RequestError as e:
            logger.warning(f"Google Speech Recognition (EN) error: {e}")
        
        # Try offline recognition as fallback
        try:
            text = self.recognizer.recognize_sphinx(audio_data)
            if text:
                return text
        except sr.UnknownValueError:
            logger.warning("Sphinx could not understand audio")
        except sr.RequestError as e:
            logger.warning(f"Sphinx error: {e}")
        
        raise RuntimeError("Could not recognize speech from audio")
    
    async def text_to_speech(self, text: str, language: str = "en") -> bytes:
        """Convert text to speech and return audio bytes."""
        if not self._initialized:
            raise RuntimeError("Audio service not initialized")
        
        try:
            # Configure voice based on language
            if language.startswith("zh"):
                # Try to find Chinese voice
                voices = self.tts_engine.getProperty('voices')
                for voice in voices:
                    if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Generate speech to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file_path = temp_file.name
            
            try:
                # Save speech to file
                self.tts_engine.save_to_file(text, temp_file_path)
                self.tts_engine.runAndWait()
                
                # Read audio data
                with open(temp_file_path, 'rb') as f:
                    audio_data = f.read()
                
                logger.info(f"✅ Text-to-speech generated for: {text[:50]}...")
                return audio_data
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"❌ Text-to-speech failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if audio services are available."""
        return AUDIO_AVAILABLE and self._initialized
    
    def get_supported_formats(self) -> list:
        """Get supported audio formats."""
        return [".wav", ".mp3", ".flac", ".m4a", ".ogg"]
    
    def get_supported_languages(self) -> list:
        """Get supported languages for speech recognition."""
        return [
            {"code": "en-US", "name": "English (US)"},
            {"code": "en-GB", "name": "English (UK)"},
            {"code": "zh-CN", "name": "Chinese (Simplified)"},
            {"code": "zh-TW", "name": "Chinese (Traditional)"}
        ] 