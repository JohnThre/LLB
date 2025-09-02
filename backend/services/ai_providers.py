import os
import httpx
from typing import Optional, List
from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        pass

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 150)
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except:
            return False

class ClaudeProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.api_key = api_key
        self.model = model
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
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
                    "https://api.anthropic.com/v1/messages",
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

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
                params={"key": self.api_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": kwargs.get("max_tokens", 150)
                    }
                }
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    params={"key": self.api_key}
                )
                return response.status_code == 200
        except:
            return False

class OllamaProvider(AIProvider):
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
                    "stream": False
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

class AIProviderManager:
    def __init__(self):
        self.providers: List[AIProvider] = []
        self.current_provider: Optional[AIProvider] = None
        self._setup_providers()
    
    def _setup_providers(self):
        if openai_key := os.getenv("OPENAI_API_KEY"):
            self.providers.append(OpenAIProvider(openai_key))
        
        if claude_key := os.getenv("ANTHROPIC_API_KEY"):
            self.providers.append(ClaudeProvider(claude_key))
        
        if gemini_key := os.getenv("GOOGLE_API_KEY"):
            self.providers.append(GeminiProvider(gemini_key))
        
        if os.getenv("OLLAMA_ENABLED", "false").lower() == "true":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama2")
            self.providers.append(OllamaProvider(base_url, model))
    
    async def initialize(self):
        for provider in self.providers:
            if await provider.is_available():
                self.current_provider = provider
                return
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        if not self.current_provider:
            await self.initialize()
        
        if not self.current_provider:
            raise RuntimeError("No AI providers available")
        
        try:
            return await self.current_provider.generate_response(prompt, **kwargs)
        except Exception:
            for provider in self.providers:
                if provider != self.current_provider and await provider.is_available():
                    try:
                        result = await provider.generate_response(prompt, **kwargs)
                        self.current_provider = provider
                        return result
                    except Exception:
                        continue
            
            raise RuntimeError("All AI providers failed")