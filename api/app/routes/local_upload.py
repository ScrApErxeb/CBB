from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pathlib import Path
import tempfile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.services import file_service

router = APIRouter(
    prefix="/sources",
    tags=["Sources"]
)


import uuid

@router.post("/upload")
def upload_local_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Convertir l'id integer en UUID déterministe
        user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(user.id))

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(file.file.read())

        file_service.process_and_upsert(tmp_path, user_id=user_uuid, db=db)

        tmp_path.unlink()

        return {"status": "success", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
