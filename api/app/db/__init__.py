# app/db/__init__.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()


# Charger les paramètres de configuration (tu pourrais utiliser un fichier config.py ou un .env)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ia_db")

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True pour afficher les requêtes SQL dans la console

# Créer la session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour nos modèles
Base = declarative_base()

# ✅ Fonction d'initialisation de la BDD
def init_db():
    from app.db.models import Base  # Import ici pour éviter les imports circulaires
    Base.metadata.create_all(bind=engine)
