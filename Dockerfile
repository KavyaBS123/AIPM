# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for Hugging Face Spaces
EXPOSE 7860

# Health check script
RUN echo '#!/bin/bash\n\
    PORT="${PORT:-8000}"\n\
    curl -f "http://localhost:$PORT/health" || exit 1' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/healthcheck.sh

# Run the application (supports HF Spaces PORT env var)
CMD ["sh", "-c", "python main.py"]
