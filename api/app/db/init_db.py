from db.session import engine
from db.models import Base

if __name__ == "__main__":
    print("📦 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès.")
