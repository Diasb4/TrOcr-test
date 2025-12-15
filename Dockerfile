FROM python:3.9-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    transformers \
    pillow

# Copy project files
COPY . /app

# Run the script
CMD ["python", "main.py"]
