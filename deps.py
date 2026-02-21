"""Dependencies for FastAPI."""
from sqlalchemy.ext.asyncio import AsyncSession

# SessionLocal is set in main at startup
SessionLocal = None


async def get_db():
    """Yield DB session."""
    async with SessionLocal() as session:
        yield session
