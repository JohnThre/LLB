import os
import httpx
from dataclasses import dataclass
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class ProviderMetadata:
    """Public metadata for a supported AI provider."""

    name: str
    display_name: str
    credential_env: str
    model_env: str
    default_model: str
    models: List[str]
    requires_api_key: bool = True

    def to_public_dict(self) -> Dict[str, object]:
        """Return provider metadata without credential values."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "default_model": self.default_model,
            "models": self.models,
            "requires_api_key": self.requires_api_key,
        }


PROVIDER_REGISTRY: Dict[str, ProviderMetadata] = {
    "ollama": ProviderMetadata(
        name="ollama",
        display_name="Ollama",
        credential_env="",
        model_env="OLLAMA_MODEL",
        default_model="llama3.2",
        models=["llama3.2", "llama3.1", "mistral", "qwen2.5"],
        requires_api_key=False,
    ),
    "github": ProviderMetadata(
        name="github",
        display_name="GitHub Models",
        credential_env="GITHUB_MODELS_TOKEN",
        model_env="GITHUB_MODELS_MODELS",
        default_model="openai/gpt-5.2",
        models=["openai/gpt-5.2", "openai/gpt-4.1", "microsoft/phi-4"],
    ),
    "openai": ProviderMetadata(
        name="openai",
        display_name="OpenAI",
        credential_env="OPENAI_API_KEY",
        model_env="OPENAI_MODEL",
        default_model="gpt-5.2",
        models=["gpt-5.2", "gpt-5-mini", "gpt-5-nano", "gpt-4.1"],
    ),
    "anthropic": ProviderMetadata(
        name="anthropic",
        display_name="Anthropic Claude",
        credential_env="ANTHROPIC_API_KEY",
        model_env="ANTHROPIC_MODEL",
        default_model="claude-opus-4-7",
        models=[
            "claude-opus-4-7",
            "claude-sonnet-4-6",
            "claude-haiku-4-5",
            "claude-3-5-haiku-latest",
        ],
    ),
    "gemini": ProviderMetadata(
        name="gemini",
        display_name="Google Gemini",
        credential_env="GOOGLE_API_KEY",
        model_env="GOOGLE_MODEL",
        default_model="gemini-3-pro-preview",
        models=[
            "gemini-3-pro-preview",
            "gemini-3-flash-preview",
            "gemini-2.5-pro",
        ],
    ),
    "mistral": ProviderMetadata(
        name="mistral",
        display_name="Mistral AI",
        credential_env="MISTRAL_API_KEY",
        model_env="MISTRAL_MODEL",
        default_model="mistral-medium-3.5",
        models=["mistral-medium-3.5", "mistral-small-4", "mistral-large-3"],
    ),
}

_DESKTOP_PROVIDER_CREDENTIALS: Dict[str, Dict[str, str]] = {}


def _normalize_provider_name(provider: str) -> str:
    """Normalize provider aliases used by UI or environment values."""
    normalized = provider.strip().lower()
    aliases = {
        "claude": "anthropic",
        "anthropic_claude": "anthropic",
        "google": "gemini",
        "google_gemini": "gemini",
        "github_models": "github",
    }
    return aliases.get(normalized, normalized)


def get_provider_catalog() -> List[Dict[str, object]]:
    """Return supported providers and default model metadata."""
    return [
        PROVIDER_REGISTRY[name].to_public_dict()
        for name in AIProviderManager.DEFAULT_PROVIDER_ORDER
    ]


def set_desktop_provider_credentials(
    credentials: Dict[str, Dict[str, str]]
) -> None:
    """Store desktop-supplied BYOK credentials in process memory."""
    _DESKTOP_PROVIDER_CREDENTIALS.clear()
    for provider_name, payload in credentials.items():
        normalized = _normalize_provider_name(provider_name)
        if normalized not in PROVIDER_REGISTRY:
            continue
        clean_payload = {
            key: value.strip()
            for key, value in payload.items()
            if key in {"api_key", "token", "model", "base_url", "api_version"}
            and isinstance(value, str)
            and value.strip()
        }
        if clean_payload:
            _DESKTOP_PROVIDER_CREDENTIALS[normalized] = clean_payload


def clear_desktop_provider_credentials() -> None:
    """Clear desktop-supplied BYOK credentials from process memory."""
    _DESKTOP_PROVIDER_CREDENTIALS.clear()


def get_desktop_provider_status() -> List[Dict[str, object]]:
    """Return masked status for desktop-supplied provider credentials."""
    statuses = []
    for name, payload in _DESKTOP_PROVIDER_CREDENTIALS.items():
        metadata = PROVIDER_REGISTRY[name]
        statuses.append(
            {
                "name": name,
                "model": payload.get("model", metadata.default_model),
                "has_api_key": bool(payload.get("api_key") or payload.get("token")),
            }
        )
    return statuses


class AIProvider(ABC):
    name: str = "unknown"
    model: str = ""
    credential_source: str = "environment"

    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        pass

class OpenAIProvider(AIProvider):
    def __init__(
        self,
        api_key: str,
        model: str = PROVIDER_REGISTRY["openai"].default_model,
        credential_source: str = "environment",
    ):
        self.name = "openai"
        self.api_key = api_key
        self.model = model
        self.credential_source = credential_source
    
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
    def __init__(
        self,
        api_key: str,
        model: str = PROVIDER_REGISTRY["anthropic"].default_model,
        credential_source: str = "environment",
    ):
        self.name = "anthropic"
        self.api_key = api_key
        self.model = model
        self.credential_source = credential_source
    
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
    def __init__(
        self,
        api_key: str,
        model: str = PROVIDER_REGISTRY["gemini"].default_model,
        credential_source: str = "environment",
    ):
        self.name = "gemini"
        self.api_key = api_key
        self.model = model
        self.credential_source = credential_source
    
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
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = PROVIDER_REGISTRY["ollama"].default_model,
        credential_source: str = "environment",
    ):
        self.name = "ollama"
        self.base_url = base_url
        self.model = model
        self.credential_source = credential_source
    
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
        model: str = PROVIDER_REGISTRY["github"].default_model,
        api_version: str = "2026-03-10",
        credential_source: str = "environment",
    ):
        self.name = "github"
        self.token = token
        self.model = model
        self.api_version = api_version
        self.credential_source = credential_source
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

class MistralProvider(AIProvider):
    def __init__(
        self,
        api_key: str,
        model: str = PROVIDER_REGISTRY["mistral"].default_model,
        credential_source: str = "environment",
    ):
        self.name = "mistral"
        self.api_key = api_key
        self.model = model
        self.credential_source = credential_source
        self.chat_url = "https://api.mistral.ai/v1/chat/completions"
        self.models_url = "https://api.mistral.ai/v1/models"

    async def generate_response(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.chat_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 150),
                    "temperature": kwargs.get("temperature", 0.7),
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.models_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                return response.status_code == 200
        except Exception:
            return False

class AIProviderManager:
    DEFAULT_PROVIDER_ORDER = [
        "ollama",
        "github",
        "openai",
        "anthropic",
        "gemini",
        "mistral",
    ]

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
        models = os.getenv(
            "GITHUB_MODELS_MODELS", PROVIDER_REGISTRY["github"].default_model
        )
        return [model.strip() for model in models.split(",") if model.strip()]

    def _provider_credentials(self, provider_name: str) -> tuple[Dict[str, str], str]:
        metadata = PROVIDER_REGISTRY[provider_name]
        if provider_name in _DESKTOP_PROVIDER_CREDENTIALS:
            return _DESKTOP_PROVIDER_CREDENTIALS[provider_name], "desktop"
        if not metadata.requires_api_key:
            return {}, "environment"
        credential = os.getenv(metadata.credential_env, "")
        if not credential:
            return {}, "environment"
        return {
            "api_key": credential,
            "token": credential,
            "model": os.getenv(metadata.model_env, metadata.default_model),
        }, "environment"

    def _setup_providers(self):
        providers_by_name: Dict[str, List[AIProvider]] = {
            "ollama": [],
            "github": [],
            "openai": [],
            "anthropic": [],
            "gemini": [],
            "mistral": [],
        }

        if os.getenv("OLLAMA_ENABLED", "false").lower() == "true":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv(
                "OLLAMA_MODEL", PROVIDER_REGISTRY["ollama"].default_model
            )
            providers_by_name["ollama"].append(
                OllamaProvider(base_url, model, "environment")
            )

        github_credentials, github_source = self._provider_credentials("github")
        if github_token := github_credentials.get("token"):
            api_version = github_credentials.get(
                "api_version", os.getenv("GITHUB_MODELS_API_VERSION", "2026-03-10")
            )
            models = (
                [github_credentials["model"]]
                if github_source == "desktop" and github_credentials.get("model")
                else self._github_models()
            )
            for model in models:
                providers_by_name["github"].append(
                    GitHubModelsProvider(github_token, model, api_version, github_source)
                )

        openai_credentials, openai_source = self._provider_credentials("openai")
        if openai_key := openai_credentials.get("api_key"):
            model = openai_credentials.get(
                "model", PROVIDER_REGISTRY["openai"].default_model
            )
            providers_by_name["openai"].append(
                OpenAIProvider(openai_key, model, openai_source)
            )

        claude_credentials, claude_source = self._provider_credentials("anthropic")
        if claude_key := claude_credentials.get("api_key"):
            model = claude_credentials.get(
                "model", PROVIDER_REGISTRY["anthropic"].default_model
            )
            providers_by_name["anthropic"].append(
                ClaudeProvider(claude_key, model, claude_source)
            )

        gemini_credentials, gemini_source = self._provider_credentials("gemini")
        if gemini_key := gemini_credentials.get("api_key"):
            model = gemini_credentials.get(
                "model", PROVIDER_REGISTRY["gemini"].default_model
            )
            providers_by_name["gemini"].append(
                GeminiProvider(gemini_key, model, gemini_source)
            )

        mistral_credentials, mistral_source = self._provider_credentials("mistral")
        if mistral_key := mistral_credentials.get("api_key"):
            model = mistral_credentials.get(
                "model", PROVIDER_REGISTRY["mistral"].default_model
            )
            providers_by_name["mistral"].append(
                MistralProvider(mistral_key, model, mistral_source)
            )

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

    def get_configured_provider_status(self) -> List[Dict[str, object]]:
        """Return masked metadata for configured provider instances."""
        statuses = []
        for provider in self.providers:
            statuses.append(
                {
                    "name": provider.name,
                    "model": provider.model,
                    "has_api_key": provider.name != "ollama",
                    "credential_source": provider.credential_source,
                }
            )
        return statuses
