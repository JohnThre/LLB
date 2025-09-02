"""
Storage service for handling file uploads and processing.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from fastapi import UploadFile
import logging
from .config import Settings
from .sanitizer import sanitize_path, sanitize_log_input

logger = logging.getLogger(__name__)

settings = Settings()


class StorageService:
    """Service for handling file storage and processing."""

    def __init__(self):
        """Initialize storage service."""
        self.base_dir = Path(settings.UPLOAD_DIR)
        self.temp_dir = self.base_dir / "temp"
        self.create_directories()

    def create_directories(self):
        """Create necessary directories."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for different file types
        (self.base_dir / "audio").mkdir(exist_ok=True)
        (self.base_dir / "documents").mkdir(exist_ok=True)
        (self.base_dir / "images").mkdir(exist_ok=True)

    async def save_upload(
        self,
        file: UploadFile,
        file_type: str = "temp",
        custom_filename: Optional[str] = None,
    ) -> Tuple[Path, str]:
        """
        Save an uploaded file.

        Args:
            file: Uploaded file
            file_type: Type of file (audio, documents, images, temp)
            custom_filename: Optional custom filename

        Returns:
            Tuple of (file path, filename)
        """
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = file.filename
            extension = Path(original_filename).suffix

            if custom_filename:
                filename = f"{custom_filename}{extension}"
            else:
                filename = f"{timestamp}_{original_filename}"

            # Determine save directory
            if file_type == "temp":
                save_dir = self.temp_dir
            else:
                save_dir = self.base_dir / file_type

            # Ensure directory exists
            save_dir.mkdir(parents=True, exist_ok=True)

            # Save file
            file_path = save_dir / filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            logger.info(f"File saved: {file_path}")
            return file_path, filename

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise

    def get_file_path(self, filename: str, file_type: str = "temp") -> Path:
        """
        Get the full path for a file.

        Args:
            filename: Name of the file
            file_type: Type of file

        Returns:
            Full file path
        """
        # Sanitize filename to prevent path traversal
        safe_filename = Path(filename).name  # Only keep filename, remove path components
        
        if file_type == "temp":
            base_dir = self.temp_dir
        else:
            base_dir = self.base_dir / file_type
        
        # Construct and validate path
        file_path = base_dir / safe_filename
        sanitized_path = sanitize_path(str(file_path), str(base_dir))
        
        return Path(sanitized_path)

    def delete_file(self, filename: str, file_type: str = "temp"):
        """
        Delete a file.

        Args:
            filename: Name of the file
            file_type: Type of file
        """
        try:
            file_path = self.get_file_path(filename, file_type)
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise

    def cleanup_temp_files(self, max_age_hours: int = 24):
        """
        Clean up temporary files older than max_age_hours.

        Args:
            max_age_hours: Maximum age of files in hours
        """
        try:
            current_time = datetime.now()
            for file_path in self.temp_dir.glob("*"):
                if file_path.is_file():
                    file_age = current_time - datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    )
                    if file_age.total_seconds() > (max_age_hours * 3600):
                        file_path.unlink()
                        logger.info(f"Cleaned up old file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {str(e)}")
            raise
