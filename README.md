# Ferox Micropayments

API for AI agents to pay you in micropayments (Lightning/sats).

## Quick Start

```bash
cd ferox-micropayments
source .venv/bin/activate
pip install -r requirements.txt  # if not done
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**API docs:** http://127.0.0.1:8000/docs

## Create a Payment

```bash
curl -X POST http://127.0.0.1:8000/v1/pay \
  -H "Content-Type: application/json" \
  -H "X-Ferox-API-Key: change-me-in-production" \
  -d '{"amount_sats": 100, "agent_id": "my-agent", "reference": "api-call-001"}'
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/pay` | POST | Create micropayment, get invoice |
| `/v1/pay/{id}` | GET | Check payment status |
| `/v1/pay/{id}/confirm` | POST | Confirm payment (testing) |
| `/v1/health` | GET | Health check |

## Next Steps

- [ ] Real Lightning invoices (LND/CLN)
- [ ] Agent wallets / prepaid balance
- [ ] Usage metering
- [ ] Webhook for payment confirmation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for full documentation.
