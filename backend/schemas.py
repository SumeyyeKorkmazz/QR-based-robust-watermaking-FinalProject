from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# --- Image Schemas ---
class ImageResponse(BaseModel):
    id: int
    filename: str
    prompt: Optional[str] = None
    ai_model: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
