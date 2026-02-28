from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services.scoring_engine import get_questions
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory session store (use Redis/Supabase in production)
sessions = {}

class CreateSessionRequest(BaseModel):
    role: str
    language: str = "en"
    user_id: str = "anonymous"

class NextQuestionRequest(BaseModel):
    language: str = "en"

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question: str
    user_answer: str
    language: str = "en"
    role: str = "Software Engineer"

@router.get("/questions")
async def get_role_questions(role: str = Query(...), language: str = Query("en")):
    """Get all questions for a specific role and language."""
    try:
        questions = get_questions(role, language)
        if not questions:
            raise HTTPException(status_code=404, detail=f"No questions found for role {role}")
        
        logger.info(f"Retrieved {len(questions)} questions for role {role} in {language}")
        
        return {
            "role": role,
            "language": language,
            "questions": questions,
            "total": len(questions)
        }
    except Exception as e:
        logger.error(f"Error getting questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
async def create_session(req: CreateSessionRequest):
    """Create a new interview practice session."""
    try:
        session_id = str(uuid.uuid4())
        questions = get_questions(req.role, req.language)
        
        sessions[session_id] = {
            "session_id": session_id,
            "role": req.role,
            "language": req.language,
            "user_id": req.user_id,
            "questions": questions,
            "current_question_index": 0,
            "answers": [],
            "feedback": [],
            "completed": False
        }
        
        logger.info(f"Created session {session_id} for role {req.role} in {req.language}")
        
        return {
            "session_id": session_id,
            "role": req.role,
            "language": req.language,
            "questions": questions,
            "current_question_index": 0
        }
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}")
async def get_session(session_id: str):
    """Retrieve an existing session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@router.post("/{session_id}/next")
async def next_question(session_id: str, req: NextQuestionRequest):
    """Move to next question in the session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    if session["current_question_index"] < len(session["questions"]) - 1:
        session["current_question_index"] += 1
        question = session["questions"][session["current_question_index"]]
    else:
        session["completed"] = True
        question = "Session completed"
    
    logger.info(f"Advanced session {session_id} to question {session['current_question_index']}")
    
    return {
        "session_id": session_id,
        "question": question,
        "question_index": session["current_question_index"],
        "total_questions": len(session["questions"]),
        "completed": session["completed"]
    }

@router.get("/{session_id}/current-question")
async def get_current_question(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    idx = session["current_question_index"]
    return {
        "question": session["questions"][idx],
        "index": idx,
        "total": len(session["questions"])
    }

@router.post("/answer")
async def submit_answer(req: SubmitAnswerRequest):
    """Submit an answer to get coaching feedback."""
    try:
        logger.info(f"Submitting answer for session {req.session_id}")
        
        # Import here to avoid circular imports
        from services.mistral_service import generate_coaching_feedback
        from services.scoring_engine import ROLE_MAPPING
        
        # Map the role (e.g., java -> Software Engineer)
        role = ROLE_MAPPING.get(req.role.lower(), req.role)
        logger.info(f"Mapped role '{req.role}' to '{role}'")
        
        logger.info(f"Processing answer for question: {req.question[:50]}...")
        
        # Generate coaching feedback using Mistral AI
        feedback = await generate_coaching_feedback(
            question=req.question,
            answer=req.user_answer,
            role=role
        )
        
        return {
            "success": True,
            "feedback": feedback,
            "session_id": req.session_id
        }
    except Exception as e:
        logger.error(f"Error processing answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
