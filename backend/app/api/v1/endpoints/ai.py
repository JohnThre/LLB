from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.core.ai import get_ai_model
from app.schemas.ai import (
    TextGenerationRequest,
    TextGenerationResponse,
    ChatCompletionRequest,
    ChatCompletionResponse,
    LanguageDetectionRequest,
    LanguageDetectionResponse,
    TextSummarizationRequest,
    TextSummarizationResponse,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    TextClassificationRequest,
    TextClassificationResponse,
    EntityExtractionRequest,
    EntityExtractionResponse
)

router = APIRouter()

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(
    *,
    request: TextGenerationRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate text based on prompt.
    """
    try:
        ai_model = get_ai_model()
        generated_text = await ai_model.generate_text(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k
        )
        return TextGenerationResponse(generated_text=generated_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/chat", response_model=ChatCompletionResponse)
async def chat_completion(
    *,
    request: ChatCompletionRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate chat completion.
    """
    try:
        ai_model = get_ai_model()
        response = await ai_model.chat_completion(
            messages=request.messages,
            max_length=request.max_length,
            temperature=request.temperature
        )
        return ChatCompletionResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(
    *,
    request: LanguageDetectionRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Detect language of text.
    """
    try:
        ai_model = get_ai_model()
        result = await ai_model.detect_language(request.text)
        return LanguageDetectionResponse(
            language=result["language"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/summarize", response_model=TextSummarizationResponse)
async def summarize_text(
    *,
    request: TextSummarizationRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Summarize text.
    """
    try:
        ai_model = get_ai_model()
        summary = await ai_model.summarize_text(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return TextSummarizationResponse(summary=summary)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/analyze-sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(
    *,
    request: SentimentAnalysisRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Analyze sentiment of text.
    """
    try:
        ai_model = get_ai_model()
        result = await ai_model.analyze_sentiment(request.text)
        return SentimentAnalysisResponse(
            sentiment=result["sentiment"],
            score=result["score"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/classify", response_model=TextClassificationResponse)
async def classify_text(
    *,
    request: TextClassificationRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Classify text into predefined categories.
    """
    try:
        ai_model = get_ai_model()
        result = await ai_model.classify_text(
            text=request.text,
            categories=request.categories
        )
        return TextClassificationResponse(
            category=result["category"],
            confidence=result["confidence"],
            scores=result["scores"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/extract-entities", response_model=EntityExtractionResponse)
async def extract_entities(
    *,
    request: EntityExtractionRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Extract named entities from text.
    """
    try:
        ai_model = get_ai_model()
        result = await ai_model.extract_entities(
            text=request.text,
            entity_types=request.entity_types
        )
        return EntityExtractionResponse(
            entities=result["entities"],
            confidence_scores=result["confidence_scores"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 