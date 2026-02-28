"""
Adaptive Math Tutor with Step Validation & Reasoning Verification
Uses Mistral Large 3 for logical consistency checking and pedagogical guidance
"""

import os
import json
import logging
from mistralai import Mistral
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Initialize Mistral client
api_key = os.environ.get("MISTRAL_API_KEY", "")
client = Mistral(api_key=api_key)

MATH_TUTOR_SYSTEM = """You are an advanced mathematical reasoning tutor with expertise in:
- Algebra, Geometry, Trigonometry, Calculus, Linear Algebra
- Problem classification and difficulty assessment
- Pedagogical guidance and error detection
- Step-by-step validation of mathematical reasoning

Your approach:
1. NEVER solve the problem immediately
2. Guide students through logical progression
3. Validate each step for correctness (algebraic and conceptual)
4. Detect and explain errors without giving solutions
5. Provide hints that guide toward the answer
6. Only provide full solution after student completion

Output STRICTLY as valid JSON with no markdown formatting or code blocks.

When validating steps:
- Check algebraic correctness
- Detect conceptual misunderstandings
- Identify common mistake patterns
- Provide targeted hints

When complete, provide:
- Clean LaTeX formatted solution
- Conceptual summary
- Similar practice problems"""

LATEX_GENERATOR_PROMPT = """You are a LaTeX formatting expert. Convert mathematical solutions into clean, properly formatted LaTeX.

Requirements:
- Use \\( ... \\) for inline math
- Use \\[ ... \\] for display math
- Properly format fractions, exponents, roots, Greek letters
- Include step-by-step solution with numbering
- Box the final answer using \\boxed{}
- Make output publication-ready

Output valid LaTeX only."""


async def analyze_problem(problem_text: str) -> Dict:
    """
    Analyze a math problem to classify topic, difficulty, and concepts needed.
    """
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "system",
                    "content": MATH_TUTOR_SYSTEM
                },
                {
                    "role": "user",
                    "content": f"""Analyze this math problem and provide initial guidance:

PROBLEM: {problem_text}

Respond with JSON:
{{
  "topic": "Topic name (Algebra, Calculus, etc.)",
  "subtopic": "Specific area",
  "difficulty": 1-5,
  "required_concepts": ["concept1", "concept2"],
  "problem_summary": "Brief problem description",
  "first_question": "Your first guiding question to start the student",
  "solution_steps_count": "Number of steps expected"
}}"""
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON response
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
            return analysis
        
        return {
            "topic": "Mathematics",
            "subtopic": "General",
            "difficulty": 3,
            "required_concepts": [],
            "problem_summary": problem_text[:100],
            "first_question": "What approach would you use to solve this?",
            "solution_steps_count": "Multiple"
        }
    except Exception as e:
        logger.error(f"Error analyzing problem: {e}")
        return {
            "topic": "Mathematics",
            "subtopic": "General",
            "difficulty": 3,
            "required_concepts": [],
            "problem_summary": problem_text[:100],
            "first_question": "What is your first step?",
            "solution_steps_count": "Unknown",
            "error": str(e)
        }


async def validate_step(problem_text: str, step_number: int, student_step: str, context: str = "") -> Dict:
    """
    Validate a student's mathematical step and provide feedback.
    """
    try:
        validation_prompt = f"""The student is working on this problem:
PROBLEM: {problem_text}

This is step {step_number} of their solution.

Previous context: {context if context else "None yet"}

Student's step: {student_step}

Validate this step and respond with JSON:
{{
  "is_correct": true/false,
  "error_type": "none|algebraic|conceptual|notation|logical",
  "confidence": 0.0-1.0,
  "explanation": "Explanation of correctness or error",
  "hint": "Hint if incorrect (not full solution)",
  "next_question": "Question to guide next step",
  "reasoning_quality_score": 1-10,
  "suggestion": "What to try instead (if wrong)"
}}"""

        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "system",
                    "content": MATH_TUTOR_SYSTEM
                },
                {
                    "role": "user",
                    "content": validation_prompt
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            feedback = json.loads(json_match.group())
            return feedback
        
        return {
            "is_correct": False,
            "error_type": "validation_error",
            "confidence": 0.5,
            "explanation": "Could not validate step",
            "hint": "Please restate your step more clearly",
            "next_question": "Try again",
            "reasoning_quality_score": 0
        }
    except Exception as e:
        logger.error(f"Error validating step: {e}")
        return {
            "is_correct": False,
            "error_type": "error",
            "confidence": 0,
            "explanation": f"Error: {str(e)}",
            "hint": "Try a different approach",
            "next_question": "What's your next step?",
            "reasoning_quality_score": 0
        }


async def generate_solution(problem_text: str, student_solution: str) -> Dict:
    """
    Generate complete solution with LaTeX and conceptual summary.
    """
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "system",
                    "content": MATH_TUTOR_SYSTEM
                },
                {
                    "role": "user",
                    "content": f"""The student completed this problem:

PROBLEM: {problem_text}

Student's solution process: {student_solution}

Now provide the complete solution with JSON:
{{
  "full_solution": "Complete written solution",
  "latex_solution": "LaTeX formatted solution with step-by-step work and final answer boxed",
  "final_answer": "The final answer",
  "key_concepts": ["concept1", "concept2"],
  "common_mistakes": ["mistake1", "mistake2"],
  "conceptual_summary": ["summary point 1", "summary point 2"],
  "recommended_exercises": [
    {{"topic": "Similar topic", "difficulty": "level", "description": "Exercise description"}}
  ],
  "mastery_score": 0.0-1.0,
  "learning_insights": "Observations about student's reasoning"
}}"""
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            solution = json.loads(json_match.group())
            return solution
        
        return {
            "full_solution": "Solution generation in progress",
            "latex_solution": "",
            "final_answer": "",
            "key_concepts": [],
            "common_mistakes": [],
            "conceptual_summary": [],
            "recommended_exercises": [],
            "mastery_score": 0.5,
            "learning_insights": "Analysis in progress"
        }
    except Exception as e:
        logger.error(f"Error generating solution: {e}")
        return {
            "full_solution": f"Error: {str(e)}",
            "latex_solution": "",
            "final_answer": "",
            "key_concepts": [],
            "common_mistakes": [],
            "conceptual_summary": [],
            "recommended_exercises": [],
            "mastery_score": 0,
            "learning_insights": "Could not generate analysis"
        }


async def generate_practice_problem(topic: str, difficulty: int) -> Dict:
    """
    Generate a similar practice problem based on topic and difficulty.
    """
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "system",
                    "content": "You are a mathematics problem generator."
                },
                {
                    "role": "user",
                    "content": f"""Generate a {difficulty}/5 difficulty math problem on {topic}.

Respond with JSON:
{{
  "problem": "The problem statement",
  "hint_sequence": ["hint1", "hint2"],
  "solution_overview": "Brief solution outline"
}}"""
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            problem = json.loads(json_match.group())
            return problem
        
        return {
            "problem": "Problem generation in progress",
            "hint_sequence": [],
            "solution_overview": ""
        }
    except Exception as e:
        logger.error(f"Error generating practice problem: {e}")
        return {
            "problem": "Could not generate problem",
            "hint_sequence": [],
            "solution_overview": "",
            "error": str(e)
        }


def format_latex_solution(solution_text: str) -> str:
    """
    Ensure solution is properly formatted as LaTeX.
    """
    try:
        # Request LaTeX formatting from Mistral
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "system",
                    "content": LATEX_GENERATOR_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Format this mathematical solution as clean LaTeX:\n\n{solution_text}"
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error formatting LaTeX: {e}")
        return solution_text
