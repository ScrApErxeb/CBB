# app/auth/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None




from datetime import datetime

class MemoryCreate(BaseModel):
    content: str
    tags: Optional[str] = ""
    source: Optional[str] = "manual"

class MemoryOut(MemoryCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
