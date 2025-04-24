from app.database import engine
from app.models import Base

# Crée toutes les tables définies dans `Base`
Base.metadata.create_all(bind=engine)
