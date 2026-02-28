"""
VoxaLab AI - Hugging Face Spaces Deployment
Serves both FastAPI backend and React frontend
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    logger.warning(f"Warning: .env file not found at {env_path}")

# Import routers with error handling
sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    from backend.routers import session
    logger.info("✓ session router imported")
except Exception as e:
    logger.error(f"✗ Failed to import session router: {e}")
    session = None

try:
    from backend.routers import analysis
    logger.info("✓ analysis router imported")
except Exception as e:
    logger.error(f"✗ Failed to import analysis router: {e}")
    analysis = None

try:
    from backend.routers import report
    logger.info("✓ report router imported")
except Exception as e:
    logger.error(f"✗ Failed to import report router: {e}")
    report = None

try:
    from backend.routers import tts
    logger.info("✓ tts router imported")
except Exception as e:
    logger.error(f"✗ Failed to import tts router: {e}")
    tts = None

try:
    from backend.routers import math_tutor
    logger.info("✓ math_tutor router imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import math_tutor router: {e}")
    import traceback
    logger.error(traceback.format_exc())
    math_tutor = None

# Create FastAPI app
app = FastAPI(
    title="VoxaLab AI",
    version="1.0.0",
    description="AI-powered interview coaching platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers only if successfully imported
if session:
    app.include_router(session.router, prefix="/session", tags=["session"])
    logger.info("✓ session router registered")
else:
    logger.warning("! session router NOT registered")

if analysis:
    app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
    logger.info("✓ analysis router registered")
else:
    logger.warning("! analysis router NOT registered")

if report:
    app.include_router(report.router, prefix="/report", tags=["report"])
    logger.info("✓ report router registered")
else:
    logger.warning("! report router NOT registered")

if tts:
    app.include_router(tts.router, prefix="/tts", tags=["tts"])
    logger.info("✓ tts router registered")
else:
    logger.warning("! tts router NOT registered")

if math_tutor:
    app.include_router(math_tutor.router, prefix="/math", tags=["math-tutor"])
    logger.info("✓ math_tutor router registered - MATH ENDPOINTS ACTIVE")
else:
    logger.error("! math_tutor router NOT registered - MATH API ENDPOINTS UNAVAILABLE")

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "service": "VoxaLab AI"}

# Serve React build files
frontend_build_path = Path(__file__).parent / "frontend" / "build"
if frontend_build_path.exists():
    # Mount static files
    app.mount("/static", StaticFiles(directory=frontend_build_path / "static"), name="static")
    
    # Serve index.html for all other routes (React Router)
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        # Don't serve react for API routes
        if full_path.startswith(("api/", "session/", "analysis/", "report/", "tts/", "health", "docs", "openapi.json")):
            return {"error": "Not found"}
        
        # Serve index.html for all other routes
        index_file = frontend_build_path / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"error": "Frontend not found"}
    
    # Serve index.html at root
    @app.get("/")
    async def root():
        index_file = frontend_build_path / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "VoxaLab AI Server is running"}
else:
    logger.warning(f"Frontend build not found at {frontend_build_path}")
    
    @app.get("/")
    async def root():
        return {
            "message": "VoxaLab AI Server",
            "status": "running",
            "api_docs": "/docs",
            "note": "Frontend build not found - API only mode"
        }

# API documentation
@app.get("/docs")
async def docs():
    return {"redirect": "/docs"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting VoxaLab AI on {host}:{port}")
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
