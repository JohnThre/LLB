import logging
from .ai_providers import AIProviderManager

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.provider_manager = AIProviderManager()
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
            if language == "zh-CN" or any(char in prompt for char in "什么健康性"):
                enhanced_prompt = f"作为专业性健康教育助手，请回答：{prompt}"
            else:
                enhanced_prompt = f"As a sexual health education assistant, answer: {prompt}"
            
            response = await self.provider_manager.generate_response(enhanced_prompt, max_tokens=150)
            return response.strip() if response else "I'm here to help with sexual health education."
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            if language == "zh-CN":
                return "抱歉，我现在无法处理您的请求。"
            else:
                return "Sorry, I'm unable to process your request right now."
    
    def is_loaded(self) -> bool:
        return self._loaded