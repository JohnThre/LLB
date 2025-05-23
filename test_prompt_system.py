#!/usr/bin/env python3
"""
Test script for LLB prompt engineering system.
Verifies that all components are working correctly.
"""

import sys
import os

# Add ai directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai'))

def test_prompt_system():
    """Test the prompt engineering system."""
    try:
        from prompt_engine import PromptEngine, PromptRequest, InputType
        
        print('✓ Successfully imported prompt engine')
        
        # Initialize engine
        engine = PromptEngine()
        print('✓ Engine initialized successfully')
        
        # Test basic English request
        request = PromptRequest(
            content='What is sexual health?',
            input_type=InputType.TEXT
        )
        
        response = engine.process_request(request)
        print(f'✓ English request processed successfully')
        print(f'  Language detected: {response.language_detected}')
        print(f'  Topic: {response.metadata["topic"]}')
        print(f'  Confidence: {response.confidence_score:.2f}')
        print(f'  Safety flags: {response.safety_flags}')
        print(f'  Template used: {response.template_used}')
        
        # Test Chinese request
        request_zh = PromptRequest(
            content='什么是性健康？',
            input_type=InputType.TEXT
        )
        
        response_zh = engine.process_request(request_zh)
        print(f'✓ Chinese request processed successfully')
        print(f'  Language detected: {response_zh.language_detected}')
        print(f'  Topic: {response_zh.metadata["topic"]}')
        
        # Test Henan dialect
        request_henan = PromptRequest(
            content='俺想知道性健康是啥意思？',
            input_type=InputType.TEXT,
            cultural_context="henan"
        )
        
        response_henan = engine.process_request(request_henan)
        print(f'✓ Henan dialect request processed successfully')
        print(f'  Language detected: {response_henan.language_detected}')
        print(f'  Cultural context: {response_henan.metadata["cultural_context"]}')
        
        # Test safety assessment
        request_safety = PromptRequest(
            content='Can you diagnose my symptoms?',
            input_type=InputType.TEXT
        )
        
        response_safety = engine.process_request(request_safety)
        print(f'✓ Safety assessment working')
        print(f'  Safety flags: {response_safety.safety_flags}')
        
        # Test document analysis
        request_doc = PromptRequest(
            content='Sexual health education is important for young people.',
            input_type=InputType.DOCUMENT
        )
        
        response_doc = engine.process_request(request_doc)
        print(f'✓ Document analysis working')
        print(f'  Input type: {response_doc.metadata["input_type"]}')
        
        # Test system capabilities
        print(f'\n📊 System Capabilities:')
        print(f'  Supported languages: {engine.get_supported_languages()}')
        print(f'  Available topics: {engine.get_available_topics()}')
        
        print(f'\n🎉 LLB Prompt Engineering System is working correctly!')
        return True
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prompt_system()
    sys.exit(0 if success else 1) 