"""
Knowledge API endpoints
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.logging import get_logger
from app.services.knowledge_service import KnowledgeService
from app.services.scheduler_service import SchedulerService

logger = get_logger(__name__)

router = APIRouter()
knowledge_service = KnowledgeService()
scheduler_service = SchedulerService()


class KnowledgeEntry(BaseModel):
    id: int
    title: str
    content: str
    summary: str
    category: str
    language: str
    keywords: List[str]
    quality_score: float


class UpdateRequest(BaseModel):
    query: Optional[str] = None


class UpdateResponse(BaseModel):
    status: str
    entries_added: int
    entries_updated: int
    topics_processed: int
    update_id: int


@router.get("/entries", response_model=List[KnowledgeEntry])
async def get_knowledge_entries(
    category: Optional[str] = Query(None, description="Filter by category"),
    language: Optional[str] = Query(None, description="Filter by language"),
    limit: int = Query(50, ge=1, le=100, description="Number of entries to return")
):
    """Get knowledge entries from database."""
    try:
        entries = await knowledge_service.get_knowledge_entries(
            category=category,
            language=language,
            limit=limit
        )
        return entries
    except Exception as e:
        logger.error(f"Error getting knowledge entries: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve knowledge entries")


@router.post("/update", response_model=UpdateResponse)
async def trigger_knowledge_update(request: UpdateRequest):
    """Trigger manual knowledge update."""
    try:
        result = await scheduler_service.trigger_manual_update(request.query)
        return UpdateResponse(**result)
    except Exception as e:
        logger.error(f"Error triggering knowledge update: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger knowledge update")


@router.get("/updates")
async def get_update_history(
    limit: int = Query(10, ge=1, le=50, description="Number of updates to return")
):
    """Get knowledge update history."""
    try:
        updates = await knowledge_service.get_update_history(limit=limit)
        return {"updates": updates}
    except Exception as e:
        logger.error(f"Error getting update history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve update history")


@router.get("/scheduler/status")
async def get_scheduler_status():
    """Get scheduler status."""
    try:
        status = scheduler_service.get_status()
        return status
    except Exception as e:
        logger.error(f"Error getting scheduler status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get scheduler status")


@router.post("/scheduler/start")
async def start_scheduler():
    """Start the knowledge update scheduler."""
    try:
        await scheduler_service.start_scheduler()
        return {"message": "Scheduler started successfully"}
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        raise HTTPException(status_code=500, detail="Failed to start scheduler")


@router.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the knowledge update scheduler."""
    try:
        await scheduler_service.stop_scheduler()
        return {"message": "Scheduler stopped successfully"}
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop scheduler")


@router.get("/categories")
async def get_categories():
    """Get available knowledge categories."""
    return {
        "categories": [
            "anatomy",
            "contraception", 
            "sti_prevention",
            "reproductive_health",
            "consent_education",
            "sexual_safety",
            "pregnancy_prevention",
            "general"
        ]
    }


@router.get("/languages")
async def get_languages():
    """Get supported languages."""
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "zh-CN", "name": "Chinese (Simplified)"}
        ]
    }