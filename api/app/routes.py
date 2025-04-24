from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Interaction, Base
from app.database import engine, SessionLocal


router = APIRouter()

# Créer la base si elle n'existe pas
Base.metadata.create_all(bind=engine)

# Dépendance pour DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/interactions")
def create_interaction(interaction: dict, db: Session = Depends(get_db)):
    new_interaction = Interaction(
        nom_personne=interaction["nom_personne"],
        type=interaction["type"],
        source=interaction["source"],
        timestamp=datetime.fromisoformat(interaction["timestamp"])
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return {"message": "Interaction enregistrée", "data": interaction}

@router.get("/last-interaction/{nom_personne}")
def get_last_interaction(nom_personne: str, db: Session = Depends(get_db)):
    interaction = db.query(Interaction)\
        .filter(Interaction.nom_personne.ilike(nom_personne))\
        .order_by(Interaction.timestamp.desc())\
        .first()
    if interaction:
        return {
            "nom_personne": interaction.nom_personne,
            "type": interaction.type,
            "source": interaction.source,
            "timestamp": interaction.timestamp.isoformat()
        }
    return {"message": f"Aucune interaction trouvée avec {nom_personne}"}
