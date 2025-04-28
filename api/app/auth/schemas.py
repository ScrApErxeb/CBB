from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: UUID  # Changer 'int' en 'UUID'
    email: EmailStr
    username: str

    model_config = {
        "from_attributes": True  # ✅ remplace orm_mode
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

# Schema pour Memory
from datetime import datetime

class MemoryCreate(BaseModel):
    content: str
    tags: Optional[str] = ""
    source: Optional[str] = "manual"

class MemoryOut(MemoryCreate):
    id: UUID  # Utilise UUID ici aussi
    timestamp: datetime

    model_config = {
        "from_attributes": True  # ✅ remplace orm_mode
    }
