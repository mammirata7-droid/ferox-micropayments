#!/bin/bash
# Run Ferox Micropayments API
cd "$(dirname "$0")"
[ -d .venv ] && source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
