# app/memory/crud.py

from sqlalchemy.orm import Session
from app.memory import models, schemas

def create_memory(db: Session, memory: schemas.MemoryCreate, user_id: int):
    db_memory = models.Memory(content=memory.content, tags=memory.tags, source=memory.source, user_id=user_id)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

def get_memory(db: Session, memory_id: int, user_id: int):
    return db.query(models.Memory).filter(models.Memory.id == memory_id, models.Memory.user_id == user_id).first()

def get_memories(db: Session, user_id: int):
    return db.query(models.Memory).filter(models.Memory.user_id == user_id).all()

def update_memory(db: Session, memory_id: int, memory: schemas.MemoryCreate, user_id: int):
    db_memory = db.query(models.Memory).filter(models.Memory.id == memory_id, models.Memory.user_id == user_id).first()
    if db_memory:
        db_memory.content = memory.content
        db_memory.tags = memory.tags
        db_memory.source = memory.source
        db.commit()
        db.refresh(db_memory)
    return db_memory

def delete_memory(db: Session, memory_id: int, user_id: int):
    db_memory = db.query(models.Memory).filter(models.Memory.id == memory_id, models.Memory.user_id == user_id).first()
    if db_memory:
        db.delete(db_memory)
        db.commit()
    return db_memory
