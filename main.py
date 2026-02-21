"""Ferox Micropayments - API for AI agents to pay you."""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import get_settings
from models.database import init_db, get_session_factory
from deps import get_db, SessionLocal
from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB. Shutdown: cleanup."""
    import deps
    settings = get_settings()
    engine = await init_db(settings.database_url)
    deps.SessionLocal = get_session_factory(engine)
    yield
    await engine.dispose()


app = FastAPI(
    title="Ferox Micropayments",
    description="API for AI agents to pay you in micropayments (Lightning/sats)",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "service": "Ferox Micropayments",
        "docs": "/docs",
        "health": "/v1/health",
        "create_payment": "POST /v1/pay",
    }
