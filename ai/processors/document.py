"""
Document processor for handling PDF and text documents.
"""

import os
from typing import Dict, Any, Optional
import PyPDF2
from loguru import logger

from ai.config import MAX_PDF_PAGES, MAX_PDF_SIZE_MB


class DocumentProcessor:
    """Document processor for PDF and text files."""
    
    def __init__(self):
        """Initialize the document processor."""
        logger.info("Initializing document processor")
    
    def process_pdf_file(
        self,
        file_path: str,
        max_pages: int = MAX_PDF_PAGES,
    ) -> Dict[str, Any]:
        """
        Process a PDF file and extract its content.
        
        Args:
            file_path: Path to PDF file
            max_pages: Maximum number of pages to process
            
        Returns:
            Extracted content and metadata
        """
        try:
            # Validate file path to prevent path traversal
            normalized_path = os.path.normpath(file_path)
            if '..' in normalized_path or not normalized_path.endswith('.pdf'):
                raise ValueError(f"Invalid file path: {file_path}")
            
            if not os.path.exists(normalized_path):
                raise FileNotFoundError(f"PDF file not found: {normalized_path}")
            
            # Check file size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > MAX_PDF_SIZE_MB:
                raise ValueError(
                    f"PDF file too large: {file_size_mb:.1f}MB "
                    f"(max: {MAX_PDF_SIZE_MB}MB)"
                )
            
            # Open and read PDF
            with open(normalized_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Get metadata
                metadata = reader.metadata
                
                # Extract text from pages
                pages = []
                for i, page in enumerate(reader.pages):
                    if i >= max_pages:
                        break
                    
                    text = page.extract_text()
                    if text:
                        pages.append({
                            'page_number': i + 1,
                            'text': text.strip()
                        })
                
                return {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'pages': pages,
                    'total_pages': len(reader.pages),
                    'processed_pages': len(pages)
                }
            
        except Exception as e:
            logger.error(f"Error processing PDF file: {str(e)}")
            raise
    
    def process_pdf_bytes(
        self,
        pdf_data: bytes,
        max_pages: int = MAX_PDF_PAGES,
    ) -> Dict[str, Any]:
        """
        Process PDF data from bytes.
        
        Args:
            pdf_data: PDF data in bytes
            max_pages: Maximum number of pages to process
            
        Returns:
            Extracted content and metadata
        """
        try:
            # Save PDF data to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(pdf_data)
                temp_path = temp_file.name
            
            try:
                result = self.process_pdf_file(temp_path, max_pages)
                return result
            finally:
                # Clean up temporary file
                os.unlink(temp_path)
                
        except Exception as e:
            logger.error(f"Error processing PDF bytes: {str(e)}")
            raise
    
    def process_text_file(
        self,
        file_path: str,
    ) -> Dict[str, Any]:
        """
        Process a text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Extracted content
        """
        try:
            # Validate file path to prevent path traversal
            normalized_path = os.path.normpath(file_path)
            if '..' in normalized_path or not normalized_path.endswith('.txt'):
                raise ValueError(f"Invalid file path: {file_path}")
            
            if not os.path.exists(normalized_path):
                raise FileNotFoundError(f"Text file not found: {normalized_path}")
            
            with open(normalized_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return {
                'text': content,
                'size': len(content),
                'lines': content.count('\n') + 1
            }
            
        except Exception as e:
            logger.error(f"Error processing text file: {str(e)}")
            raise 