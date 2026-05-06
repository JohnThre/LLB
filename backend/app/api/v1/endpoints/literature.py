"""
Approved literature management endpoints.
"""

from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, HttpUrl

from app.api import deps
from app.models.user import User
from app.services.literature_service import literature_service

router = APIRouter()


class LiteratureSourceCreate(BaseModel):
    """Payload for a source submitted for review."""

    title: str = Field(..., min_length=3, max_length=500)
    publisher: str = Field(..., min_length=2, max_length=250)
    language: Literal["en", "zh-CN"]
    source_type: Literal["official", "peer_reviewed"]
    url: HttpUrl
    topics: List[str] = Field(..., min_length=1)
    excerpt: str = Field(..., min_length=20, max_length=1200)
    jurisdiction: Optional[str] = Field("global", max_length=50)
    doi: Optional[str] = Field(None, max_length=120)
    pmid: Optional[str] = Field(None, max_length=80)


class LiteratureSourceResponse(BaseModel):
    """Reviewable source response."""

    id: str
    title: str
    publisher: str
    language: str
    source_type: str
    url: str
    topics: List[str]
    excerpt: str
    status: str
    jurisdiction: str
    publication_date: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    reviewed_by: Optional[str] = None


class LiteratureSourcesResponse(BaseModel):
    """List wrapper for literature sources."""

    sources: List[LiteratureSourceResponse]


def require_manage_literature(
    current_user: User = Depends(deps.get_current_active_user),
) -> User:
    """Require the manage_literature permission for mutating source actions."""
    if current_user.role not in {"admin", "moderator"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="manage_literature permission required",
        )
    return current_user


@router.get("/sources", response_model=LiteratureSourcesResponse)
async def list_sources(
    language: Optional[Literal["en", "zh-CN"]] = Query(None),
    status_filter: Optional[Literal["pending", "approved", "archived"]] = Query(
        "approved", alias="status"
    ),
) -> Dict[str, Any]:
    """List reviewable literature sources."""
    sources = literature_service.list_sources(language=language, status=status_filter)
    return {"sources": [source.to_dict() for source in sources]}


@router.post(
    "/sources",
    response_model=LiteratureSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_source(
    request: LiteratureSourceCreate,
    _: User = Depends(require_manage_literature),
) -> Dict[str, object]:
    """Create a pending source for admin review."""
    source = literature_service.create_source(
        {
            **request.model_dump(),
            "url": str(request.url),
        }
    )
    return source.to_dict()


@router.post("/sources/{source_id}/approve", response_model=LiteratureSourceResponse)
async def approve_source(
    source_id: str,
    current_user: User = Depends(require_manage_literature),
) -> Dict[str, object]:
    """Approve a source so it can support chat answers."""
    try:
        source = literature_service.approve_source(source_id, current_user.email)
    except KeyError:
        raise HTTPException(status_code=404, detail="Source not found") from None
    return source.to_dict()


@router.post("/sources/{source_id}/archive", response_model=LiteratureSourceResponse)
async def archive_source(
    source_id: str,
    _: User = Depends(require_manage_literature),
) -> Dict[str, object]:
    """Archive a source so it no longer supports chat answers."""
    try:
        source = literature_service.archive_source(source_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Source not found") from None
    return source.to_dict()
