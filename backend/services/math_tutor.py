"""
Adaptive Math Tutor with Step Validation & Reasoning Verification
Uses Mistral Large 3 for logical consistency checking and pedagogical guidance
"""

import os
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Initialize Mistral client with error handling
api_key = os.environ.get("MISTRAL_API_KEY", "").strip()
if not api_key:
    logger.warning("⚠️ MISTRAL_API_KEY not found in environment - Math Tutor will use demo fallback")
    client = None
else:
    try:
        from mistralai import Mistral
        client = Mistral(api_key=api_key)
        logger.info("✓ Mistral client initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize Mistral client: {e}")
        client = None

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
        if not client:
            logger.warning("Mistral client not available, using demo mode for problem analysis")
            return {
                "topic": "Advanced Mathematics",
                "subtopic": "Number Theory & Analysis",
                "difficulty": 4,
                "required_concepts": ["Dirichlet's Pigeonhole Principle", "Weyl's Equidistribution", "Irrational Numbers"],
                "problem_summary": problem_text[:150],
                "first_question": "Can you explain what it means for a set to be dense in [0,1]?",
                "solution_steps_count": "3-4",
                "mode": "demo"
            }
        
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
            "error": str(e),
            "mode": "fallback"
        }


async def validate_step(problem_text: str, step_number: int, student_step: str, context: str = "") -> Dict:
    """
    Validate a student's mathematical step and provide feedback.
    """
    try:
        if not client:
            logger.warning("Mistral client not available, using demo mode for step validation")
            return {
                "is_correct": True,
                "error_type": "none",
                "confidence": 0.8,
                "explanation": "Your step appears mathematically sound. You're on the right track!",
                "hint": "",
                "next_question": "What's your reasoning for this step? Can you explain it?",
                "reasoning_quality_score": 8,
                "suggestion": "",
                "mode": "demo"
            }
        
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
            "reasoning_quality_score": 0,
            "mode": "fallback"
        }


async def generate_solution(problem_text: str, student_solution: str) -> Dict:
    """
    Generate complete solution with LaTeX and conceptual summary.
    """
    try:
        if not client:
            logger.warning("Mistral client not available, using demo mode for solution generation")
            return {
                "full_solution": f"Your solution approach: {student_solution}\n\nMathematical Solution:\nLet α be irrational.\nBy Dirichlet's Pigeonhole Principle, for any N, there exist integers m, n with 1 ≤ n ≤ N such that |mα - n| < 1/N.\nThis means {mα} < 1/N, so the fractional part gets arbitrarily close to 0.\nSimilarly, by considering the sequence {nα} for n = 1, 2, ..., N, we can make {nα} approach any value in [0,1).\nBy Weyl's Equidistribution Theorem, the sequence {nα} is equidistributed modulo 1.\nTherefore, the fractional parts {nα} are dense in [0,1].",
                "latex_solution": "\\[\\text{Given } \\alpha \\text{ irrational, we prove } \\{n\\alpha\\} \\text{ is dense in } [0,1]\\]\n\\[\\text{Step 1: Apply Dirichlet's Principle}\\]\n\\[\\forall N \\in \\mathbb{N}, \\exists m,n: |m\\alpha - n| < \\frac{1}{N}\\]\n\\[\\text{Step 2: Consequence for fractional parts}\\]\n\\[\\{m\\alpha\\} < \\frac{1}{N} \\text{ or } \\{m\\alpha\\} > 1 - \\frac{1}{N}\\]\n\\[\\text{Step 3: Apply Weyl's Equidistribution}\\]\n\\[\\text{Sequence } \\{n\\alpha\\} \\text{ is equidistributed modulo } 1\\]\n\\[\\boxed{\\text{Therefore, } \\{n\\alpha\\} \\text{ is dense in } [0,1]}\\]",
                "final_answer": "The fractional parts {nα} of an irrational α are dense in [0,1]",
                "key_concepts": ["Dirichlet Pigeonhole Principle", "Weyl Equidistribution Theorem", "Irrational Approximation"],
                "common_mistakes": ["Confusing density with measure", "Missing the modular arithmetic step"],
                "conceptual_summary": ["The result shows how irrational multiples distribute uniformly", "It combines combinatorial and analytic arguments"],
                "recommended_exercises": [{"topic": "Equidistribution", "difficulty": "Advanced", "description": "Prove using three-distance theorem"}],
                "mastery_score": 0.85,
                "learning_insights": "Beautiful result demonstrating the Pigeonhole Principle with number theory",
                "mode": "demo"
            }
        
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
            "learning_insights": "Could not generate analysis",
            "mode": "fallback"
        }


async def generate_practice_problem(topic: str, difficulty: int) -> Dict:
    """
    Generate a similar practice problem based on topic and difficulty.
    """
    try:
        if not client:
            logger.warning("Mistral client not available, using demo mode for practice problem generation")
            return {
                "problem": f"Generate a proof that for an irrational number α, the sequence {{nα}} is dense in [0,1]",
                "hint_sequence": [
                    "Start with the definition of density: for any ε > 0 and any point in [0,1], can you find a point in {nα}?",
                    "Consider using the Pigeonhole Principle with N intervals",
                    "Think about how Dirichlet's Approximation Theorem might help"
                ],
                "solution_overview": "Use Dirichlet's Pigeonhole Principle to show {nα} gets arbitrarily close to any point. Then apply Weyl's Equidistribution to show the sequence visits all regions uniformly.",
                "mode": "demo"
            }
        
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
            "error": str(e),
            "mode": "fallback"
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
