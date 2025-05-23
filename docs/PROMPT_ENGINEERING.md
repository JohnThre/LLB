# LLB Prompt Engineering System

## Overview

The LLB (爱学伴) prompt engineering system provides a comprehensive framework for generating contextually appropriate, culturally sensitive, and educationally effective prompts for sexual health education using the Gemma 3 1B model.

## Key Features

### 🎯 **Few-Shot Learning**
- Pre-built examples for common sexual health topics
- Contextual examples that guide AI responses
- Culturally appropriate example sets

### 🌍 **Multilingual Support**
- English (American and British)
- Simplified Chinese (Mandarin)
- Henan Dialect support
- Automatic language detection

### 🛡️ **Safety & Content Filtering**
- Automatic safety assessment
- Age-appropriate content filtering
- Medical advice detection and redirection
- Cultural sensitivity checks

### 📚 **Topic Classification**
- Basic sexual health education
- Safety and protection
- Contraception methods
- Anatomy and physiology
- Relationships and communication
- STI prevention and education
- Consent education

### 📄 **Document Analysis**
- PDF content extraction
- Fact-checking capabilities
- Educational question generation
- Content summarization
- Safety assessment of documents

## System Architecture

```
PromptEngine
├── SexualHealthPrompts    # Core educational templates
├── LanguagePrompts        # Multilingual and cultural support
├── DocumentPrompts        # PDF analysis and processing
└── Safety Assessment      # Content filtering and validation
```

## Quick Start

### Basic Usage

```python
from ai.prompt_engine import PromptEngine, PromptRequest, InputType

# Initialize the engine
engine = PromptEngine()

# Create a request
request = PromptRequest(
    content="What is sexual health?",
    input_type=InputType.TEXT
)

# Process the request
response = engine.process_request(request)

# Use the formatted prompt with Gemma 3 1B
formatted_prompt = response.formatted_prompt
```

### Multilingual Example

```python
# Chinese question
request = PromptRequest(
    content="什么是性健康？",
    input_type=InputType.TEXT
)
response = engine.process_request(request)

# Henan dialect with cultural context
request = PromptRequest(
    content="俺想知道性健康是啥意思？",
    input_type=InputType.TEXT,
    cultural_context="henan"
)
response = engine.process_request(request)
```

### Document Analysis

```python
# Analyze PDF content
request = PromptRequest(
    content="[PDF content text]",
    input_type=InputType.DOCUMENT
)
response = engine.process_request(request)
```

## Template Categories

### 1. Sexual Health Education Templates

#### Basic Education (`basic_education`)
- Fundamental concepts of sexual health
- Age-appropriate introductory information
- Non-judgmental, evidence-based responses

#### Safety Education (`safety`)
- Safe sex practices
- Risk reduction strategies
- Protection methods and their effectiveness

#### Contraception (`contraception`)
- Birth control methods overview
- Effectiveness rates and considerations
- Healthcare provider consultation guidance

#### Anatomy & Physiology (`anatomy`)
- Reproductive system education
- Menstrual cycle explanation
- Body awareness and health

#### Relationships (`relationship`)
- Communication skills
- Healthy relationship dynamics
- Partner discussions about sexual health

#### STI Prevention (`sti`)
- Sexually transmitted infection education
- Prevention strategies
- Testing and treatment information

#### Consent Education (`consent`)
- Consent definition and importance
- Boundary setting and respect
- Communication about consent

### 2. Language Support Templates

#### Language Detection
- Automatic identification of English, Chinese, and Henan dialect
- Pattern-based recognition with high accuracy
- Fallback mechanisms for unclear input

#### Cultural Adaptation
- Chinese cultural context considerations
- Henan regional dialect support
- Western cultural perspective integration

#### Translation Support
- English ↔ Chinese translation templates
- Cultural appropriateness in translations
- Medical terminology accuracy

### 3. Document Analysis Templates

#### Content Extraction
- Key topic identification
- Educational value assessment
- Relevance scoring for sexual health education

#### Fact Checking
- Medical accuracy verification
- Evidence-based claim validation
- Correction suggestions for inaccurate information

#### Question Generation
- Comprehension questions from content
- Application-based learning questions
- Critical thinking prompts

#### Safety Assessment
- Content appropriateness evaluation
- Risk identification in documents
- Age-appropriate content verification

## Few-Shot Learning Examples

The system includes carefully crafted few-shot examples for each topic:

### English Example
```
User: What is sexual health?
Assistant: Sexual health is a state of physical, emotional, mental and social 
well-being related to sexuality. It includes having pleasurable and safe sexual 
experiences, free of coercion, discrimination, and violence...
```

### Chinese Example
```
用户：什么是性健康？
助手：性健康是指与性相关的身体、情感、精神和社会福祉状态。它包括拥有愉悦和安全的性体验，
免受强迫、歧视和暴力...
```

### Henan Dialect Example
```
用户：俺想知道性健康是啥意思？
助手：性健康就是说你的身体、心理和社会方面都要健康，跟性有关的事情都要安全、愉快，
不能被人强迫或者歧视...
```

## Safety Features

### Content Filtering
- Harmful content detection
- Age-inappropriate material flagging
- Medical advice boundary enforcement

### Cultural Sensitivity
- Regional cultural considerations
- Traditional value respect while maintaining scientific accuracy
- Appropriate language and terminology usage

### Medical Boundaries
- Clear distinction between education and medical advice
- Healthcare provider referral recommendations
- Symptom discussion limitations

## Integration with Gemma 3 1B

### Prompt Optimization
The system generates prompts optimized for Gemma 3 1B's capabilities:

1. **Clear System Instructions**: Establishes the AI's role as a sexual health educator
2. **Few-Shot Examples**: Provides context and expected response format
3. **Specific Guidelines**: Includes safety, cultural, and educational requirements
4. **Variable Substitution**: Seamlessly integrates user questions into templates

### Example Integration

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from ai.prompt_engine import PromptEngine, PromptRequest, InputType

# Load Gemma 3 1B model
tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-1b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-1b")

# Initialize prompt engine
prompt_engine = PromptEngine()

# Process user input
user_question = "How can I practice safe sex?"
request = PromptRequest(
    content=user_question,
    input_type=InputType.TEXT
)
response = prompt_engine.process_request(request)

# Generate AI response
inputs = tokenizer(response.formatted_prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512, temperature=0.7)
ai_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## Configuration Options

### Language Settings
```python
# Set preferred language
request.language = "zh-CN"

# Set cultural context
request.cultural_context = "chinese"  # or "henan", "western"
```

### Safety Levels
```python
# Adjust safety filtering
request.safety_level = "strict"  # "strict", "standard", "relaxed"
```

### Age Groups
```python
# Specify target age group
request.user_age_group = "teen"  # "child", "teen", "adult"
```

## Customization

### Adding Custom Templates

```python
from ai.prompts.base import PromptTemplate, PromptType, FewShotExample

# Create custom template
custom_template = PromptTemplate(
    template="Custom question: {user_question}\n\nProvide specialized response...",
    prompt_type=PromptType.EDUCATIONAL,
    language="en",
    few_shot_examples=[
        FewShotExample(
            input_text="Example question",
            expected_output="Example response",
            language="en"
        )
    ]
)

# Add to engine
engine.add_custom_template("custom_topic", custom_template, "sexual_health")
```

### Extending Language Support

```python
# Add new language patterns
engine.language_patterns["new_lang"] = [
    r'pattern1',
    r'pattern2'
]

# Add topic patterns for new language
engine.topic_patterns["new_topic"] = [
    r'english_pattern',
    r'new_language_pattern'
]
```

## Performance Considerations

### Template Selection
- O(1) template lookup by name
- O(n) pattern matching for topic classification
- Confidence scoring for optimal template selection

### Memory Usage
- Templates loaded once at initialization
- Minimal runtime memory overhead
- Efficient string formatting and substitution

### Scalability
- Modular design allows easy extension
- Template caching for frequently used prompts
- Batch processing support for multiple requests

## Best Practices

### 1. Template Design
- Keep examples concise but comprehensive
- Include diverse scenarios in few-shot examples
- Maintain consistent tone and style across languages

### 2. Safety Implementation
- Always validate user input before processing
- Implement multiple safety check layers
- Provide clear guidance when redirecting to healthcare providers

### 3. Cultural Sensitivity
- Research cultural norms for target regions
- Test templates with native speakers
- Balance cultural respect with scientific accuracy

### 4. Performance Optimization
- Cache frequently used templates
- Minimize regex pattern complexity
- Use efficient string operations

## Testing and Validation

### Unit Tests
```bash
cd ai/
python -m pytest tests/test_prompts.py
```

### Integration Tests
```bash
python ai/prompt_demo.py
```

### Manual Testing
```python
# Test specific scenarios
from ai.prompt_demo import demo_topic_classification
demo_topic_classification()
```

## Troubleshooting

### Common Issues

1. **Language Detection Fails**
   - Check input text length (minimum 10 characters recommended)
   - Verify language patterns are correctly defined
   - Use explicit language parameter as fallback

2. **Template Not Found**
   - Verify template name spelling
   - Check if template exists for specified language
   - Use fallback template selection

3. **Safety Flags Triggered Unexpectedly**
   - Review safety pattern definitions
   - Adjust safety level if appropriate
   - Check for false positive patterns

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check template selection process
response = engine.process_request(request)
print(f"Template used: {response.template_used}")
print(f"Safety flags: {response.safety_flags}")
print(f"Confidence: {response.confidence_score}")
```

## Future Enhancements

### Planned Features
- Voice input processing integration
- Advanced cultural context detection
- Machine learning-based template selection
- Real-time template performance analytics
- Extended dialect support

### Contribution Guidelines
1. Follow existing code style and patterns
2. Include comprehensive tests for new features
3. Update documentation for any API changes
4. Ensure cultural sensitivity in all additions
5. Validate medical accuracy with healthcare professionals

## Support and Resources

### Documentation
- [API Reference](./API_REFERENCE.md)
- [Cultural Guidelines](./CULTURAL_GUIDELINES.md)
- [Safety Standards](./SAFETY_STANDARDS.md)

### Community
- GitHub Issues for bug reports
- Discussion forum for feature requests
- Cultural advisory board for sensitivity review

---

*This prompt engineering system is designed to provide safe, accurate, and culturally appropriate sexual health education. Always prioritize user safety and encourage professional medical consultation when appropriate.* 