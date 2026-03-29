FROM python:3.11-slim

# Create the Hugging Face user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

# Install system dependencies (for OpenCV/PIL)
USER root
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
USER user

# Install Python requirements
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=user . .

# Hugging Face uses port 7860
ENV PORT=7860
EXPOSE 7860

# Start Flask with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]