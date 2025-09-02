"""
Model service for LLB application using multiple AI providers.
Supports OpenAI, Claude, Gemini, Ollama, and Chrome Web AI.
"""

import os
import asyncio
from typing import Optional, Dict, Any
import logging
import sys

# Add AI directory to path for prompt engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai'))

logger = logging.getLogger(__name__)

try:
    from prompt_engine import PromptEngine, PromptRequest, InputType
    PROMPT_ENGINE_AVAILABLE = True
except ImportError:
    PROMPT_ENGINE_AVAILABLE = False
    logger.warning("⚠️ Prompt engine not available.")

from .ai_providers import AIProviderManager


class ModelService:
    """Service for managing multiple AI providers."""
    
    def __init__(self):
        self.provider_manager = AIProviderManager()
        self._loaded = False
        
        # Initialize prompt engine if available
        if PROMPT_ENGINE_AVAILABLE:
            self.prompt_engine = PromptEngine()
            logger.info("✅ Prompt engine initialized")
        else:
            self.prompt_engine = None
            logger.warning("⚠️ Prompt engine not available")
        
        # Model configuration
        self.max_length = 1024
        self.max_new_tokens = 150
        
    async def load_model(self):
        """Initialize AI providers."""
        try:
            logger.info("🔄 Initializing AI providers...")
            await self.provider_manager.initialize()
            
            available_providers = self.provider_manager.get_available_providers()
            current_provider = self.provider_manager.get_current_provider_name()
            
            if current_provider:
                logger.info(f"✅ AI providers initialized. Using: {current_provider}")
                logger.info(f"📋 Available providers: {', '.join(available_providers)}")
                self._loaded = True
            else:
                logger.error("❌ No AI providers available")
                raise RuntimeError("No AI providers available. Please configure API keys.")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI providers: {e}")
            raise RuntimeError(f"AI provider initialization failed: {e}")
    
    async def generate_response(self, prompt: str) -> str:
        """Generate response using the loaded model."""
        return await self.generate_response_with_language(prompt, "en")

    async def generate_response_with_language(self, prompt: str, language: str = "en") -> str:
        """Generate response using AI providers with language awareness."""
        if not self._loaded:
            raise RuntimeError("AI providers not initialized. Call load_model() first.")
        
        try:
            # Use prompt engine to create better prompts
            if self.prompt_engine:
                logger.info("🔧 Using prompt engine to enhance prompt...")
                request = PromptRequest(
                    content=prompt,
                    input_type=InputType.TEXT,
                    language=language,
                    cultural_context="chinese" if language.startswith("zh") else "western",
                    safety_level="standard"
                )
                
                prompt_response = self.prompt_engine.process_request(request)
                enhanced_prompt = prompt_response.formatted_prompt
                logger.info(f"✅ Enhanced prompt: {enhanced_prompt[:100]}...")
            else:
                # Create a basic sexual health education prompt
                if language == "zh-CN" or "什么" in prompt or "健康" in prompt or "性" in prompt:
                    enhanced_prompt = f"作为一个专业的性健康教育助手，请回答以下问题：{prompt}"
                else:
                    enhanced_prompt = f"As a professional sexual health education assistant, please answer: {prompt}"
                logger.info(f"✅ Basic prompt format: {enhanced_prompt[:100]}...")
            
            # Generate response using provider manager
            logger.info(f"🤖 Generating response for language: {language}...")
            
            response = await self.provider_manager.generate_response(
                enhanced_prompt,
                max_tokens=self.max_new_tokens,
                temperature=0.7
            )
            
            if response and len(response.strip()) > 3:
                cleaned_response = self._clean_response(response, prompt)
                logger.info(f"✅ Generated response: {cleaned_response[:100]}...")
                return cleaned_response
            else:
                # Fallback response
                if language == "zh-CN" or "什么" in prompt or "健康" in prompt or "性" in prompt:
                    return "我是您的性健康教育助手。请告诉我您想了解什么，我会尽力帮助您。"
                else:
                    return "I'm your sexual health education assistant. Please tell me what you'd like to know and I'll do my best to help you."
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            # Return fallback response instead of raising error
            if language == "zh-CN" or "什么" in prompt or "健康" in prompt or "性" in prompt:
                return "抱歉，我现在无法处理您的请求。请稍后再试。"
            else:
                return "Sorry, I'm unable to process your request right now. Please try again later."
    
    def _is_valid_response(self, response: str) -> bool:
        """Check if a response is valid."""
        if not response or len(response.strip()) < 3:
            return False
        
        # Check if response is mostly repetitive
        words = response.split()
        if len(words) > 10:
            unique_words = set(words)
            uniqueness_ratio = len(unique_words) / len(words)
            if uniqueness_ratio < 0.2:
                return False
        
        return True
    
    def _clean_response(self, response: str, original_prompt: str) -> str:
        """Clean up the response."""
        if isinstance(response, list):
            response = response[0]
        
        response = str(response).strip()
        
        # Remove the original prompt from response if it's included at the start
        if response.startswith(original_prompt):
            response = response[len(original_prompt):].strip()
        
        # Clean up common AI response artifacts
        response = response.replace("\\n\\n", "\\n").strip()
        
        # Ensure response ends properly
        if len(response) > 200 and not response.endswith(('.', '!', '?', '。', '！', '？')):
            sentences = response.split('.')
            if len(sentences) > 2:
                response = '.'.join(sentences[:-1]) + '.'
        
        return response
    
    def _is_invalid_response(self, response: str) -> bool:
        """Check if a response contains invalid tokens or patterns."""
        return not self._is_valid_response(response)
    
    async def generate_streaming_response(self, prompt: str):
        """Generate streaming response (for future implementation)."""
        response = await self.generate_response(prompt)
        yield response
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get AI provider information."""
        if not self._loaded:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "current_provider": self.provider_manager.get_current_provider_name(),
            "available_providers": self.provider_manager.get_available_providers(),
            "max_length": self.max_length,
            "max_new_tokens": self.max_new_tokens,
        }
    
    async def cleanup(self):
        """Clean up AI provider resources."""
        self._loaded = False
        logger.info("🧹 AI provider resources cleaned up")
    
    def optimize_for_inference(self):
        """Apply inference optimizations."""
        if not self._loaded:
            return
        
        logger.info("⚡ AI providers optimized for inference")
    
    async def warm_up(self):
        """Warm up AI providers with a test generation."""
        if not self._loaded:
            return
        
        try:
            logger.info("🔥 Warming up AI providers...")
            test_prompt = "Hello"
            await self.generate_response(test_prompt)
            logger.info("✅ AI providers warmed up successfully")
        except Exception as e:
            logger.error(f"❌ AI provider warm-up failed: {e}")
            raise RuntimeError(f"AI provider warm-up failed: {e}")
    
    async def generate_response_with_topic(self, prompt: str, topic: str = None) -> str:
        """Generate response using the loaded model with topic information."""
        return await self.generate_response_with_language(prompt, "en")

    async def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all AI providers."""
        return await self.provider_manager.get_status()