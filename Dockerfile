# Use Python 3.11 slim base image
FROM python:3.11-slim

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

# Install system dependencies for Playwright (before installing browsers)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers only (skip system deps that fail)
RUN playwright install chromium webkit

# Try to install browser dependencies, but don't fail if some are missing
RUN playwright install-deps chromium webkit || echo "Some browser dependencies could not be installed, continuing..."

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/templates /app/static /app/data

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/ || exit 1

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]