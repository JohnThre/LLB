"""
Base prompt template system for LLB sexual health education AI.
Provides core functionality for prompt engineering and few-shot learning.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import re


class PromptType(Enum):
    """Types of prompts supported by the system."""
    EDUCATIONAL = "educational"
    CONVERSATIONAL = "conversational"
    DOCUMENT_ANALYSIS = "document_analysis"
    SAFETY_CHECK = "safety_check"
    LANGUAGE_DETECTION = "language_detection"


@dataclass
class FewShotExample:
    """Structure for few-shot learning examples."""
    input_text: str
    expected_output: str
    context: Optional[str] = None
    language: str = "en"
    
    def format(self) -> str:
        """Format the example for inclusion in prompts."""
        if self.context:
            return f"Context: {self.context}\nUser: {self.input_text}\n" \
                   f"Assistant: {self.expected_output}"
        return f"User: {self.input_text}\nAssistant: {self.expected_output}"


class PromptTemplate:
    """Base class for creating and managing prompt templates."""
    
    def __init__(
        self,
        template: str,
        prompt_type: PromptType,
        language: str = "en",
        few_shot_examples: Optional[List[FewShotExample]] = None,
        system_prompt: Optional[str] = None
    ):
        self.template = template
        self.prompt_type = prompt_type
        self.language = language
        self.few_shot_examples = few_shot_examples or []
        self.system_prompt = system_prompt or self._default_system_prompt()
    
    def _default_system_prompt(self) -> str:
        """Default system prompt for sexual health education."""
        return (
            "You are a knowledgeable, compassionate sexual health educator "
            "providing accurate, non-judgmental information. Always prioritize "
            "safety, consent, and evidence-based information. Be culturally "
            "sensitive and age-appropriate in your responses."
        )
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        # Build the complete prompt
        prompt_parts = [self.system_prompt]
        
        # Add few-shot examples if available
        if self.few_shot_examples:
            prompt_parts.append("\nHere are some examples:")
            for example in self.few_shot_examples:
                prompt_parts.append(f"\n{example.format()}")
            prompt_parts.append("\nNow, please respond to the following:")
        
        # Add the main template
        formatted_template = self.template.format(**kwargs)
        prompt_parts.append(f"\n{formatted_template}")
        
        return "\n".join(prompt_parts)
    
    def add_example(self, example: FewShotExample) -> None:
        """Add a few-shot example to the template."""
        self.few_shot_examples.append(example)
    
    def validate_variables(self, **kwargs) -> bool:
        """Validate that all required template variables are provided."""
        try:
            self.template.format(**kwargs)
            return True
        except KeyError:
            return False


class PromptManager:
    """Manages multiple prompt templates and provides selection logic."""
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self.language_mappings: Dict[str, str] = {
            "en": "english",
            "zh-CN": "chinese_simplified",
            "zh-TW": "chinese_traditional"
        }
    
    def register_template(self, name: str, template: PromptTemplate) -> None:
        """Register a new prompt template."""
        self.templates[name] = template
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Retrieve a template by name."""
        return self.templates.get(name)
    
    def get_templates_by_type(
        self, 
        prompt_type: PromptType
    ) -> List[PromptTemplate]:
        """Get all templates of a specific type."""
        return [
            template for template in self.templates.values()
            if template.prompt_type == prompt_type
        ]
    
    def get_templates_by_language(self, language: str) -> List[PromptTemplate]:
        """Get all templates for a specific language."""
        return [
            template for template in self.templates.values()
            if template.language == language
        ]
    
    def select_best_template(
        self,
        prompt_type: PromptType,
        language: str = "en",
        context: Optional[str] = None
    ) -> Optional[PromptTemplate]:
        """Select the best template based on type, language, and context."""
        candidates = [
            template for template in self.templates.values()
            if template.prompt_type == prompt_type and 
               template.language == language
        ]
        
        if not candidates:
            # Fallback to English if no template found for the language
            candidates = [
                template for template in self.templates.values()
                if template.prompt_type == prompt_type and 
                   template.language == "en"
            ]
        
        # For now, return the first candidate
        # In the future, this could include more sophisticated selection logic
        return candidates[0] if candidates else None
    
    def create_dynamic_prompt(
        self,
        base_template: str,
        examples: List[FewShotExample],
        prompt_type: PromptType,
        language: str = "en"
    ) -> PromptTemplate:
        """Create a dynamic prompt template with examples."""
        return PromptTemplate(
            template=base_template,
            prompt_type=prompt_type,
            language=language,
            few_shot_examples=examples
        )
    
    def export_templates(self, filepath: str) -> None:
        """Export all templates to a JSON file."""
        export_data = {}
        for name, template in self.templates.items():
            export_data[name] = {
                "template": template.template,
                "prompt_type": template.prompt_type.value,
                "language": template.language,
                "system_prompt": template.system_prompt,
                "few_shot_examples": [
                    {
                        "input_text": ex.input_text,
                        "expected_output": ex.expected_output,
                        "context": ex.context,
                        "language": ex.language
                    }
                    for ex in template.few_shot_examples
                ]
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    def import_templates(self, filepath: str) -> None:
        """Import templates from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        for name, data in import_data.items():
            examples = [
                FewShotExample(
                    input_text=ex["input_text"],
                    expected_output=ex["expected_output"],
                    context=ex.get("context"),
                    language=ex.get("language", "en")
                )
                for ex in data.get("few_shot_examples", [])
            ]
            
            template = PromptTemplate(
                template=data["template"],
                prompt_type=PromptType(data["prompt_type"]),
                language=data.get("language", "en"),
                few_shot_examples=examples,
                system_prompt=data.get("system_prompt")
            )
            
            self.register_template(name, template) 