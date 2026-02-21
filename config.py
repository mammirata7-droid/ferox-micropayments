"""Ferox Micropayments configuration."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """App settings from env vars."""
    app_name: str = "Ferox Micropayments"
    debug: bool = False
    
    # API
    api_key_header: str = "X-Ferox-API-Key"
    api_secret: str = "change-me-in-production"
    
    # Database (/tmp is writable on Railway; override with FEROX_DATABASE_URL for local)
    database_url: str = "sqlite+aiosqlite:////tmp/ferox.db"
    
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
    return Settings()
