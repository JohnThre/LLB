"""
Tests for AI service functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.ai_service import AIService


@pytest.fixture
def ai_service():
    """Create AI service instance for testing."""
    return AIService()


@pytest.mark.asyncio
async def test_ai_service_initialization(ai_service):
    """Test AI service initialization."""
    with patch.object(ai_service, '_ensure_services'):
        await ai_service.initialize()
        assert ai_service.is_initialized is True


@pytest.mark.asyncio
async def test_ai_service_cleanup(ai_service):
    """Test AI service cleanup."""
    ai_service.is_initialized = True
    ai_service.model_service = AsyncMock()
    
    await ai_service.cleanup()
    assert ai_service.is_initialized is False


def test_detect_language_english(ai_service):
    """Test language detection for English text."""
    text = "What is sexual health education?"
    language = ai_service._detect_language(text)
    assert language == "en"


def test_detect_language_chinese(ai_service):
    """Test language detection for Chinese text."""
    text = "什么是性健康教育？"
    language = ai_service._detect_language(text)
    assert language == "zh-CN"


def test_detect_language_henan_dialect(ai_service):
    """Test language detection for Henan dialect."""
    text = "俺想知道啥是性健康"
    language = ai_service._detect_language(text)
    assert language == "zh-CN-henan"


def test_classify_topic_anatomy(ai_service):
    """Test topic classification for anatomy."""
    message = "Tell me about human anatomy and body development"
    topic = ai_service._classify_topic(message, "en")
    assert topic == "anatomy"


def test_classify_topic_contraception(ai_service):
    """Test topic classification for contraception."""
    message = "What are the different types of birth control?"
    topic = ai_service._classify_topic(message, "en")
    assert topic == "contraception"


def test_classify_topic_chinese(ai_service):
    """Test topic classification for Chinese text."""
    message = "避孕套怎么使用？"
    topic = ai_service._classify_topic(message, "zh-CN")
    assert topic == "contraception"


@pytest.mark.asyncio
async def test_generate_response_success(ai_service):
    """Test successful response generation."""
    ai_service.is_initialized = True
    ai_service.model_service = AsyncMock()
    ai_service.prompt_engine = MagicMock()
    
    ai_service.model_service.generate_response_with_language.return_value = "Test response"
    ai_service.prompt_engine.generate_prompt.return_value = "Test prompt"
    
    response = await ai_service.generate_response("Test message", "en")
    
    assert "response" in response
    assert "language" in response
    assert "confidence" in response
    assert "safety_score" in response


@pytest.mark.asyncio
async def test_generate_response_not_initialized(ai_service):
    """Test response generation when service not initialized."""
    ai_service.is_initialized = False
    
    with pytest.raises(RuntimeError, match="AI service not initialized"):
        await ai_service.generate_response("Test message", "en")


def test_is_ready(ai_service):
    """Test is_ready method."""
    ai_service.is_initialized = False
    assert ai_service.is_ready() is False
    
    ai_service.is_initialized = True
    assert ai_service.is_ready() is True


def test_get_supported_languages(ai_service):
    """Test get supported languages."""
    languages = ai_service.get_supported_languages()
    assert isinstance(languages, list)
    assert "en" in languages
    assert "zh-CN" in languages


def test_get_model_info(ai_service):
    """Test get model info."""
    info = ai_service.get_model_info()
    assert isinstance(info, dict)
    assert "name" in info
    assert info["name"] == "Gemma 4 Health Tuned"
    assert info["prompt_system"] == "source_backed_sexual_health"
    assert "version" in info
    assert "loaded" in info


@pytest.mark.asyncio
async def test_generate_fallback_response_uses_source_backed_english_prompt(ai_service):
    """Fallback generation keeps the source-backed English instruction."""
    ai_service.model_service = AsyncMock()
    ai_service.model_service.generate_response_with_language.return_value = "Fallback"

    response = await ai_service._generate_fallback_response(
        "How do condoms help prevent STIs?", "en", "en"
    )

    prompt = ai_service.model_service.generate_response_with_language.call_args.args[0]
    assert "provided approved literature" in prompt
    assert response["prompt_used"] == "basic_fallback"


@pytest.mark.asyncio
async def test_generate_fallback_response_uses_source_backed_chinese_prompt(ai_service):
    """Fallback generation keeps the source-backed Simplified Chinese instruction."""
    ai_service.model_service = AsyncMock()
    ai_service.model_service.generate_response_with_language.return_value = "兜底回答"

    response = await ai_service._generate_fallback_response(
        "安全套如何帮助预防艾滋？", "zh-CN", "zh-CN"
    )

    prompt = ai_service.model_service.generate_response_with_language.call_args.args[0]
    assert "已提供的资料" in prompt
    assert response["language"] == "zh-CN"


def test_get_available_topics(ai_service):
    """Test get available topics."""
    topics = ai_service.get_available_topics()
    assert isinstance(topics, list)
    assert "anatomy" in topics
    assert "contraception" in topics
    assert "consent_education" in topics
