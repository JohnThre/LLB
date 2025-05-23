"""Tests for prompt engineering system."""

import pytest
from prompt_engine import PromptEngine, PromptRequest, InputType


def test_prompt_engine_initialization():
    """Test prompt engine can be initialized."""
    engine = PromptEngine()
    assert engine is not None
    assert hasattr(engine, 'process_request')


def test_basic_prompt_processing(sample_text):
    """Test basic prompt processing."""
    engine = PromptEngine()
    request = PromptRequest(
        content=sample_text,
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    assert response is not None
    assert hasattr(response, 'formatted_prompt')


def test_language_detection(sample_chinese_text):
    """Test language detection functionality."""
    engine = PromptEngine()
    request = PromptRequest(
        content=sample_chinese_text,
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    assert response.language_detected in ['zh-CN', 'zh']


def test_supported_languages():
    """Test getting supported languages."""
    engine = PromptEngine()
    languages = engine.get_supported_languages()
    assert 'en' in languages
    assert 'zh-CN' in languages


def test_available_topics():
    """Test getting available topics."""
    engine = PromptEngine()
    topics = engine.get_available_topics()
    assert 'basic_education' in topics
    assert 'safety' in topics
    assert 'contraception' in topics
