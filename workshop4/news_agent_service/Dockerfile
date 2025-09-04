# news_gcs_agent/Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a symbolic link for uv and uvx in /usr/local/bin
RUN ln -s /root/.local/bin/uv /usr/local/bin/uv
RUN ln -s /root/.local/bin/uvx /usr/local/bin/uvx

# Install Node.js and npm (if still needed for other purposes)
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Install Python dependencies using uv with the --system flag
RUN uv pip install --no-cache-dir --system -r requirements.txt

# Download the NLTK 'punkt' and 'punkt_tab' tokenizer models
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

COPY . .

# Cloud Run provides the PORT environment variable
ENV PORT 8080

# Expose the port the app runs on
EXPOSE $PORT

# Run the FastAPI application using uvicorn within a shell
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]