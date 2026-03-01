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
    """Text-to-Speech service using ElevenLabs - with lazy initialization"""
    
    def __init__(self):
        """Initialize ElevenLabs client with lazy loading"""
        self.client = None
        self.available = False
        self._initialized = False
        
    def _init_client(self):
        """Lazy initialization of ElevenLabs client (called on first use)"""
        if self._initialized:
            return
        
        self._initialized = True
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            logger.warning("⚠️  ELEVENLABS_API_KEY not found in environment variables")
            logger.warning("📝 To enable voice synthesis on HF Spaces:")
            logger.warning("   1. Go to HuggingFace Space Settings > Secrets")
            logger.warning("   2. Add ELEVENLABS_API_KEY (get from https://elevenlabs.io/app/api-keys)")
            logger.warning("   3. Restart the space")
            self.client = None
            self.available = False
            return
        
        try:
            self.client = ElevenLabs(api_key=api_key)
            self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
            self.available = True
            logger.info("✓ ElevenLabs TTS service initialized successfully")
            logger.info(f"  Voice ID: {self.voice_id[:8]}...")
        except Exception as e:
            logger.error(f"✗ Failed to initialize ElevenLabs client: {e}")
            self.client = None
            self.available = False
        
    async def speak(self, text: str, voice_id: str = None, language: str = "en") -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            voice_id: Optional voice ID override
            language: Language code (default: "en")
            
        Returns:
            Audio bytes in MP3 format, or None if failed
        """
        # Lazy initialization on first use
        self._init_client()
        
        if not self.client:
            logger.error("✗ ElevenLabs client not initialized - ELEVENLABS_API_KEY not set")
            return None
        
        if not self.available:
            logger.error("✗ ElevenLabs service not available")
            return None
            
        try:
            # Use provided voice_id or default
            use_voice_id = voice_id or self.voice_id
            
            logger.info(f"🔊 TTS: Generating audio with voice {use_voice_id[:8]}... for text length {len(text)}")
            
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
            result = audio_bytes.getvalue()
            logger.info(f"✓ TTS: Successfully generated {len(result)} bytes of audio")
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"✗ TTS Error: {error_msg}")
            
            # Log specific error types
            if "401" in error_msg or "Unauthorized" in error_msg or "authentication" in error_msg.lower():
                logger.error("✗ 401 UNAUTHORIZED: ELEVENLABS_API_KEY is invalid or expired")
                logger.error("   Check: https://elevenlabs.io/app/api-keys")
            elif "429" in error_msg or "rate" in error_msg.lower():
                logger.error("✗ 429 RATE LIMITED: Too many requests to ElevenLabs - please wait and try again")
            elif "400" in error_msg or "Invalid request" in error_msg:
                logger.error(f"✗ 400 BAD REQUEST: Check text or voice parameters")
            else:
                logger.error(f"✗ Service error: {error_msg[:100]}")
            
            return None
    
    async def get_available_voices(self):
        """Get list of available voices"""
        # Lazy initialization on first use
        self._init_client()
        
        if not self.client or not self.available:
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

# Initialize TTS service (lazy loading - actual client init happens on first use)
tts_service = TTSService()
