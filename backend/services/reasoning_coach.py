"""
Interactive Mathematical Reasoning Coach
Validates each step of student work, detects errors, provides adaptive hints
"""

import os
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Initialize Mistral client - Try real API, fall back to demo if unavailable
try:
    from mistralai import Mistral
    api_key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if api_key:
        client = Mistral(api_key=api_key)
        logger.info("✓ Mistral client initialized for reasoning coach with mathstral-7b")
    else:
        logger.warning("⚠️ MISTRAL_API_KEY not set - Using demo mode")
        client = None
except Exception as e:
    logger.warning(f"⚠️ Failed to initialize Mistral, using demo mode: {e}")
    client = None

REASONING_COACH_SYSTEM = """You are MathΣtral Reasoning Coach, an expert mathematical tutor specialized in:
- Problem classification and difficulty assessment
- Step-by-step solution validation
- Error detection (algebraic, logical, conceptual)
- Adaptive pedagogical guidance
- Structured multi-turn reasoning

Your philosophy:
1. NEVER solve problems immediately
2. Guide students through structured reasoning
3. Validate each step rigorously
4. Detect error types precisely
5. Provide hints that guide without spoiling
6. Only reveal full solution after guided interaction

Output STRICTLY as valid JSON with no markdown formatting."""


async def classify_problem(problem_text: str) -> Dict:
    """
    Classify a math problem and return metadata for the reasoning session.
    Uses Mistral mathstral-7b for intelligent analysis.
    """
    try:
        if not client:
            logger.info("Using demo problem classification")
            return {
                "topic": "Mathematics",
                "subtopic": "Problem-Solving",
                "difficulty": 3,
                "required_concepts": ["Logical reasoning", "Problem analysis"],
                "solution_steps": 5,
                "first_question": "What type of problem is this and what information are we given?",
                "mode": "demo"
            }
        
        prompt = f"""Classify this math problem:

PROBLEM: {problem_text}

Provide:
1. Topic (e.g., Algebra, Calculus, Linear Algebra, etc.)
2. Subtopic
3. Difficulty (1-5, where 5 is graduate level)
4. Required concepts (list 3-5 key concepts)
5. Estimated number of steps to solve
6. The FIRST question to ask the student (open-ended, guiding question)

Output as JSON:
{{
  "topic": "...",
  "subtopic": "...",
  "difficulty": 3,
  "required_concepts": ["concept1", "concept2", "concept3"],
  "solution_steps": 5,
  "first_question": "Open-ended question that guides without solving"
}}"""

        response = client.chat.complete(
            model="mathstral-7b",
            messages=[
                {"role": "system", "content": REASONING_COACH_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        content = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            logger.info(f"✓ Problem classified by Mistral: {result.get('topic')}")
            return result
        return json.loads(content)
    
    except Exception as e:
        logger.warning(f"Error classifying problem, using demo: {e}")
        return {
            "topic": "Mathematics",
            "subtopic": "Problem-Solving",
            "difficulty": 3,
            "required_concepts": ["Logical reasoning", "Problem analysis"],
            "solution_steps": 5,
            "first_question": "What type of problem is this and what information are we given?",
            "mode": "demo"
        }


async def validate_step(
    problem_text: str,
    step_number: int,
    student_answer: str,
    context: List[Dict] = None
) -> Dict:
    """
    Validate a student's submitted step using Mistral mathstral-7b.
    Returns: correctness, error type, explanation, next hint level
    """
    try:
        if not client:
            logger.info("Using demo step validation")
            return {
                "is_correct": True,
                "confidence": 0.85,
                "explanation": "Your approach looks correct. Let's continue to the next step.",
                "error_type": None,
                "justification": "Your reasoning follows logically from the problem setup.",
                "next_action": "request_next_step",
                "mode": "demo"
            }
        
        context_text = ""
        if context:
            context_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context[-3:]])
        
        context_section = f"CONTEXT SO FAR:\n{context_text}" if context_text else ""
        
        prompt = f"""You are validating a student's work on a math problem.

PROBLEM: {problem_text}

STEP NUMBER: {step_number}

STUDENT'S ANSWER/WORK:
{student_answer}

{context_section}

Validate this step:
1. Is it mathematically correct? (yes/no)
2. Error type if wrong: 'algebraic', 'logical', 'conceptual', 'incomplete', 'notation', or 'none'
3. Clear explanation of why it's correct or what's wrong
4. Justification using specific math principles
5. Next action: 'request_next_step', 'provide_hint', 'request_revision'

Output as JSON:
{{
  "is_correct": true,
  "confidence": 0.95,
  "explanation": "Clear explanation",
  "error_type": "none",
  "justification": "Why this is correct/incorrect using math principles",
  "next_action": "request_next_step"
}}"""

        response = client.chat.complete(
            model="mathstral-7b",
            messages=[
                {"role": "system", "content": REASONING_COACH_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600
        )
        
        content = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            logger.info(f"✓ Step {step_number} validated by Mistral: correct={result.get('is_correct')}")
            return result
        return json.loads(content)
    
    except Exception as e:
        logger.warning(f"Error validating step, using demo: {e}")
        return {
            "is_correct": True,
            "confidence": 0.7,
            "explanation": "Your work appears correct. Continue to the next step.",
            "error_type": None,
            "justification": "Reasoning follows logically",
            "next_action": "request_next_step",
            "mode": "demo"
        }


async def generate_adaptive_hint(
    problem_text: str,
    step_number: int,
    current_attempt: str,
    hint_level: int = 1,
    context: List[Dict] = None
) -> Dict:
    """
    Generate a hint appropriate to the hint level.
    Level 1: Small nudge
    Level 2: Concept reminder
    Level 3: Structural guidance
    Level 4: Partial reveal (almost the answer)
    """
    try:
        hint_guidance = {
            1: "Provide a small nudge without revealing the approach",
            2: "Remind them of the key concept or theorem needed",
            3: "Guide them toward the structural approach without calculation",
            4: "Almost give away the answer - guide to the final step"
        }
        
        if not client:
            logger.info(f"Using demo hint level {hint_level}")
            demo_hints = {
                1: "Think about what information you have and what you need to find.",
                2: "Remember the key mathematical principle or formula for this type of problem.",
                3: "Consider breaking this down into smaller steps - what's the logical structure?",
                4: "You're very close - just complete the final calculation or simplification."
            }
            return {
                "hint": demo_hints.get(hint_level, "Continue working through this systematically."),
                "guidance": hint_guidance.get(hint_level, ""),
                "direction": "Move toward the solution step by step",
                "hint_level": hint_level,
                "mode": "demo"
            }
        
        prompt = f"""Generate a LEVEL {hint_level} hint for a student stuck on a math problem.

PROBLEM: {problem_text}
STEP: {step_number}
STUDENT'S ATTEMPT: {current_attempt}

HINT GUIDANCE: {hint_guidance.get(hint_level, 'Provide helpful guidance')}

Generate a hint that:
- Is appropriate to level {hint_level}
- Guides toward the solution without spoiling
- References specific mathematical principles

Output as JSON:
{{
  "hint": "The actual hint text",
  "guidance": "Brief strategic guidance",
  "direction": "What direction to move in"
}}"""

        response = client.chat.complete(
            model="mathstral-7b",
            messages=[
                {"role": "system", "content": REASONING_COACH_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=400
        )
        
        content = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            hint_data = json.loads(json_match.group())
            hint_data["hint_level"] = hint_level
            logger.info(f"✓ Level {hint_level} hint generated by Mistral")
            return hint_data
        
        result = json.loads(content)
        result["hint_level"] = hint_level
        return result
    
    except Exception as e:
        logger.warning(f"Error generating hint, using demo: {e}")
        demo_hints = {
            1: "Think about what information you have and what you need to find.",
            2: "Remember the key mathematical principle or formula for this type of problem.",
            3: "Consider breaking this down into smaller steps - what's the logical structure?",
            4: "You're very close - just complete the final calculation or simplification."
        }
        return {
            "hint": demo_hints.get(hint_level, "Continue systematically"),
            "guidance": "Keep working through the problem",
            "direction": "Step by step",
            "hint_level": hint_level,
            "mode": "demo"
        }


async def generate_final_solution(
    problem_text: str,
    steps_history: List[Dict]
) -> Dict:
    """
    Generate complete step-by-step solution using Mistral with LaTeX formatting.
    """
    try:
        if not client:
            logger.info("Using demo solution generation")
            return {
                "solution_steps": [
                    {"step": 1, "description": "Understand the problem and identify what we need to find", "latex": ""},
                    {"step": 2, "description": "Gather the given information", "latex": ""},
                    {"step": 3, "description": "Choose the appropriate approach or formula", "latex": ""},
                    {"step": 4, "description": "Apply the method step by step", "latex": ""},
                    {"step": 5, "description": "Verify the answer makes sense", "latex": ""}
                ],
                "final_answer": "Solution completed",
                "final_answer_latex": "\\text{Answer}",
                "concepts_used": ["Problem-solving", "Mathematical reasoning"],
                "common_mistakes": ["Skipping steps", "Not verifying answers"],
                "practice_problems": ["Practice problem 1", "Practice problem 2"],
                "mode": "demo"
            }
        
        steps_context = "\n".join([f"Step {s.get('number', '?')}: {s.get('work', '')}" for s in steps_history])
        
        prompt = f"""Generate a complete mathematical solution with LaTeX formatting.

PROBLEM: {problem_text}

STUDENT'S WORK HISTORY:
{steps_context}

Provide:
1. Complete step-by-step solution (5-8 steps)
2. Final answer with LaTeX
3. Key concepts used
4. Common mistakes to avoid
5. Two similar practice problems

Output as JSON:
{{
  "solution_steps": [
    {{"step": 1, "description": "...", "latex": "..."}},
    ...
  ],
  "final_answer": "Plain text answer",
  "final_answer_latex": "\\\\boxed{{answer}}",
  "concepts_used": ["concept1", "concept2"],
  "common_mistakes": ["mistake1", "mistake2"],
  "practice_problems": ["problem1", "problem2"]
}}"""

        response = client.chat.complete(
            model="mathstral-7b",
            messages=[
                {"role": "system", "content": REASONING_COACH_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1200
        )
        
        content = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            logger.info(f"✓ Complete solution generated by Mistral")
            return result
        return json.loads(content)
    
    except Exception as e:
        logger.warning(f"Error generating solution, using demo: {e}")
        return {
            "solution_steps": [
                {"step": 1, "description": "Work through systematically", "latex": ""}
            ],
            "final_answer": "Solution complete",
            "final_answer_latex": "\\text{Answer}",
            "concepts_used": ["Mathematical reasoning"],
            "common_mistakes": ["Not verifying work"],
            "practice_problems": ["Try similar problems"],
            "mode": "demo"
        }


async def detect_completion(
    problem_text: str,
    steps_history: List[Dict]
) -> Dict:
    """
    Determine if the student has completed the solution logically using Mistral.
    """
    try:
        if not client:
            logger.info("Using demo completion detection")
            return {
                "is_complete": False,
                "progress": 60,
                "next_step": "Continue with the next logical step in your solution",
                "mode": "demo"
            }
        
        steps_summary = "\n".join([f"Step {s.get('number', '?')}: {s.get('work', '')[:100]}" for s in steps_history])
        
        prompt = f"""Evaluate if a student has completed solving a math problem.

PROBLEM: {problem_text}

STEPS COMPLETED:
{steps_summary}

Determine:
1. Is the solution mathematically complete?
2. Progress percentage (0-100)
3. What's needed to finish (if incomplete)

Output as JSON:
{{
  "is_complete": true,
  "progress": 85,
  "next_step": "Verify the final answer and conclude"
}}"""

        response = client.chat.complete(
            model="mathstral-7b",
            messages=[
                {"role": "system", "content": REASONING_COACH_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        content = response.choices[0].message.content
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            logger.info(f"✓ Completion detected by Mistral: {result.get('progress')}%")
            return result
        return json.loads(content)
    
    except Exception as e:
        logger.warning(f"Error detecting completion, using demo: {e}")
        return {
            "is_complete": False,
            "progress": 50,
            "next_step": "Continue working through the problem step by step",
            "mode": "demo"
        }
