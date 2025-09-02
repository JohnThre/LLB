import logging
import sys
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ai_providers import AIProviderManager

# Lazy imports to avoid circular dependencies
AIProviderManager = None
PromptEngine = None

def _get_ai_provider_manager():
    global AIProviderManager
    if AIProviderManager is None:
        try:
            from .ai_providers import AIProviderManager as APM
            AIProviderManager = APM
        except ImportError:
            pass
    return AIProviderManager

def _get_prompt_engine():
    global PromptEngine
    if PromptEngine is None:
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai'))
            from prompts import PromptEngine as PE
            PromptEngine = PE
        except ImportError:
            pass
    return PromptEngine

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.provider_manager = None
        self.prompt_engine = None
        self._loaded = False
    
    def _ensure_services(self):
        """Lazy load services when needed."""
        if self.provider_manager is None:
            APM = _get_ai_provider_manager()
            if APM:
                self.provider_manager = APM()
        
        if self.prompt_engine is None:
            PE = _get_prompt_engine()
            if PE:
                self.prompt_engine = PE()
        
    async def load_model(self):
        self._ensure_services()
        if self.provider_manager:
            await self.provider_manager.initialize()
        self._loaded = True
    
    async def generate_response(self, prompt: str) -> str:
        return await self.generate_response_with_language(prompt, "en")

    async def generate_response_with_language(self, prompt: str, language: str = "en") -> str:
        if not self._loaded:
            raise RuntimeError("AI providers not initialized")
        
        try:
            self._ensure_services()
            # Generate optimized prompt if available
            if self.prompt_engine:
                enhanced_prompt = self.prompt_engine.enhance_response_quality(prompt)
            else:
                enhanced_prompt = prompt
            
            if self.provider_manager:
                response = await self.provider_manager.generate_response(
                    enhanced_prompt, 
                    max_tokens=200,
                    temperature=0.7
                )
            else:
                response = None
            
            return self._clean_response(response) if response else self._fallback_response(language)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response(language)
    
    def _clean_response(self, response: str) -> str:
        """Clean and format response."""
        return response.strip()
    
    def _fallback_response(self, language: str) -> str:
        """Provide fallback response when AI fails."""
        if language == "zh-CN":
            return "我是您的性健康教育助手，请告诉我您想了解什么。"
        return "I'm your sexual health education assistant. How can I help you?"
    
    def is_loaded(self) -> bool:
        return self._loaded