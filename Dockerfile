# ==============================================================================
# Multi-Stage Dockerfile: Mobile Money Fraud Surveillance System in Nigeria
# Miva Open University - Master of Information Technology (MIT 8313)
# Researcher: Olakunle Awotunbo (2025/B/MIT/1384)
# ==============================================================================

# Stage 1: Build & Dependency Wheel Cache
FROM python:3.11-slim AS builder

WORKDIR /app

# Install compilation prerequisites
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Final Lean Production Runtime
FROM python:3.11-slim AS runner

WORKDIR /app

# Install minimal runtime libraries (libgomp1 required for XGBoost OpenMP acceleration)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python wheels from builder
COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir /wheels/*

# Copy application source code
COPY security.py feature_engineering.py data_generator.py models.py train.py api.py app.py ./
COPY tests/ ./tests/
COPY entrypoint.sh ./

# Create runtime directories
RUN mkdir -p data models screenshots && chmod +x entrypoint.sh

# Expose Streamlit (8501) and FastAPI (8000)
EXPOSE 8000 8501

# Healthcheck targeting FastAPI health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Launch both microservices
ENTRYPOINT ["./entrypoint.sh"]

