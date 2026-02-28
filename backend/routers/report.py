from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scoring_engine import generate_full_report, calculate_performance_metrics
from datetime import datetime

router = APIRouter()

class GenerateReportRequest(BaseModel):
    sessions: list
    role: str
    user_name: str = "Candidate"

class SessionAnswer(BaseModel):
    question: str
    answer: str
    score: float = None
    feedback: str = None
    timestamp: str = None

class AnalyticsRequest(BaseModel):
    sessions: list
    role: str

@router.post("/generate")
async def generate_report(req: GenerateReportRequest):
    """Generate a comprehensive practice session report with Mistral analysis."""
    try:
        if not req.sessions or len(req.sessions) == 0:
            raise HTTPException(status_code=400, detail="At least one session is required")
        
        report = await generate_full_report(req.sessions, req.role)
        report["user_name"] = req.user_name
        report["role"] = req.role
        report["generated_at"] = datetime.now().isoformat()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analytics")
async def get_analytics(req: AnalyticsRequest):
    """Generate detailed performance analytics for sessions."""
    try:
        if not req.sessions or len(req.sessions) == 0:
            raise HTTPException(status_code=400, detail="At least one session is required")
        
        metrics = calculate_performance_metrics(req.sessions, req.role)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summary")
async def get_summary(req: AnalyticsRequest):
    """Generate a quick summary of session performance."""
    try:
        if not req.sessions or len(req.sessions) == 0:
            raise HTTPException(status_code=400, detail="At least one session is required")
        
        total_score = sum(s.get("overall", 5) for s in req.sessions) / len(req.sessions)
        return {
            "role": req.role,
            "sessions_count": len(req.sessions),
            "average_score": round(total_score, 1),
            "max_score": max(s.get("overall", 5) for s in req.sessions),
            "min_score": min(s.get("overall", 5) for s in req.sessions),
            "timestamps": [s.get("timestamp", "N/A") for s in req.sessions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
