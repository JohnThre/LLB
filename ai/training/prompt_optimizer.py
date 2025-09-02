"""
Prompt optimization system for LLB sexual health education.
Optimizes prompts for better model performance using the main prompt system.
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import sys
import os

# Add the ai directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prompts.sexual_health import SexualHealthPrompts
from prompt_engine import PromptEngine, PromptRequest, InputType

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'services'))
from model_service import ModelService

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
    """Optimizes prompts for sexual health education using the main prompt system."""
    
    def __init__(self):
        self.model_service = ModelService()
        self.prompt_engine = PromptEngine()
        self.sexual_health_prompts = SexualHealthPrompts()
        
        # Test questions for evaluation
        self.test_questions = {
            "en": [
                "What is sexual health?",
                "How do condoms work?",
                "What are STIs?",
                "How to communicate about consent?",
                "What is reproductive anatomy?",
                "What is sexual orientation?",
                "How to discuss sexual health with a partner?",
                "What is emergency contraception?"
            ],
            "zh-CN": [
                "什么是性健康？",
                "安全套如何工作？",
                "什么是性传播疾病？",
                "如何沟通同意问题？",
                "什么是生殖解剖学？",
                "什么是性取向？",
                "如何与伴侣讨论性健康？",
                "什么是紧急避孕？"
            ]
        }
    
    async def initialize(self):
        """Initialize the model service."""
        logger.info("Initializing model service for prompt optimization...")
        await self.model_service.load_model()
        logger.info("✅ Model service initialized")
    
    async def test_prompt_template(self, template_name: str, language: str) -> Dict[str, Any]:
        """Test a prompt template with multiple questions."""
        logger.info(f"Testing template '{template_name}' for language '{language}'")
        
        # Get the template from the main prompt system
        template = self.sexual_health_prompts.get_template(template_name, language)
        if not template:
            logger.error(f"Template '{template_name}' not found for language '{language}'")
            return {
                "template_name": template_name,
                "language": language,
                "test_results": [],
                "average_quality": 0.0,
                "success_rate": 0.0,
                "error": "Template not found"
            }
        
        results = {
            "template_name": template_name,
            "language": language,
            "test_results": [],
            "average_quality": 0.0,
            "success_rate": 0.0
        }
        
        successful_tests = 0
        total_quality = 0.0
        
        for question in self.test_questions[language]:
            try:
                # Create a prompt request
                request = PromptRequest(
                    content=question,
                    language=language,
                    input_type=InputType.TEXT
                )
                
                # Generate prompt using the prompt engine
                formatted_prompt = self.prompt_engine.generate_prompt(request)
                
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
                
                # Sanitize question to prevent log injection
                safe_question = str(question).replace('\n', ' ').replace('\r', ' ')
                logger.info(f"  Question: {safe_question[:30]}... Quality: {quality_score:.2f}")
                
            except Exception as e:
                # Sanitize question to prevent log injection
                safe_question = str(question).replace('\n', ' ').replace('\r', ' ')
                logger.error(f"  Failed for question '{safe_question}': {e}")
                results["test_results"].append({
                    "question": question,
                    "prompt": formatted_prompt if 'formatted_prompt' in locals() else "",
                    "response": None,
                    "quality_score": 0.0,
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate metrics
        total_tests = len(self.test_questions[language])
        results["success_rate"] = successful_tests / total_tests if total_tests > 0 else 0.0
        results["average_quality"] = total_quality / successful_tests if successful_tests > 0 else 0.0
        
        # Sanitize template_name to prevent log injection
        safe_template_name = str(template_name).replace('\n', ' ').replace('\r', ' ')
        logger.info(f"  Template '{safe_template_name}': Success rate: {results['success_rate']:.2f}, Avg quality: {results['average_quality']:.2f}")
        
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
            "en": ["health", "sexual", "safe", "protection", "education", "body", "anatomy", "consent", "relationship"],
            "zh-CN": ["健康", "性", "安全", "保护", "教育", "身体", "解剖", "同意", "关系"]
        }
        
        keyword_matches = sum(1 for keyword in health_keywords.get(language, []) 
                             if keyword in response_lower)
        if keyword_matches > 0:
            quality_score += min(0.4, keyword_matches * 0.1)
        
        return min(1.0, quality_score)
    
    async def optimize_prompts(self) -> Dict[str, Any]:
        """Optimize prompts for all languages using the main prompt system."""
        logger.info("Starting prompt optimization using main prompt system...")
        
        import time
        optimization_results = {
            "timestamp": time.time(),  # Use server-controlled time
            "languages": {},
            "best_templates": {}
        }
        
        # Get available templates from the main prompt system
        available_templates = self.sexual_health_prompts.get_all_templates()
        
        # Use server-controlled supported languages only
        supported_languages = ["en", "zh-CN"]
        for language in supported_languages:
            logger.info(f"\n🔄 Optimizing prompts for language: {language}")
            
            language_results = {
                "templates": [],
                "best_template": None,
                "best_score": 0.0
            }
            
            # Test templates for this language
            template_names = [name for name in available_templates.keys() if name.endswith(f"_{language}")]
            
            for template_name in template_names:
                # Validate template access - only allow predefined templates
                allowed_templates = ["basic", "detailed", "educational", "conversational"]
                base_name = template_name.replace(f"_{language}", "")
                if base_name not in allowed_templates:
                    logger.warning(f"Skipping unauthorized template: {base_name}")
                    continue
                result = await self.test_prompt_template(base_name, language)
                language_results["templates"].append(result)
                
                # Track best template
                combined_score = (result["success_rate"] + result["average_quality"]) / 2
                if combined_score > language_results["best_score"]:
                    language_results["best_score"] = combined_score
                    language_results["best_template"] = {
                        "name": base_name,
                        "score": combined_score
                    }
            
            optimization_results["languages"][language] = language_results
            optimization_results["best_templates"][language] = language_results["best_template"]
            
            logger.info(f"✅ Best template for {language}: {language_results['best_template']}")
        
        return optimization_results
    
    async def save_optimized_prompts(self, results: Dict[str, Any], filepath: str = None):
        """Save optimization results to file."""
        if filepath is None:
            # Use secure default path within current directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(base_dir, "optimization_results.json")
        else:
            # Validate filepath to prevent path traversal
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.abspath(filepath)
            if not filepath.startswith(base_dir):
                raise ValueError(f"Invalid file path: {filepath}")
        
        # Convert results to JSON-serializable format
        serializable_results = {
            "timestamp": results["timestamp"],
            "languages": {},
            "best_templates": results["best_templates"],
            "summary": {
                "total_languages": len(results["languages"]),
                "total_templates_tested": sum(len(lang_data["templates"]) for lang_data in results["languages"].values())
            }
        }
        
        for lang, lang_data in results["languages"].items():
            serializable_results["languages"][lang] = {
                "best_template": lang_data["best_template"],
                "best_score": lang_data["best_score"],
                "template_count": len(lang_data["templates"]),
                "templates": [
                    {
                        "name": t["template_name"],
                        "success_rate": t["success_rate"],
                        "average_quality": t["average_quality"]
                    }
                    for t in lang_data["templates"]
                ]
            }
        
        # Final validation before file write
        if not os.path.basename(filepath).endswith('.json'):
            raise ValueError("Only JSON files are allowed")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Optimization results saved to {filepath}")
    
    async def cleanup(self):
        """Clean up resources."""
        if self.model_service:
            await self.model_service.cleanup()
        logger.info("🧹 Prompt optimizer cleanup complete")


async def main():
    """Main function for prompt optimization."""
    optimizer = PromptOptimizer()
    
    try:
        await optimizer.initialize()
        results = await optimizer.optimize_prompts()
        await optimizer.save_optimized_prompts(results)
        
        # Print summary
        print("\n" + "="*50)
        print("PROMPT OPTIMIZATION SUMMARY")
        print("="*50)
        
        for language, best_template in results["best_templates"].items():
            if best_template:
                print(f"{language}: {best_template['name']} (score: {best_template['score']:.3f})")
            else:
                print(f"{language}: No suitable template found")
        
    except Exception as e:
        logger.error(f"❌ Optimization failed: {e}")
        raise
    finally:
        await optimizer.cleanup()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 