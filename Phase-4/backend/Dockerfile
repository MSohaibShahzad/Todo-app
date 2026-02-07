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

# Run database migrations and start server
# Use Railway's PORT environment variable if available, otherwise default to 8000
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
