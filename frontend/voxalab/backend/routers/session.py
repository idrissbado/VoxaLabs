from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scoring_engine import get_questions
import uuid

router = APIRouter()

# In-memory session store (use Redis/Supabase in production)
sessions = {}

class CreateSessionRequest(BaseModel):
    role: str
    user_id: str = "anonymous"

class SessionResponse(BaseModel):
    session_id: str
    role: str
    questions: list
    current_question_index: int

@router.post("/create")
async def create_session(req: CreateSessionRequest):
    session_id = str(uuid.uuid4())
    questions = get_questions(req.role)
    
    sessions[session_id] = {
        "session_id": session_id,
        "role": req.role,
        "user_id": req.user_id,
        "questions": questions,
        "current_question_index": 0,
        "answers": [],
        "completed": False
    }
    
    return {
        "session_id": session_id,
        "role": req.role,
        "questions": questions,
        "current_question_index": 0
    }

@router.get("/{session_id}")
async def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@router.post("/{session_id}/next")
async def next_question(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    if session["current_question_index"] < len(session["questions"]) - 1:
        session["current_question_index"] += 1
    else:
        session["completed"] = True
    
    return session

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
