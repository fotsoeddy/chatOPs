FROM python:3.11-slim

WORKDIR /app

# Install dependencies and ssh client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends openssh-client && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Make scripts executable
RUN chmod +x scripts/*.sh

# Expose FastAPI port
EXPOSE 8100

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]