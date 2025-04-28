from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

# Prend la valeur depuis .env, avec fallback sur une valeur par défaut (utile en local/dev)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ia_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

