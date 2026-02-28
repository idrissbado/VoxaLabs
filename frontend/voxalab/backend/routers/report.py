from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scoring_engine import generate_full_report

router = APIRouter()

class GenerateReportRequest(BaseModel):
    sessions: list
    role: str
    user_name: str = "Candidate"

@router.post("/generate")
async def generate_report(req: GenerateReportRequest):
    """Generate a full practice session report."""
    try:
        report = await generate_full_report(req.sessions, req.role)
        report["user_name"] = req.user_name
        report["role"] = req.role
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
