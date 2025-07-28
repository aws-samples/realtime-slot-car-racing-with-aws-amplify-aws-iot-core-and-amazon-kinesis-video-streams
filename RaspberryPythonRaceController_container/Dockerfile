FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create log directory
RUN mkdir -p /var/log

# Create non-root user
RUN useradd -m -u 1000 racecontroller
RUN chown -R racecontroller:racecontroller /app /var/log
USER racecontroller

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('localhost', 8883), timeout=5)" || exit 1

# Run the application
CMD ["python", "-m", "src.main"]