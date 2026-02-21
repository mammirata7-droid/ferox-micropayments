"""Pydantic schemas for Ferox API."""
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class PaymentRequest(BaseModel):
    """Request to create a micropayment."""
    amount_sats: int = Field(..., ge=1, le=1_000_000, description="Amount in satoshis (1 sat = 0.00000001 BTC)")
    agent_id: str = Field(..., min_length=1, max_length=128, description="Unique identifier for the paying agent")
    reference: str | None = Field(None, max_length=256, description="Optional reference for the payment")
    callback_url: str | None = Field(None, description="URL to notify when payment completes")
    metadata: dict | None = Field(None, description="Optional metadata for the payment")


class InvoiceResponse(BaseModel):
    """Response with payment invoice / details."""
    payment_id: str
    invoice: str | None = None  # Lightning invoice string, or payment address
    amount_sats: int
    status: PaymentStatus
    expires_at: datetime | None = None
    created_at: datetime


class PaymentStatusResponse(BaseModel):
    """Payment status check response."""
    payment_id: str
    status: PaymentStatus
    amount_sats: int
    paid_at: datetime | None = None
    created_at: datetime


class AgentWallet(BaseModel):
    """Agent wallet balance (for metered usage)."""
    agent_id: str
    balance_sats: int
    total_paid_sats: int
    created_at: datetime
    updated_at: datetime


class UsageRecord(BaseModel):
    """Record of usage for metering."""
    agent_id: str
    service: str
    units: int
    amount_sats: int
    timestamp: datetime
