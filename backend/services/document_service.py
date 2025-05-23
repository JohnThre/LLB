"""
Document service for LLB application.
Handles PDF processing and text extraction.
"""

import os
import tempfile
import asyncio
from typing import Optional, Dict, Any
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

try:
    import PyPDF2
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("⚠️ PDF libraries not available. Install PyPDF2 and pdfplumber for PDF support.")


class DocumentService:
    """Service for handling document processing."""
    
    def __init__(self):
        self._initialized = PDF_AVAILABLE
        
        if not PDF_AVAILABLE:
            logger.warning("⚠️ Document service not fully available without PDF libraries")
        else:
            logger.info("✅ Document service initialized")
    
    async def extract_text(self, file: UploadFile) -> str:
        """Extract text from uploaded document."""
        if not self._initialized:
            raise RuntimeError("Document service not initialized - PDF libraries missing")
        
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # Extract text using multiple methods
                text = await self._extract_pdf_text(temp_file_path)
                
                if not text.strip():
                    raise ValueError("No text could be extracted from the document")
                
                logger.info(f"✅ Extracted {len(text)} characters from document")
                return text
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"❌ Document text extraction failed: {e}")
            raise
    
    async def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods."""
        text = ""
        
        # Method 1: Try pdfplumber (better for complex layouts)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                logger.info("✅ Text extracted using pdfplumber")
                return text
                
        except Exception as e:
            logger.warning(f"⚠️ pdfplumber extraction failed: {e}")
        
        # Method 2: Try PyPDF2 (fallback)
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                logger.info("✅ Text extracted using PyPDF2")
                return text
                
        except Exception as e:
            logger.warning(f"⚠️ PyPDF2 extraction failed: {e}")
        
        raise RuntimeError("Could not extract text from PDF using any method")
    
    async def analyze_document_structure(self, file: UploadFile) -> Dict[str, Any]:
        """Analyze document structure and metadata."""
        if not self._initialized:
            raise RuntimeError("Document service not initialized")
        
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                analysis = {}
                
                # Basic file info
                analysis['file_size'] = len(content)
                analysis['file_name'] = file.filename
                
                # PDF-specific analysis
                with pdfplumber.open(temp_file_path) as pdf:
                    analysis['page_count'] = len(pdf.pages)
                    analysis['metadata'] = pdf.metadata or {}
                    
                    # Analyze first page for structure
                    if pdf.pages:
                        first_page = pdf.pages[0]
                        analysis['has_images'] = len(first_page.images) > 0
                        analysis['has_tables'] = len(first_page.find_tables()) > 0
                        
                        # Text statistics
                        text = first_page.extract_text() or ""
                        analysis['estimated_text_length'] = len(text) * len(pdf.pages)
                        analysis['language_hints'] = self._detect_language_hints(text)
                
                logger.info(f"✅ Document analysis completed: {analysis}")
                return analysis
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"❌ Document analysis failed: {e}")
            raise
    
    def _detect_language_hints(self, text: str) -> list:
        """Detect language hints from text sample."""
        hints = []
        
        # Check for Chinese characters
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            hints.append("chinese")
        
        # Check for English patterns
        if any(word in text.lower() for word in ['the', 'and', 'or', 'but', 'in', 'on', 'at']):
            hints.append("english")
        
        # Check for common sexual health terms
        health_terms_en = ['health', 'sexual', 'contraception', 'education', 'safety']
        health_terms_zh = ['健康', '性', '避孕', '教育', '安全']
        
        if any(term in text.lower() for term in health_terms_en):
            hints.append("sexual_health_en")
        
        if any(term in text for term in health_terms_zh):
            hints.append("sexual_health_zh")
        
        return hints
    
    async def validate_document(self, file: UploadFile) -> Dict[str, Any]:
        """Validate document for safety and appropriateness."""
        validation = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "file_info": {}
        }
        
        try:
            # Check file size (limit to 10MB)
            content = await file.read()
            file_size = len(content)
            
            validation["file_info"]["size"] = file_size
            validation["file_info"]["name"] = file.filename
            
            if file_size > 10 * 1024 * 1024:  # 10MB
                validation["errors"].append("File size exceeds 10MB limit")
                validation["is_valid"] = False
            
            # Check file type
            if not file.filename.lower().endswith('.pdf'):
                validation["warnings"].append("Only PDF files are fully supported")
            
            # Reset file position for further processing
            await file.seek(0)
            
            # If PDF libraries available, do deeper validation
            if self._initialized:
                try:
                    # Try to extract a small sample to verify it's a valid PDF
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(content)
                        temp_file_path = temp_file.name
                    
                    try:
                        with pdfplumber.open(temp_file_path) as pdf:
                            if len(pdf.pages) == 0:
                                validation["errors"].append("PDF appears to be empty")
                                validation["is_valid"] = False
                            elif len(pdf.pages) > 100:
                                validation["warnings"].append("Large document - processing may take time")
                    
                    finally:
                        os.unlink(temp_file_path)
                        
                except Exception as e:
                    validation["errors"].append(f"Invalid PDF format: {str(e)}")
                    validation["is_valid"] = False
            
            logger.info(f"✅ Document validation completed: {validation}")
            return validation
            
        except Exception as e:
            logger.error(f"❌ Document validation failed: {e}")
            validation["errors"].append(f"Validation error: {str(e)}")
            validation["is_valid"] = False
            return validation
    
    def is_available(self) -> bool:
        """Check if document service is available."""
        return self._initialized
    
    def get_supported_formats(self) -> list:
        """Get supported document formats."""
        return [".pdf"]
    
    def get_max_file_size(self) -> int:
        """Get maximum file size in bytes."""
        return 10 * 1024 * 1024  # 10MB 