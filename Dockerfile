# ----------------------------------------------------------------------------
# Soko Bora - Dockerfile
# ----------------------------------------------------------------------------
# Pinned, slim base image for a smaller attack surface and reproducible builds.
FROM python:3.11-slim

# Prevent .pyc files and enable unbuffered stdout/stderr so logs appear
# immediately in `docker logs`.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# gcc + libpq-dev are required to build psycopg2 (PostgreSQL driver).
# Removed after install to keep the final image small.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest first so this layer is cached and only
# reinstalled when requirements.txt actually changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY app/ ./app/

# ----------------------------------------------------------------------------
# Security: run as a non-root user
# ----------------------------------------------------------------------------
RUN groupadd --system appuser && \
    useradd --system --gid appuser --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Container-level health check, backed by the app's own /health route.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run with gunicorn (production WSGI server) rather than Flask's dev server.
# `app.main:app` points at the `app` object created by create_app() in
# app/main.py.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.main:app"]
