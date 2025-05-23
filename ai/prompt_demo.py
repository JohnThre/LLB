"""
Demonstration script for LLB prompt engineering system.
Shows various use cases and examples of the prompt system in action.
"""

import json
from typing import List, Dict
from prompt_engine import PromptEngine, PromptRequest, InputType


def demo_basic_usage():
    """Demonstrate basic usage of the prompt engine."""
    print("=== LLB Prompt Engineering Demo ===\n")
    
    engine = PromptEngine()
    
    # Example 1: Basic English question
    print("1. Basic English Question:")
    request = PromptRequest(
        content="What is sexual health?",
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    print(f"Language Detected: {response.language_detected}")
    print(f"Topic: {response.metadata['topic']}")
    print(f"Confidence: {response.confidence_score:.2f}")
    print(f"Template: {response.template_used}")
    print(f"Prompt Preview: {response.formatted_prompt[:200]}...\n")
    
    # Example 2: Chinese question
    print("2. Chinese Question:")
    request = PromptRequest(
        content="什么是性健康？",
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    print(f"Language Detected: {response.language_detected}")
    print(f"Topic: {response.metadata['topic']}")
    print(f"Confidence: {response.confidence_score:.2f}")
    print(f"Prompt Preview: {response.formatted_prompt[:200]}...\n")
    
    # Example 3: Henan dialect
    print("3. Henan Dialect Question:")
    request = PromptRequest(
        content="俺想知道性健康是啥意思？",
        input_type=InputType.TEXT,
        cultural_context="henan"
    )
    response = engine.process_request(request)
    print(f"Language Detected: {response.language_detected}")
    print(f"Cultural Context: {response.metadata['cultural_context']}")
    print(f"Topic: {response.metadata['topic']}")
    print(f"Confidence: {response.confidence_score:.2f}")
    print(f"Prompt Preview: {response.formatted_prompt[:200]}...\n")


def demo_topic_classification():
    """Demonstrate topic classification capabilities."""
    print("=== Topic Classification Demo ===\n")
    
    engine = PromptEngine()
    
    test_questions = [
        ("How can I practice safe sex?", "safety"),
        ("What are different types of birth control?", "contraception"),
        ("Can you explain the menstrual cycle?", "anatomy"),
        ("How do I talk to my partner about sex?", "relationship"),
        ("What are STIs and how to prevent them?", "sti"),
        ("What does consent mean?", "consent"),
        ("Tell me about sexual health basics", "basic_education")
    ]
    
    for question, expected_topic in test_questions:
        request = PromptRequest(
            content=question,
            input_type=InputType.TEXT
        )
        response = engine.process_request(request)
        detected_topic = response.metadata['topic']
        
        status = "✓" if detected_topic == expected_topic else "✗"
        print(f"{status} '{question}'")
        print(f"   Expected: {expected_topic}, Detected: {detected_topic}")
        print(f"   Confidence: {response.confidence_score:.2f}\n")


def demo_safety_assessment():
    """Demonstrate safety assessment features."""
    print("=== Safety Assessment Demo ===\n")
    
    engine = PromptEngine()
    
    safety_test_cases = [
        "Is it safe to have unprotected sex?",
        "I think I might have an STI, what should I do?",
        "Can you diagnose my symptoms?",
        "What are some risky sexual behaviors?",
        "How to have safe sex?"
    ]
    
    for question in safety_test_cases:
        request = PromptRequest(
            content=question,
            input_type=InputType.TEXT
        )
        response = engine.process_request(request)
        
        print(f"Question: '{question}'")
        print(f"Safety Flags: {response.safety_flags}")
        print(f"Confidence: {response.confidence_score:.2f}")
        if response.safety_flags:
            print(f"⚠️  Safety concerns detected")
        else:
            print(f"✓ No safety concerns")
        print()


def demo_document_analysis():
    """Demonstrate document analysis capabilities."""
    print("=== Document Analysis Demo ===\n")
    
    engine = PromptEngine()
    
    sample_document = """
    Sexual health is a state of physical, emotional, mental and social 
    well-being in relation to sexuality. It requires a positive and 
    respectful approach to sexuality and sexual relationships, as well 
    as the possibility of having pleasurable and safe sexual experiences, 
    free of coercion, discrimination and violence.
    
    Contraceptive methods include barrier methods like condoms, hormonal 
    methods like birth control pills, and long-acting reversible 
    contraceptives like IUDs. Each method has different effectiveness 
    rates and considerations.
    """
    
    request = PromptRequest(
        content=sample_document,
        input_type=InputType.DOCUMENT
    )
    response = engine.process_request(request)
    
    print("Document Analysis:")
    print(f"Language: {response.language_detected}")
    print(f"Template Used: {response.template_used}")
    print(f"Confidence: {response.confidence_score:.2f}")
    print(f"Prompt Preview: {response.formatted_prompt[:300]}...\n")


def demo_multilingual_support():
    """Demonstrate multilingual support."""
    print("=== Multilingual Support Demo ===\n")
    
    engine = PromptEngine()
    
    multilingual_questions = [
        ("How to prevent STIs?", "en"),
        ("如何预防性传播疾病？", "zh-CN"),
        ("俺咋样才能预防性病？", "zh-CN-henan"),
        ("What is consent in relationships?", "en"),
        ("什么是关系中的同意？", "zh-CN")
    ]
    
    for question, expected_lang in multilingual_questions:
        request = PromptRequest(
            content=question,
            input_type=InputType.TEXT
        )
        response = engine.process_request(request)
        
        print(f"Question: '{question}'")
        print(f"Expected Language: {expected_lang}")
        print(f"Detected Language: {response.language_detected}")
        print(f"Topic: {response.metadata['topic']}")
        print(f"Match: {'✓' if response.language_detected == expected_lang else '✗'}")
        print()


def demo_cultural_adaptation():
    """Demonstrate cultural adaptation features."""
    print("=== Cultural Adaptation Demo ===\n")
    
    engine = PromptEngine()
    
    cultural_scenarios = [
        {
            "question": "How to talk to parents about sex education?",
            "context": "chinese",
            "language": "zh-CN"
        },
        {
            "question": "俺和对象咋样才能安全地过性生活？",
            "context": "henan", 
            "language": "zh-CN"
        },
        {
            "question": "What are cultural differences in sex education?",
            "context": "western",
            "language": "en"
        }
    ]
    
    for scenario in cultural_scenarios:
        request = PromptRequest(
            content=scenario["question"],
            input_type=InputType.TEXT,
            language=scenario["language"],
            cultural_context=scenario["context"]
        )
        response = engine.process_request(request)
        
        print(f"Question: '{scenario['question']}'")
        print(f"Cultural Context: {scenario['context']}")
        print(f"Language: {response.language_detected}")
        print(f"Template: {response.template_used}")
        print(f"Confidence: {response.confidence_score:.2f}")
        print()


def demo_few_shot_examples():
    """Demonstrate few-shot learning examples in prompts."""
    print("=== Few-Shot Learning Examples ===\n")
    
    engine = PromptEngine()
    
    # Get a template with few-shot examples
    template = engine.sexual_health_prompts.get_template("basic_education", "en")
    
    if template and template.few_shot_examples:
        print("Few-shot examples in basic education template:")
        for i, example in enumerate(template.few_shot_examples, 1):
            print(f"\nExample {i}:")
            print(f"Input: {example.input_text}")
            print(f"Output: {example.expected_output[:100]}...")
            print(f"Language: {example.language}")
    
    # Show how examples are included in formatted prompts
    request = PromptRequest(
        content="Is it normal to have questions about sexuality?",
        input_type=InputType.TEXT
    )
    response = engine.process_request(request)
    
    print(f"\nFormatted prompt includes examples:")
    print(f"Prompt length: {len(response.formatted_prompt)} characters")
    print("Examples are automatically included in the prompt to guide the AI model.")


def generate_usage_report():
    """Generate a usage report showing system capabilities."""
    print("=== LLB Prompt Engineering System Report ===\n")
    
    engine = PromptEngine()
    
    print("Supported Languages:")
    for lang in engine.get_supported_languages():
        print(f"  - {lang}")
    
    print(f"\nAvailable Topics:")
    for topic in engine.get_available_topics():
        print(f"  - {topic}")
    
    print(f"\nTemplate Categories:")
    print(f"  - Sexual Health: {len(engine.sexual_health_prompts.get_all_templates())} templates")
    print(f"  - Language Support: {len(engine.language_prompts.manager.templates)} templates")
    print(f"  - Document Analysis: {len(engine.document_prompts.manager.templates)} templates")
    
    print(f"\nDocument Analysis Types:")
    for analysis_type in engine.document_prompts.get_all_analysis_types():
        print(f"  - {analysis_type}")
    
    print(f"\nSafety Features:")
    print(f"  - Language detection and filtering")
    print(f"  - Content safety assessment")
    print(f"  - Medical advice detection")
    print(f"  - Age-appropriate content filtering")
    print(f"  - Cultural sensitivity adaptation")


def main():
    """Run all demonstration functions."""
    try:
        demo_basic_usage()
        demo_topic_classification()
        demo_safety_assessment()
        demo_document_analysis()
        demo_multilingual_support()
        demo_cultural_adaptation()
        demo_few_shot_examples()
        generate_usage_report()
        
        print("\n=== Demo Complete ===")
        print("The LLB prompt engineering system is ready for integration!")
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("Please check the prompt system setup.")


if __name__ == "__main__":
    main() 