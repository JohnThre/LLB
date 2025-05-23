"""
Chat schemas for request/response validation.
"""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, constr


class MessageBase(BaseModel):
    """Base message schema."""

    content: constr(min_length=1, max_length=4000) = Field(
        ..., description="Message content"
    )
    role: Literal["user", "assistant", "system"] = Field(
        ..., description="Message role (user/assistant/system)"
    )


class MessageCreate(MessageBase):
    """Schema for creating a new message."""


class MessageResponse(MessageBase):
    """Schema for message response."""

    id: str = Field(..., description="Message ID")
    chat_id: str = Field(..., description="Chat ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    """Base chat schema."""

    title: constr(min_length=1, max_length=100) = Field(
        ..., description="Chat title"
    )


class ChatCreate(ChatBase):
    """Schema for creating a new chat."""


class ChatUpdate(BaseModel):
    """Schema for updating a chat."""

    title: Optional[constr(min_length=1, max_length=100)] = Field(
        None, description="Chat title"
    )
    is_archived: Optional[bool] = Field(
        None, description="Whether the chat is archived"
    )
    is_pinned: Optional[bool] = Field(
        None, description="Whether the chat is pinned"
    )


class ChatResponse(ChatBase):
    """Schema for chat response."""

    id: str = Field(..., description="Chat ID")
    user_id: str = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    is_archived: bool = Field(False, description="Whether the chat is archived")
    is_pinned: bool = Field(False, description="Whether the chat is pinned")

    class Config:
        from_attributes = True


class ChatHistoryResponse(ChatResponse):
    """Schema for chat history response."""

    messages: List[MessageResponse] = Field(
        default_factory=list, description="Chat messages"
    )
