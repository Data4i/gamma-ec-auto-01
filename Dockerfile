FROM python:3.12-slim

# Install system dependencies including libpq-dev and gcc
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn

COPY . .

EXPOSE 8000

CMD ["python3", "main.py"]
