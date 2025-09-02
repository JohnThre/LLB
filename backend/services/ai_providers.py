"""
AI Providers Service for LLB - Supporting multiple AI providers
Supports: OpenAI, Claude (Anthropic), Gemini, Ollama, Chrome Web AI
"""

import os
import asyncio
import httpx
from typing import Dict, Any, Optional, List, AsyncGenerator
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 150),
                    "temperature": kwargs.get("temperature", 0.7)
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except:
            return False
    
    def get_provider_name(self) -> str:
        return "OpenAI"


class ClaudeProvider(AIProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": self.model,
                    "max_tokens": kwargs.get("max_tokens", 150),
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]
    
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "test"}]
                    }
                )
                return response.status_code == 200
        except:
            return False
    
    def get_provider_name(self) -> str:
        return "Claude"


class GeminiProvider(AIProvider):
    """Google Gemini API provider"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/models/{self.model}:generateContent",
                params={"key": self.api_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": kwargs.get("max_tokens", 150),
                        "temperature": kwargs.get("temperature", 0.7)
                    }
                }
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    params={"key": self.api_key}
                )
                return response.status_code == 200
        except:
            return False
    
    def get_provider_name(self) -> str:
        return "Gemini"


class OllamaProvider(AIProvider):
    """Ollama local AI provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7),
                        "num_predict": kwargs.get("max_tokens", 150)
                    }
                }
            )
            response.raise_for_status()
            return response.json()["response"]
    
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
    
    def get_provider_name(self) -> str:
        return "Ollama"


class ChromeWebAIProvider(AIProvider):
    """Chrome Web AI provider (experimental)"""
    
    def __init__(self, model: str = "gemini-nano"):
        self.model = model
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        # This would require browser integration
        # For now, return a placeholder response
        return "Chrome Web AI integration requires browser context. Please use other providers."
    
    async def is_available(self) -> bool:
        # Chrome Web AI requires browser context
        return False
    
    def get_provider_name(self) -> str:
        return "Chrome Web AI"


class AIProviderManager:
    """Manages multiple AI providers with fallback support"""
    
    def __init__(self):
        self.providers: List[AIProvider] = []
        self.current_provider: Optional[AIProvider] = None
        self._setup_providers()
    
    def _setup_providers(self):
        """Setup available providers based on environment variables"""
        
        # OpenAI
        if openai_key := os.getenv("OPENAI_API_KEY"):
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            self.providers.append(OpenAIProvider(openai_key, model))
        
        # Claude
        if claude_key := os.getenv("ANTHROPIC_API_KEY"):
            model = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")
            self.providers.append(ClaudeProvider(claude_key, model))
        
        # Gemini
        if gemini_key := os.getenv("GOOGLE_API_KEY"):
            model = os.getenv("GEMINI_MODEL", "gemini-pro")
            self.providers.append(GeminiProvider(gemini_key, model))
        
        # Ollama
        if os.getenv("OLLAMA_ENABLED", "false").lower() == "true":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama2")
            self.providers.append(OllamaProvider(base_url, model))
        
        # Chrome Web AI
        if os.getenv("CHROME_WEB_AI_ENABLED", "false").lower() == "true":
            self.providers.append(ChromeWebAIProvider())
    
    async def initialize(self):
        """Initialize and find the first available provider"""
        for provider in self.providers:
            if await provider.is_available():
                self.current_provider = provider
                logger.info(f"Using AI provider: {provider.get_provider_name()}")
                return
        
        if not self.current_provider:
            logger.warning("No AI providers available")
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using current provider with fallback"""
        if not self.current_provider:
            await self.initialize()
        
        if not self.current_provider:
            raise RuntimeError("No AI providers available")
        
        try:
            return await self.current_provider.generate_response(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Provider {self.current_provider.get_provider_name()} failed: {e}")
            
            # Try fallback providers
            for provider in self.providers:
                if provider != self.current_provider and await provider.is_available():
                    try:
                        result = await provider.generate_response(prompt, **kwargs)
                        self.current_provider = provider
                        logger.info(f"Switched to provider: {provider.get_provider_name()}")
                        return result
                    except Exception as fallback_error:
                        logger.error(f"Fallback provider {provider.get_provider_name()} failed: {fallback_error}")
                        continue
            
            raise RuntimeError("All AI providers failed")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [provider.get_provider_name() for provider in self.providers]
    
    def get_current_provider_name(self) -> Optional[str]:
        """Get current provider name"""
        return self.current_provider.get_provider_name() if self.current_provider else None
    
    async def get_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {}
        for provider in self.providers:
            status[provider.get_provider_name()] = await provider.is_available()
        return {
            "providers": status,
            "current": self.get_current_provider_name(),
            "total_providers": len(self.providers)
        }