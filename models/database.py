"""Database models and setup."""
import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()

IN_MEMORY_URL = "sqlite+aiosqlite:///file::memory:?cache=shared"


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String(64), primary_key=True)
    agent_id = Column(String(128), nullable=False, index=True)
    amount_sats = Column(Integer, nullable=False)
    status = Column(String(32), default="pending")
    invoice = Column(Text, nullable=True)
    reference = Column(String(256), nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)
    callback_url = Column(String(512), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AgentBalance(Base):
    __tablename__ = "agent_balances"
    
    agent_id = Column(String(128), primary_key=True)
    balance_sats = Column(Integer, default=0)
    total_paid_sats = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UsageLog(Base):
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String(128), nullable=False, index=True)
    service = Column(String(64), nullable=False)
    units = Column(Integer, default=1)
    amount_sats = Column(Integer, nullable=False)
    payment_id = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


async def init_db(database_url: str):
    """Create tables. Ensures parent dir exists for file-based SQLite."""
    # Ensure parent directory exists for file-based DB (e.g. /data/ferox.db -> /data)
    if database_url.startswith("sqlite") and ":memory:" not in database_url and "memory" not in database_url:
        try:
            # Extract path from sqlite+aiosqlite:///path or sqlite+aiosqlite:////abs/path
            parts = database_url.split("///", 1)
            if len(parts) == 2:
                path = parts[1].split("?")[0]  # strip query params
                parent = os.path.dirname(path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
        except Exception:
            pass  # ignore; SQLite will raise if it can't create
    # StaticPool for in-memory SQLite - keeps single connection, avoids DB destruction on request end
    poolclass = StaticPool if ":memory:" in database_url or "memory" in database_url else None
    pool_kw = {"poolclass": poolclass} if poolclass else {}
    engine = create_async_engine(database_url, echo=False, **pool_kw)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


def get_session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
