"""
Language support and detection prompts for LLB application.
Handles multilingual interactions and language-specific responses.
"""

from typing import Dict, List, Optional
from prompts.base import PromptTemplate, PromptType, FewShotExample, PromptManager


class LanguagePrompts:
    """Language detection and multilingual support prompts."""
    
    def __init__(self):
        self.manager = PromptManager()
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize language support templates."""
        self._create_language_detection_templates()
        self._create_translation_templates()
        self._create_dialect_support_templates()
        self._create_cultural_adaptation_templates()
    
    def _create_language_detection_templates(self):
        """Create language detection prompt templates."""
        
        detection_examples = [
            FewShotExample(
                input_text="What is sexual health?",
                expected_output="Language: English (en)",
                language="en"
            ),
            FewShotExample(
                input_text="什么是性健康？",
                expected_output="Language: Chinese Simplified (zh-CN)",
                language="zh-CN"
            ),
            FewShotExample(
                input_text="俺想问问性健康是啥意思？",
                expected_output="Language: Henan Dialect (zh-CN-henan)",
                context="Henan dialect uses '俺' instead of '我' and '啥' instead of '什么'",
                language="zh-CN"
            ),
            FewShotExample(
                input_text="Can you tell me about contraception methods?",
                expected_output="Language: English (en)",
                language="en"
            )
        ]
        
        detection_template = PromptTemplate(
            template=(
                "Analyze the following text and identify the language. "
                "Consider regional dialects and variations:\n\n"
                "Text: {input_text}\n\n"
                "Respond with the language code in the format: "
                "Language: [Language Name] ([code])\n"
                "Supported languages:\n"
                "- English (en)\n"
                "- Chinese Simplified (zh-CN)\n"
                "- Henan Dialect (zh-CN-henan)"
            ),
            prompt_type=PromptType.LANGUAGE_DETECTION,
            language="en",
            few_shot_examples=detection_examples,
            system_prompt=(
                "You are a language detection system that can identify "
                "English, Mandarin Chinese, and Henan dialect. Pay attention "
                "to dialect-specific vocabulary and grammar patterns."
            )
        )
        
        self.manager.register_template("language_detection", detection_template)
    
    def _create_translation_templates(self):
        """Create translation prompt templates."""
        
        # English to Chinese translation
        en_to_zh_examples = [
            FewShotExample(
                input_text="Translate: 'Sexual health is important for everyone.'",
                expected_output="性健康对每个人都很重要。",
                language="zh-CN"
            ),
            FewShotExample(
                input_text="Translate: 'Consent is essential in all relationships.'",
                expected_output="在所有关系中，同意都是必不可少的。",
                language="zh-CN"
            )
        ]
        
        en_to_zh_template = PromptTemplate(
            template=(
                "Translate the following sexual health education content "
                "from English to Simplified Chinese. Maintain accuracy and "
                "cultural appropriateness:\n\n"
                "English: {source_text}\n\n"
                "Provide only the Chinese translation:"
            ),
            prompt_type=PromptType.CONVERSATIONAL,
            language="zh-CN",
            few_shot_examples=en_to_zh_examples,
            system_prompt=(
                "You are a professional translator specializing in sexual "
                "health education content. Ensure translations are culturally "
                "appropriate and medically accurate for Chinese audiences."
            )
        )
        
        # Chinese to English translation
        zh_to_en_examples = [
            FewShotExample(
                input_text="翻译：'性教育应该从青春期开始。'",
                expected_output="Sex education should begin during adolescence.",
                language="en"
            ),
            FewShotExample(
                input_text="翻译：'安全套是预防性传播疾病的有效方法。'",
                expected_output="Condoms are an effective method for preventing sexually transmitted diseases.",
                language="en"
            )
        ]
        
        zh_to_en_template = PromptTemplate(
            template=(
                "Translate the following sexual health education content "
                "from Chinese to English. Maintain accuracy and "
                "professional tone:\n\n"
                "Chinese: {source_text}\n\n"
                "Provide only the English translation:"
            ),
            prompt_type=PromptType.CONVERSATIONAL,
            language="en",
            few_shot_examples=zh_to_en_examples,
            system_prompt=(
                "You are a professional translator specializing in sexual "
                "health education content. Ensure translations are accurate "
                "and use appropriate medical terminology in English."
            )
        )
        
        self.manager.register_template("translate_en_to_zh", en_to_zh_template)
        self.manager.register_template("translate_zh_to_en", zh_to_en_template)
    
    def _create_dialect_support_templates(self):
        """Create Henan dialect support templates."""
        
        henan_examples = [
            FewShotExample(
                input_text="俺想知道性健康是啥意思？",
                expected_output=(
                    "性健康就是说你的身体、心理和社会方面都要健康，"
                    "跟性有关的事情都要安全、愉快，不能被人强迫或者歧视。"
                    "简单说就是要有安全的性生活，要互相尊重。"
                ),
                context="Henan dialect question about sexual health",
                language="zh-CN"
            ),
            FewShotExample(
                input_text="俺和对象咋样才能安全地过性生活？",
                expected_output=(
                    "安全的性生活主要是这几个方面：一是要用安全套，"
                    "二是要定期检查身体，三是要和对象好好沟通，"
                    "四是要确保双方都同意。记住，安全最重要。"
                ),
                context="Henan dialect question about safe sex",
                language="zh-CN"
            )
        ]
        
        henan_template = PromptTemplate(
            template=(
                "用户用河南话问了一个性健康问题：{user_question}\n\n"
                "请用通俗易懂的中文回答，要考虑到河南地区的文化背景。"
                "回答要准确、不带偏见，并且要适合当地人的理解方式。"
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="zh-CN",
            few_shot_examples=henan_examples,
            system_prompt=(
                "你是一位了解河南文化的性健康教育工作者。"
                "用简单明了的中文回答问题，要考虑到当地的文化背景和语言习惯。"
                "始终提供准确、非评判性的信息。"
            )
        )
        
        self.manager.register_template("henan_dialect_support", henan_template)
    
    def _create_cultural_adaptation_templates(self):
        """Create culturally adapted prompt templates."""
        
        # Chinese cultural adaptation
        chinese_cultural_examples = [
            FewShotExample(
                input_text="在中国文化背景下，如何与父母谈论性教育？",
                expected_output=(
                    "在中国文化中，与父母谈论性教育确实比较敏感。"
                    "可以从健康角度入手，比如说是为了保护自己的身体健康。"
                    "也可以通过书籍、文章等方式间接交流。"
                    "重要的是要尊重家庭的价值观，同时获得必要的健康知识。"
                    "如果直接交流困难，可以寻求学校老师或医生的帮助。"
                ),
                language="zh-CN"
            )
        ]
        
        chinese_cultural_template = PromptTemplate(
            template=(
                "用户问题：{user_question}\n\n"
                "请从中国文化背景出发，提供关于性健康教育的建议。"
                "要考虑到传统文化价值观，同时提供科学准确的信息。"
                "回答要尊重文化敏感性，但不能妥协科学准确性。"
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="zh-CN",
            few_shot_examples=chinese_cultural_examples,
            system_prompt=(
                "你是一位了解中国文化的性健康教育专家。"
                "在提供科学准确信息的同时，要考虑到中国的文化背景和社会环境。"
                "要平衡传统价值观和现代健康教育的需要。"
            )
        )
        
        # Western cultural adaptation for Chinese users
        western_adaptation_examples = [
            FewShotExample(
                input_text="西方国家的性教育和中国有什么不同？",
                expected_output=(
                    "西方国家的性教育通常更加开放和系统化。"
                    "主要差异包括：1）开始年龄更早，通常从小学就开始；"
                    "2）内容更全面，包括性取向、性别认同等话题；"
                    "3）更强调个人选择和权利；4）家庭和学校的参与度更高。"
                    "但无论文化背景如何，核心都是保护健康和安全。"
                ),
                language="zh-CN"
            )
        ]
        
        western_adaptation_template = PromptTemplate(
            template=(
                "用户问题：{user_question}\n\n"
                "请比较和解释不同文化背景下的性健康教育方法。"
                "要客观地介绍西方和中国的不同做法，"
                "帮助用户理解文化差异，同时强调共同的健康目标。"
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="zh-CN",
            few_shot_examples=western_adaptation_examples,
            system_prompt=(
                "你是一位跨文化性健康教育专家。"
                "能够客观地比较不同文化的性教育方法，"
                "帮助用户理解文化差异，同时强调健康和安全的共同目标。"
            )
        )
        
        self.manager.register_template("chinese_cultural", chinese_cultural_template)
        self.manager.register_template("western_adaptation", western_adaptation_template)
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text."""
        template = self.manager.get_template("language_detection")
        if not template:
            raise RuntimeError("Language detection template not available")
        
        prompt = template.format(input_text=text)
        # This would be processed by the AI model
        return prompt
    
    def get_culturally_appropriate_template(
        self, 
        topic: str, 
        language: str,
        cultural_context: Optional[str] = None
    ) -> Optional[PromptTemplate]:
        """Get a culturally appropriate template for the given context."""
        if cultural_context == "chinese" and language == "zh-CN":
            return self.manager.get_template("chinese_cultural")
        elif cultural_context == "henan" and language == "zh-CN":
            return self.manager.get_template("henan_dialect_support")
        else:
            # Return standard template for the language
            return self.manager.get_template(f"{topic}_{language}")
    
    def get_translation_template(
        self, 
        source_lang: str, 
        target_lang: str
    ) -> Optional[PromptTemplate]:
        """Get translation template for language pair."""
        template_name = f"translate_{source_lang}_to_{target_lang}"
        return self.manager.get_template(template_name) 