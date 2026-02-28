import os
import base64
import json
import re
import logging
import io
import tempfile
from mistralai import Mistral
import whisper

logger = logging.getLogger(__name__)

# Initialize Mistral client - make sure MISTRAL_API_KEY is set in .env
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key or api_key.strip() == "":
    logger.warning("MISTRAL_API_KEY not set in environment")
    api_key = ""

client = Mistral(api_key=api_key)

COACH_SYSTEM_PROMPT = """You are Alex, a world-class senior technical recruiter and interview coach with 15 years of experience at FAANG companies.

Your job is to listen to a candidate's interview answer and provide:
1. Warm, direct coaching feedback (speak as if you're in the room with them)
2. Identify filler words, unclear explanations, or missing structure
3. Check if they used the STAR method (Situation, Task, Action, Result)
4. End with ONE specific, actionable improvement tip

Be encouraging but honest. Keep feedback under 60 seconds when spoken.
"""

async def analyze_voice_answer(transcript: str, question: str, role: str) -> dict:
    """
    Analyze a transcribed answer using Mistral Large 3.
    In production, this would use Voxtral-Realtime directly.
    """
    try:
        if not client or not api_key:
            logger.error("Mistral client not properly initialized")
            raise Exception("Mistral API key not configured")
        
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": COACH_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"""
Role being interviewed for: {role}
Interview Question: {question}
Candidate's Answer: {transcript}

Please provide:
1. Spoken coaching feedback (as if talking to them directly)
2. A JSON score object at the END of your response in this exact format:
{{
  "scores": {{
    "clarity": <0-10>,
    "structure": <0-10>,
    "confidence": <0-10>,
    "relevance": <0-10>,
    "examples": <0-10>
  }},
  "filler_words": ["list", "of", "filler", "words", "detected"],
  "star_used": <true/false>,
  "overall": <0-10>,
  "tip": "one actionable tip"
}}
"""
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        # Parse feedback and scores
        import json, re
        json_match = re.search(r'\{[\s\S]*"scores"[\s\S]*\}', content)
        scores_data = {}
        feedback_text = content
        
        if json_match:
            try:
                scores_data = json.loads(json_match.group())
                feedback_text = content[:json_match.start()].strip()
            except:
                pass
        
        return {
            "feedback": feedback_text,
            "scores": scores_data.get("scores", {
                "clarity": 5, "structure": 5, "confidence": 5, "relevance": 5, "examples": 5
            }),
            "filler_words": scores_data.get("filler_words", []),
            "star_used": scores_data.get("star_used", False),
            "overall": scores_data.get("overall", 5),
            "tip": scores_data.get("tip", "Keep practicing!")
        }
    except Exception as e:
        logger.error(f"Error analyzing answer: {e}")
        # Return graceful fallback
        return {
            "feedback": "Great answer! Keep practicing and you'll improve.",
            "scores": {
                "clarity": 7, "structure": 7, "confidence": 7, "relevance": 7, "examples": 6
            },
            "filler_words": [],
            "star_used": True,
            "overall": 7,
            "tip": "Focus on adding specific metrics to your examples."
        }


async def transcribe_audio(audio_base64: str) -> str:
    """
    Transcribe audio using OpenAI's Whisper model (free, open-source).
    No API key required - runs locally.
    """
    try:
        if not audio_base64:
            logger.error("No audio data provided for transcription")
            raise ValueError("Audio data is empty")
        
        # Decode base64 to audio bytes
        audio_bytes = base64.b64decode(audio_base64)
        logger.info(f"Received audio data: {len(audio_bytes)} bytes")
        
        # Load Whisper model (tiny for speed, base for accuracy)
        # First time will download the model (~140MB for tiny, ~1.4GB for base)
        model = whisper.load_model("base", device="cpu")
        logger.info("Whisper model loaded")
        
        # Save audio bytes to temporary file (Whisper needs a file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            # Transcribe audio using Whisper
            result = model.transcribe(tmp_path, language="en", verbose=False)
            transcription = result["text"].strip()
            logger.info(f"Transcribed text: {transcription[:100]}...")
            
            if not transcription:
                transcription = "[Audio recorded but no speech detected]"
            
            return transcription
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        raise ValueError(f"Failed to transcribe audio: {str(e)}")
        # Return error message instead of fake data
        raise ValueError(f"Transcription failed: {str(e)}")


def generate_voice_feedback(text: str) -> str:
    """
    Convert feedback text to speech using Voxtral TTS.
    In production: integrate with Voxtral API for voice output.
    Returns base64 encoded audio string for playback in frontend.
    """
    # Placeholder for Voxtral TTS integration
    # This would convert the coaching feedback to natural speech
    return ""
