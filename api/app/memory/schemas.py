# app/memory/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

# Schéma pour la création d'une mémoire
class MemoryCreate(BaseModel):
    content: str
    tags: Optional[str] = ""
    source: Optional[str] = "manual"

# Schéma pour afficher une mémoire


class MemoryOut(BaseModel):
    id: int
    content: str
    tags: str
    source: str
    timestamp: datetime

    class Config:
        from_attributes = True  # ou orm_mode = True si V1 de Pydantic




# app/memory/schemas.py

class MemorySource(str, Enum):
    MANUAL = "manual"
    EMAIL = "email"
    CHAT = "chat"
    BROWSER = "browser"
    VOICE = "voice"

class MemoryCreate(BaseModel):
    content: str
    tags: list[str] = []
    source: MemorySource = MemorySource.MANUAL  # <--- important
