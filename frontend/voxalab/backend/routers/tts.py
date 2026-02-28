"""
Text-to-Speech Router
Handles audio generation endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.tts_service import tts_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class TextInput(BaseModel):
    """Text input for TTS"""
    text: str
    voice_id: str = None

@router.post("/speak")
async def speak(input_data: TextInput):
    """
    Convert text to speech
    
    Args:
        input_data: TextInput with text and optional voice_id
        
    Returns:
        Audio stream in MP3 format
    """
    if not input_data.text or len(input_data.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Limit text length for safety
    if len(input_data.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
    
    audio_bytes = await tts_service.speak(input_data.text)
    
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate audio")
    
    return StreamingResponse(
        iter([audio_bytes]),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=audio.mp3"}
    )

@router.get("/voices")
async def get_voices():
    """Get available TTS voices"""
    voices = await tts_service.get_available_voices()
    return {"voices": voices}
