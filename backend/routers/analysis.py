from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
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
        error_msg = str(e)
        logger.error(f"❌ Error analyzing audio: {error_msg}")
        
        # If 401 Unauthorized, return demo feedback instead of failing
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Returning demo audio analysis")
            return {
                "transcript": "This is a demo transcription of your audio response.",
                "user_answer": "This is a demo transcription of your audio response.",
                "coaching_feedback": "Good response! Your voice was clear and well-structured. Add more specific examples to strengthen your answer.",
                "clarity_score": 8,
                "depth_score": 7,
                "communication_score": 8,
                "strengths": ["Clear speech", "Coherent structure", "Good pacing"],
                "improvements": ["Add measurable metrics", "Include specific examples"],
                "follow_up_question": "Can you elaborate on your solution with concrete examples?",
                "filler_words": [],
                "word_count": 45,
                "status": "success",
                "demo_mode": True
            }
        
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
        error_msg = str(e)
        logger.error(f"❌ Error analyzing answer: {error_msg}")
        
        # If 401 Unauthorized, return demo feedback
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Returning demo feedback")
            return {
                "user_answer": req.user_answer,
                "coaching_feedback": "Excellent response! You provided a clear and structured answer.",
                "clarity_score": 8,
                "depth_score": 7,
                "communication_score": 8,
                "strengths": ["Clear articulation", "Logical structure", "Good communication"],
                "improvements": ["Add more specific examples", "Include measurable results"],
                "follow_up_question": "Can you tell us more about the specific metrics used?",
                "filler_words": [],
                "word_count": len(req.user_answer.split()),
                "transcription": req.user_answer if req.is_audio else None,
                "demo_mode": True
            }
        
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
        error_msg = str(e)
        logger.error(f"❌ Error processing follow-up: {error_msg}")
        
        # If 401 Unauthorized, return demo feedback
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Returning demo follow-up feedback")
            return {
                "user_answer": req.user_answer,
                "coaching_feedback": "Great follow-up answer! Very insightful.",
                "clarity_score": 8,
                "depth_score": 8,
                "communication_score": 8,
                "strengths": ["Thoughtful response", "Good engagement", "Clear explanation"],
                "improvements": ["Could include timing details", "Consider edge cases"],
                "follow_up_question": "What would you do differently if requirements changed?",
                "demo_mode": True
            }
        
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
async def transcribe_only(
    file: UploadFile = File(...),
    language: str = Form(default="en")
):
    """Transcribe audio file without analysis."""
    try:
        logger.info("Transcribing audio file")
        
        # Read file bytes
        audio_bytes = await file.read()
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Transcribe
        transcript = await transcribe_audio(audio_base64)
        
        if not transcript or transcript.startswith("Demo:"):
            logger.warning("⚠️ Whisper module not available - using demo transcription")
            return {
                "success": True,
                "transcript": transcript,
                "mode": "demo",
                "note": "Audio transcription module not available. Please ensure Whisper is properly installed."
            }
        
        logger.info(f"✓ Successfully transcribed audio ({len(transcript)} chars)")
        return {
            "success": True,
            "transcript": transcript,
            "mode": "real"
        }
    except Exception as e:
        logger.error(f"✗ Transcription error: {str(e)}")
        logger.error(f"✗ Check if Whisper module is installed: pip install openai-whisper")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
