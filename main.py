"""Ferox Micropayments - API for AI agents to pay you."""
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import get_settings
from models.database import init_db, get_session_factory
from deps import get_db, SessionLocal
from api.routes import router

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB. Shutdown: cleanup."""
    import deps
    log.info("Starting Ferox Micropayments (PORT=%s)", os.environ.get("PORT", "8000"))
    try:
        settings = get_settings()
        engine = await init_db(settings.database_url)
        deps.SessionLocal = get_session_factory(engine)
        log.info("Database initialized")
    except Exception as e:
        log.exception("Startup failed: %s", e)
        raise
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
    """Root - redirects to docs for browsers."""
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Ferox Micropayments</title></head>
    <body style="font-family:sans-serif; padding:2rem;">
    <h1>Ferox Micropayments</h1>
    <p>API for AI agents to pay you in micropayments.</p>
    <ul>
    <li><a href="/docs">API Docs (Swagger)</a></li>
    <li><a href="/v1/health">Health Check</a></li>
    </ul>
    </body>
    </html>
    """)
