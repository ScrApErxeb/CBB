from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models import Memory, User
from app.memory.schemas import MemoryCreate, MemoryOut

from datetime import datetime

router = APIRouter()

@router.post("/", response_model=MemoryOut)
def create_memory(data: MemoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    memory = Memory(
        content=data.content,
        tags=data.tags,
        source=data.source,
        user_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory
