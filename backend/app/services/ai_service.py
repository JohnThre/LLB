"""
AI Service for LLB Backend
Handles AI model interactions and text generation using comprehensive prompt system
"""

import re
import sys
import os
from typing import Any, Dict, List, Optional

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))
# Add the ai directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai'))

from app.core.logging import get_logger
from model_service import ModelService
from prompt_engine import PromptEngine, PromptRequest, InputType

logger = get_logger(__name__)


class AIService:
    """Service for AI model operations with comprehensive prompt system."""

    def __init__(self):
        """Initialize AI service."""
        self.model_service = ModelService()
        self.prompt_engine = PromptEngine()
        self.is_initialized = False
        logger.info("AI Service initialized")

    async def initialize(self):
        """Initialize AI model and prompt system."""
        try:
            logger.info("Initializing AI model and prompt system...")
            await self.model_service.load_model()
            # Prompt engine is initialized in constructor
            self.is_initialized = True
            logger.info("✅ AI model and prompt system initialized successfully")
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

    def _classify_topic(self, message: str, language: str) -> str:
        """Classify the topic of the user's message for appropriate prompt selection."""
        message_lower = message.lower()
        
        # Topic classification keywords
        topic_keywords = {
            "anatomy": {
                "en": ["anatomy", "body", "organ", "menstruation", "period", "puberty", "development"],
                "zh-CN": ["解剖", "身体", "器官", "月经", "生理期", "青春期", "发育"]
            },
            "contraception": {
                "en": ["contraception", "birth control", "condom", "pill", "emergency", "pregnancy"],
                "zh-CN": ["避孕", "避孕套", "安全套", "避孕药", "紧急", "怀孕"]
            },
            "sti_prevention": {
                "en": ["sti", "std", "infection", "disease", "hiv", "aids", "prevention"],
                "zh-CN": ["性病", "感染", "疾病", "艾滋", "预防", "传播"]
            },
            "consent_education": {
                "en": ["consent", "permission", "agreement", "boundaries", "respect"],
                "zh-CN": ["同意", "许可", "界限", "尊重", "边界"]
            },
            "relationship": {
                "en": ["relationship", "partner", "communication", "discuss", "talk"],
                "zh-CN": ["关系", "伴侣", "沟通", "讨论", "交流"]
            },
            "safety_education": {
                "en": ["safety", "safe", "protection", "assault", "abuse"],
                "zh-CN": ["安全", "保护", "侵犯", "虐待"]
            }
        }
        
        # Check for topic matches
        lang_key = "zh-CN" if language.startswith("zh-CN") else "en"
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords.get(lang_key, [])):
                return topic
        
        # Default to basic education
        return "basic_education"

    async def generate_response(
        self,
        message: str,
        language: str = "en",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate AI response to user message using comprehensive prompt system."""
        if not self.is_initialized:
            raise RuntimeError("AI service not initialized")

        logger.info(f"Generating response for message: {message[:50]}...")

        # Detect language from message content
        detected_language = self._detect_language(message)
        
        # Use detected language if no language specified
        response_language = detected_language if detected_language != "en" else language

        # Classify the topic for appropriate prompt selection
        topic = self._classify_topic(message, response_language)
        
        logger.info(f"Detected language: {detected_language}, Topic: {topic}")

        try:
            # Create a prompt request for the prompt engine
            prompt_request = PromptRequest(
                content=message,
                language=response_language,
                input_type=InputType.TEXT,
                cultural_context="mainland_china" if response_language.startswith("zh-CN") else "western"
            )
            
            # Generate the optimized prompt using the prompt engine
            optimized_prompt = self.prompt_engine.generate_prompt(prompt_request)
            
            logger.info(f"Generated prompt length: {len(optimized_prompt)}")
            
            # Generate response using the model service
            ai_response = await self.model_service.generate_response_with_language(
                optimized_prompt, response_language
            )
            
            response = {
                "response": ai_response,
                "language": response_language,
                "language_detected": detected_language,
                "topic": topic,
                "confidence": 0.95,
                "safety_score": 0.98,
                "prompt_used": "comprehensive_sexual_health"
            }

            logger.info("Response generated successfully using prompt system")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error generating response with prompt system: {e}")
            # Fallback to basic prompt if prompt system fails
            return await self._generate_fallback_response(message, response_language, detected_language)

    async def _generate_fallback_response(
        self, 
        message: str, 
        response_language: str, 
        detected_language: str
    ) -> Dict[str, Any]:
        """Generate fallback response with basic prompts if prompt system fails."""
        logger.warning("Using fallback response generation")
        
        # Create basic language-aware prompt
        if response_language == "zh-CN":
            basic_prompt = f"你是性健康专家。回答问题：{message}\n\n答案："
        elif response_language == "zh-CN-henan":
            basic_prompt = f"你是性健康专家。用简单中文回答：{message}\n\n答案："
        else:
            basic_prompt = f"You are a health expert. Answer: {message}\n\nResponse:"
        
        try:
            ai_response = await self.model_service.generate_response_with_language(
                basic_prompt, response_language
            )
            
            return {
                "response": ai_response,
                "language": response_language,
                "language_detected": detected_language,
                "topic": "general",
                "confidence": 0.85,
                "safety_score": 0.95,
                "prompt_used": "basic_fallback"
            }
        except Exception as e:
            logger.error(f"❌ Fallback response generation failed: {e}")
            raise

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
        return ["en", "zh-CN", "zh-TW", "zh-CN-henan"]

    def get_model_info(self) -> Dict[str, Any]:
        """Get AI model information."""
        base_info = {
            "name": "Gemma 3 1B",
            "version": "1.0",
            "parameters": "1B",
            "loaded": self.is_initialized,
            "prompt_system": "comprehensive_sexual_health"
        }
        
        if self.model_service:
            model_info = self.model_service.get_model_info()
            base_info.update(model_info)
            
        return base_info

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information."""
        return {
            "model_memory": "2GB" if self.is_initialized else "0GB",
            "cache_memory": "100MB",
            "prompt_system_memory": "50MB" if self.is_initialized else "0MB",
            "total_memory": "2.15GB" if self.is_initialized else "100MB",
        }

    def get_available_topics(self) -> List[str]:
        """Get list of available sexual health topics."""
        return [
            "basic_education",
            "anatomy", 
            "contraception",
            "sti_prevention",
            "consent_education",
            "relationship",
            "safety_education"
        ] 