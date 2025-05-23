"""
Sexual health education prompt templates for LLB application.
Provides specialized prompts for various sexual health topics with 
culturally sensitive and age-appropriate content.
"""

from typing import List, Dict
from prompts.base import PromptTemplate, PromptType, FewShotExample, PromptManager


class SexualHealthPrompts:
    """Collection of sexual health education prompt templates."""
    
    def __init__(self):
        self.manager = PromptManager()
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize all sexual health prompt templates."""
        self._create_basic_education_templates()
        self._create_safety_templates()
        self._create_relationship_templates()
        self._create_anatomy_templates()
        self._create_contraception_templates()
        self._create_sti_templates()
        self._create_consent_templates()
    
    def _create_basic_education_templates(self):
        """Create basic sexual health education templates."""
        
        # English basic education template
        basic_examples_en = [
            FewShotExample(
                input_text="What is sexual health?",
                expected_output=(
                    "Sexual health is a state of physical, emotional, mental "
                    "and social well-being related to sexuality. It includes "
                    "having pleasurable and safe sexual experiences, free of "
                    "coercion, discrimination, and violence. Sexual health "
                    "requires a positive and respectful approach to sexuality "
                    "and sexual relationships, as well as the possibility of "
                    "having pleasurable and safe sexual experiences."
                ),
                language="en"
            ),
            FewShotExample(
                input_text="Is it normal to have questions about sex?",
                expected_output=(
                    "Absolutely! Having questions about sex and sexuality is "
                    "completely normal and healthy. Everyone has questions at "
                    "different stages of their life. It's important to seek "
                    "accurate, reliable information from trusted sources like "
                    "healthcare providers, certified sex educators, or "
                    "evidence-based educational resources."
                ),
                language="en"
            )
        ]
        
        basic_template_en = PromptTemplate(
            template=(
                "User Question: {user_question}\n\n"
                "Please provide a comprehensive, age-appropriate, and "
                "scientifically accurate response about sexual health. "
                "Focus on education, safety, and well-being. If the question "
                "requires medical advice, recommend consulting a healthcare "
                "professional."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=basic_examples_en,
            system_prompt=(
                "You are a certified sexual health educator providing "
                "evidence-based, non-judgmental information. Always prioritize "
                "safety, consent, and accurate medical information. Be "
                "culturally sensitive and age-appropriate."
            )
        )
        
        # Chinese basic education template
        basic_examples_zh = [
            FewShotExample(
                input_text="什么是性健康？",
                expected_output=(
                    "性健康是指与性相关的身体、情感、精神和社会福祉状态。"
                    "它包括拥有愉悦和安全的性体验，免受强迫、歧视和暴力。"
                    "性健康需要对性和性关系采取积极和尊重的态度，"
                    "以及拥有愉悦和安全性体验的可能性。"
                ),
                language="zh-CN"
            ),
            FewShotExample(
                input_text="对性有疑问是正常的吗？",
                expected_output=(
                    "当然！对性和性行为有疑问是完全正常和健康的。"
                    "每个人在生活的不同阶段都会有疑问。"
                    "重要的是要从可信的来源寻求准确、可靠的信息，"
                    "如医疗保健提供者、认证的性教育工作者或基于证据的教育资源。"
                ),
                language="zh-CN"
            )
        ]
        
        basic_template_zh = PromptTemplate(
            template=(
                "用户问题：{user_question}\n\n"
                "请提供全面、适龄且科学准确的性健康回答。"
                "重点关注教育、安全和福祉。如果问题需要医疗建议，"
                "建议咨询医疗专业人员。"
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="zh-CN",
            few_shot_examples=basic_examples_zh,
            system_prompt=(
                "您是一位认证的性健康教育工作者，提供基于证据的、"
                "非评判性的信息。始终优先考虑安全、同意和准确的医疗信息。"
                "要有文化敏感性和年龄适宜性。"
            )
        )
        
        self.manager.register_template("basic_education_en", basic_template_en)
        self.manager.register_template("basic_education_zh", basic_template_zh)
    
    def _create_safety_templates(self):
        """Create safety-focused prompt templates."""
        
        safety_examples_en = [
            FewShotExample(
                input_text="How can I practice safe sex?",
                expected_output=(
                    "Safe sex practices include: 1) Using barrier methods like "
                    "condoms or dental dams consistently and correctly, "
                    "2) Getting regular STI testing for you and your partner(s), "
                    "3) Having open, honest communication about sexual health "
                    "with partners, 4) Limiting the number of sexual partners, "
                    "5) Avoiding sex under the influence of drugs or alcohol, "
                    "6) Ensuring enthusiastic consent from all parties involved."
                ),
                language="en"
            )
        ]
        
        safety_template_en = PromptTemplate(
            template=(
                "Safety Question: {user_question}\n\n"
                "Provide comprehensive safety information focusing on harm "
                "reduction, protection methods, and risk awareness. Include "
                "practical steps and emphasize the importance of communication "
                "and consent."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=safety_examples_en
        )
        
        self.manager.register_template("safety_education_en", safety_template_en)
    
    def _create_relationship_templates(self):
        """Create relationship and communication prompt templates."""
        
        relationship_examples_en = [
            FewShotExample(
                input_text="How do I talk to my partner about sexual preferences?",
                expected_output=(
                    "Open communication about sexual preferences is crucial for "
                    "a healthy relationship. Start by: 1) Choosing a comfortable, "
                    "private setting outside the bedroom, 2) Using 'I' statements "
                    "to express your feelings and desires, 3) Being specific but "
                    "respectful about what you enjoy or want to try, 4) Actively "
                    "listening to your partner's responses without judgment, "
                    "5) Respecting boundaries and being willing to compromise, "
                    "6) Making it an ongoing conversation, not a one-time talk."
                ),
                language="en"
            )
        ]
        
        relationship_template_en = PromptTemplate(
            template=(
                "Relationship Question: {user_question}\n\n"
                "Provide guidance on healthy communication, relationship "
                "dynamics, and building trust. Focus on mutual respect, "
                "consent, and emotional well-being in intimate relationships."
            ),
            prompt_type=PromptType.CONVERSATIONAL,
            language="en",
            few_shot_examples=relationship_examples_en
        )
        
        self.manager.register_template("relationship_en", relationship_template_en)
    
    def _create_anatomy_templates(self):
        """Create anatomy and physiology education templates."""
        
        anatomy_examples_en = [
            FewShotExample(
                input_text="Can you explain the menstrual cycle?",
                expected_output=(
                    "The menstrual cycle is a monthly process where the body "
                    "prepares for potential pregnancy. It typically lasts 28 days "
                    "but can range from 21-35 days. The cycle has four phases: "
                    "1) Menstrual phase (days 1-5): shedding of uterine lining, "
                    "2) Follicular phase (days 1-13): egg development, "
                    "3) Ovulation (around day 14): egg release, "
                    "4) Luteal phase (days 15-28): uterine lining thickening. "
                    "Understanding your cycle can help with family planning and "
                    "overall health awareness."
                ),
                language="en"
            )
        ]
        
        anatomy_template_en = PromptTemplate(
            template=(
                "Anatomy Question: {user_question}\n\n"
                "Provide accurate, scientific information about human anatomy "
                "and physiology related to sexual and reproductive health. "
                "Use appropriate medical terminology while keeping explanations "
                "accessible and educational."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=anatomy_examples_en
        )
        
        self.manager.register_template("anatomy_en", anatomy_template_en)
    
    def _create_contraception_templates(self):
        """Create contraception education templates."""
        
        contraception_examples_en = [
            FewShotExample(
                input_text="What are the different types of birth control?",
                expected_output=(
                    "There are several types of birth control methods: "
                    "1) Barrier methods (condoms, diaphragms, cervical caps), "
                    "2) Hormonal methods (birth control pills, patches, rings, "
                    "injections, implants), 3) Intrauterine devices (IUDs), "
                    "4) Permanent methods (tubal ligation, vasectomy), "
                    "5) Natural methods (fertility awareness, withdrawal). "
                    "Each method has different effectiveness rates, benefits, "
                    "and considerations. It's important to discuss options with "
                    "a healthcare provider to find the best method for your "
                    "individual needs and circumstances."
                ),
                language="en"
            )
        ]
        
        contraception_template_en = PromptTemplate(
            template=(
                "Contraception Question: {user_question}\n\n"
                "Provide comprehensive, unbiased information about "
                "contraceptive methods, their effectiveness, benefits, "
                "and considerations. Always recommend consulting with "
                "healthcare providers for personalized advice."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=contraception_examples_en
        )
        
        self.manager.register_template("contraception_en", contraception_template_en)
    
    def _create_sti_templates(self):
        """Create STI education and prevention templates."""
        
        sti_examples_en = [
            FewShotExample(
                input_text="How can I prevent sexually transmitted infections?",
                expected_output=(
                    "STI prevention strategies include: 1) Using latex or "
                    "polyurethane condoms consistently and correctly during "
                    "vaginal, anal, and oral sex, 2) Getting tested regularly "
                    "and knowing your partner's STI status, 3) Limiting the "
                    "number of sexual partners, 4) Avoiding sharing needles "
                    "or other drug equipment, 5) Getting vaccinated against "
                    "preventable STIs like HPV and Hepatitis B, 6) Considering "
                    "pre-exposure prophylaxis (PrEP) if at high risk for HIV. "
                    "Remember, many STIs can be asymptomatic, so regular "
                    "testing is crucial even if you feel healthy."
                ),
                language="en"
            )
        ]
        
        sti_template_en = PromptTemplate(
            template=(
                "STI Question: {user_question}\n\n"
                "Provide accurate information about sexually transmitted "
                "infections, including prevention, testing, and treatment "
                "options. Emphasize the importance of regular testing and "
                "professional medical care. Avoid stigmatizing language."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=sti_examples_en
        )
        
        self.manager.register_template("sti_prevention_en", sti_template_en)
    
    def _create_consent_templates(self):
        """Create consent education templates."""
        
        consent_examples_en = [
            FewShotExample(
                input_text="What does consent mean in sexual situations?",
                expected_output=(
                    "Consent is a clear, enthusiastic, and ongoing agreement "
                    "to participate in sexual activity. Key aspects of consent: "
                    "1) It must be freely given without coercion or pressure, "
                    "2) It can be withdrawn at any time, 3) It must be informed "
                    "- all parties understand what they're agreeing to, "
                    "4) It requires capacity - people under the influence of "
                    "drugs/alcohol or below the age of consent cannot give "
                    "valid consent, 5) It's specific - consent to one activity "
                    "doesn't mean consent to all activities, 6) It should be "
                    "ongoing - check in with your partner throughout intimate "
                    "encounters."
                ),
                language="en"
            )
        ]
        
        consent_template_en = PromptTemplate(
            template=(
                "Consent Question: {user_question}\n\n"
                "Provide clear, comprehensive information about consent, "
                "emphasizing its importance in all sexual interactions. "
                "Focus on communication, respect, and understanding "
                "boundaries. Include practical guidance for ensuring "
                "enthusiastic consent."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=consent_examples_en
        )
        
        self.manager.register_template("consent_education_en", consent_template_en)
    
    def get_template(self, topic: str, language: str = "en") -> PromptTemplate:
        """Get a template for a specific topic and language."""
        template_name = f"{topic}_{language}"
        return self.manager.get_template(template_name)
    
    def get_all_templates(self) -> Dict[str, PromptTemplate]:
        """Get all available templates."""
        return self.manager.templates
    
    def add_custom_template(
        self, 
        name: str, 
        template: PromptTemplate
    ) -> None:
        """Add a custom template to the collection."""
        self.manager.register_template(name, template) 