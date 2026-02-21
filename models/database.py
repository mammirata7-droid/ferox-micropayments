"""Database models and setup."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

Base = declarative_base()


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
    """Create tables."""
    engine = create_async_engine(database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


def get_session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
