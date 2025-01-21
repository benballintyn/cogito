# Stage 1: Build dependencies and install package
FROM python:3.11-slim AS builder

# Install curl (for Poetry) and other required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Poetry's path
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy project configuration files
COPY pyproject.toml poetry.lock README.md ./

# Copy the package source code
COPY cogito/ ./cogito/

# Install dependencies and the package (excluding dev dependencies)
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

# Stage 2: Final image with installed package
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy installed dependencies and package from the builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Copy the installed package source for downstream use
COPY --from=builder /app/cogito /app/cogito

# Verify that the package is installed (optional)
RUN python -c "import cogito"

# Command to run when the container starts (can be overridden by downstream images)
CMD ["python"]
