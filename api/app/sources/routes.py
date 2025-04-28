# app/routes/sources_routes.py
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, HTTPException
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




from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.auth.dependencies import get_current_user  # Si tu as de l'auth
from app.db.crud_search import save_search
from app.vector.qdrant_utils import upsert_search_results
from app.models.user import User
from app.sources.internet.ddg import ddg_search
from app.sources.internet.schemas import SearchResponse

@router.get("/search/ddg", response_model=SearchResponse)
async def search_ddg(
    query: str = Query(..., description="Terme à rechercher sur DuckDuckGo"),
    max_results: int = Query(10, ge=1, le=50, description="Nombre maximum de résultats"),
    region: str = Query('fr-fr', description="Région pour la recherche (ex: 'fr-fr', 'us-en')"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Rechercher sur DuckDuckGo, sauvegarder la recherche, et stocker les résultats dans Qdrant.
    """
    # 1. Sauvegarder la recherche dans PostgreSQL
    search = save_search(db, user_id=current_user.id, query=query)

    # 2. Rechercher sur DuckDuckGo
    results = ddg_search(query, region=region, max_results=max_results)

    # 3. Sauvegarder les résultats dans Qdrant
    upsert_search_results(search_id=search.id, results=results)

    return {"query": query, "results": results}
