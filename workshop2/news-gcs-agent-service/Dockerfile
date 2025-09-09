FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run provides the PORT environment variable
ENV PORT 8080

# Expose the port the app runs on
EXPOSE $PORT

# Run the FastAPI application using uvicorn within a shell
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
