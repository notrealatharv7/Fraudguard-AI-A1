# Use a lightweight official Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (better Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose default local port (Railway injects PORT dynamically)
EXPOSE 8001

# Run FastAPI using Railway-compatible dynamic port
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8001}"]
