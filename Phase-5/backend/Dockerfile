# Backend Dockerfile for FastAPI application
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv package manager using pip
RUN pip install --no-cache-dir uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -e .

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start server
# Note: Migrations should be run manually or via Kubernetes Job, not on every container start
# Using python -m instead of uv run to avoid creating new venv (dependencies already installed)
CMD ["sh", "-c", "python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
