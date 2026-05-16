"""Desktop-local control endpoints.

These routes are intended for the Electron main process. They must be
protected by a per-launch token because they can update in-memory BYOK
credentials for provider calls.
"""

import os
from typing import Dict, List, Optional

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from services import ai_providers

router = APIRouter()


class DesktopProviderCredential(BaseModel):
    """Provider credential payload supplied by the desktop shell."""

    api_key: Optional[str] = Field(None, min_length=1)
    token: Optional[str] = Field(None, min_length=1)
    model: Optional[str] = Field(None, min_length=1)
    base_url: Optional[str] = Field(None, min_length=1)
    api_version: Optional[str] = Field(None, min_length=1)


class DesktopProviderCredentialRequest(BaseModel):
    """Request body for setting desktop provider credentials."""

    credentials: Dict[str, DesktopProviderCredential]


class DesktopProviderStatus(BaseModel):
    """Masked provider credential status."""

    name: str
    model: str
    has_api_key: bool


class DesktopProviderCredentialResponse(BaseModel):
    """Response body for desktop credential updates."""

    providers: List[DesktopProviderStatus]


def _verify_desktop_token(header_token: Optional[str]) -> None:
    """Validate the desktop per-launch control token."""
    expected_token = os.getenv("LLB_DESKTOP_CONTROL_TOKEN")
    if not expected_token or header_token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid desktop control token",
        )


@router.post(
    "/provider-credentials",
    response_model=DesktopProviderCredentialResponse,
)
async def set_provider_credentials(
    request: DesktopProviderCredentialRequest,
    desktop_token: Optional[str] = Header(None, alias="x-llb-desktop-token"),
) -> DesktopProviderCredentialResponse:
    """Set in-memory provider credentials supplied by Electron."""
    _verify_desktop_token(desktop_token)
    credentials = {
        provider: payload.model_dump(exclude_none=True)
        for provider, payload in request.credentials.items()
    }
    ai_providers.set_desktop_provider_credentials(credentials)
    return DesktopProviderCredentialResponse(
        providers=[
            DesktopProviderStatus(**provider)
            for provider in ai_providers.get_desktop_provider_status()
        ]
    )
