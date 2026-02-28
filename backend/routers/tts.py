"""
Text-to-Speech Router
Handles audio generation endpoints with multi-language support
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
    language: str = "en"

@router.post("/speak")
async def speak(input_data: TextInput):
    """
    Convert text to speech with multi-language support
    
    Args:
        input_data: TextInput with text, optional voice_id, and language code
        
    Returns:
        Audio stream in MP3 format
    """
    if not input_data.text or len(input_data.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Limit text length for safety
    if len(input_data.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
    
    logger.info(f"Generating speech for language {input_data.language}")
    
    audio_bytes = await tts_service.speak(
        input_data.text, 
        voice_id=input_data.voice_id,
        language=input_data.language
    )
    
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
