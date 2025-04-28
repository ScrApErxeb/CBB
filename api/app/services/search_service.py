from app.models import Search, User
from app.db.session import SessionLocal
from app.sources.internet.ddg import ddg_search
from app.vector.qdrant_utils import upsert_search_results
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import uuid  # Importer la librairie UUID

def search_and_store(query: str, user_id: str):
    """
    Effectue la recherche, enregistre la recherche dans PostgreSQL
    et envoie les résultats dans Qdrant.
    """
    # Créer une session DB
    with SessionLocal() as db:  # Utilisation d'un gestionnaire de contexte pour gérer la session
        try:
            # Convertir user_id en UUID si c'est un string
            if isinstance(user_id, int):
                user_id = uuid.UUID(user_id)  # Convertir en UUID si nécessaire
            
            # Rechercher l'utilisateur dans la base de données
            user = db.query(User).filter(User.id == user_id).one()  # Trouver l'utilisateur par son UUID

            # Créer une entrée pour la recherche dans PostgreSQL
            search_query = Search(query=query, user_id=user.id)  # Utiliser la classe Search et non la fonction search
            db.add(search_query)
            db.commit()
            db.refresh(search_query)  # Récupérer l'ID de la recherche

            # Effectuer la recherche sur Internet (par exemple avec DuckDuckGo)
            results = ddg_search(query)
            
            # Insérer les résultats dans Qdrant
            upsert_search_results(search_query.id, results)
            
            return results

        except NoResultFound:
            raise Exception(f"L'utilisateur avec ID {user_id} n'existe pas.")
        except Exception as e:
            db.rollback()  # Rollback si une exception survient
            raise Exception(f"Erreur lors de la recherche ou de l'insertion : {str(e)}")
