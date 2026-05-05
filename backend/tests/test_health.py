import pytest

def test_basic_functionality():
    """Test basic functionality without full app initialization"""
    # Test basic Python functionality
    assert 1 + 1 == 2
    
def test_imports():
    """Test that core modules can be imported"""
    try:
        from app.core.config import settings
        assert settings.PROJECT_NAME == "LLB API"
    except ImportError as e:
        pytest.fail(f"Failed to import core modules: {e}")