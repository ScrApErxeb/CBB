from db.session import engine
from models.base import Base
import app.models  # <-- nécessaire pour tout charger

if __name__ == "__main__":
    print("📦 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès.")
