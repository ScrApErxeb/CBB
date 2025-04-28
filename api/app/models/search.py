from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class Search(Base):
    __tablename__ = 'search_queries'

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)  # Terme de la recherche
    user_id = Column(Integer, ForeignKey('users.id'))  # L'ID de l'utilisateur
    timestamp = Column(DateTime, default=datetime.utcnow)  # Date de la recherche

    user = relationship('User', back_populates='search_queries')  # Relation avec la table 'User'
