from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.voxtral_service import analyze_voice_answer, transcribe_audio
from services.scoring_engine import detect_filler_words, check_star_method
from services.mistral_service import generate_improved_answer, generate_follow_up_questions
import base64

router = APIRouter()

class AnalyzeTextRequest(BaseModel):
    transcript: str
    question: str
    role: str
    session_id: str = ""

class AnalyzeAudioRequest(BaseModel):
    audio_base64: str
    question: str
    role: str
    session_id: str = ""

@router.post("/text")
async def analyze_text_answer(req: AnalyzeTextRequest):
    """Analyze a text transcript of an interview answer."""
    try:
        # Get AI coaching feedback and scores
        result = await analyze_voice_answer(req.transcript, req.question, req.role)
        
        # Enrich with local analysis
        result["filler_words_detail"] = detect_filler_words(req.transcript)
        result["star_breakdown"] = check_star_method(req.transcript)
        result["word_count"] = len(req.transcript.split())
        result["estimated_duration_seconds"] = len(req.transcript.split()) * 0.4  # ~150 wpm
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio")
async def analyze_audio_answer(req: AnalyzeAudioRequest):
    """Analyze an audio recording of an interview answer."""
    try:
        # Transcribe audio
        transcript = await transcribe_audio(req.audio_base64)
        
        # Analyze transcript
        result = await analyze_voice_answer(transcript, req.question, req.role)
        result["transcript"] = transcript
        result["filler_words_detail"] = detect_filler_words(transcript)
        result["star_breakdown"] = check_star_method(transcript)
        result["word_count"] = len(transcript.split())
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/improved-answer")
async def get_improved_answer(req: AnalyzeTextRequest):
    """Get an example of an improved answer."""
    try:
        improved = await generate_improved_answer(req.question, req.transcript, req.role)
        follow_ups = await generate_follow_up_questions(req.question, req.transcript)
        return {
            "improved_answer": improved,
            "follow_up_questions": follow_ups
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
