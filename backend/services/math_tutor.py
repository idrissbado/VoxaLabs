"""
Adaptive Math Tutor with Step Validation & Reasoning Verification
Uses MathΣtral (via Mistral API) for expert mathematical problem solving and pedagogical guidance
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

MATH_TUTOR_SYSTEM = """You are MathΣtral, an expert mathematical reasoning AI specialized in:
- Algebra, Geometry, Trigonometry, Calculus, Linear Algebra, Differential Equations, Abstract Algebra
- Problem classification and difficulty assessment
- Pedagogical guidance and sophisticated error detection
- Step-by-step validation of mathematical reasoning with deep conceptual understanding
- Generating clean, publication-quality LaTeX mathematical notation

Your approach:
1. NEVER solve the problem immediately in basic contexts
2. Guide students through logical progression with Socratic method
3. Validate each step for algebraic AND conceptual correctness
4. Detect and explain errors without giving solutions prematurely
5. Provide hints that guide toward the answer without spoiling
6. Provide full solution ONLY after student completion
7. When providing hints: consider difficulty level 1-5 (1=beginner, 5=expert)

Output STRICTLY as valid JSON with no markdown formatting or code blocks.

When validating steps:
- Check algebraic correctness rigorously
- Detect conceptual misunderstandings
- Identify common mistake patterns
- Provide targeted pedagogical hints
- Suggest alternative approaches when applicable

When complete, provide:
- Complete written solution with all steps
- Clean LaTeX formatted solution (publication quality)
- Key concepts involved
- Common mistakes to avoid
- Conceptual insights
- Recommended similar practice problems with difficulty levels
- Mastery score (0.0-1.0) based on student's approach quality
- Learning insights about the student's mathematical reasoning"""

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
            model="mathstral-7b",
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
        error_msg = str(e)
        logger.error(f"✗ Error analyzing problem: {error_msg}")
        
        # If 401 Unauthorized, return demo data
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Math Tutor using demo mode")
            return {
                "topic": "Advanced Mathematics",
                "subtopic": "Number Theory & Analysis",
                "difficulty": 4,
                "required_concepts": ["Logic", "Proof Structure", "Problem Solving"],
                "problem_summary": problem_text[:150],
                "first_question": "Can you rewrite this problem in your own words?",
                "solution_steps_count": "3-4",
                "mode": "demo"
            }
        
        # For other errors, return fallback
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
            model="mathstral-7b",
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
        error_msg = str(e)
        logger.error(f"✗ Error validating step: {error_msg}")
        
        # If 401 Unauthorized, return demo feedback
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Math Tutor using demo mode")
            return {
                "is_correct": True,
                "error_type": "none",
                "confidence": 0.8,
                "explanation": "Your step appears correct. Good work!",
                "hint": "",
                "next_question": "Can you explain your reasoning?",
                "reasoning_quality_score": 7,
                "suggestion": "",
                "mode": "demo"
            }
        
        # For other errors
        return {
            "is_correct": False,
            "error_type": "error",
            "confidence": 0,
            "explanation": "Could not validate step",
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
            model="mathstral-7b",
            messages=[
                {
                    "role": "system",
                    "content": MATH_TUTOR_SYSTEM
                },
                {
                    "role": "user",
                    "content": f"""The student completed this math problem:

PROBLEM: {problem_text}

Student's solution process: {student_solution}

Generate the COMPLETE mathematical solution with detailed steps and explanations. 
Output as JSON:
{{
  "full_solution": "Complete step-by-step written solution with all work shown",
  "latex_solution": "Publication-quality LaTeX solution: each step numbered with \\n separators, final answer in \\boxed{{}}",
  "final_answer": "The concise final answer",
  "key_concepts": ["concept1", "concept2", "concept3"],
  "common_mistakes": ["mistake1", "mistake2"],
  "conceptual_summary": ["insight1", "insight2"],
  "recommended_exercises": [{{"topic": "Related topic", "difficulty": 1-5, "description": "similar problem"}}],
  "mastery_score": 0.0-1.0,
  "learning_insights": "Observations about the student's mathematical approach"
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
        error_msg = str(e)
        logger.error(f"✗ Error generating solution: {error_msg}")
        
        # If 401 Unauthorized, return demo solution
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Math Tutor using demo mode")
            return {
                "full_solution": "Complete step-by-step solution (demo mode)",
                "latex_solution": r"\[\text{Solution Steps:} \\ \text{Step 1: Identify the pattern} \\ \text{Step 2: Apply the formula} \\ \boxed{\text{Final Answer}}\]",
                "final_answer": "Solution available in demo mode",
                "key_concepts": ["Problem Analysis", "Solution Strategy"],
                "common_mistakes": ["Skipping steps", "Calculation errors"],
                "conceptual_summary": ["This problem demonstrates important mathematical principles"],
                "recommended_exercises": [{"topic": "Similar Problems", "difficulty": "intermediate", "description": "Practice more problems like this"}],
                "mastery_score": 0.75,
                "learning_insights": "Good attempt - keep practicing!",
                "mode": "demo"
            }
        
        # For other errors
        return {
            "full_solution": "Could not generate solution",
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
            model="mathstral-7b",
            messages=[
                {
                    "role": "system",
                    "content": "You are MathΣtral, an expert mathematics problem generator. Generate challenging, well-structured problems."
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
        error_msg = str(e)
        logger.error(f"✗ Error generating practice problem: {error_msg}")
        
        # If 401 Unauthorized, return demo problem
        if "401" in error_msg or "Unauthorized" in error_msg:
            logger.warning("⚠️ 401 Unauthorized - Math Tutor using demo mode")
            return {
                "problem": f"Practice Problem ({topic}): Solve a similar problem on this topic",
                "hint_sequence": [
                    "What concepts from the original problem apply here?",
                    "Can you identify the key steps?",
                    "What patterns do you notice?"
                ],
                "solution_overview": "Follow the same approach as the original problem",
                "mode": "demo"
            }
        
        # For other errors
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
        # Request LaTeX formatting from MathΣtral
        response = client.chat.complete(
            model="mathstral-7b",
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


async def generate_hint(problem_text: str, student_progress: str = "") -> Dict:
    """
    Generate a pedagogical hint using MathΣtral.
    Does NOT give away the answer.
    """
    try:
        if not client:
            logger.warning("Mistral client not available, using demo hint")
            return {
                "hint": "Try breaking the problem into smaller parts. What's the first thing you need to find?",
                "hint_level": 1,
                "guidance": "Focus on identifying the key variables and what they represent",
                "next_steps": ["Identify all given information", "Write down what you need to find", "Recall relevant formulas"],
                "common_error_to_avoid": "Jumping to the answer without understanding the problem structure",
                "mode": "demo"
            }
        
        prompt = f"""Generate a PEDAGOGICAL HINT for this math problem.
CRITICAL: Do NOT solve or give away the answer!

PROBLEM: {problem_text}

{f'Student progress so far: {student_progress}' if student_progress else 'Student just started'}

Output as JSON:
{{
  "hint": "A guiding sentence that helps without revealing the solution",
  "hint_level": 1-5 (1=very basic, 5=almost there),
  "guidance": "Brief strategy to use",
  "next_steps": ["step1", "step2", "step3"],
  "common_error_to_avoid": "One common mistake students make here"
}}"""

        response = client.chat.complete(
            model="mathstral-7b",
            messages=[
                {
                    "role": "system",
                    "content": MATH_TUTOR_SYSTEM
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        content = response.choices[0].message.content
        
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(content)
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error generating hint: {error_msg}")
        if "401" in error_msg or "Unauthorized" in error_msg:
            return {
                "hint": "Review the problem statement carefully and identify what information is given and what you need to find",
                "hint_level": 2,
                "guidance": "Start by listing all known values and what you're solving for",
                "next_steps": ["List all given information", "Identify the target variable", "Look for a relevant formula or theorem"],
                "common_error_to_avoid": "Don't jump to the answer without showing all work",
                "demo_mode": True
            }
        raise


async def generate_downloadable_solution(problem_text: str, solution_data: Dict, format_type: str = "markdown") -> Dict:
    """
    Generate solution in downloadable format (markdown, latex, or json).
    Formats: 'markdown', 'latex', 'html'
    """
    try:
        solution_text = solution_data.get("full_solution", "")
        latex_solution = solution_data.get("latex_solution", "")
        final_answer = solution_data.get("final_answer", "")
        
        if format_type.lower() == "latex":
            # Return LaTeX formatted solution
            return {
                "format": "latex",
                "content": latex_solution or solution_text,
                "filename": "solution.tex",
                "mime_type": "text/plain"
            }
        
        elif format_type.lower() == "markdown":
            # Convert to Markdown format
            markdown_content = f"""# Mathematical Solution

## Problem
{problem_text}

## Solution
{solution_text}

## Final Answer
**{final_answer}**

### Key Concepts
{chr(10).join(f"- {concept}" for concept in solution_data.get("key_concepts", []))}

### Common Mistakes to Avoid
{chr(10).join(f"- {mistake}" for mistake in solution_data.get("common_mistakes", []))}

### Recommended Practice
{chr(10).join(f"- {exc.get('description', '')} (Difficulty: {exc.get('difficulty', '')})" for exc in solution_data.get("recommended_exercises", []))}

---
*Generated by VoxaLab Math Tutor*
"""
            return {
                "format": "markdown",
                "content": markdown_content,
                "filename": "solution.md",
                "mime_type": "text/markdown"
            }
        
        elif format_type.lower() == "html":
            # Convert to HTML format with styling
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Math Solution</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 20px; }}
        .problem {{ background: #ecf0f1; padding: 15px; border-left: 4px solid #3498db; margin: 15px 0; }}
        .solution {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #27ae60; margin: 15px 0; }}
        .answer {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0; font-weight: bold; }}
        ul {{ margin: 10px 0; padding-left: 20px; }}
        li {{ margin: 8px 0; }}
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <h1>Mathematical Solution</h1>
    
    <div class="problem">
        <h2>Problem</h2>
        <p>{problem_text}</p>
    </div>
    
    <div class="solution">
        <h2>Solution</h2>
        <p>{solution_text.replace(chr(10), '<br>')}</p>
    </div>
    
    <div class="answer">
        <h2>Final Answer</h2>
        <p>{final_answer}</p>
    </div>
    
    <h2>Key Concepts</h2>
    <ul>
        {chr(10).join(f"<li>{concept}</li>" for concept in solution_data.get("key_concepts", []))}
    </ul>
    
    <h2>Common Mistakes to Avoid</h2>
    <ul>
        {chr(10).join(f"<li>{mistake}</li>" for mistake in solution_data.get("common_mistakes", []))}
    </ul>
    
    <h2>Recommended Practice Problems</h2>
    <ul>
        {chr(10).join(f"<li>{exc.get('description', '')} (Difficulty: {exc.get('difficulty', '')})</li>" for exc in solution_data.get("recommended_exercises", []))}
    </ul>
    
    <hr>
    <p style="color: #7f8c8d; font-size: 12px;">Generated by VoxaLab Math Tutor</p>
</body>
</html>"""
            return {
                "format": "html",
                "content": html_content,
                "filename": "solution.html",
                "mime_type": "text/html"
            }
        
        else:
            # Default JSON format
            return {
                "format": "json",
                "content": json.dumps(solution_data, indent=2),
                "filename": "solution.json",
                "mime_type": "application/json"
            }
    
    except Exception as e:
        logger.error(f"Error generating downloadable solution: {e}")
        raise
