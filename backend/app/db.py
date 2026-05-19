from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# --------------------------------------------------------------------------- #
# Engine
# --------------------------------------------------------------------------- #
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,               # set True for debugging
    future=True,
)

# --------------------------------------------------------------------------- #
# Session factory
# --------------------------------------------------------------------------- #
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --------------------------------------------------------------------------- #
# Base class for models
# --------------------------------------------------------------------------- #
Base = declarative_base()

# --------------------------------------------------------------------------- #
# Dependency for route handlers
# --------------------------------------------------------------------------- #
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session