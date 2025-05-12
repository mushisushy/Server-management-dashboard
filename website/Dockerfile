# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies and CA certs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libssl-dev \
        ca-certificates \
        && update-ca-certificates && \
        rm -rf /var/lib/apt/lists/*

# Copy requirement files and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your entire app (make sure init_db.py is in the root directory!)
COPY . .

# Default command to run the DB initializer first, then the app
CMD ["sh", "-c", "echo '👉 Running init_db.py...' && python init_db.py && echo '👉 Starting main.py...' && python main.py"]
