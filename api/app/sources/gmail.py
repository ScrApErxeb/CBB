import os
from datetime import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from app.db.session import SessionLocal
from app.db.models import Email
from app.vector.embedding import get_embedding
from app.vector.qdrant_utils import upsert_email_vector

# ✉️ Portée Gmail minimale pour lire les mails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 📍 Chemin vers les fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "..", "credentials", "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "..", "credentials", "token.json")


def get_gmail_service():
    creds = None

    if not os.path.exists(TOKEN_PATH):
        if not os.path.exists(CREDENTIALS_PATH):
            raise FileNotFoundError(f"Fichier credentials.json introuvable à : {CREDENTIALS_PATH}")

        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    else:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)

                with open(TOKEN_PATH, "w") as token_file:
                    token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def fetch_recent_emails(max_results=5):
    service = get_gmail_service()
    db = SessionLocal()

    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    new_emails = []
    for msg in messages:
        msg_id = msg['id']

        if db.query(Email).filter(Email.id == msg_id).first():
            continue

        msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
        snippet = msg_data.get('snippet')
        internal_date = int(msg_data.get('internalDate', 0)) / 1000

        if snippet:
            email = Email(
                id=msg_id,
                snippet=snippet,
                internal_date=datetime.fromtimestamp(internal_date)
            )
            db.add(email)

            # 🚀 Embedding + Qdrant
            embedding = get_embedding(snippet)
            upsert_email_vector(
                email_id=msg_id,
                embedding=embedding.tolist(),
                internal_date=datetime.fromtimestamp(internal_date).isoformat()
            )

            new_emails.append(snippet)

    db.commit()
    db.close()

    return new_emails

def fetch_all_emails(max_results=100):
    service = get_gmail_service()
    db = SessionLocal()

    page_token = None
    emails = []

    while True:
        results = service.users().messages().list(userId='me', maxResults=max_results, pageToken=page_token).execute()
        messages = results.get('messages', [])

        for msg in messages:
            msg_id = msg['id']
            if db.query(Email).filter(Email.id == msg_id).first():
                continue

            msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
            snippet = msg_data.get('snippet')
            internal_date = int(msg_data.get('internalDate', 0)) / 1000

            if snippet:
                email = Email(
                    id=msg_id,
                    snippet=snippet,
                    internal_date=datetime.fromtimestamp(internal_date)
                )
                db.add(email)
                
                # 🚀 Embedding + Qdrant
                embedding = get_embedding(snippet)
                upsert_email_vector(
                    email_id=msg_id,
                    embedding=embedding.tolist(),
                    internal_date=datetime.fromtimestamp(internal_date).isoformat()
                )

                emails.append(snippet)

        page_token = results.get('nextPageToken')

        if not page_token:
            break

    db.commit()
    db.close()

    return emails


if __name__ == "__main__":
    emails = fetch_all_emails()
    for i, email in enumerate(emails, 1):
        print(f"\n--- Email {i} ---\n{email}")
