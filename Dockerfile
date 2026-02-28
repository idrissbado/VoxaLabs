# VoxaLab AI - Docker Container for HF Spaces
# Optimized for faster builds

FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Set environment variables before pip install
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy Python requirements first (for better layer caching)
COPY requirements.txt requirements.txt

# Install Python dependencies with optimization flags
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY --chown=user backend/ /app/backend/

# Copy frontend build (pre-built React static files)
COPY --chown=user frontend/build/ /app/frontend/build/

# Copy main app.py
COPY --chown=user app.py /app/app.py

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health').read()" || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
