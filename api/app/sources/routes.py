from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.memory.models import Memory
from app.sources.gmail import fetch_recent_emails
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter()

@router.post("/import/gmail")
def import_gmail_emails(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    snippets = fetch_recent_emails()
    for snippet in snippets:
        new_memory = Memory(
            content=snippet,
            tags=["email"],
            source="email",
            user_id=current_user.id
        )
        db.add(new_memory)
    db.commit()
    return {"message": f"{len(snippets)} emails imported."}
