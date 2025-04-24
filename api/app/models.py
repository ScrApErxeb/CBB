from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship


Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    nom_personne = Column(String, index=True)
    type = Column(String)  # appel, message, etc.
    source = Column(String)  # WhatsApp, Téléphone, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)


from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    memories = relationship("Memory", back_populates="user", cascade="all, delete-orphan")


