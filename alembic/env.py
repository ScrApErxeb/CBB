from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import os
import sys

# Ajouter le chemin vers le dossier contenant `app`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))

# Importer la Base SQLAlchemy et les modèles
from api.app.db.session import Base  # ta Base declarative
from api.app.db import models  # important pour que Alembic voie les modèles

# Config Alembic
config = context.config

# Interprète le fichier .ini si nécessaire
fileConfig(config.config_file_name)

# Cible de migration
target_metadata = Base.metadata


def run_migrations_offline():
    """Migrations en mode 'offline' (génère SQL mais n'exécute pas)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # compare aussi les types SQL
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Migrations en mode 'online' (se connecte à la DB et exécute)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # compare aussi les types SQL
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
