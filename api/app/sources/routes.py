# app/routes/sources_routes.py
from fastapi import APIRouter, Depends
from app.sources.gmail import fetch_recent_emails, fetch_all_emails, fetch_single_email
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/collect_emails")
def collect_emails_route(user=Depends(get_current_user)):
    try:
        emails = fetch_recent_emails()
        return {"message": f"{len(emails)} nouveaux emails collectés.", "emails": emails}
    except Exception as e:
        return {"message": str(e)}

@router.get("/collect_all_emails")
def collect_all_emails_route(user=Depends(get_current_user)):
    try:
        emails = fetch_all_emails()
        return {"message": f"{len(emails)} emails collectés.", "emails": emails}
    except Exception as e:
        return {"message": str(e)}

@router.get("/mail_test")
def mail_test(user=Depends(get_current_user)):
    try:
        snippet, sender = fetch_single_email()
        if snippet and sender:
            return {"message": "Test d'email réussi.", "email": snippet, "sender": sender}
        else:
            return {"message": "Aucun email trouvé ou une erreur s'est produite."}
    except Exception as e:
        return {"message": str(e)}



# app/sources/routes.py
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pathlib import Path
import tempfile

from app.auth.dependencies import get_current_user
from app.sources.local_files import file_service


from app.db.database import get_db  # <-- pense à bien avoir ce import
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

