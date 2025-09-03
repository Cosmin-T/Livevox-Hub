# Use Ubuntu-based Python image for better Playwright support
FROM python:3.11-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements-deploy.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Install basic system dependencies and let Playwright handle browser deps
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers first
RUN playwright install chromium webkit

# Install Playwright system dependencies (this handles all the missing libraries)
RUN playwright install-deps chromium webkit

# Copy application code
COPY . .

# Create necessary directories and move JSON files to data volume
RUN mkdir -p /app/templates /app/static /app/data && \
    mv /app/*.json /app/data/ 2>/dev/null || true

# Create data volume for persistent storage
VOLUME ["/app/data"]

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/ || exit 1

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]