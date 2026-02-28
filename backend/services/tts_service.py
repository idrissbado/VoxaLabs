"""
ElevenLabs Text-to-Speech Service
Converts coach responses to natural-sounding audio
"""

import os
import logging
from io import BytesIO
from elevenlabs.client import ElevenLabs
from elevenlabs import play

logger = logging.getLogger(__name__)

class TTSService:
    """Text-to-Speech service using ElevenLabs"""
    
    def __init__(self):
        """Initialize ElevenLabs client"""
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            logger.warning("ELEVENLABS_API_KEY not set - TTS disabled")
            self.client = None
            return
        
        self.client = ElevenLabs(api_key=api_key)
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
        
    async def speak(self, text: str, voice_id: str = None, language: str = "en") -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            voice_id: Optional voice ID override
            language: Language code (default: "en")
            
        Returns:
            Audio bytes in MP3 format
        """
        if not self.client:
            logger.error("ElevenLabs client not initialized")
            return None
            
        try:
            # Use provided voice_id or default
            use_voice_id = voice_id or self.voice_id
            
            audio = self.client.generate(
                text=text,
                voice=use_voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Convert generator to bytes
            audio_bytes = BytesIO()
            for chunk in audio:
                audio_bytes.write(chunk)
            
            audio_bytes.seek(0)
            return audio_bytes.getvalue()
            
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return None
    
    async def get_available_voices(self):
        """Get list of available voices"""
        if not self.client:
            return []
            
        try:
            voices = self.client.voices.get_all()
            return [
                {
                    "id": voice.voice_id,
                    "name": voice.name,
                    "preview_url": voice.preview_url if hasattr(voice, 'preview_url') else None
                }
                for voice in voices
            ]
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return []

# Initialize TTS service
tts_service = TTSService()
