# VoxaLab AI - Docker Container
# Multi-stage build: Build frontend, then run app

# Stage 1: Build frontend (optional - using pre-built)
# We use the pre-built frontend/build directory

# Stage 2: Run the app
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy Python requirements
COPY --chown=user requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy backend code
COPY --chown=user backend/ /app/backend/

# Copy frontend build (pre-built React static files)
COPY --chown=user frontend/build/ /app/frontend/build/

# Copy main app.py
COPY --chown=user app.py /app/app.py

# Set environment
ENV PYTHONUNBUFFERED=1

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

# Run the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
