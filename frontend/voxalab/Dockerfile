# Unified Dockerfile for VoxaLab (backend + frontend)
FROM node:18-alpine as frontend-builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

COPY frontend/src ./src
COPY frontend/public ./public

RUN npm run build

# Final stage - Python with FastAPI serving both
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install backend requirements
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt uvicorn

# Copy backend code
COPY backend ./backend

# Copy built frontend
COPY --from=frontend-builder /app/build ./frontend/build

# Copy HF Spaces main file
COPY main_hf.py .

# Expose HF Spaces default port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Start unified server
CMD ["python", "main_hf.py"]
