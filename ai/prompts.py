"""
Optimized AI prompt system for sexual health education.
"""

import re
from typing import Dict, Optional
from enum import Enum

class PromptType(Enum):
    BASIC = "basic"
    SAFETY = "safety"
    MEDICAL = "medical"

class PromptEngine:
    def __init__(self):
        self.prompts = {
            "en": {
                PromptType.BASIC: (
                    "You are a professional sexual health educator. "
                    "Provide accurate, age-appropriate information about: {topic}. "
                    "Question: {question}"
                ),
                PromptType.SAFETY: (
                    "You are a sexual health educator focused on safety. "
                    "Address this safety concern with practical advice: {question}. "
                    "Emphasize protection and professional consultation when needed."
                ),
                PromptType.MEDICAL: (
                    "You are a sexual health educator. This question may require medical advice: {question}. "
                    "Provide general information and strongly recommend consulting a healthcare provider."
                )
            },
            "zh-CN": {
                PromptType.BASIC: (
                    "您是专业的性健康教育工作者。"
                    "请提供关于{topic}的准确、适龄信息。"
                    "问题：{question}"
                ),
                PromptType.SAFETY: (
                    "您是专注于安全的性健康教育工作者。"
                    "请针对此安全问题提供实用建议：{question}。"
                    "强调保护措施和必要时的专业咨询。"
                ),
                PromptType.MEDICAL: (
                    "您是性健康教育工作者。此问题可能需要医疗建议：{question}。"
                    "请提供一般信息并强烈建议咨询医疗专业人员。"
                )
            }
        }
        
        self.topics = {
            "contraception": ["birth control", "condom", "pill", "避孕", "安全套"],
            "anatomy": ["body", "menstrual", "reproductive", "身体", "月经", "生殖"],
            "safety": ["safe", "protection", "risk", "安全", "保护", "风险"],
            "relationship": ["partner", "communication", "伴侣", "沟通"],
            "sti": ["infection", "disease", "hiv", "性病", "感染", "艾滋"],
            "consent": ["consent", "permission", "同意", "许可"]
        }
        
        self.medical_keywords = [
            "diagnose", "treatment", "medication", "doctor", "pain", "symptoms",
            "诊断", "治疗", "药物", "医生", "疼痛", "症状"
        ]
        
        self.safety_keywords = [
            "unsafe", "dangerous", "risky", "harmful", "abuse",
            "不安全", "危险", "有害", "虐待"
        ]

    def detect_language(self, text: str) -> str:
        """Detect if text is Chinese or English."""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        return "zh-CN" if chinese_chars > 0 else "en"

    def classify_topic(self, text: str) -> str:
        """Classify the main topic of the question."""
        text_lower = text.lower()
        
        for topic, keywords in self.topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return "general"

    def determine_prompt_type(self, text: str) -> PromptType:
        """Determine the appropriate prompt type."""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in self.medical_keywords):
            return PromptType.MEDICAL
        
        if any(keyword in text_lower for keyword in self.safety_keywords):
            return PromptType.SAFETY
        
        return PromptType.BASIC

    def generate_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Generate optimized prompt for the question."""
        language = self.detect_language(question)
        topic = self.classify_topic(question)
        prompt_type = self.determine_prompt_type(question)
        
        template = self.prompts[language][prompt_type]
        
        return template.format(
            question=question,
            topic=topic,
            context=context or ""
        )

    def enhance_response_quality(self, question: str) -> str:
        """Add response quality guidelines to prompt."""
        language = self.detect_language(question)
        base_prompt = self.generate_prompt(question)
        
        if language == "zh-CN":
            quality_guide = (
                "\n\n请确保回答：1) 科学准确 2) 文化敏感 3) 年龄适宜 4) 非评判性"
            )
        else:
            quality_guide = (
                "\n\nEnsure your response is: 1) Scientifically accurate "
                "2) Culturally sensitive 3) Age-appropriate 4) Non-judgmental"
            )
        
        return base_prompt + quality_guide