# Ferox Micropayments – Setup Guide

API for AI agents to pay you in micropayments (Lightning/sats).

## Quick Start

```bash
cd /home/mauricio/agents/playground/ferox-micropayments
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000/docs** for the API docs.

## API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/pay` | POST | Create micropayment, get invoice |
| `/v1/pay/{id}` | GET | Check payment status |
| `/v1/pay/{id}/confirm` | POST | Confirm payment (testing) |
| `/v1/health` | GET | Health check |

## Create a Payment (AI Agent Flow)

```bash
curl -X POST http://127.0.0.1:8000/v1/pay \
  -H "Content-Type: application/json" \
  -H "X-Ferox-API-Key: change-me-in-production" \
  -d '{
    "amount_sats": 100,
    "agent_id": "agent-abc-123",
    "reference": "api-call-001",
    "metadata": {"service": "image-gen"}
  }'
```

Response includes `payment_id`, `invoice` (Lightning), `status`, `expires_at`.

## Payment Flow

1. **Agent** calls `POST /v1/pay` → receives invoice
2. **Agent** (or user) pays the Lightning invoice
3. **Webhook** (or polling) confirms payment → `POST /v1/pay/{id}/confirm`
4. **Agent** checks `GET /v1/pay/{id}` until `status: completed`

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `FEROX_API_SECRET` | API key for merchant auth (required in prod) |
| `FEROX_DATABASE_URL` | SQLite by default |
| `FEROX_LIGHTNING_*` | Lightning node (optional) |

## Lightning Integration (LNbits)

To accept real Lightning payments:

1. Get a free wallet at **https://legend.lnbits.com**
2. Create wallet, copy the **Invoice/Payment** API key
3. Add to `.env`:
   ```
   FEROX_LNBITS_ENABLED=true
   FEROX_LNBITS_URL=https://legend.lnbits.com
   FEROX_LNBITS_API_KEY=your-invoice-key
   ```
4. Restart the app. New payments will create real Lightning invoices.

## Deployment

- **Railway**: Connect GitHub, add `FEROX_API_SECRET`, deploy
- **Render**: Uses `render.yaml`, add env vars in dashboard
- **Fly.io**: `fly launch`, `fly secrets set FEROX_API_SECRET=...`, `fly deploy`

See `YOUR_TASKS.md` for step-by-step instructions.
