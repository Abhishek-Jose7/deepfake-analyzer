FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads reports checkpoints

# Expose port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1
# GROQ_API_KEY should be set as a Hugging Face Space secret

# Run the application
CMD ["python", "main.py"]
