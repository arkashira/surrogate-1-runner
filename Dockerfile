# /opt/axentx/surrogate-1/Dockerfile
# Minimal multi-stage build for surrogate-1 API server
# Target: <500MB image using Python 3.11 slim base

# ===========================================
# Stage 1: Builder - Install dependencies
# ===========================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/axentx/surrogate-1

# Copy requirements first for cache optimization
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===========================================
# Stage 2: Runtime - Minimal final image
# ===========================================
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/axentx/surrogate-1

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY . .

EXPOSE 8080

# Run the API server
CMD ["python", "main.py"]