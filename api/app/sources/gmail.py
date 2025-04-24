import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ✉️ Portée Gmail minimale pour lire les mails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 📍 Chemin vers les fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "..", "credentials", "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "..", "credentials", "token.json")



def get_gmail_service():
    creds = None

    # 🆕 Si l'utilisateur ne s'est jamais authentifié
    if not os.path.exists(TOKEN_PATH):
        if not os.path.exists(CREDENTIALS_PATH):
            raise FileNotFoundError(f"Fichier credentials.json introuvable à : {CREDENTIALS_PATH}")

        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)

        # ✅ Lancement console (pour éviter erreur browser sur serveur)
        creds = flow.run_local_server(port=0)

        # 💾 Enregistrer le token d'authentification
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    else:
        # 🔁 Utiliser le token existant
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # Vérifier si le token est expiré ou invalide
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)

                # 💾 Enregistrer le nouveau token
                with open(TOKEN_PATH, "w") as token_file:
                    token_file.write(creds.to_json())

    # 🔧 Construire le service Gmail
    return build('gmail', 'v1', credentials=creds)




def fetch_recent_emails(max_results=5):
    service = get_gmail_service()

    # 📩 Liste des messages
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data.get('snippet')
        if snippet:
            emails.append(snippet)

    return emails


if __name__ == "__main__":
    emails = fetch_recent_emails()
    for i, email in enumerate(emails, 1):
        print(f"\n--- Email {i} ---\n{email}")
