"""Ferox Micropayments configuration."""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


def _default_database_url() -> str:
    """Use Railway volume if mounted, else in-memory.
    If volume path fails at startup, main.py falls back to in-memory.
    """
    mount = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "").strip()
    if mount:
        path = mount.rstrip("/") + "/ferox.db"
        return f"sqlite+aiosqlite:///{path}"
    return "sqlite+aiosqlite:///file::memory:?cache=shared"


class Settings(BaseSettings):
    """App settings from env vars."""
    app_name: str = "Ferox Micropayments"
    debug: bool = False
    
    # API
    api_key_header: str = "X-Ferox-API-Key"
    api_secret: str = "change-me-in-production"
    
    # Database (Railway volume or in-memory; FEROX_DATABASE_URL overrides)
    database_url: str = ""
    
    # Payment backends - LNbits (easy Lightning)
    lnbits_enabled: bool = False
    lnbits_url: str = "https://legend.lnbits.com"
    lnbits_api_key: str = ""
    
    # Webhook for payment confirmation
    webhook_url: str | None = None
    
    class Config:
        env_file = ".env"
        env_prefix = "FEROX_"


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if not s.database_url:
        s = s.model_copy(update={"database_url": _default_database_url()})
    return s
