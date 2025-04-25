# app/vector/qdrant_utils.py

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Charger les variables d'environnement
load_dotenv()

# Connexion dynamique au client Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url=QDRANT_URL)



import uuid

def upsert_email_vector(email_id: str, embedding: list, internal_date: str):
    # Convertir email_id en UUID valide
    try:
        email_uuid = uuid.UUID(email_id)  # Si email_id est déjà un UUID valide
    except ValueError:
        email_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, email_id)  # Générer un UUID à partir de l'ID d'email

    client.upsert(
        collection_name="emails",
        points=[
            {
                "id": str(email_uuid),  # Convertir en string UUID
                "vector": embedding,
                "payload": {
                    "email_id": email_id,
                    "internal_date": internal_date
                }
            }
        ]
    )
