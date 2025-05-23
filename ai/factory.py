"""
AI Factory for creating and managing AI components in the LLB application.
"""

import os
from typing import Dict, Any, Optional

from loguru import logger

from ai.models.gemma import GemmaModel
from ai.processors.speech import SpeechProcessor
from ai.processors.document import DocumentProcessor
from ai.processors.language import LanguageProcessor
from ai.config import (
    WHISPER_MODEL,
    USE_4BIT_QUANTIZATION,
    USE_8BIT_QUANTIZATION,
)


class AIFactory:
    """
    Factory for creating and managing AI components.
    
    This class provides a single point of access for all AI functionality
    in the application, managing the lifecycle of various models and processors.
    """
    
    def __init__(self):
        """Initialize the AI factory."""
        self._gemma_model: Optional[GemmaModel] = None
        self._speech_processor: Optional[SpeechProcessor] = None
        self._document_processor: Optional[DocumentProcessor] = None
        self._language_processor: Optional[LanguageProcessor] = None
        
        logger.info("AI Factory initialized")
    
    def get_gemma_model(
        self, 
        device: Optional[str] = None,
        use_4bit: bool = USE_4BIT_QUANTIZATION,
        use_8bit: bool = USE_8BIT_QUANTIZATION,
    ) -> GemmaModel:
        """
        Get a Gemma model instance, creating it if needed.
        
        Args:
            device: Device to run on
            use_4bit: Whether to use 4-bit quantization
            use_8bit: Whether to use 8-bit quantization
            
        Returns:
            GemmaModel instance
        """
        if not self._gemma_model:
            logger.info("Creating new Gemma model")
            self._gemma_model = GemmaModel(
                device=device,
                use_4bit=use_4bit,
                use_8bit=use_8bit,
            )
        
        return self._gemma_model
    
    def get_speech_processor(
        self, 
        model_size: str = WHISPER_MODEL,
        device: Optional[str] = None,
    ) -> SpeechProcessor:
        """
        Get a speech processor instance, creating it if needed.
        
        Args:
            model_size: Size of the Whisper model
            device: Device to run on
            
        Returns:
            SpeechProcessor instance
        """
        if not self._speech_processor:
            logger.info(f"Creating speech processor with model: {model_size}")
            self._speech_processor = SpeechProcessor(
                model_size=model_size,
                device=device,
            )
        
        return self._speech_processor
    
    def get_document_processor(self) -> DocumentProcessor:
        """
        Get a document processor instance, creating it if needed.
        
        Returns:
            DocumentProcessor instance
        """
        if not self._document_processor:
            logger.info("Creating document processor")
            self._document_processor = DocumentProcessor()
        
        return self._document_processor
    
    def get_language_processor(self) -> LanguageProcessor:
        """
        Get a language processor instance, creating it if needed.
        
        Returns:
            LanguageProcessor instance
        """
        if not self._language_processor:
            logger.info("Creating language processor")
            self._language_processor = LanguageProcessor()
        
        return self._language_processor
    
    def generate_text(
        self, 
        prompt: str,
        **kwargs
    ) -> str:
        """
        Generate text using the Gemma model.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        model = self.get_gemma_model()
        results = model.generate(prompt=prompt, **kwargs)
        return results[0] if results else ""
    
    def chat(
        self, 
        messages: list,
        **kwargs
    ) -> str:
        """
        Generate a response in a conversational context.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional generation parameters
            
        Returns:
            Generated response
        """
        model = self.get_gemma_model()
        return model.chat(messages=messages, **kwargs)
    
    def transcribe_audio(
        self, 
        audio_data, 
        is_file_path: bool = False,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe audio data.
        
        Args:
            audio_data: Audio data (file path or bytes)
            is_file_path: Whether audio_data is a file path
            language: Language code
            
        Returns:
            Transcription result
        """
        processor = self.get_speech_processor()
        
        if is_file_path:
            return processor.transcribe_audio_file(audio_data, language)
        else:
            return processor.transcribe_audio_bytes(audio_data, language)
    
    def process_document(
        self, 
        document_data, 
        is_file_path: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a document.
        
        Args:
            document_data: Document data (file path or bytes)
            is_file_path: Whether document_data is a file path
            
        Returns:
            Extracted content
        """
        processor = self.get_document_processor()
        
        if is_file_path:
            return processor.process_pdf_file(document_data)
        else:
            return processor.process_pdf_bytes(document_data)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of the given text.
        
        Args:
            text: Input text
            
        Returns:
            Language detection result
        """
        processor = self.get_language_processor()
        return processor.detect_language(text)
    
    def shutdown(self):
        """Clean up resources when shutting down."""
        # Clear all models to free up GPU memory
        self._gemma_model = None
        self._speech_processor = None
        self._document_processor = None
        self._language_processor = None
        
        # Force garbage collection
        import gc
        gc.collect()
        
        if hasattr(gc, 'collect'):
            gc.collect()
        
        # For PyTorch models, manually clear CUDA cache
        try:
            import torch
            if hasattr(torch.cuda, 'empty_cache'):
                torch.cuda.empty_cache()
                logger.info("CUDA cache cleared")
        except (ImportError, AttributeError):
            pass
        
        logger.info("AI Factory shut down successfully") 