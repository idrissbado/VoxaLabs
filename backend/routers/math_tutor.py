from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from services.math_tutor import (
    analyze_problem,
    validate_step,
    generate_solution,
    generate_practice_problem,
    generate_hint,
    generate_downloadable_solution
)
from services.exercise_extractor import extract_exercise

router = APIRouter()


class ProblemAnalysisRequest(BaseModel):
    problem_text: str


class StepValidationRequest(BaseModel):
    problem_text: str
    step_number: int
    student_step: str
    context: str = ""


class SolutionGenerationRequest(BaseModel):
    problem_text: str
    student_solution: str


class PracticeProblemRequest(BaseModel):
    topic: str
    difficulty: int


class HintRequest(BaseModel):
    problem_text: str
    student_progress: str = ""


class DownloadSolutionRequest(BaseModel):
    problem_text: str
    solution_data: dict
    format_type: str = "markdown"  # markdown, latex, html, json


@router.post("/analyze")
async def analyze_math_problem(req: ProblemAnalysisRequest):
    """Analyze a math problem and provide initial guidance."""
    try:
        analysis = await analyze_problem(req.problem_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate-step")
async def validate_math_step(req: StepValidationRequest):
    """Validate a student's mathematical step."""
    try:
        if req.step_number < 1:
            raise HTTPException(status_code=400, detail="Step number must be >= 1")
        if not req.student_step.strip():
            raise HTTPException(status_code=400, detail="Student step cannot be empty")
        
        feedback = await validate_step(
            req.problem_text,
            req.step_number,
            req.student_step,
            req.context
        )
        return feedback
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-solution")
async def generate_complete_solution(req: SolutionGenerationRequest):
    """Generate complete solution with LaTeX formatting."""
    try:
        if not req.student_solution.strip():
            raise HTTPException(status_code=400, detail="Student solution cannot be empty")
        
        solution = await generate_solution(
            req.problem_text,
            req.student_solution
        )
        return solution
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/practice-problem")
async def get_practice_problem(req: PracticeProblemRequest):
    """Generate a similar practice problem."""
    try:
        if not 1 <= req.difficulty <= 5:
            raise HTTPException(status_code=400, detail="Difficulty must be 1-5")
        if not req.topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        problem = await generate_practice_problem(req.topic, req.difficulty)
        return problem
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hint")
async def get_hint(req: HintRequest):
    """Generate a pedagogical hint to guide student without giving answer."""
    try:
        if not req.problem_text.strip():
            raise HTTPException(status_code=400, detail="Problem text cannot be empty")
        
        hint = await generate_hint(req.problem_text, req.student_progress)
        return hint
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download")
async def download_solution(req: DownloadSolutionRequest):
    """Generate solution in downloadable format (markdown, latex, html, json)."""
    try:
        if not req.problem_text.strip():
            raise HTTPException(status_code=400, detail="Problem text cannot be empty")
        if not req.solution_data:
            raise HTTPException(status_code=400, detail="Solution data cannot be empty")
        
        valid_formats = ["markdown", "latex", "html", "json"]
        if req.format_type.lower() not in valid_formats:
            raise HTTPException(status_code=400, detail=f"Invalid format. Must be one of: {', '.join(valid_formats)}")
        
        downloadable = await generate_downloadable_solution(
            req.problem_text,
            req.solution_data,
            req.format_type
        )
        return downloadable
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract")
async def extract_math_exercise(
    file: UploadFile = File(None),
    text_input: str = Form(None)
):
    """
    Extract math exercise from multiple formats:
    - Text: Direct input
    - Image: JPG, PNG (OCR)
    - PDF: PDF documents
    - LaTeX: .tex files
    """
    try:
        # Priority: file upload over text
        if file:
            file_bytes = await file.read()
            filename = file.filename
            
            # Detect file type from extension
            ext = filename.lower().split('.')[-1]
            file_type_map = {
                'jpg': 'image', 'jpeg': 'image', 'png': 'image',
                'pdf': 'pdf',
                'tex': 'latex', 'latex': 'latex',
                'txt': 'text'
            }
            
            file_type = file_type_map.get(ext)
            if not file_type:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {ext}. Supported: image (jpg, png), pdf, latex (.tex), text (.txt)",
                    "mode": "error"
                }
            
            result = await extract_exercise(file_bytes, filename, file_type)
            
        elif text_input:
            # Direct text input
            result = await extract_exercise(text_input.encode('utf-8'), "exercise.txt", "text")
        else:
            return {
                "success": False,
                "error": "Please provide either a file or text input",
                "mode": "error"
            }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting exercise: {str(e)}",
            "mode": "error"
        }


@router.get("/health")
async def math_router_health():
    """Health check for math tutor service."""
    return {
        "status": "operational",
        "service": "math-tutor",
        "endpoints": 4
    }
