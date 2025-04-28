# app/db/crud_search.py

from sqlalchemy.orm import Session
from app.models.search import Search

def save_search(db: Session, user_id: int, query: str) -> Search:
    search = Search(user_id=user_id, query=query)
    db.add(search)
    db.commit()
    db.refresh(search)
    return search
