#!/usr/bin/env python3
"""
Fix Gemma 3 1B model prompt issues
Tests different prompt formats to avoid <unused> tokens
"""

import asyncio
import sys
import os

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'services'))

from model_service import ModelService


async def test_prompt_formats():
    """Test different prompt formats to find ones that work."""
    print("🔧 Testing different prompt formats for Gemma 3 1B...")
    
    model_service = ModelService()
    
    try:
        # Load model
        print("📥 Loading model...")
        await model_service.load_model()
        print("✅ Model loaded successfully!")
        
        # Test different prompt formats
        test_prompts = [
            "What is health?",
            "Health:",
            "Q: What is health?\nA:",
            "Question: What is health?\nAnswer:",
            "Explain health.",
            "Sexual health means",
            "Define: health",
            "Health is"
        ]
        
        successful_prompts = []
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n🧪 Test {i}: '{prompt}'")
            try:
                # Generate with minimal parameters
                response = await model_service.generate_response_with_language(prompt, "en")
                
                # Check if response is valid
                if response and len(response.strip()) > 5 and '<unused' not in response:
                    print(f"✅ SUCCESS: {response[:100]}...")
                    successful_prompts.append((prompt, response))
                else:
                    print(f"❌ FAILED: Invalid response")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)[:100]}...")
        
        print(f"\n📊 Results: {len(successful_prompts)}/{len(test_prompts)} prompts successful")
        
        if successful_prompts:
            print("\n✅ Successful prompt formats:")
            for prompt, response in successful_prompts:
                print(f"  - '{prompt}' → '{response[:50]}...'")
        else:
            print("\n❌ No successful prompts found")
            
        return successful_prompts
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        print("🧹 Cleaning up...")
        await model_service.cleanup()
        print("✅ Cleanup complete")


async def test_model_config():
    """Test model configuration and tokenizer."""
    print("\n🔍 Testing model configuration...")
    
    model_service = ModelService()
    
    try:
        await model_service.load_model()
        
        # Check model info
        info = model_service.get_model_info()
        print(f"📊 Model info: {info}")
        
        # Check if model has tokenizer
        if hasattr(model_service.model, 'preprocessor'):
            print("✅ Model has preprocessor")
            if hasattr(model_service.model.preprocessor, 'tokenizer'):
                print("✅ Model has tokenizer")
                tokenizer = model_service.model.preprocessor.tokenizer
                
                # Test tokenization
                test_text = "Hello world"
                try:
                    tokens = tokenizer(test_text)
                    print(f"✅ Tokenization test: '{test_text}' → {tokens}")
                except Exception as e:
                    print(f"❌ Tokenization failed: {e}")
            else:
                print("❌ Model missing tokenizer")
        else:
            print("❌ Model missing preprocessor")
            
    except Exception as e:
        print(f"❌ Config test failed: {e}")
    finally:
        await model_service.cleanup()


async def fix_model_generation():
    """Test raw model generation without preprocessing."""
    print("\n🛠️ Testing raw model generation...")
    
    model_service = ModelService()
    
    try:
        await model_service.load_model()
        
        # Test direct model access
        simple_input = "Health"
        print(f"🔤 Testing simple input: '{simple_input}'")
        
        try:
            # Use the model's generate method directly with different parameters
            raw_response = model_service.model.generate(simple_input, max_length=50)
            print(f"📝 Raw response: {raw_response}")
            
            if isinstance(raw_response, str) and '<unused' not in raw_response:
                print("✅ Raw generation successful!")
                return True
            else:
                print("❌ Raw generation still has issues")
                
        except Exception as e:
            print(f"❌ Raw generation failed: {e}")
            
    except Exception as e:
        print(f"❌ Fix test failed: {e}")
    finally:
        await model_service.cleanup()
    
    return False


async def main():
    """Main test function."""
    print("🚀 Starting Gemma 3 1B Model Fix Tests")
    print("="*50)
    
    # Test 1: Model configuration
    await test_model_config()
    
    # Test 2: Raw generation
    await fix_model_generation()
    
    # Test 3: Prompt formats
    successful_prompts = await test_prompt_formats()
    
    print("\n" + "="*50)
    print("🏁 Test Summary")
    print("="*50)
    
    if successful_prompts:
        print("✅ Found working prompt formats!")
        print("💡 Recommended prompt format:")
        best_prompt, best_response = successful_prompts[0]
        print(f"   Template: '{best_prompt}' → '{best_response[:50]}...'")
    else:
        print("❌ No working prompt formats found")
        print("💡 Recommendations:")
        print("   1. Check model file integrity")
        print("   2. Verify tokenizer configuration")
        print("   3. Try downloading a fresh model")


if __name__ == "__main__":
    asyncio.run(main()) 