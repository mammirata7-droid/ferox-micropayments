"""Lightning Network integration via LNbits."""
import httpx
from config import get_settings


async def create_lnbits_invoice(amount_sats: int, memo: str = "Ferox micropayment") -> str | None:
    """
    Create a real Lightning invoice via LNbits.
    Returns the invoice string (lnbc...) or None on failure.
    """
    settings = get_settings()
    if not settings.lnbits_enabled or not settings.lnbits_api_key:
        return None

    url = f"{settings.lnbits_url.rstrip('/')}/api/v1/payments"
    headers = {"X-Api-Key": settings.lnbits_api_key, "Content-Type": "application/json"}
    payload = {"out": False, "amount": amount_sats, "memo": memo[:200]}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data.get("payment_request")
    except Exception:
        return None


async def check_lnbits_payment(payment_hash: str) -> bool:
    """Check if an LNbits payment is paid."""
    settings = get_settings()
    if not settings.lnbits_enabled or not settings.lnbits_api_key:
        return False

    url = f"{settings.lnbits_url.rstrip('/')}/api/v1/payments/{payment_hash}"
    headers = {"X-Api-Key": settings.lnbits_api_key}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data.get("paid", False)
    except Exception:
        return False
