"""
Chat endpoints for managing conversations and messages.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api import deps
from app.models.user import User
from app.models.chat import Chat, Message
from app.schemas.chat import (
    ChatCreate,
    ChatResponse,
    MessageCreate,
    MessageResponse,
    ChatHistoryResponse,
    ChatUpdate
)

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def create_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_in: ChatCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new chat.
    """
    chat = Chat(
        title=chat_in.title,
        user_id=current_user.id
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.get("/", response_model=List[ChatResponse])
def read_chats(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    archived: bool = False,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user's chats.
    """
    query = db.query(Chat).filter(
        Chat.user_id == current_user.id,
        Chat.is_archived == archived
    )
    
    # Order by pinned status and updated time
    chats = query.order_by(
        desc(Chat.is_pinned),
        desc(Chat.updated_at)
    ).offset(skip).limit(limit).all()
    
    return chats

@router.get("/{chat_id}", response_model=ChatHistoryResponse)
def read_chat(
    chat_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get chat by ID with messages.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return chat

@router.post("/{chat_id}/messages", response_model=MessageResponse)
def create_message(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    message_in: MessageCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new message in chat.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    message = Message(
        content=message_in.content,
        role=message_in.role,
        chat_id=chat_id
    )
    db.add(message)
    
    # Update chat's updated_at timestamp
    chat.updated_at = func.now()
    db.add(chat)
    
    db.commit()
    db.refresh(message)
    return message

@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
def read_messages(
    chat_id: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve chat messages.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    messages = db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(
        Message.created_at
    ).offset(skip).limit(limit).all()
    
    return messages

@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    chat_in: ChatUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update chat details.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    update_data = chat_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chat, field, value)
    
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.delete("/{chat_id}", response_model=ChatResponse)
def delete_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a chat and all its messages.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Delete all messages in the chat
    db.query(Message).filter(Message.chat_id == chat_id).delete()
    
    # Delete the chat
    db.delete(chat)
    db.commit()
    return chat

@router.delete("/{chat_id}/messages/{message_id}", response_model=MessageResponse)
def delete_message(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    message_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a specific message from a chat.
    """
    # Verify chat ownership
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Get and delete the message
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.chat_id == chat_id
    ).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    db.delete(message)
    db.commit()
    return message

@router.put("/{chat_id}/archive", response_model=ChatResponse)
def archive_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Archive a chat.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    chat.is_archived = True
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.put("/{chat_id}/unarchive", response_model=ChatResponse)
def unarchive_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Unarchive a chat.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    chat.is_archived = False
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.put("/{chat_id}/pin", response_model=ChatResponse)
def pin_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Pin a chat.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    chat.is_pinned = True
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@router.put("/{chat_id}/unpin", response_model=ChatResponse)
def unpin_chat(
    *,
    db: Session = Depends(deps.get_db),
    chat_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Unpin a chat.
    """
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    chat.is_pinned = False
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat 