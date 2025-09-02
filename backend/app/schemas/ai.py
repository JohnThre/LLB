"""AI schemas stub"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TextGenerationRequest(BaseModel):
    prompt: str
    max_length: int = 100
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50

class TextGenerationResponse(BaseModel):
    generated_text: str

class ChatCompletionRequest(BaseModel):
    messages: List[Dict[str, str]]
    max_length: int = 100
    temperature: float = 0.7

class ChatCompletionResponse(BaseModel):
    response: str

class LanguageDetectionRequest(BaseModel):
    text: str

class LanguageDetectionResponse(BaseModel):
    language: str
    confidence: float

class TextSummarizationRequest(BaseModel):
    text: str
    max_length: int = 100
    min_length: int = 10

class TextSummarizationResponse(BaseModel):
    summary: str

class SentimentAnalysisRequest(BaseModel):
    text: str

class SentimentAnalysisResponse(BaseModel):
    sentiment: str
    score: float
    confidence: float

class TextClassificationRequest(BaseModel):
    text: str
    categories: List[str]

class TextClassificationResponse(BaseModel):
    category: str
    confidence: float
    scores: Dict[str, float]

class EntityExtractionRequest(BaseModel):
    text: str
    entity_types: Optional[List[str]] = None

class EntityExtractionResponse(BaseModel):
    entities: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]