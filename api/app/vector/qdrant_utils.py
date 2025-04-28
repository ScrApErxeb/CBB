# app/vector/qdrant_utils.py

import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from app.vector.embedding import get_embedding  # Assurez-vous que le chemin d'importation est correct

# Charger les variables d'environnement
load_dotenv()

# Connexion au client Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL = os.getenv("QDRANT_URL", f"http://{QDRANT_HOST}:{QDRANT_PORT}")

client = QdrantClient(url=QDRANT_URL)

# -----------------------------------
# Pour EMAILS
# -----------------------------------

def upsert_email_vector(email_id: str, embedding: list, internal_date: str):
    # Convertir email_id en UUID valide
    try:
        email_uuid = uuid.UUID(email_id)  # Si email_id est déjà un UUID
    except ValueError:
        email_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, email_id)  # Générer un UUID à partir de l'email_id

    client.upsert(
        collection_name="emails",
        points=[
            {
                "id": str(email_uuid),
                "vector": embedding,
                "payload": {
                    "email_id": email_id,
                    "internal_date": internal_date
                }
            }
        ]
    )

# -----------------------------------
# Pour DOCUMENTS LOCAUX
# -----------------------------------

import uuid
from app.vector.embedding import get_embedding

def upsert_local_document(user_id: str, text: str, filename: str):
    embedding = get_embedding(text)
    point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{user_id}:{filename}"))

    client.upsert(
        collection_name="local_documents",
        points=[
            {
                "id": point_id,
                "vector": embedding,
                "payload": {
                    "user_id": user_id,
                    "filename": filename,
                    "text": text[:5000]  # (optionnel) tronquer le texte
                }
            }
        ]
    )


from qdrant_client.models import PointStruct
import numpy as np


from app.vector.embedding import get_embedding

def upsert_search_results(search_id: int, results: list):
    points = []
    
    for result in results:
        title = result.get('title')
        description = result.get('description')
        
        if not title or not description:
            continue  # Ne pas traiter si manque title/description
        
        # Création du texte complet pour embedding
        text_to_embed = f"{title}\n{description}"
        vector = get_embedding(text_to_embed)  # 🚀 Vrai embedding ici !

        # Générer un UUID valide pour chaque point
        point_id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{search_id}_{title}")

        # Ajouter le point
        points.append(PointStruct(
            id=str(point_id),  # Utiliser UUID valide
            vector=vector,
            payload={
                'search_id': search_id,
                'title': title,
                'description': description
            }
        ))
    
    if points:
        try:
            print(f"Inserting {len(points)} points into Qdrant")
            client.upsert(collection_name='search_results', points=points)
        except Exception as e:
            print(f"Error during upsert: {e}")




from qdrant_client.models import Distance, VectorParams

def init_qdrant_collections():
    """if not client.collection_exists("search_results"):
        client.recreate_collection(
            collection_name="search_results",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )"""
    pass

