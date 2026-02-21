"""Railway-friendly startup: reads PORT from env (no shell expansion issues)."""
import os
import uvicorn

port = int(os.environ.get("PORT", 8000))
uvicorn.run("main:app", host="0.0.0.0", port=port)
