# File: Dockerfile

FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
 && rm -rf /var/lib/apt/lists/*

# Copy Poetry config files first (for layer caching)
COPY ./pyproject.toml ./poetry.lock* ./README.md ./

# Install Poetry and dependencies
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy the entire project into container
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Run Uvicorn on container start
CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]