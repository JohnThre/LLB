#!/usr/bin/env python3
"""
Test script for LLB Gemma 3 1B model
"""

import asyncio
import sys
import os

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'services'))

from model_service import ModelService


async def test_model():
    """Test the model loading and generation."""
    print("🔄 Testing LLB Gemma 3 1B model...")
    
    model_service = ModelService()
    
    try:
        # Test model loading
        print("📥 Loading model...")
        await model_service.load_model()
        print("✅ Model loaded successfully!")
        
        # Test model info
        info = model_service.get_model_info()
        print(f"📊 Model info: {info}")
        
        # Test generation with English
        print("\n🔤 Testing English generation...")
        english_prompt = "Human: You are a sexual health educator. What is sexual health?\n\nAssistant:"
        english_response = await model_service.generate_response_with_language(english_prompt, "en")
        print(f"📝 English response: {english_response[:200]}...")
        
        # Test generation with Chinese
        print("\n🔤 Testing Chinese generation...")
        chinese_prompt = "Human: 你是性健康教育专家。什么是性健康？\n\nAssistant:"
        chinese_response = await model_service.generate_response_with_language(chinese_prompt, "zh-CN")
        print(f"📝 Chinese response: {chinese_response[:200]}...")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        await model_service.cleanup()
        print("✅ Cleanup complete")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_model())
    sys.exit(0 if success else 1) 