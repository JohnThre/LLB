from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = "user"


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    name: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: str

    class Config:
        from_attributes = True


# Additional properties to return via API
class UserResponse(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


# User preferences
class UserPreferences(BaseModel):
    language: str = "en"
    theme: str = "light"
    notifications: bool = True


# User settings
class UserSettings(BaseModel):
    privacy_mode: bool = False
    data_retention_days: int = 30
    auto_delete_chats: bool = False
    voice_enabled: bool = True
    file_upload_enabled: bool = True
