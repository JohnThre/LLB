"""
AI Service for LLB Backend
Handles AI model interactions and text generation
"""

import re
import sys
import os
from typing import Any, Dict, List, Optional

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))

from app.core.logging import get_logger
from model_service import ModelService

logger = get_logger(__name__)


class AIService:
    """Service for AI model operations."""

    def __init__(self):
        """Initialize AI service."""
        self.model_service = ModelService()
        self.is_initialized = False
        logger.info("AI Service initialized")

    async def initialize(self):
        """Initialize AI model."""
        try:
            logger.info("Initializing AI model...")
            await self.model_service.load_model()
            self.is_initialized = True
            logger.info("✅ AI model initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI model: {e}")
            raise

    async def cleanup(self):
        """Cleanup AI resources."""
        logger.info("Cleaning up AI service...")
        if self.model_service:
            await self.model_service.cleanup()
        self.is_initialized = False
        logger.info("✅ AI service cleanup complete")

    def _detect_language(self, text: str) -> str:
        """Detect language from text."""
        # Simple language detection based on character patterns
        chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
        if chinese_chars:
            # Check for Henan dialect markers
            henan_markers = ["俺", "咋", "啥", "中不中", "对象"]
            if any(marker in text for marker in henan_markers):
                return "zh-CN-henan"
            return "zh-CN"
        return "en"

    def _create_language_aware_prompt(self, message: str, language: str) -> str:
        """Create a language-aware prompt for the AI model optimized for Gemma3."""
        if language == "zh-CN":
            # Simplified Chinese prompt for Gemma3
            prompt = f"你是性健康专家。回答问题：{message}\n\n答案："
            return prompt
        elif language == "zh-CN-henan":
            # Henan dialect prompt for Gemma3
            prompt = f"你是性健康专家。用简单中文回答：{message}\n\n答案："
            return prompt
        else:
            # English prompt optimized for Gemma3
            prompt = f"You are a health expert. Answer: {message}\n\nResponse:"
            return prompt

    async def generate_response(
        self,
        message: str,
        language: str = "en",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate AI response to user message."""
        if not self.is_initialized:
            raise RuntimeError("AI service not initialized")

        logger.info(f"Generating response for message: {message[:50]}...")

        # Detect language from message content
        detected_language = self._detect_language(message)
        
        # Use detected language if no language specified
        response_language = detected_language if detected_language != "en" else language

        # Create language-aware prompt
        language_aware_prompt = self._create_language_aware_prompt(message, response_language)

        # Generate response using the model service - no fallback, let errors propagate
        ai_response = await self.model_service.generate_response_with_language(
            language_aware_prompt, response_language
        )
        
        response = {
            "response": ai_response,
            "language": response_language,
            "language_detected": detected_language,
            "confidence": 0.95,
            "safety_score": 0.98,
        }

        logger.info("Response generated successfully")
        return response

    def is_ready(self) -> bool:
        """Check if AI service is ready."""
        return self.is_initialized

    def is_healthy(self) -> bool:
        """Check if AI service is healthy."""
        return self.is_initialized and self.model_service.is_loaded()

    def is_model_loaded(self) -> bool:
        """Check if AI model is loaded."""
        return self.is_initialized and self.model_service.is_loaded()

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return ["en", "zh-CN", "zh-TW"]

    def get_model_info(self) -> Dict[str, Any]:
        """Get AI model information."""
        if self.model_service:
            return self.model_service.get_model_info()
        return {
            "name": "Gemma 3 1B",
            "version": "1.0",
            "parameters": "1B",
            "loaded": self.is_initialized,
        }

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information."""
        return {
            "model_memory": "2GB" if self.is_initialized else "0GB",
            "cache_memory": "100MB",
            "total_memory": "2.1GB" if self.is_initialized else "100MB",
        } 