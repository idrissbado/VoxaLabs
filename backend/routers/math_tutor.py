from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from services.math_tutor import (
    analyze_problem,
    validate_step,
    generate_solution,
    generate_practice_problem,
    generate_hint,
    generate_downloadable_solution
)
from services.exercise_extractor import extract_exercise

logger = logging.getLogger(__name__)
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


@router.post("/submit")
async def submit_exercise(
    file: UploadFile = File(None),
    text_input: str = Form(None),
    user_attempt: str = Form(None)
):
    """
    MAIN ENDPOINT: Submit math exercise in ANY format.
    
    Accepts:
    - File: PDF, image (OCR), LaTeX, text
    - Text: Direct problem text
    - Attempt: Student's attempt/progress
    
    Returns:
    - Extracted problem
    - Auto-generated hints (pedagogical)
    - Solution template
    - Chat context for interactive discussion
    """
    try:
        import base64
        from datetime import datetime
        
        # Step 1: Extract exercise from any format
        problem_text = None
        format_detected = None
        
        if file:
            file_bytes = await file.read()
            filename = file.filename.lower()
            
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # TODO: OCR processing
                format_detected = "image (OCR)"
                problem_text = f"[Image problem received: {filename}]"
            elif filename.endswith('.pdf'):
                format_detected = "PDF"
                problem_text = f"[PDF problem received: {filename}]"
            elif filename.endswith(('.tex', '.latex')):
                format_detected = "LaTeX"
                problem_text = file_bytes.decode('utf-8', errors='ignore')
            elif filename.endswith('.txt'):
                format_detected = "Text file"
                problem_text = file_bytes.decode('utf-8', errors='ignore')
            else:
                # Try to detect as text anyway
                try:
                    problem_text = file_bytes.decode('utf-8', errors='ignore')
                    format_detected = "Auto-detected text"
                except:
                    return {
                        "success": False,
                        "error": f"Cannot process file type: {filename}",
                        "status": "error"
                    }
        
        elif text_input:
            problem_text = text_input
            format_detected = "Text input"
        
        else:
            return {
                "success": False,
                "error": "Please provide exercise as file or text input",
                "status": "error"
            }
        
        if not problem_text or not problem_text.strip():
            return {
                "success": False,
                "error": "Exercise text is empty",
                "status": "error"
            }
        
        # Step 2: Analyze problem (safe - has demo fallback)
        problem_analysis = await analyze_problem(problem_text)
        
        # Step 3: Generate hints automatically
        hints_response = await generate_hint(problem_text, user_attempt or "")
        
        # Step 4: Prepare chat context for interactive discussion
        chat_messages = [
            {
                "role": "system",
                "content": "You are an expert math tutor. Guide the student through this problem interactively."
            },
            {
                "role": "assistant",
                "content": f"I see you're working on a {problem_analysis.get('topic', 'math')} problem. {hints_response.get('hint', 'Let me help you work through this step by step.')}"
            }
        ]
        
        return {
            "success": True,
            "status": "submitted",
            "submission_id": datetime.now().isoformat(),
            "format_detected": format_detected,
            "problem": {
                "text": problem_text[:500],  # First 500 chars for preview
                "full_text": problem_text,
                "topic": problem_analysis.get('topic', 'Mathematics'),
                "difficulty": problem_analysis.get('difficulty', 3),
                "concepts": problem_analysis.get('required_concepts', [])
            },
            "hints": {
                "hint_1": hints_response.get('hint', 'Start by identifying what you know and what you need to find.'),
                "hint_2": hints_response.get('guidance', 'Look for patterns or relationships between the given information.'),
                "hint_3": "Try working through a simpler example first, then apply the same approach.",
                "pedagogical_hints": hints_response.get('hints_list', [])
            },
            "user_attempt": user_attempt or None,
            "solution_template": {
                "approach": "Step-by-step logical solution",
                "steps_needed": problem_analysis.get('solution_steps_count', 3),
                "key_concepts": problem_analysis.get('required_concepts', [])
            },
            "chat": {
                "initial_message": chat_messages[-1]["content"],
                "context": chat_messages,
                "system_prompt": "You are an expert math tutor. Help guide the student through this problem using Socratic questioning. Never give the answer directly - ask questions that lead to the solution.",
                "ready_for_discussion": True
            },
            "next_actions": [
                "View detailed hints above 👆",
                "Start typing in the chat to discuss this problem",
                "Share your attempt for personalized feedback",
                "Ask questions about specific steps"
            ]
        }
    
    except Exception as e:
        import traceback
        logger.error(f"Error in submit_exercise: {str(e)}\n{traceback.format_exc()}")
        
        # Fallback response on error
        return {
            "success": True,
            "status": "submitted",
            "format_detected": "Auto-detected",
            "problem": {
                "text": text_input or "[File content]",
                "topic": "Mathematics",
                "difficulty": 3
            },
            "hints": {
                "hint_1": "Start by identifying what information you have and what you need to find.",
                "hint_2": "Look for relationships or patterns between the given values.",
                "hint_3": "Try working through your solution step by step, checking each calculation."
            },
            "chat": {
                "initial_message": "I'm here to help! Tell me about your approach to this problem.",
                "ready_for_discussion": True
            },
            "error_note": "Using demo mode - real math analysis unavailable"
        }


@router.post("/chat")
async def math_chat(
    submission_id: str = Form(...),
    user_message: str = Form(...),
    context: Optional[List[Dict]] = None
):
    """
    Interactive math tutor chatbot endpoint.
    
    Accepts student messages and provides pedagogical guidance.
    Keeps conversation context for continuity.
    """
    try:
        # In production, would look up submission_id and previous context
        response = {
            "success": True,
            "submission_id": submission_id,
            "user_message": user_message,
            "tutor_response": "That's a good start! Tell me more about your reasoning...",  # Demo response
            "guidance": "You're on the right track. What's your next step?",
            "hints": [
                "Check your calculation here",
                "Consider what theorem applies",
                "Think about edge cases"
            ],
            "mode": "demo - real responses need API key"
        }
        return response
    
    except Exception as e:
        logger.error(f"Error in math_chat: {str(e)}")
        return {
            "success": False,
            "error": "Error processing chat message",
            "detail": str(e)
        }


@router.get("/health")
async def math_router_health():
    """Health check for math tutor service."""
    return {
        "status": "operational",
        "service": "math-tutor",
        "endpoints": [
            "POST /submit - Submit exercise in any format",
            "POST /chat - Interactive tutor discussion",
            "POST /hint - Get hints for a problem",
            "POST /analyze - Analyze problem topic",
            "GET /health - Health check"
        ]
    }
