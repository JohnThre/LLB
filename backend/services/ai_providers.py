import os
import httpx
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

class AIProvider(ABC):
    name: str = "unknown"
    model: str = ""

    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        pass

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.name = "openai"
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
        self.name = "anthropic"
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
        self.name = "gemini"
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
        self.name = "ollama"
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

class GitHubModelsProvider(AIProvider):
    def __init__(
        self,
        token: str,
        model: str = "openai/gpt-4.1",
        api_version: str = "2026-03-10",
    ):
        self.name = "github"
        self.token = token
        self.model = model
        self.api_version = api_version
        self.inference_url = "https://models.github.ai/inference/chat/completions"
        self.catalog_url = "https://models.github.ai/catalog/models"

    def _headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": self.api_version,
            "Content-Type": "application/json",
        }

    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.inference_url,
                headers=self._headers(),
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 150),
                    "temperature": kwargs.get("temperature", 0.7),
                    "stream": False,
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.catalog_url,
                    headers=self._headers(),
                )
                return response.status_code == 200
        except Exception:
            return False

class AIProviderManager:
    DEFAULT_PROVIDER_ORDER = ["ollama", "github", "openai", "anthropic", "gemini"]

    def __init__(self):
        self.providers: List[AIProvider] = []
        self.current_provider: Optional[AIProvider] = None
        self._setup_providers()

    def _provider_order(self) -> List[str]:
        custom_order = [
            provider.strip().lower()
            for provider in os.getenv("AI_PROVIDER_ORDER", "").split(",")
            if provider.strip()
        ]
        ordered = custom_order[:]
        for provider in self.DEFAULT_PROVIDER_ORDER:
            if provider not in ordered:
                ordered.append(provider)
        return ordered

    def _github_models(self) -> List[str]:
        models = os.getenv("GITHUB_MODELS_MODELS", "openai/gpt-4.1")
        return [model.strip() for model in models.split(",") if model.strip()]

    def _setup_providers(self):
        providers_by_name: Dict[str, List[AIProvider]] = {
            "ollama": [],
            "github": [],
            "openai": [],
            "anthropic": [],
            "gemini": [],
        }

        if os.getenv("OLLAMA_ENABLED", "false").lower() == "true":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama2")
            providers_by_name["ollama"].append(OllamaProvider(base_url, model))

        if github_token := os.getenv("GITHUB_MODELS_TOKEN"):
            api_version = os.getenv("GITHUB_MODELS_API_VERSION", "2026-03-10")
            for model in self._github_models():
                providers_by_name["github"].append(
                    GitHubModelsProvider(github_token, model, api_version)
                )

        if openai_key := os.getenv("OPENAI_API_KEY"):
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            providers_by_name["openai"].append(OpenAIProvider(openai_key, model))
        
        if claude_key := os.getenv("ANTHROPIC_API_KEY"):
            model = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
            providers_by_name["anthropic"].append(ClaudeProvider(claude_key, model))
        
        if gemini_key := os.getenv("GOOGLE_API_KEY"):
            model = os.getenv("GOOGLE_MODEL", "gemini-pro")
            providers_by_name["gemini"].append(GeminiProvider(gemini_key, model))

        for provider_name in self._provider_order():
            self.providers.extend(providers_by_name.get(provider_name, []))
    
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

    def get_provider_info(self) -> Dict[str, object]:
        available_providers = []
        for provider in self.providers:
            if provider.name not in available_providers:
                available_providers.append(provider.name)
        if (
            self.current_provider
            and self.current_provider.name not in available_providers
        ):
            available_providers.append(self.current_provider.name)
        return {
            "provider": self.current_provider.name if self.current_provider else None,
            "model": self.current_provider.model if self.current_provider else None,
            "available_providers": available_providers,
        }
