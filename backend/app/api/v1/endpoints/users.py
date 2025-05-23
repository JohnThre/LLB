from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserCreate,
    UserPreferences,
    UserSettings
)
from app.core.security import get_password_hash, verify_password

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user.
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/me/change-password", response_model=UserResponse)
def change_password(
    *,
    db: Session = Depends(deps.get_db),
    current_password: str,
    new_password: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Change user password.
    """
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    current_user.hashed_password = get_password_hash(new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", response_model=UserResponse)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete current user.
    """
    db.delete(current_user)
    db.commit()
    return current_user

@router.get("/me/preferences", response_model=UserPreferences)
def get_user_preferences(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user preferences.
    """
    return current_user.preferences

@router.put("/me/preferences", response_model=UserPreferences)
def update_user_preferences(
    *,
    db: Session = Depends(deps.get_db),
    preferences: UserPreferences,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update user preferences.
    """
    current_user.preferences = preferences.dict()
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user.preferences

@router.get("/me/settings", response_model=UserSettings)
def get_user_settings(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user settings.
    """
    return current_user.settings

@router.put("/me/settings", response_model=UserSettings)
def update_user_settings(
    *,
    db: Session = Depends(deps.get_db),
    settings: UserSettings,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update user settings.
    """
    current_user.settings = settings.dict()
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user.settings 