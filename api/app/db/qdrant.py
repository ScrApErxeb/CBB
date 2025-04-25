from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient(host="qdrant", port=6333)  # en docker

# Créer la collection (à faire une seule fois)

'''client.recreate_collection(
    collection_name="emails",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # taille selon modèle
)
'''