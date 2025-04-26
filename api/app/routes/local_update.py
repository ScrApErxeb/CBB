from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pathlib import Path
import tempfile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.services import file_service

router = APIRouter(
    prefix="/sources",
    tags=["Sources"]
)

@router.post("/upload")
def upload_local_file(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(SessionLocal)
):
    try:
        # Sauver temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(file.file.read())
        
        # Process + Qdrant + save historique
        file_service.process_and_upsert(tmp_path, user_id=user_id, db=db)

        # Nettoyer fichier temporaire
        tmp_path.unlink()

        return {"status": "success", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
