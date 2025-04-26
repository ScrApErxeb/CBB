from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from init_db import init_db  # ta fonction que tu créeras

from app.auth.routes import router as auth_router
from app.memory.routes import router as memory_router
from app.sources.routes import router as sources_router

app = FastAPI(
    title="IA Perso API",
    description="Backend de l'assistant IA personnel 🧠",
    version="0.1.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à sécuriser en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(memory_router, prefix="", tags=["Memory"])
app.include_router(sources_router, prefix="/sources", tags=["Sources"])

# Init DB
init_db()


from app.vector.qdrant_utils import init_qdrant_collections

init_qdrant_collections()