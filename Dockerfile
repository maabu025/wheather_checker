# ─────────────────────────────────────────────────────────────
# CropGuard Ghana — Dockerfile
# Python 3.11 / Flask application
# ─────────────────────────────────────────────────────────────

# Use a specific slim Python image — never just "python"
# slim = smaller image without unnecessary build tools
FROM python:3.11-slim

# Metadata labels
LABEL maintainer="CropGuard Ghana Team"
LABEL description="CropGuard Ghana — AI crop disease detection chatbot for Ghanaian farmers"
LABEL version="1.0"

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE: prevents Python from writing .pyc files
# PYTHONUNBUFFERED: ensures logs appear immediately (important for Docker)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000

# Install dependencies FIRST (before copying source code)
# This leverages Docker layer caching — if requirements.txt hasn't changed,
# Docker skips the pip install step on rebuilds (much faster)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source code
# .dockerignore ensures __pycache__, .env, venv etc. are NOT copied
COPY src/ ./src/

# Create a non-root user for security
# Running as root inside a container is a serious security risk
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Transfer ownership of the app directory to the new user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Document which port the app listens on
# (does NOT publish it — that's docker-compose's job)
EXPOSE 5000

# Health check: Docker pings this endpoint every 30s
# If it fails 3 times, the container is marked "unhealthy"
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Start the app with gunicorn (production WSGI server)
# -w 2: 2 worker processes
# -b 0.0.0.0:5000: listen on all interfaces
# src.app:app — the Flask app object inside src/app.py
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "src.app:app"]