import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

load_dotenv(dotenv_path="/app/.env")

# 🔧 Patch the config to use DATABASE_URL from the environment
database_url = os.getenv("DATABASE_URL")
if database_url:
    config = context.config
    config.set_main_option("sqlalchemy.url", database_url)
else:
    raise RuntimeError("DATABASE_URL not set in environment.")

# ✅ Log debug info to inspect what's really used
print("ENV_DUMP_START")
print("DATABASE_URL =", os.getenv("DATABASE_URL"))
print("sqlalchemy.url =", config.get_main_option("sqlalchemy.url"))
print("ENV_DUMP_END")

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Import models and metadata
from src.core.data.models import Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
