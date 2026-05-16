"""Tests for AI provider fallback behavior."""

import pytest

from services import ai_providers
from services.ai_providers import AIProviderManager, GitHubModelsProvider, MistralProvider
from services.model_service import ModelService


class FakeResponse:
    """Small httpx response stand-in for provider tests."""

    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise ai_providers.httpx.HTTPStatusError(
                "request failed",
                request=None,
                response=self,
            )

    def json(self):
        return self._payload


class FakeAsyncClient:
    """Capture async HTTP requests without reaching the network."""

    responses = []
    requests = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, **kwargs):
        self.requests.append(("POST", url, kwargs))
        return self.responses.pop(0)

    async def get(self, url, **kwargs):
        self.requests.append(("GET", url, kwargs))
        return self.responses.pop(0)


@pytest.fixture(autouse=True)
def fake_http_client(monkeypatch):
    """Patch provider HTTP calls for deterministic tests."""
    FakeAsyncClient.responses = []
    FakeAsyncClient.requests = []
    monkeypatch.setattr(ai_providers.httpx, "AsyncClient", FakeAsyncClient)


@pytest.fixture(autouse=True)
def clear_provider_env(monkeypatch):
    """Remove provider env so tests opt in to exactly what they need."""
    for key in (
        "AI_PROVIDER_ORDER",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "GITHUB_MODELS_TOKEN",
        "GITHUB_MODELS_MODELS",
        "GITHUB_MODELS_API_VERSION",
        "OLLAMA_ENABLED",
        "OLLAMA_BASE_URL",
        "OLLAMA_MODEL",
        "MISTRAL_API_KEY",
        "MISTRAL_MODEL",
    ):
        monkeypatch.delenv(key, raising=False)
    ai_providers.clear_desktop_provider_credentials()
    yield
    ai_providers.clear_desktop_provider_credentials()


def test_provider_catalog_uses_current_defaults_without_secrets():
    """Provider catalog exposes current model defaults, not credentials."""
    catalog = ai_providers.get_provider_catalog()
    providers = {provider["name"]: provider for provider in catalog}

    assert providers["openai"]["default_model"] == "gpt-5.2"
    assert "gpt-5-mini" in providers["openai"]["models"]
    assert providers["anthropic"]["default_model"] == "claude-opus-4-7"
    assert providers["gemini"]["default_model"] == "gemini-3-pro-preview"
    assert providers["mistral"]["default_model"] == "mistral-medium-3.5"

    for provider in catalog:
        assert "api_key" not in provider
        assert "token" not in provider


@pytest.mark.asyncio
async def test_mistral_provider_posts_chat_completion_request():
    """Mistral provider sends OpenAI-compatible chat completion requests."""
    FakeAsyncClient.responses = [
        FakeResponse(
            200,
            {"choices": [{"message": {"content": "Hello from Mistral"}}]},
        )
    ]
    provider = MistralProvider(
        api_key="mistral-key",
        model="mistral-medium-3.5",
    )

    result = await provider.generate_response(
        "Say hello",
        max_tokens=321,
        temperature=0.1,
    )

    assert result == "Hello from Mistral"
    method, url, kwargs = FakeAsyncClient.requests[0]
    assert method == "POST"
    assert url == "https://api.mistral.ai/v1/chat/completions"
    assert kwargs["headers"]["Authorization"] == "Bearer mistral-key"
    assert kwargs["json"] == {
        "model": "mistral-medium-3.5",
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 321,
        "temperature": 0.1,
    }


def test_provider_manager_prefers_desktop_credentials_over_environment(monkeypatch):
    """Desktop BYOK credentials override process-level environment values."""
    monkeypatch.setenv("OPENAI_API_KEY", "env-openai-key")
    monkeypatch.setenv("OPENAI_MODEL", "env-model")
    ai_providers.set_desktop_provider_credentials(
        {"openai": {"api_key": "desktop-openai-key", "model": "desktop-model"}}
    )

    manager = AIProviderManager()

    assert len(manager.providers) == 1
    provider = manager.providers[0]
    assert provider.name == "openai"
    assert provider.api_key == "desktop-openai-key"
    assert provider.model == "desktop-model"


def test_provider_manager_masks_configured_provider_status(monkeypatch):
    """Provider status reports key presence without exposing key material."""
    monkeypatch.setenv("MISTRAL_API_KEY", "mistral-secret")
    manager = AIProviderManager()

    status = manager.get_configured_provider_status()

    assert status == [
        {
            "name": "mistral",
            "model": "mistral-medium-3.5",
            "has_api_key": True,
            "credential_source": "environment",
        }
    ]
    assert "mistral-secret" not in str(status)


@pytest.mark.asyncio
async def test_github_models_provider_posts_chat_completion_request():
    """GitHub Models provider sends the documented chat inference request."""
    FakeAsyncClient.responses = [
        FakeResponse(
            200,
            {
                "choices": [
                    {"message": {"role": "assistant", "content": "Hello from GitHub"}}
                ]
            },
        )
    ]
    provider = GitHubModelsProvider(
        token="ghp_test",
        model="openai/gpt-4.1",
        api_version="2026-03-10",
    )

    result = await provider.generate_response(
        "Say hello",
        max_tokens=123,
        temperature=0.2,
    )

    assert result == "Hello from GitHub"
    method, url, kwargs = FakeAsyncClient.requests[0]
    assert method == "POST"
    assert url == "https://models.github.ai/inference/chat/completions"
    assert kwargs["headers"]["Authorization"] == "Bearer ghp_test"
    assert kwargs["headers"]["Accept"] == "application/vnd.github+json"
    assert kwargs["headers"]["X-GitHub-Api-Version"] == "2026-03-10"
    assert kwargs["json"] == {
        "model": "openai/gpt-4.1",
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 123,
        "temperature": 0.2,
        "stream": False,
    }


def test_provider_manager_uses_free_first_order(monkeypatch):
    """Local and GitHub providers are preferred before paid direct APIs."""
    monkeypatch.setenv("OLLAMA_ENABLED", "true")
    monkeypatch.setenv("GITHUB_MODELS_TOKEN", "github-token")
    monkeypatch.setenv("GITHUB_MODELS_MODELS", "openai/gpt-4.1, microsoft/phi-4")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")

    manager = AIProviderManager()

    assert [provider.name for provider in manager.providers] == [
        "ollama",
        "github",
        "github",
        "openai",
        "anthropic",
        "gemini",
    ]
    assert [provider.model for provider in manager.providers[:3]] == [
        "llama3.2",
        "openai/gpt-4.1",
        "microsoft/phi-4",
    ]


def test_provider_manager_respects_custom_order(monkeypatch):
    """Provider order can be configured without exposing users to bot choices."""
    monkeypatch.setenv("AI_PROVIDER_ORDER", "github,ollama")
    monkeypatch.setenv("OLLAMA_ENABLED", "true")
    monkeypatch.setenv("GITHUB_MODELS_TOKEN", "github-token")
    monkeypatch.setenv("GITHUB_MODELS_MODELS", "openai/gpt-4.1")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")

    manager = AIProviderManager()

    assert [provider.name for provider in manager.providers] == [
        "github",
        "ollama",
        "openai",
    ]


@pytest.mark.asyncio
async def test_manager_falls_back_between_github_models(monkeypatch):
    """Multiple configured GitHub model IDs are tried in order."""
    monkeypatch.setenv("GITHUB_MODELS_TOKEN", "github-token")
    monkeypatch.setenv("GITHUB_MODELS_MODELS", "model-a, model-b")
    FakeAsyncClient.responses = [
        FakeResponse(200, {"models": []}),
        FakeResponse(429, {"message": "rate limited"}),
        FakeResponse(200, {"models": []}),
        FakeResponse(
            200,
            {"choices": [{"message": {"content": "second model answered"}}]},
        ),
    ]
    manager = AIProviderManager()
    await manager.initialize()

    result = await manager.generate_response("Question")

    assert result == "second model answered"
    assert manager.current_provider.model == "model-b"


@pytest.mark.asyncio
async def test_provider_manager_reports_active_provider(monkeypatch):
    """Status metadata includes active provider and model without token data."""
    monkeypatch.setenv("GITHUB_MODELS_TOKEN", "github-token")
    monkeypatch.setenv("GITHUB_MODELS_MODELS", "openai/gpt-4.1")
    FakeAsyncClient.responses = [FakeResponse(200, {"models": []})]
    manager = AIProviderManager()

    await manager.initialize()

    assert manager.get_provider_info() == {
        "provider": "github",
        "model": "openai/gpt-4.1",
        "available_providers": ["github"],
    }


def test_model_service_includes_provider_metadata():
    """Model status includes active provider details when available."""
    manager = ai_providers.AIProviderManager()
    manager.current_provider = GitHubModelsProvider(
        token="github-token",
        model="openai/gpt-4.1",
    )
    service = ModelService()
    service.provider_manager = manager
    service._loaded = True

    assert service.get_model_info() == {
        "provider": "github",
        "model": "openai/gpt-4.1",
        "available_providers": ["github"],
    }
