"""
Language processor for language detection and translation.
"""

from typing import Dict, Any, Optional
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline
)
from loguru import logger

from ai.config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE


class LanguageProcessor:
    """Language processor for detection and translation."""
    
    def __init__(self):
        """Initialize the language processor."""
        logger.info("Initializing language processor")
        self._load_models()
    
    def _load_models(self):
        """Load language detection and translation models."""
        try:
            # Load language detection model
            self.detector = pipeline(
                "text-classification",
                model="papluca/xlm-roberta-base-language-detection",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Load translation model
            self.translator = pipeline(
                "translation",
                model="Helsinki-NLP/opus-mt-mul-en",
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("Language models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading language models: {str(e)}")
            raise
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text.
        
        Args:
            text: Input text
            
        Returns:
            Language detection result
        """
        try:
            if not text.strip():
                return {
                    'language': DEFAULT_LANGUAGE,
                    'confidence': 1.0
                }
            
            # Get language detection result
            result = self.detector(text)[0]
            
            # Extract language code and confidence
            lang_code = result['label'].lower()
            confidence = result['score']
            
            # Normalize language code
            if lang_code == 'zh':
                lang_code = 'zh-CN'
            
            # Use default language if not supported
            if lang_code not in SUPPORTED_LANGUAGES:
                lang_code = DEFAULT_LANGUAGE
            
            return {
                'language': lang_code,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            raise
    
    def translate_text(
        self,
        text: str,
        target_language: str = 'en',
        source_language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Translate text to the target language.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional)
            
        Returns:
            Translation result
        """
        try:
            if not text.strip():
                return {
                    'translated_text': '',
                    'source_language': source_language or DEFAULT_LANGUAGE,
                    'target_language': target_language
                }
            
            # Detect source language if not provided
            if not source_language:
                detection = self.detect_language(text)
                source_language = detection['language']
            
            # Skip translation if source and target are the same
            if source_language == target_language:
                return {
                    'translated_text': text,
                    'source_language': source_language,
                    'target_language': target_language
                }
            
            # Translate text
            result = self.translator(
                text,
                src_lang=source_language,
                tgt_lang=target_language
            )
            
            return {
                'translated_text': result[0]['translation_text'],
                'source_language': source_language,
                'target_language': target_language
            }
            
        except Exception as e:
            logger.error(f"Error translating text: {str(e)}")
            raise 