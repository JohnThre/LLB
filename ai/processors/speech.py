"""
Speech processor for audio transcription using Whisper.
"""

import os
from typing import Dict, Any, Optional, Union
import torch
import whisper
from loguru import logger

from ai.config import WHISPER_MODEL


class SpeechProcessor:
    """Speech processor for audio transcription."""
    
    def __init__(
        self,
        model_size: str = WHISPER_MODEL,
        device: Optional[str] = None,
    ):
        """
        Initialize the speech processor.
        
        Args:
            model_size: Size of the Whisper model
            device: Device to run on
        """
        self.model_size = model_size
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        
        logger.info(f"Loading Whisper {model_size} model on {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            self.model = whisper.load_model(
                self.model_size,
                device=self.device
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            raise
    
    def transcribe_audio_file(
        self,
        file_path: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe audio from a file.
        
        Args:
            file_path: Path to audio file
            language: Language code (optional)
            
        Returns:
            Transcription result
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Audio file not found: {file_path}")
            
            result = self.model.transcribe(
                file_path,
                language=language,
                fp16=self.device == 'cuda'
            )
            
            return {
                'text': result['text'],
                'segments': result['segments'],
                'language': result.get('language', language)
            }
            
        except Exception as e:
            logger.error(f"Error transcribing audio file: {str(e)}")
            raise
    
    def transcribe_audio_bytes(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe audio from bytes.
        
        Args:
            audio_data: Audio data in bytes
            language: Language code (optional)
            
        Returns:
            Transcription result
        """
        try:
            # Save audio data to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            try:
                result = self.transcribe_audio_file(temp_path, language)
                return result
            finally:
                # Clean up temporary file
                os.unlink(temp_path)
                
        except Exception as e:
            logger.error(f"Error transcribing audio bytes: {str(e)}")
            raise 