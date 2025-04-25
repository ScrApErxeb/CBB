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
