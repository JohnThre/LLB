"""
FastAPI routes for file upload and management.
"""

import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from loguru import logger

from ..core.config import Settings
from ..core.storage import StorageService

settings = Settings()
router = APIRouter(prefix="/api/files", tags=["Files"])

# Initialize storage service
storage_service = StorageService()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    file_type: str = "temp",
):
    """
    Upload a file.

    Args:
        file: File to upload
        file_type: Type of file (audio, documents, images, temp)

    Returns:
        Upload result with file information
    """
    try:
        # Validate file type
        if file_type not in ["audio", "documents", "images", "temp"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail=f"File type not allowed: {file_ext}"
            )

        # Save file
        file_path, filename = await storage_service.save_upload(
            file, file_type=file_type
        )

        return {
            "filename": filename,
            "fileType": file_type,
            "size": os.path.getsize(file_path),
            "url": f"/api/files/{file_type}/{filename}",
        }

    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"File upload failed: {str(e)}"
        )


@router.get("/{file_type}/{filename}")
async def get_file(
    file_type: str,
    filename: str,
):
    """
    Get a file.

    Args:
        file_type: Type of file
        filename: Name of the file

    Returns:
        File response
    """
    try:
        file_path = storage_service.get_file_path(filename, file_type)

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path, filename=filename)

    except Exception as e:
        logger.error(f"File retrieval error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"File retrieval failed: {str(e)}"
        )


@router.delete("/{file_type}/{filename}")
async def delete_file(
    file_type: str,
    filename: str,
):
    """
    Delete a file.

    Args:
        file_type: Type of file
        filename: Name of the file
    """
    try:
        storage_service.delete_file(filename, file_type)
        return {"message": "File deleted successfully"}

    except Exception as e:
        logger.error(f"File deletion error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"File deletion failed: {str(e)}"
        )
