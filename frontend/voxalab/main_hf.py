from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env if it exists (local development)
env_path = Path("/app/backend/.env")
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env from {env_path}")
else:
    print("⚠️ .env file not found - using HF Spaces Repository Secrets")

# Add backend to path
sys.path.insert(0, '/app/backend')

# Create main app FIRST
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log environment variables
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"✅ MISTRAL_API_KEY set: {bool(os.getenv('MISTRAL_API_KEY'))}")
logger.info(f"✅ ELEVENLABS_API_KEY set: {bool(os.getenv('ELEVENLABS_API_KEY'))}")
logger.info(f"✅ HUGGINGFACE_API_KEY set: {bool(os.getenv('HUGGINGFACE_API_KEY'))}")

# Import and include backend routes
try:
    from routers import session, analysis, report, tts
    
    app.include_router(session.router, prefix="/session", tags=["session"])
    app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
    app.include_router(report.router, prefix="/report", tags=["report"])
    app.include_router(tts.router, prefix="/tts", tags=["tts"])
    
    logger.info("✅ Backend routes loaded successfully")
except Exception as e:
    logger.error(f"❌ Error loading backend routes: {e}")
    import traceback
    traceback.print_exc()

# Mount static React build
react_build_path = "/app/frontend/build"
if os.path.exists(react_build_path):
    static_path = os.path.join(react_build_path, "static")
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path, check_dir=False), name="static")
    logger.info(f"✅ React build found at {react_build_path}")
else:
    logger.warning(f"⚠️ React build not found at {react_build_path}")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "mistral_key": bool(os.getenv('MISTRAL_API_KEY'))}

@app.get("/")
async def serve_react():
    """Serve React app"""
    index_file = os.path.join(react_build_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "React app not built", "path": react_build_path}

@app.get("/{path_name:path}")
async def serve_react_routes(path_name: str):
    """Serve React for all routes (SPA)"""
    # Don't interfere with API routes
    if path_name.startswith("api/") or path_name.startswith("session/") or \
       path_name.startswith("analysis/") or path_name.startswith("report/") or \
       path_name.startswith("tts/"):
        return {"error": "Not found"}
    
    index_file = os.path.join(react_build_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting VoxaLab server on 0.0.0.0:7860")
    uvicorn.run(app, host="0.0.0.0", port=7860)
