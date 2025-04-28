from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    nom_personne = Column(String, index=True)
    type = Column(String)  # appel, message, etc.
    source = Column(String)  # WhatsApp, Téléphone, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
