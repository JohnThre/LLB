import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.models.chat import Chat, Message
from backend.app.schemas.chat import ChatCreate, MessageCreate
from backend.app.crud.chat import (
    create_chat,
    get_chat,
    get_chats,
    update_chat,
    delete_chat,
    archive_chat,
    pin_chat,
    unpin_chat,
)

def test_create_chat(db: Session):
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    assert chat.title == "Test Chat"
    assert not chat.is_archived
    assert not chat.is_pinned
    assert chat.pinned_at is None

def test_get_chat(db: Session):
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    retrieved_chat = get_chat(db, chat.id)
    assert retrieved_chat.id == chat.id
    assert retrieved_chat.title == chat.title

def test_get_chats(db: Session):
    # Create multiple chats
    chats = [
        ChatCreate(title=f"Test Chat {i}") for i in range(3)
    ]
    created_chats = [create_chat(db, chat) for chat in chats]
    
    # Test getting all chats
    all_chats = get_chats(db)
    assert len(all_chats) >= len(created_chats)
    
    # Test getting non-archived chats
    non_archived = get_chats(db, archived=False)
    assert all(not chat.is_archived for chat in non_archived)
    
    # Test getting pinned chats
    pin_chat(db, created_chats[0].id)
    pinned = get_chats(db, pinned=True)
    assert len(pinned) >= 1
    assert any(chat.id == created_chats[0].id for chat in pinned)

def test_update_chat(db: Session):
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    
    # Update title
    updated_chat = update_chat(db, chat.id, {"title": "Updated Chat"})
    assert updated_chat.title == "Updated Chat"
    
    # Update with invalid data
    with pytest.raises(ValueError):
        update_chat(db, chat.id, {"invalid_field": "value"})

def test_delete_chat(db: Session):
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    
    # Delete chat
    delete_chat(db, chat.id)
    deleted_chat = get_chat(db, chat.id)
    assert deleted_chat is None

def test_archive_chat(db: Session):
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    
    # Archive chat
    archived_chat = archive_chat(db, chat.id)
    assert archived_chat.is_archived
    
    # Unarchive chat
    unarchived_chat = archive_chat(db, chat.id, archive=False)
    assert not unarchived_chat.is_archived

def test_pin_chat(db: Session):
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    
    # Pin chat
    pinned_chat = pin_chat(db, chat.id)
    assert pinned_chat.is_pinned
    assert pinned_chat.pinned_at is not None
    
    # Unpin chat
    unpinned_chat = unpin_chat(db, chat.id)
    assert not unpinned_chat.is_pinned
    assert unpinned_chat.pinned_at is None

def test_chat_messages(db: Session):
    # Create chat
    chat_data = ChatCreate(title="Test Chat")
    chat = create_chat(db, chat_data)
    
    # Add messages
    messages = [
        MessageCreate(content=f"Test message {i}", role="user")
        for i in range(3)
    ]
    
    for msg in messages:
        message = Message(
            chat_id=chat.id,
            content=msg.content,
            role=msg.role
        )
        db.add(message)
    db.commit()
    
    # Verify messages
    retrieved_chat = get_chat(db, chat.id)
    assert len(retrieved_chat.messages) == 3
    assert all(msg.role == "user" for msg in retrieved_chat.messages) 