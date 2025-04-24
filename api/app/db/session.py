from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://user:password@localhost:5432/ia_db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/ia_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()  # Cette ligne définit Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()