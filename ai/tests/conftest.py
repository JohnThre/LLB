"""Shared test fixtures for AI module tests."""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "What is sexual health education?"


@pytest.fixture
def sample_chinese_text():
    """Sample Chinese text for testing."""
    return "什么是性健康教育？"


@pytest.fixture
def mock_model_path():
    """Mock model path for testing."""
    return "ai/models/gemma3-keras-gemma3_1b-v3"
