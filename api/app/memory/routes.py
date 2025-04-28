# app/memory/routes.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.memory import schemas
from app.models import memory as models
from app.auth.dependencies import get_current_user
from app.models import User
 
router = APIRouter()

@router.post("/memories/", response_model=schemas.MemoryOut)
def create_memory(memory: schemas.MemoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_memory = models.Memory(content=memory.content, tags=memory.tags, source=memory.source, user_id=current_user.id)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

@router.get("/memories/{memory_id}", response_model=schemas.MemoryOut)
def read_memory(memory_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_memory = db.query(models.Memory).filter(models.Memory.id == memory_id, models.Memory.user_id == current_user.id).first()
    if db_memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return db_memory

@router.get("/memories/", response_model=list[schemas.MemoryOut])
def get_memories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_memories = db.query(models.Memory).filter(models.Memory.user_id == current_user.id).all()
    return db_memories

@router.put("/memories/{memory_id}", response_model=schemas.MemoryOut)
def update_memory(memory_id: int, memory: schemas.MemoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_memory = db.query(models.Memory).filter(models.Memory.id == memory_id, models.Memory.user_id == current_user.id).first()
    if db_memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")

    db_memory.content = memory.content
    db_memory.tags = memory.tags
    db_memory.source = memory.source
    db.commit()
    db.refresh(db_memory)
    return db_memory

@router.delete("/memories/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_memory = db.query(models.Memory).filter(models.Memory.id == memory_id, models.Memory.user_id == current_user.id).first()
    if db_memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")

    db.delete(db_memory)
    db.commit()
    return {"message": "Memory deleted successfully"}
