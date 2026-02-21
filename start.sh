#!/bin/sh
# Start Ferox - uses PORT from Railway/Render/Fly if set
PORT=${PORT:-8000}
exec uvicorn main:app --host 0.0.0.0 --port $PORT
