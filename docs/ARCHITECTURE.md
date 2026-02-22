# Ferox Micropayments — Technical Architecture

## Overview

Ferox is a REST API that enables AI agents to pay for services in micropayments using the Bitcoin Lightning Network. It acts as a payment gateway between AI agents (clients) and service providers (merchants).

---

## System Architecture

```
┌─────────────────┐     HTTPS      ┌──────────────────────┐     Lightning     ┌─────────────┐
│   AI Agent      │ ──────────────►│  Ferox API           │ ◄───────────────► │  LNbits     │
│   (Client)      │  POST /v1/pay  │  (FastAPI)           │  Invoice/Pay     │  (Optional) │
└─────────────────┘                └──────────┬───────────┘                  └─────────────┘
                                              │
                                              │ SQLite
                                              ▼
                                     ┌───────────────────┐
                                     │  Database         │
                                     │  (payments, etc.)  │
                                     └───────────────────┘
```

---

## Components

### 1. API Layer (`main.py`, `api/routes.py`)

- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)
- **Auth:** API key via `X-Ferox-API-Key` header
- **Endpoints:**
  - `POST /v1/pay` — Create micropayment, returns Lightning invoice
  - `GET /v1/pay/{id}` — Check payment status
  - `POST /v1/pay/{id}/confirm` — Manually confirm (testing/webhook)
  - `GET /v1/health` — Health check

### 2. Service Layer (`services/`)

| Service      | Responsibility                          |
|-------------|------------------------------------------|
| `payment.py`| Create payments, status, mark paid       |
| `lightning.py` | LNbits integration for real invoices   |

### 3. Data Layer (`models/`)

| Model         | Purpose                                      |
|---------------|----------------------------------------------|
| `Payment`     | Invoice, amount, status, agent_id, metadata  |
| `AgentBalance`| Per-agent balance (for metered usage)        |
| `UsageLog`    | Usage records for metering                   |

### 4. Configuration (`config.py`)

- **Settings:** Pydantic Settings from env vars
- **Prefix:** `FEROX_`
- **Database:** SQLite (file or in-memory); auto-detects Railway volume
- **Lightning:** LNbits URL + API key when enabled

---

## Data Flow

### Create Payment

1. Agent sends `POST /v1/pay` with `amount_sats`, `agent_id`, optional `reference`, `callback_url`, `metadata`
2. API validates request and checks API key
3. Payment service generates Lightning invoice (LNbits or mock)
4. Payment record is stored in DB
5. Response returns `payment_id`, `invoice`, `status`, `expires_at`

### Confirm Payment

1. **Production:** LNbits webhook notifies Ferox when invoice is paid
2. **Testing:** Agent calls `POST /v1/pay/{id}/confirm`
3. Payment status updated to `completed`, `paid_at` set

---

## Technology Stack

| Layer    | Technology                    |
|----------|-------------------------------|
| Runtime  | Python 3.12                   |
| API      | FastAPI, Uvicorn              |
| Database | SQLite + aiosqlite + SQLAlchemy 2.0 |
| Payments | LNbits (Lightning)            |
| Config   | Pydantic Settings              |
| HTTP     | httpx (async)                 |

---

## Deployment

- **Container:** Docker (Python 3.12-slim)
- **Platforms:** Railway, Render, Fly.io
- **Database:** In-memory by default; file-based when `RAILWAY_VOLUME_MOUNT_PATH` or `FEROX_DATABASE_URL` is set
- **Port:** Read from `PORT` env (Railway/Render)

---

## Security

- API key required for all payment endpoints
- No authentication for `/` and `/v1/health`
- Secret stored in env (`FEROX_API_SECRET`), never in code

---

## Extensibility

- **Webhook:** `FEROX_WEBHOOK_URL` for payment confirmation callbacks
- **LNbits:** Swap URL/API key for different Lightning backends
- **Database:** Override `FEROX_DATABASE_URL` for PostgreSQL, etc.
