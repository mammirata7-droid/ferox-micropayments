"""API routes for Ferox micropayments."""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from models.schemas import PaymentRequest, InvoiceResponse, PaymentStatusResponse, PaymentStatus
from models.database import Payment
from services.payment import create_payment, get_payment, mark_paid
from deps import get_db

router = APIRouter(prefix="/v1", tags=["payments"])


def verify_api_key(x_ferox_api_key: str | None = Header(None, alias="X-Ferox-API-Key")):
    """Verify API key for merchant/recipient auth."""
    settings = get_settings()
    # In dev, allow no key if api_secret is default
    if settings.api_secret != "change-me-in-production" and x_ferox_api_key != settings.api_secret:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True


@router.post("/pay", response_model=InvoiceResponse)
async def create_micropayment(
    req: PaymentRequest,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_api_key),
):
    """
    Create a micropayment. Returns an invoice (Lightning) or payment address.
    AI agents call this to pay for services.
    """
    payment = await create_payment(
        db=db,
        amount_sats=req.amount_sats,
        agent_id=req.agent_id,
        reference=req.reference,
        callback_url=req.callback_url,
        metadata=req.metadata,
    )
    
    return InvoiceResponse(
        payment_id=payment.id,
        invoice=payment.invoice,
        amount_sats=payment.amount_sats,
        status=PaymentStatus(payment.status),
        expires_at=payment.expires_at,
        created_at=payment.created_at,
    )


@router.get("/pay/{payment_id}", response_model=PaymentStatusResponse)
async def get_payment_status(
    payment_id: str,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_api_key),
):
    """Check payment status. Agents poll this to confirm payment."""
    
    payment = await get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return PaymentStatusResponse(
        payment_id=payment.id,
        status=PaymentStatus(payment.status),
        amount_sats=payment.amount_sats,
        paid_at=payment.paid_at,
        created_at=payment.created_at,
    )


@router.post("/pay/{payment_id}/confirm")
async def confirm_payment(
    payment_id: str,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_api_key),
):
    """
    Manually confirm a payment (for testing / webhook simulation).
    In production, Lightning node sends webhook on payment.
    """
    
    ok = await mark_paid(db, payment_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Payment not found or already completed")
    return {"status": "confirmed"}


@router.get("/health")
async def health():
    """Health check for load balancers."""
    return {"status": "ok", "service": "ferox-micropayments"}
