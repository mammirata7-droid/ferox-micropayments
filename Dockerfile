# Ferox Micropayments - production image
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .
RUN chmod +x start.sh

# Run as root (Railway /tmp needs write access; appuser had permission issues)
EXPOSE 8000

# Python reads PORT from env (avoids shell expansion issues on Railway)
CMD ["python", "run.py"]
