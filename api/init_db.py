# app/db/init_db.py

from app.models.base import Base
from app.db.session import engine
import app.models  # ← pour charger tous les modèles dans SQLAlchemy

def init_db():
    Base.metadata.create_all(bind=engine)
