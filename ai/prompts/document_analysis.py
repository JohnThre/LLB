"""
Document analysis prompts for LLB application.
Handles PDF document processing and content extraction for sexual health education.
"""

from typing import Dict, List, Optional
from prompts.base import PromptTemplate, PromptType, FewShotExample, PromptManager


class DocumentPrompts:
    """Document analysis and processing prompt templates."""
    
    def __init__(self):
        self.manager = PromptManager()
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize document analysis templates."""
        self._create_content_extraction_templates()
        self._create_summarization_templates()
        self._create_fact_checking_templates()
        self._create_question_generation_templates()
        self._create_safety_assessment_templates()
    
    def _create_content_extraction_templates(self):
        """Create content extraction prompt templates."""
        
        extraction_examples_en = [
            FewShotExample(
                input_text=(
                    "Document content: 'Sexual health encompasses physical, "
                    "emotional, mental and social well-being in relation to "
                    "sexuality. It requires a positive and respectful approach "
                    "to sexuality and sexual relationships.'"
                ),
                expected_output=(
                    "Key Topics Identified:\n"
                    "1. Sexual health definition\n"
                    "2. Physical well-being\n"
                    "3. Emotional well-being\n"
                    "4. Mental health aspects\n"
                    "5. Social well-being\n"
                    "6. Positive approach to sexuality\n"
                    "7. Respectful relationships\n\n"
                    "Content Type: Educational/Definitional\n"
                    "Relevance: High - Core sexual health concepts"
                ),
                language="en"
            ),
            FewShotExample(
                input_text=(
                    "Document content: 'Contraceptive methods include barrier "
                    "methods like condoms, hormonal methods like birth control "
                    "pills, and long-acting reversible contraceptives like IUDs.'"
                ),
                expected_output=(
                    "Key Topics Identified:\n"
                    "1. Contraceptive methods overview\n"
                    "2. Barrier methods (condoms)\n"
                    "3. Hormonal contraception (pills)\n"
                    "4. Long-acting contraceptives (IUDs)\n\n"
                    "Content Type: Educational/Informational\n"
                    "Relevance: High - Contraception education"
                ),
                language="en"
            )
        ]
        
        extraction_template_en = PromptTemplate(
            template=(
                "Analyze the following document content and extract key "
                "sexual health education topics:\n\n"
                "Document Content: {document_content}\n\n"
                "Please identify:\n"
                "1. Main topics covered\n"
                "2. Content type (educational, medical, research, etc.)\n"
                "3. Relevance to sexual health education\n"
                "4. Any safety concerns or misinformation\n"
                "5. Target audience (if identifiable)\n\n"
                "Format your response clearly with sections for each aspect."
            ),
            prompt_type=PromptType.DOCUMENT_ANALYSIS,
            language="en",
            few_shot_examples=extraction_examples_en,
            system_prompt=(
                "You are a sexual health education content analyst. "
                "Extract and categorize information from documents, "
                "identifying key topics, accuracy, and educational value. "
                "Flag any potentially harmful or inaccurate information."
            )
        )
        
        # Chinese version
        extraction_examples_zh = [
            FewShotExample(
                input_text=(
                    "文档内容：'性健康包括与性相关的身体、情感、精神和社会福祉。"
                    "它需要对性和性关系采取积极和尊重的态度。'"
                ),
                expected_output=(
                    "识别的关键主题：\n"
                    "1. 性健康定义\n"
                    "2. 身体健康\n"
                    "3. 情感健康\n"
                    "4. 精神健康方面\n"
                    "5. 社会福祉\n"
                    "6. 对性的积极态度\n"
                    "7. 尊重的关系\n\n"
                    "内容类型：教育/定义性\n"
                    "相关性：高 - 核心性健康概念"
                ),
                language="zh-CN"
            )
        ]
        
        extraction_template_zh = PromptTemplate(
            template=(
                "分析以下文档内容并提取关键的性健康教育主题：\n\n"
                "文档内容：{document_content}\n\n"
                "请识别：\n"
                "1. 涵盖的主要主题\n"
                "2. 内容类型（教育、医疗、研究等）\n"
                "3. 与性健康教育的相关性\n"
                "4. 任何安全问题或错误信息\n"
                "5. 目标受众（如果可识别）\n\n"
                "请清晰地格式化您的回答，为每个方面设置部分。"
            ),
            prompt_type=PromptType.DOCUMENT_ANALYSIS,
            language="zh-CN",
            few_shot_examples=extraction_examples_zh,
            system_prompt=(
                "您是性健康教育内容分析师。"
                "从文档中提取和分类信息，识别关键主题、准确性和教育价值。"
                "标记任何潜在有害或不准确的信息。"
            )
        )
        
        self.manager.register_template("content_extraction_en", extraction_template_en)
        self.manager.register_template("content_extraction_zh", extraction_template_zh)
    
    def _create_summarization_templates(self):
        """Create document summarization templates."""
        
        summary_examples_en = [
            FewShotExample(
                input_text=(
                    "Document: A 10-page research paper on adolescent sexual "
                    "health education programs, discussing implementation "
                    "strategies, effectiveness measures, and cultural considerations."
                ),
                expected_output=(
                    "Document Summary:\n\n"
                    "Title: Adolescent Sexual Health Education Programs\n"
                    "Type: Research Paper\n"
                    "Length: 10 pages\n\n"
                    "Key Points:\n"
                    "• Implementation strategies for sex education programs\n"
                    "• Methods for measuring program effectiveness\n"
                    "• Cultural considerations in program design\n"
                    "• Focus on adolescent population\n\n"
                    "Educational Value: High - provides evidence-based "
                    "approaches to sexual health education\n\n"
                    "Recommended Use: Reference for educators and program "
                    "developers working with adolescents"
                ),
                language="en"
            )
        ]
        
        summary_template_en = PromptTemplate(
            template=(
                "Create a comprehensive summary of the following document "
                "focused on sexual health education content:\n\n"
                "Document: {document_content}\n\n"
                "Include:\n"
                "1. Document type and scope\n"
                "2. Key points and main arguments\n"
                "3. Educational value assessment\n"
                "4. Recommended use cases\n"
                "5. Any limitations or concerns\n\n"
                "Keep the summary concise but comprehensive."
            ),
            prompt_type=PromptType.DOCUMENT_ANALYSIS,
            language="en",
            few_shot_examples=summary_examples_en,
            system_prompt=(
                "You are a sexual health education content summarizer. "
                "Create clear, accurate summaries that highlight the "
                "educational value and practical applications of documents."
            )
        )
        
        self.manager.register_template("document_summary_en", summary_template_en)
    
    def _create_fact_checking_templates(self):
        """Create fact-checking prompt templates."""
        
        fact_check_examples_en = [
            FewShotExample(
                input_text=(
                    "Claim from document: 'Condoms are 100% effective at "
                    "preventing pregnancy and STIs when used correctly.'"
                ),
                expected_output=(
                    "Fact Check Result: PARTIALLY ACCURATE\n\n"
                    "Analysis:\n"
                    "• Condoms are highly effective but not 100% perfect\n"
                    "• Typical use effectiveness for pregnancy prevention: ~85%\n"
                    "• Perfect use effectiveness: ~98%\n"
                    "• Very effective for STI prevention but not 100%\n\n"
                    "Correction: 'Condoms are highly effective at preventing "
                    "pregnancy and STIs when used correctly and consistently, "
                    "with effectiveness rates of approximately 98% for pregnancy "
                    "prevention with perfect use.'\n\n"
                    "Recommendation: Update claim to reflect accurate statistics"
                ),
                language="en"
            ),
            FewShotExample(
                input_text=(
                    "Claim from document: 'Sexual health education should "
                    "begin in elementary school to provide age-appropriate "
                    "foundation knowledge.'"
                ),
                expected_output=(
                    "Fact Check Result: ACCURATE\n\n"
                    "Analysis:\n"
                    "• Supported by major health organizations (WHO, AAP)\n"
                    "• Age-appropriate education improves health outcomes\n"
                    "• Early education helps prevent abuse and promotes safety\n"
                    "• Evidence shows benefits of comprehensive programs\n\n"
                    "Supporting Evidence: Multiple studies and health "
                    "organization guidelines support early, age-appropriate "
                    "sexual health education.\n\n"
                    "Recommendation: Claim is accurate and well-supported"
                ),
                language="en"
            )
        ]
        
        fact_check_template_en = PromptTemplate(
            template=(
                "Fact-check the following claim from a sexual health document:\n\n"
                "Claim: {claim}\n\n"
                "Provide:\n"
                "1. Accuracy assessment (Accurate/Partially Accurate/Inaccurate)\n"
                "2. Detailed analysis of the claim\n"
                "3. Supporting or contradicting evidence\n"
                "4. Corrected version if needed\n"
                "5. Recommendation for document improvement\n\n"
                "Base your assessment on current medical and scientific consensus."
            ),
            prompt_type=PromptType.SAFETY_CHECK,
            language="en",
            few_shot_examples=fact_check_examples_en,
            system_prompt=(
                "You are a sexual health fact-checker with access to current "
                "medical and scientific knowledge. Verify claims against "
                "established evidence and provide accurate corrections when needed."
            )
        )
        
        self.manager.register_template("fact_check_en", fact_check_template_en)
    
    def _create_question_generation_templates(self):
        """Create question generation templates for documents."""
        
        question_examples_en = [
            FewShotExample(
                input_text=(
                    "Document section: 'Contraceptive methods vary in "
                    "effectiveness, cost, and ease of use. Barrier methods "
                    "like condoms provide dual protection against pregnancy "
                    "and STIs, while hormonal methods like birth control "
                    "pills are highly effective for pregnancy prevention.'"
                ),
                expected_output=(
                    "Generated Questions:\n\n"
                    "Comprehension Questions:\n"
                    "1. What factors should be considered when choosing "
                    "contraceptive methods?\n"
                    "2. What is the advantage of barrier methods over "
                    "hormonal methods?\n\n"
                    "Application Questions:\n"
                    "3. How would you advise someone choosing between "
                    "condoms and birth control pills?\n"
                    "4. What questions should someone ask their healthcare "
                    "provider about contraception?\n\n"
                    "Critical Thinking Questions:\n"
                    "5. Why might someone choose a less effective method "
                    "over a more effective one?\n"
                    "6. How do cultural factors influence contraceptive choices?"
                ),
                language="en"
            )
        ]
        
        question_template_en = PromptTemplate(
            template=(
                "Generate educational questions based on the following "
                "document content:\n\n"
                "Content: {document_content}\n\n"
                "Create questions at different levels:\n"
                "1. Comprehension questions (understanding key facts)\n"
                "2. Application questions (using information practically)\n"
                "3. Critical thinking questions (analysis and evaluation)\n\n"
                "Ensure questions are appropriate for sexual health education "
                "and promote deeper understanding."
            ),
            prompt_type=PromptType.EDUCATIONAL,
            language="en",
            few_shot_examples=question_examples_en,
            system_prompt=(
                "You are an educational content developer specializing in "
                "sexual health education. Create thoughtful questions that "
                "help learners engage with and understand the material at "
                "different cognitive levels."
            )
        )
        
        self.manager.register_template("question_generation_en", question_template_en)
    
    def _create_safety_assessment_templates(self):
        """Create safety assessment templates for documents."""
        
        safety_examples_en = [
            FewShotExample(
                input_text=(
                    "Document content: 'Natural family planning methods are "
                    "just as effective as modern contraceptives and have no "
                    "side effects, making them the best choice for everyone.'"
                ),
                expected_output=(
                    "Safety Assessment: CONCERNING\n\n"
                    "Issues Identified:\n"
                    "1. Overstated effectiveness claims\n"
                    "2. Inappropriate universal recommendation\n"
                    "3. Dismisses individual needs and circumstances\n"
                    "4. May discourage use of more effective methods\n\n"
                    "Risk Level: MODERATE\n"
                    "- Could lead to unintended pregnancies\n"
                    "- Provides misleading information about effectiveness\n\n"
                    "Recommendations:\n"
                    "• Correct effectiveness statistics\n"
                    "• Emphasize individual choice and consultation\n"
                    "• Present balanced view of all methods\n"
                    "• Include healthcare provider guidance"
                ),
                language="en"
            ),
            FewShotExample(
                input_text=(
                    "Document content: 'Comprehensive sexual health education "
                    "includes information about anatomy, reproduction, "
                    "contraception, STI prevention, and healthy relationships "
                    "presented in an age-appropriate manner.'"
                ),
                expected_output=(
                    "Safety Assessment: SAFE\n\n"
                    "Positive Aspects:\n"
                    "1. Comprehensive approach\n"
                    "2. Age-appropriate consideration\n"
                    "3. Includes essential health topics\n"
                    "4. Balanced educational content\n\n"
                    "Risk Level: LOW\n"
                    "- Promotes evidence-based education\n"
                    "- Supports informed decision-making\n\n"
                    "Recommendations:\n"
                    "• Content appears appropriate and safe\n"
                    "• Aligns with best practices in sex education\n"
                    "• No safety concerns identified"
                ),
                language="en"
            )
        ]
        
        safety_template_en = PromptTemplate(
            template=(
                "Assess the safety and appropriateness of the following "
                "sexual health document content:\n\n"
                "Content: {document_content}\n\n"
                "Evaluate:\n"
                "1. Accuracy of medical/health information\n"
                "2. Potential for harm or misinformation\n"
                "3. Age-appropriateness of content\n"
                "4. Cultural sensitivity\n"
                "5. Bias or agenda concerns\n\n"
                "Provide a safety rating and specific recommendations."
            ),
            prompt_type=PromptType.SAFETY_CHECK,
            language="en",
            few_shot_examples=safety_examples_en,
            system_prompt=(
                "You are a sexual health content safety assessor. "
                "Identify potential risks, misinformation, or inappropriate "
                "content that could harm users or provide misleading "
                "health information. Prioritize user safety and accuracy."
            )
        )
        
        self.manager.register_template("safety_assessment_en", safety_template_en)
    
    def analyze_document(
        self, 
        content: str, 
        analysis_type: str = "extraction",
        language: str = "en"
    ) -> Optional[PromptTemplate]:
        """Get appropriate template for document analysis."""
        template_name = f"{analysis_type}_{language}"
        return self.manager.get_template(template_name)
    
    def get_all_analysis_types(self) -> List[str]:
        """Get list of available analysis types."""
        return [
            "content_extraction",
            "document_summary", 
            "fact_check",
            "question_generation",
            "safety_assessment"
        ] 