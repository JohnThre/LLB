"""
Custom exceptions for LLB Backend
Provides structured error handling and HTTP status codes
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class LLBException(Exception):
    """Base exception for LLB application."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class LLBHTTPException(HTTPException):
    """Base HTTP exception for LLB application."""

    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.details = details or {}
        super().__init__(
            status_code=status_code,
            detail={"message": message, "details": self.details},
        )


# AI Model Exceptions
class ModelNotLoadedException(LLBException):
    """Raised when AI model is not loaded."""

    def __init__(self, model_name: str):
        super().__init__(
            f"Model '{model_name}' is not loaded", {"model_name": model_name}
        )


class ModelLoadException(LLBException):
    """Raised when AI model fails to load."""

    def __init__(self, model_name: str, error: str):
        super().__init__(
            f"Failed to load model '{model_name}': {error}",
            {"model_name": model_name, "error": error},
        )


class ModelInferenceException(LLBException):
    """Raised when AI model inference fails."""

    def __init__(self, model_name: str, error: str):
        super().__init__(
            f"Model inference failed for '{model_name}': {error}",
            {"model_name": model_name, "error": error},
        )


# File Processing Exceptions
class FileProcessingException(LLBException):
    """Raised when file processing fails."""

    def __init__(self, filename: str, error: str):
        super().__init__(
            f"Failed to process file '{filename}': {error}",
            {"filename": filename, "error": error},
        )


class UnsupportedFileTypeException(LLBHTTPException):
    """Raised when file type is not supported."""

    def __init__(self, file_type: str, supported_types: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"File type '{file_type}' is not supported",
            details={
                "file_type": file_type,
                "supported_types": supported_types,
            },
        )


class FileSizeExceededException(LLBHTTPException):
    """Raised when file size exceeds limit."""

    def __init__(self, file_size: int, max_size: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            message=f"File size {file_size} bytes exceeds limit of {max_size} bytes",
            details={"file_size": file_size, "max_size": max_size},
        )


# Language Processing Exceptions
class LanguageNotSupportedException(LLBHTTPException):
    """Raised when language is not supported."""

    def __init__(self, language: str, supported_languages: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Language '{language}' is not supported",
            details={
                "language": language,
                "supported_languages": supported_languages,
            },
        )


class LanguageDetectionException(LLBException):
    """Raised when language detection fails."""

    def __init__(self, text: str, error: str):
        super().__init__(
            f"Failed to detect language for text: {error}",
            {"text_preview": text[:100], "error": error},
        )


# Content Safety Exceptions
class ContentSafetyException(LLBHTTPException):
    """Raised when content violates safety guidelines."""

    def __init__(self, reason: str, safety_flags: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Content violates safety guidelines: {reason}",
            details={"reason": reason, "safety_flags": safety_flags},
        )


class InappropriateContentException(LLBHTTPException):
    """Raised when content is inappropriate for the context."""

    def __init__(self, content_type: str, context: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Content type '{content_type}' is inappropriate for context '{context}'",
            details={"content_type": content_type, "context": context},
        )


# Audio Processing Exceptions
class AudioProcessingException(LLBException):
    """Raised when audio processing fails."""

    def __init__(self, error: str, audio_info: Optional[Dict] = None):
        super().__init__(
            f"Audio processing failed: {error}",
            {"error": error, "audio_info": audio_info or {}},
        )


class AudioFormatException(LLBHTTPException):
    """Raised when audio format is not supported."""

    def __init__(self, format_type: str, supported_formats: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Audio format '{format_type}' is not supported",
            details={
                "format_type": format_type,
                "supported_formats": supported_formats,
            },
        )


# Document Processing Exceptions
class DocumentProcessingException(LLBException):
    """Raised when document processing fails."""

    def __init__(self, document_name: str, error: str):
        super().__init__(
            f"Failed to process document '{document_name}': {error}",
            {"document_name": document_name, "error": error},
        )


class DocumentParsingException(LLBException):
    """Raised when document parsing fails."""

    def __init__(self, document_name: str, page_number: Optional[int] = None):
        super().__init__(
            f"Failed to parse document '{document_name}'"
            + (f" at page {page_number}" if page_number else ""),
            {"document_name": document_name, "page_number": page_number},
        )


# Configuration Exceptions
class ConfigurationException(LLBException):
    """Raised when configuration is invalid."""

    def __init__(self, config_key: str, error: str):
        super().__init__(
            f"Configuration error for '{config_key}': {error}",
            {"config_key": config_key, "error": error},
        )


# Service Exceptions
class ServiceUnavailableException(LLBHTTPException):
    """Raised when a service is unavailable."""

    def __init__(self, service_name: str, reason: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=f"Service '{service_name}' is unavailable: {reason}",
            details={"service_name": service_name, "reason": reason},
        )


class ServiceTimeoutException(LLBHTTPException):
    """Raised when a service times out."""

    def __init__(self, service_name: str, timeout_seconds: int):
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            message=f"Service '{service_name}' timed out after {timeout_seconds} seconds",
            details={
                "service_name": service_name,
                "timeout_seconds": timeout_seconds,
            },
        )
