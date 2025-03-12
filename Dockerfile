# Use Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies required for pandas and other libraries
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (excluding .env via .dockerignore)
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]