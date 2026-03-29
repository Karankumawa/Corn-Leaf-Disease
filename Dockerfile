FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for Pillow and OpenCV (if needed)
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port (7860 is the default for HuggingFace Spaces, 10000 for Render)
ENV PORT=7860
EXPOSE 7860

# Run the app using Gunicorn for production standard
CMD ["gunicorn", "-b", "0.0.0.0:7860", "server:app"]
