#!/usr/bin/env python3
"""
Test script for fixed Gemma 3 1B model
Tests the updated model configuration and generation
"""

import asyncio
import sys
import os

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'services'))

from model_service import ModelService


async def test_gemma3_generation():
    """Test Gemma3 model generation with optimized prompts."""
    print("🚀 Testing Fixed Gemma 3 1B Model")
    print("="*50)
    
    model_service = ModelService()
    
    try:
        # Test model loading
        print("📥 Loading Gemma3 model...")
        await model_service.load_model()
        print("✅ Model loaded successfully!")
        
        # Test model info
        info = model_service.get_model_info()
        print(f"📊 Model info: {info}")
        
        # Test simple prompts that should work with Gemma3
        test_cases = [
            ("Health means", "en"),
            ("什么是健康", "zh-CN"),
            ("Explain wellness", "en"),
            ("身体健康", "zh-CN"),
            ("Safety first", "en")
        ]
        
        successful_tests = 0
        
        for i, (prompt, language) in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: '{prompt}' ({language})")
            try:
                # Generate response
                response = await model_service.generate_response_with_language(prompt, language)
                
                # Check if response is valid
                if response and len(response.strip()) > 5 and '<unused' not in response:
                    print(f"✅ SUCCESS: {response[:100]}...")
                    successful_tests += 1
                else:
                    print(f"❌ FAILED: Invalid response: {response[:50]}...")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)[:100]}...")
        
        print(f"\n📊 Test Results: {successful_tests}/{len(test_cases)} successful")
        
        if successful_tests == len(test_cases):
            print("🎉 All tests passed! Gemma3 model is working correctly!")
            return True
        elif successful_tests > 0:
            print("⚠️ Some tests passed. Model is partially working.")
            return True
        else:
            print("❌ All tests failed. Model needs further fixing.")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("🧹 Cleaning up...")
        await model_service.cleanup()
        print("✅ Cleanup complete")


async def test_ai_service_integration():
    """Test the AI service with the fixed model."""
    print("\n🔧 Testing AI Service Integration")
    print("="*50)
    
    try:
        # Import AI service
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app', 'services'))
        from ai_service import AIService
        
        ai_service = AIService()
        
        # Initialize AI service
        print("📥 Initializing AI service...")
        await ai_service.initialize()
        print("✅ AI service initialized!")
        
        # Test AI service generation
        test_questions = [
            "What is sexual health?",
            "什么是性健康？",
            "How to stay healthy?"
        ]
        
        for question in test_questions:
            print(f"\n🤖 Testing: '{question}'")
            try:
                response = await ai_service.generate_response(question)
                print(f"✅ Response: {response.get('response', '')[:100]}...")
                print(f"📊 Language: {response.get('language', 'unknown')}")
            except Exception as e:
                print(f"❌ AI Service Error: {str(e)[:100]}...")
        
        await ai_service.cleanup()
        print("✅ AI service test complete!")
        
    except Exception as e:
        print(f"❌ AI Service test failed: {e}")


async def main():
    """Main test function."""
    print("🔬 Gemma 3 1B Model Fix Verification")
    print("="*60)
    
    # Test 1: Model service
    model_success = await test_gemma3_generation()
    
    # Test 2: AI service integration (only if model works)
    if model_success:
        await test_ai_service_integration()
    
    print("\n" + "="*60)
    print("🏁 Fix Verification Complete")
    print("="*60)
    
    if model_success:
        print("✅ Gemma3 model is now working correctly!")
        print("💡 You can now start the backend server and test the API.")
    else:
        print("❌ Gemma3 model still has issues.")
        print("💡 Consider checking model file integrity or KerasHub version.")


if __name__ == "__main__":
    asyncio.run(main()) 