from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routers import session, analysis, report, tts, math_tutor
import uvicorn
from dotenv import load_dotenv
import os
from pathlib import Path

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
    print(f"Warning: .env file not found at {env_path}")

# Verify keys are loaded
import logging
logging.info(f"MISTRAL_API_KEY set: {bool(os.getenv('MISTRAL_API_KEY'))}")
logging.info(f"ELEVENLABS_API_KEY set: {bool(os.getenv('ELEVENLABS_API_KEY'))}")

app = FastAPI(title="PrepCoach AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router, prefix="/session", tags=["session"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(report.router, prefix="/report", tags=["report"])
app.include_router(tts.router, prefix="/tts", tags=["tts"])
app.include_router(math_tutor.router, prefix="/math", tags=["math-tutor"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "VoiceCoach AI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
