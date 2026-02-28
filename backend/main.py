from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# =============================================================================
# MISTRAL HACKATHON - VoxaLab AI Interview Coaching Platform
# =============================================================================
# This app uses Mistral AI for:
# 1. Coaching Feedback: Mistral Large 3 (mistralai SDK)
# 2. Question Bank: Mistral-powered role mapping
# 3. Audio Transcription: Whisper (future: Mistral Voxtral)
# 
# Key Endpoints:
# - POST /session/answer → Mistral Large generates coaching feedback
# - POST /analysis/transcribe → Whisper transcribes audio
# - GET /session/questions → Role-mapped question bank
# =============================================================================

# Load environment variables from .env file (one directory up from backend)
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    logger.warning(f"Warning: .env file not found at {env_path}")

# Verify keys are loaded
logger.debug(f"MISTRAL_API_KEY set: {bool(os.getenv('MISTRAL_API_KEY'))}")
logger.debug(f"ELEVENLABS_API_KEY set: {bool(os.getenv('ELEVENLABS_API_KEY'))}")

# Import routers with error handling
try:
    from routers import session
    logger.info("✓ session router imported")
except Exception as e:
    logger.error(f"✗ Failed to import session router: {e}")
    session = None

try:
    from routers import analysis
    logger.info("✓ analysis router imported")
except Exception as e:
    logger.error(f"✗ Failed to import analysis router: {e}")
    analysis = None

try:
    from routers import report
    logger.info("✓ report router imported")
except Exception as e:
    logger.error(f"✗ Failed to import report router: {e}")
    report = None

try:
    from routers import tts
    logger.info("✓ tts router imported")
except Exception as e:
    logger.error(f"✗ Failed to import tts router: {e}")
    tts = None

try:
    from routers import math_tutor
    logger.info("✓ math_tutor router imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import math_tutor router: {e}")
    import traceback
    logger.error(traceback.format_exc())
    math_tutor = None

app = FastAPI(title="PrepCoach AI", version="1.0.0")

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
    logger.warning("! session router NOT registered (import failed)")

if analysis:
    app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
    logger.info("✓ analysis router registered")
else:
    logger.warning("! analysis router NOT registered (import failed)")

if report:
    app.include_router(report.router, prefix="/report", tags=["report"])
    logger.info("✓ report router registered")
else:
    logger.warning("! report router NOT registered (import failed)")

if tts:
    app.include_router(tts.router, prefix="/tts", tags=["tts"])
    logger.info("✓ tts router registered")
else:
    logger.warning("! tts router NOT registered (import failed)")

if math_tutor:
    app.include_router(math_tutor.router, prefix="/math", tags=["math-tutor"])
    logger.info("✓ math_tutor router registered - ENDPOINTS ACTIVE")
else:
    logger.error("! math_tutor router NOT registered (import failed) - API ENDPOINTS UNAVAILABLE")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "VoiceCoach AI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
