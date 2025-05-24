"""
Prompt Optimizer for LLB Gemma 3 1B Model
Optimizes prompts to avoid <unused> tokens and improve response quality
"""

import os
import sys
import json
import asyncio
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import logging

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'services'))

from model_service import ModelService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PromptTemplate:
    """Template for prompt optimization."""
    name: str
    template: str
    language: str
    expected_quality: float
    test_cases: List[str]


class PromptOptimizer:
    """Optimizes prompts for better model responses."""
    
    def __init__(self):
        self.model_service = ModelService()
        self.optimized_prompts = {}
        
        # Define base prompt templates
        self.base_templates = {
            "en": [
                {
                    "name": "direct_instruction",
                    "template": "You are a sexual health educator. Answer this question: {question}",
                    "expected_quality": 0.7
                },
                {
                    "name": "conversational",
                    "template": "Human: I have a question about sexual health: {question}\n\nAssistant:",
                    "expected_quality": 0.8
                },
                {
                    "name": "structured",
                    "template": "Question: {question}\n\nAs a sexual health expert, I will provide accurate information:\n\nAnswer:",
                    "expected_quality": 0.9
                }
            ],
            "zh-CN": [
                {
                    "name": "direct_instruction",
                    "template": "你是性健康教育专家。请回答这个问题：{question}",
                    "expected_quality": 0.7
                },
                {
                    "name": "conversational", 
                    "template": "Human: 我有一个关于性健康的问题：{question}\n\nAssistant:",
                    "expected_quality": 0.8
                },
                {
                    "name": "structured",
                    "template": "问题：{question}\n\n作为性健康专家，我将提供准确的信息：\n\n回答：",
                    "expected_quality": 0.9
                }
            ]
        }
        
        # Test questions for evaluation
        self.test_questions = {
            "en": [
                "What is sexual health?",
                "How do condoms work?",
                "What are STIs?",
                "How to communicate about consent?",
                "What is reproductive anatomy?"
            ],
            "zh-CN": [
                "什么是性健康？",
                "安全套如何工作？",
                "什么是性传播疾病？",
                "如何沟通同意问题？",
                "什么是生殖解剖学？"
            ]
        }
    
    async def initialize(self):
        """Initialize the model service."""
        logger.info("Initializing model service for prompt optimization...")
        await self.model_service.load_model()
        logger.info("✅ Model service initialized")
    
    async def test_prompt_template(self, template: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Test a prompt template with multiple questions."""
        logger.info(f"Testing template '{template['name']}' for language '{language}'")
        
        results = {
            "template": template,
            "language": language,
            "test_results": [],
            "average_quality": 0.0,
            "success_rate": 0.0
        }
        
        successful_tests = 0
        total_quality = 0.0
        
        for question in self.test_questions[language]:
            try:
                # Format the prompt
                formatted_prompt = template["template"].format(question=question)
                
                # Generate response
                response = await self.model_service.generate_response_with_language(
                    formatted_prompt, language
                )
                
                # Evaluate response quality
                quality_score = self._evaluate_response_quality(response, question, language)
                
                test_result = {
                    "question": question,
                    "prompt": formatted_prompt,
                    "response": response,
                    "quality_score": quality_score,
                    "success": quality_score > 0.5
                }
                
                results["test_results"].append(test_result)
                
                if test_result["success"]:
                    successful_tests += 1
                    total_quality += quality_score
                
                logger.info(f"  Question: {question[:30]}... Quality: {quality_score:.2f}")
                
            except Exception as e:
                logger.error(f"  Failed for question '{question}': {e}")
                results["test_results"].append({
                    "question": question,
                    "prompt": formatted_prompt,
                    "response": None,
                    "quality_score": 0.0,
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate metrics
        total_tests = len(self.test_questions[language])
        results["success_rate"] = successful_tests / total_tests if total_tests > 0 else 0.0
        results["average_quality"] = total_quality / successful_tests if successful_tests > 0 else 0.0
        
        logger.info(f"  Template '{template['name']}': Success rate: {results['success_rate']:.2f}, Avg quality: {results['average_quality']:.2f}")
        
        return results
    
    def _evaluate_response_quality(self, response: str, question: str, language: str) -> float:
        """Evaluate the quality of a response."""
        if not response or len(response.strip()) < 10:
            return 0.0
        
        quality_score = 0.0
        
        # Check for garbage tokens
        garbage_patterns = ['<unused', '<unk>', '<pad>', '[UNK]', '[PAD]']
        has_garbage = any(pattern in response for pattern in garbage_patterns)
        if has_garbage:
            return 0.1  # Very low score for garbage responses
        
        # Length check (reasonable response length)
        if 20 <= len(response) <= 500:
            quality_score += 0.3
        
        # Language consistency check
        if language == "zh-CN":
            chinese_chars = len([c for c in response if '\u4e00' <= c <= '\u9fff'])
            if chinese_chars > len(response) * 0.3:  # At least 30% Chinese characters
                quality_score += 0.3
        else:
            english_words = len([w for w in response.split() if w.isalpha()])
            if english_words > len(response.split()) * 0.7:  # At least 70% English words
                quality_score += 0.3
        
        # Content relevance (basic keyword matching)
        question_lower = question.lower()
        response_lower = response.lower()
        
        # Sexual health keywords
        health_keywords = {
            "en": ["health", "sexual", "safe", "protection", "education", "body", "anatomy"],
            "zh-CN": ["健康", "性", "安全", "保护", "教育", "身体", "解剖"]
        }
        
        keyword_matches = sum(1 for keyword in health_keywords.get(language, []) 
                             if keyword in response_lower)
        if keyword_matches > 0:
            quality_score += min(0.4, keyword_matches * 0.1)
        
        return min(1.0, quality_score)
    
    async def optimize_prompts(self) -> Dict[str, Any]:
        """Optimize prompts for all languages."""
        logger.info("Starting prompt optimization...")
        
        optimization_results = {
            "timestamp": asyncio.get_event_loop().time(),
            "languages": {},
            "best_templates": {}
        }
        
        for language in ["en", "zh-CN"]:
            logger.info(f"\n🔄 Optimizing prompts for language: {language}")
            
            language_results = {
                "templates": [],
                "best_template": None,
                "best_score": 0.0
            }
            
            # Test all templates for this language
            for template in self.base_templates[language]:
                result = await self.test_prompt_template(template, language)
                language_results["templates"].append(result)
                
                # Track best template
                combined_score = (result["success_rate"] + result["average_quality"]) / 2
                if combined_score > language_results["best_score"]:
                    language_results["best_score"] = combined_score
                    language_results["best_template"] = template
            
            optimization_results["languages"][language] = language_results
            optimization_results["best_templates"][language] = language_results["best_template"]
            
            logger.info(f"✅ Best template for {language}: '{language_results['best_template']['name']}' (score: {language_results['best_score']:.2f})")
        
        return optimization_results
    
    async def save_optimized_prompts(self, results: Dict[str, Any], filepath: str = None):
        """Save optimized prompts to file."""
        if filepath is None:
            filepath = os.path.join(os.path.dirname(__file__), "optimized_prompts.json")
        
        # Create simplified output for saving
        output = {
            "timestamp": results["timestamp"],
            "optimized_templates": {}
        }
        
        for language, template in results["best_templates"].items():
            output["optimized_templates"][language] = {
                "name": template["name"],
                "template": template["template"],
                "expected_quality": template["expected_quality"]
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Optimized prompts saved to: {filepath}")
    
    async def cleanup(self):
        """Cleanup resources."""
        if self.model_service:
            await self.model_service.cleanup()


async def main():
    """Main optimization function."""
    optimizer = PromptOptimizer()
    
    try:
        # Initialize
        await optimizer.initialize()
        
        # Optimize prompts
        results = await optimizer.optimize_prompts()
        
        # Save results
        await optimizer.save_optimized_prompts(results)
        
        # Print summary
        print("\n" + "="*60)
        print("PROMPT OPTIMIZATION SUMMARY")
        print("="*60)
        
        for language, template in results["best_templates"].items():
            print(f"\n🌍 Language: {language}")
            print(f"📝 Best Template: {template['name']}")
            print(f"📊 Expected Quality: {template['expected_quality']}")
            print(f"🔤 Template: {template['template'][:100]}...")
        
        print("\n✅ Optimization complete!")
        
    except Exception as e:
        logger.error(f"❌ Optimization failed: {e}")
        raise
    finally:
        await optimizer.cleanup()


if __name__ == "__main__":
    asyncio.run(main()) 