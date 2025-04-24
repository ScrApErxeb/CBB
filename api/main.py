from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.memory.routes import router as memory_router  # Ou via __init__.py si tu préfères from app.memory import memory_router

app = FastAPI(
    title="IA Perso API",
    description="Backend de l'assistant IA personnel 🧠",
    version="0.1.0"
)

# Configuration CORS (si nécessaire, sinon tu peux supprimer)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Pour dev uniquement, à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(memory_router, prefix="", tags=["Memory"])  # Les routes sont déjà définies avec /memories/ dedans


from app.sources.routes import router as sources_router
app.include_router(sources_router, prefix="/sources", tags=["Sources"])
