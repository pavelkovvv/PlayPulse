from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool

from settings import config_loader


SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{config_loader('POSTGRES_DB_USER')}:"
    f"{config_loader('POSTGRES_DB_PASSWORD')}@"
    f"{config_loader('POSTGRES_DB_HOST')}:"
    f"{config_loader('POSTGRES_DB_PORT')}/"
    f"{config_loader('POSTGRES_DB_NAME')}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, poolclass=NullPool)

SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass


async def get_obj_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
