# Real Estate Wholesale System
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY dashboard_backend.py .
COPY offer_and_contract_system.py .
COPY property_scraper_and_analysis.py .
COPY vapi_voice_system.py .
COPY approval_workflow_api.py .
COPY vapi_backend_api.py .


# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start application
CMD sh -c "uvicorn dashboard_backend:app --host 0.0.0.0 --port ${PORT:-8000}"
