"""
Main prompt engineering engine for LLB sexual health education application.
Integrates all prompt components and provides unified interface.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# Use absolute imports instead of relative imports
from prompts.base import (
    PromptTemplate, PromptManager, PromptType, FewShotExample
)
from prompts.sexual_health import SexualHealthPrompts
from prompts.language_support import LanguagePrompts
from prompts.document_analysis import DocumentPrompts


class InputType(Enum):
    """Types of user input supported."""
    TEXT = "text"
    VOICE = "voice"
    DOCUMENT = "document"


@dataclass
class PromptRequest:
    """Structure for prompt requests."""
    content: str
    input_type: InputType
    language: Optional[str] = None
    context: Optional[str] = None
    user_age_group: Optional[str] = None  # child, teen, adult
    cultural_context: Optional[str] = None  # chinese, western, henan
    safety_level: str = "standard"  # strict, standard, relaxed


@dataclass
class PromptResponse:
    """Structure for prompt responses."""
    formatted_prompt: str
    template_used: str
    language_detected: str
    safety_flags: List[str]
    confidence_score: float
    metadata: Dict[str, Any]


class PromptEngine:
    """Main prompt engineering engine for LLB application."""
    
    def __init__(self):
        self.sexual_health_prompts = SexualHealthPrompts()
        self.language_prompts = LanguagePrompts()
        self.document_prompts = DocumentPrompts()
        
        # Language detection patterns
        self.language_patterns = {
            "zh-CN": [
                r'[\u4e00-\u9fff]',  # Chinese characters
                r'什么|怎么|为什么|如何',  # Common question words
                r'性健康|避孕|安全套'  # Sexual health terms
            ],
            "zh-CN-henan": [
                r'俺|咋|啥|中不中',  # Henan dialect markers
                r'对象|老婆|老公'  # Regional relationship terms
            ],
            "en": [
                r'\b(what|how|why|when|where)\b',  # Question words
                r'\b(sexual|health|contraception|condom)\b'  # Health terms
            ]
        }
        
        # Topic classification patterns
        self.topic_patterns = {
            "basic_education": [
                r'what is|definition|explain|basic|introduction',
                r'什么是|定义|解释|基本|介绍'
            ],
            "safety": [
                r'safe|safety|protection|prevent|risk',
                r'安全|保护|预防|风险'
            ],
            "contraception": [
                r'birth control|contraception|condom|pill|iud',
                r'避孕|安全套|避孕药|节育'
            ],
            "anatomy": [
                r'anatomy|body|menstrual|cycle|reproductive',
                r'解剖|身体|月经|生殖'
            ],
            "relationship": [
                r'relationship|partner|communication|talk',
                r'关系|伴侣|沟通|交流'
            ],
            "sti": [
                r'sti|std|infection|disease|hiv|aids',
                r'性病|感染|艾滋|梅毒'
            ],
            "consent": [
                r'consent|permission|agreement|boundaries',
                r'同意|许可|界限|边界'
            ]
        }
    
    def process_request(self, request: PromptRequest) -> PromptResponse:
        """Process a prompt request and return formatted response."""
        
        # Step 1: Detect language if not provided
        if not request.language:
            request.language = self._detect_language(request.content)
        
        # Step 2: Classify topic
        topic = self._classify_topic(request.content, request.language)
        
        # Step 3: Assess safety requirements
        safety_flags = self._assess_safety(request.content, request.context)
        
        # Step 4: Select appropriate template
        template = self._select_template(
            request, topic, safety_flags
        )
        
        # Step 5: Format prompt
        formatted_prompt = self._format_prompt(
            template, request, topic
        )
        
        # Step 6: Calculate confidence score
        confidence = self._calculate_confidence(
            request, template, topic
        )
        
        return PromptResponse(
            formatted_prompt=formatted_prompt,
            template_used=template.__class__.__name__ if template else "none",
            language_detected=request.language,
            safety_flags=safety_flags,
            confidence_score=confidence,
            metadata={
                "topic": topic,
                "input_type": request.input_type.value,
                "cultural_context": request.cultural_context,
                "age_group": request.user_age_group
            }
        )
    
    def _detect_language(self, content: str) -> str:
        """Detect the language of the input content."""
        scores = {"en": 0, "zh-CN": 0, "zh-CN-henan": 0}
        
        for lang, patterns in self.language_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                scores[lang] += matches
        
        # Special handling for Henan dialect
        if scores["zh-CN-henan"] > 0:
            return "zh-CN-henan"
        
        # Return language with highest score
        detected = max(scores, key=scores.get)
        return detected if scores[detected] > 0 else "en"
    
    def _classify_topic(self, content: str, language: str) -> str:
        """Classify the topic of the user's question."""
        scores = {}
        
        for topic, patterns in self.topic_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                score += matches
            scores[topic] = score
        
        # Return topic with highest score, default to basic_education
        if not scores or max(scores.values()) == 0:
            return "basic_education"
        
        return max(scores, key=scores.get)
    
    def _assess_safety(
        self, 
        content: str, 
        context: Optional[str]
    ) -> List[str]:
        """Assess safety requirements and flag potential issues."""
        flags = []
        
        # Check for potentially harmful content
        harmful_patterns = [
            r'unsafe|dangerous|risky|harmful',
            r'不安全|危险|有害'
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                flags.append("potential_safety_concern")
        
        # Check for age-inappropriate content
        explicit_patterns = [
            r'explicit|graphic|detailed sexual',
            r'露骨|详细性'
        ]
        
        for pattern in explicit_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                flags.append("age_verification_needed")
        
        # Check for medical advice requests
        medical_patterns = [
            r'diagnose|treatment|medication|doctor',
            r'诊断|治疗|药物|医生'
        ]
        
        for pattern in medical_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                flags.append("medical_consultation_recommended")
        
        return flags
    
    def _select_template(
        self,
        request: PromptRequest,
        topic: str,
        safety_flags: List[str]
    ) -> Optional[PromptTemplate]:
        """Select the most appropriate template for the request."""
        
        # Handle document analysis
        if request.input_type == InputType.DOCUMENT:
            return self.document_prompts.analyze_document(
                request.content, "content_extraction", request.language
            )
        
        # Handle safety concerns
        if "potential_safety_concern" in safety_flags:
            return self._get_safety_template(request.language)
        
        # Handle cultural context
        if request.cultural_context:
            template = self.language_prompts.get_culturally_appropriate_template(
                topic, request.language, request.cultural_context
            )
            if template:
                return template
        
        # Get standard sexual health template
        lang_code = "en" if request.language.startswith("zh-CN-") else request.language
        return self.sexual_health_prompts.get_template(topic, lang_code)
    
    def _get_safety_template(self, language: str) -> PromptTemplate:
        """Get safety-focused template for potentially concerning content."""
        
        if language.startswith("zh"):
            system_prompt = (
                "您是一位专业的性健康教育工作者。"
                "当遇到可能不安全的问题时，请优先考虑用户的安全和健康。"
                "提供准确的信息，并在必要时建议寻求专业医疗帮助。"
            )
            template_text = (
                "用户问题：{user_question}\n\n"
                "请提供安全、准确的性健康信息。"
                "如果问题涉及潜在风险，请强调安全措施和专业咨询的重要性。"
            )
        else:
            system_prompt = (
                "You are a professional sexual health educator. "
                "When addressing potentially unsafe questions, prioritize "
                "user safety and health. Provide accurate information and "
                "recommend professional medical help when necessary."
            )
            template_text = (
                "User Question: {user_question}\n\n"
                "Please provide safe, accurate sexual health information. "
                "If the question involves potential risks, emphasize safety "
                "measures and the importance of professional consultation."
            )
        
        return PromptTemplate(
            template=template_text,
            prompt_type=PromptType.SAFETY_CHECK,
            language=language,
            system_prompt=system_prompt
        )
    
    def _format_prompt(
        self,
        template: Optional[PromptTemplate],
        request: PromptRequest,
        topic: str
    ) -> str:
        """Format the final prompt using the selected template."""
        
        if not template:
            raise RuntimeError(f"No template available for topic '{topic}' and language '{request.language}'")
        
        # Prepare template variables
        variables = {
            "user_question": request.content,
            "document_content": request.content if request.input_type == InputType.DOCUMENT else "",
            "source_text": request.content,
            "claim": request.content,
            "input_text": request.content
        }
        
        # Add context if available
        if request.context:
            variables["context"] = request.context
        
        try:
            return template.format(**variables)
        except KeyError as e:
            raise RuntimeError(f"Template formatting failed: missing variable '{e.args[0]}'") from e
    
    def _calculate_confidence(
        self,
        request: PromptRequest,
        template: Optional[PromptTemplate],
        topic: str
    ) -> float:
        """Calculate confidence score for the prompt selection."""
        
        confidence = 0.5  # Base confidence
        
        # Increase confidence for exact language match
        if template and template.language == request.language:
            confidence += 0.2
        
        # Increase confidence for clear topic classification
        topic_patterns = self.topic_patterns.get(topic, [])
        if topic_patterns:
            # Calculate topic score based on pattern matches
            topic_score = 0
            for pattern in topic_patterns:
                matches = len(re.findall(pattern, request.content, re.IGNORECASE))
                topic_score += matches
            
            if topic_score > 0:
                confidence += min(0.2, topic_score * 0.1)
        
        # Increase confidence for cultural context match
        if request.cultural_context and template:
            confidence += 0.1
        
        # Decrease confidence for safety flags
        if request.context and "safety" in request.context:
            confidence -= 0.1
        
        return min(1.0, max(0.0, confidence))
    
    def add_custom_template(
        self,
        name: str,
        template: PromptTemplate,
        category: str = "sexual_health"
    ) -> None:
        """Add a custom template to the appropriate category."""
        
        if category == "sexual_health":
            self.sexual_health_prompts.add_custom_template(name, template)
        elif category == "language":
            self.language_prompts.manager.register_template(name, template)
        elif category == "document":
            self.document_prompts.manager.register_template(name, template)
    
    def get_available_topics(self) -> List[str]:
        """Get list of available topics."""
        return list(self.topic_patterns.keys())
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return ["en", "zh-CN", "zh-CN-henan"]
    
    def generate_prompt(self, request: PromptRequest) -> str:
        """Generate a formatted prompt from a request (simplified interface)."""
        response = self.process_request(request)
        return response.formatted_prompt
    
    def export_all_templates(self, filepath: str) -> None:
        """Export all templates to a file."""
        all_templates = {}
        
        # Collect templates from all categories
        all_templates.update(self.sexual_health_prompts.get_all_templates())
        all_templates.update(self.language_prompts.manager.templates)
        all_templates.update(self.document_prompts.manager.templates)
        
        # Export using the base manager
        manager = PromptManager()
        manager.templates = all_templates
        manager.export_templates(filepath) 