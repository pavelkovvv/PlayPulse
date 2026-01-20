import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# --- Импорт базы и моделей ---
from src.database import Base, SQLALCHEMY_DATABASE_URI  # noqa
from src.models import *  # noqa

# Alembic Config
config = context.config

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata для autogenerate
target_metadata = Base.metadata


def get_sync_url(async_url: str) -> str:
    """
    Alembic работает с sync URL,
    поэтому убираем +asyncpg
    """
    if async_url.startswith("postgresql+asyncpg://"):
        return async_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return async_url


def run_migrations_online() -> None:
    sync_url = get_sync_url(SQLALCHEMY_DATABASE_URI)

    connectable = create_async_engine(
        SQLALCHEMY_DATABASE_URI,
        poolclass=pool.NullPool,
    )

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    def do_run_migrations(connection) -> None:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    raise RuntimeError("Offline migrations are not supported with async engine")
else:
    run_migrations_online()
