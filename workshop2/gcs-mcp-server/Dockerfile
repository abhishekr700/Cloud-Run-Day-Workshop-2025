# gcs_mcp_server/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PORT 8080
EXPOSE $PORT

CMD ["python3", "main.py"]

