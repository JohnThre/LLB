import logging
import sys
import os

# Add AI directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai'))

from .ai_providers import AIProviderManager
from prompts import PromptEngine

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.provider_manager = AIProviderManager()
        self.prompt_engine = PromptEngine()
        self._loaded = False
        
    async def load_model(self):
        await self.provider_manager.initialize()
        self._loaded = True
    
    async def generate_response(self, prompt: str) -> str:
        return await self.generate_response_with_language(prompt, "en")

    async def generate_response_with_language(self, prompt: str, language: str = "en") -> str:
        if not self._loaded:
            raise RuntimeError("AI providers not initialized")
        
        try:
            # Generate optimized prompt
            enhanced_prompt = self.prompt_engine.enhance_response_quality(prompt)
            
            response = await self.provider_manager.generate_response(
                enhanced_prompt, 
                max_tokens=200,
                temperature=0.7
            )
            
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