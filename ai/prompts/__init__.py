"""
Prompt engineering module for LLB sexual health education AI.
Provides template-based prompts with few-shot learning capabilities.
"""

from prompts.base import PromptTemplate, PromptManager
from prompts.sexual_health import SexualHealthPrompts
from prompts.language_support import LanguagePrompts
from prompts.document_analysis import DocumentPrompts

__all__ = [
    'PromptTemplate',
    'PromptManager', 
    'SexualHealthPrompts',
    'LanguagePrompts',
    'DocumentPrompts'
] 