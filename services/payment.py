"""Payment service - invoice creation, status, Lightning via LNbits."""
import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from models.database import Payment
from models.schemas import PaymentStatus
from services.lightning import create_lnbits_invoice


async def create_payment(
    db: AsyncSession,
    amount_sats: int,
    agent_id: str,
    reference: str | None = None,
    callback_url: str | None = None,
    metadata: dict | None = None,
) -> Payment:
    """Create a new payment record and generate invoice (LNbits or mock)."""
    settings = get_settings()
    payment_id = f"ferox_{uuid.uuid4().hex[:16]}"
    expires_at = datetime.utcnow() + timedelta(hours=1)

    memo = f"Ferox {payment_id}" + (f" - {reference}" if reference else "")
    invoice = await create_lnbits_invoice(amount_sats, memo)
    if not invoice:
        invoice = f"lnbc{amount_sats}n1mock_invoice_for_ferox_{payment_id}"
    
    payment = Payment(
        id=payment_id,
        agent_id=agent_id,
        amount_sats=amount_sats,
        status=PaymentStatus.PENDING,
        invoice=invoice,
        reference=reference,
        metadata_=metadata,
        callback_url=callback_url,
        expires_at=expires_at,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def get_payment(db: AsyncSession, payment_id: str) -> Payment | None:
    """Get payment by ID."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def mark_paid(db: AsyncSession, payment_id: str) -> bool:
    """Mark payment as completed (called by webhook or polling)."""
    payment = await get_payment(db, payment_id)
    if not payment or payment.status != PaymentStatus.PENDING:
        return False
    payment.status = PaymentStatus.COMPLETED
    payment.paid_at = datetime.utcnow()
    await db.commit()
    return True
