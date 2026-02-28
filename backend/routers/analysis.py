from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from services.voxtral_service import analyze_voice_answer, transcribe_audio
from services.scoring_engine import detect_filler_words, check_star_method
from services.mistral_service import generate_improved_answer, generate_follow_up_questions, generate_coaching_feedback
import base64
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class FeedbackRequest(BaseModel):
    session_id: str
    question: str
    user_answer: str
    audio_base64: Optional[str] = None
    is_audio: bool = False
    language: str = "en"
    context: List[Dict] = []

class FollowUpRequest(BaseModel):
    session_id: str
    question: str
    user_answer: str
    follow_up: str
    language: str = "en"
    context: List[Dict] = []

class AnalyzeAudioRequest(BaseModel):
    audio_base64: str
    question: str
    role: str
    session_id: str
    language: str = "en"

class AnalyzeTextRequest(BaseModel):
    question: str
    transcript: str
    role: str

@router.post("/audio")
async def analyze_audio_answer(req: AnalyzeAudioRequest):
    """Analyze audio recording: transcribe and provide feedback."""
    try:
        logger.info(f"Analyzing audio for session {req.session_id}")
        
        # Transcribe the audio
        transcript = await transcribe_audio(req.audio_base64)
        logger.info(f"Transcribed audio: {transcript[:100]}...")
        
        # Generate comprehensive feedback
        coaching_data = await generate_coaching_feedback(
            question=req.question,
            answer=transcript,
            language=req.language,
            context=[]
        )
        
        # Local analysis
        filler_analysis = detect_filler_words(transcript)
        
        return {
            "transcript": transcript,
            "user_answer": transcript,
            "coaching_feedback": coaching_data.get("feedback", ""),
            "clarity_score": coaching_data.get("clarity_score", 7),
            "depth_score": coaching_data.get("depth_score", 7),
            "communication_score": coaching_data.get("communication_score", 7),
            "strengths": coaching_data.get("strengths", []),
            "improvements": coaching_data.get("improvements", []),
            "follow_up_question": coaching_data.get("follow_up", None),
            "filler_words": filler_analysis,
            "word_count": len(transcript.split()),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error analyzing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def analyze_answer(req: FeedbackRequest):
    """Comprehensive answer analysis with multi-language support."""
    try:
        logger.info(f"Analyzing answer for session {req.session_id} in language {req.language}")
        
        answer_text = req.user_answer
        
        # If audio, transcribe first
        if req.is_audio and req.audio_base64:
            logger.info("Transcribing audio...")
            answer_text = await transcribe_audio(req.audio_base64)
        
        # Generate comprehensive feedback
        coaching_data = await generate_coaching_feedback(
            question=req.question,
            answer=answer_text,
            language=req.language,
            context=req.context
        )
        
        # Local analysis
        filler_analysis = detect_filler_words(answer_text)
        
        return {
            "user_answer": answer_text,
            "coaching_feedback": coaching_data.get("feedback", ""),
            "clarity_score": coaching_data.get("clarity_score", 7),
            "depth_score": coaching_data.get("depth_score", 7),
            "communication_score": coaching_data.get("communication_score", 7),
            "strengths": coaching_data.get("strengths", []),
            "improvements": coaching_data.get("improvements", []),
            "follow_up_question": coaching_data.get("follow_up", None),
            "filler_words": filler_analysis,
            "word_count": len(answer_text.split()),
            "transcription": answer_text if req.is_audio else None
        }
    except Exception as e:
        logger.error(f"Error analyzing answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/followup")
async def handle_follow_up(req: FollowUpRequest):
    """Handle follow-up question and answer."""
    try:
        logger.info(f"Processing follow-up for session {req.session_id}")
        
        # Generate follow-up feedback with context
        coaching_data = await generate_coaching_feedback(
            question=req.follow_up,
            answer=req.user_answer,
            language=req.language,
            context=req.context,
            is_followup=True
        )
        
        return {
            "user_answer": req.user_answer,
            "coaching_feedback": coaching_data.get("feedback", ""),
            "clarity_score": coaching_data.get("clarity_score", 7),
            "depth_score": coaching_data.get("depth_score", 7),
            "communication_score": coaching_data.get("communication_score", 7),
            "strengths": coaching_data.get("strengths", []),
            "improvements": coaching_data.get("improvements", []),
            "follow_up_question": coaching_data.get("follow_up", None),
        }
    except Exception as e:
        logger.error(f"Error processing follow-up: {str(e)}")
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

@router.post("/transcribe")
async def transcribe_only(req: AnalyzeAudioRequest):
    """Just transcribe audio without analysis."""
    try:
        logger.info("Transcribing audio")
        transcript = await transcribe_audio(req.audio_base64)
        return {
            "success": True,
            "transcript": transcript
        }
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
