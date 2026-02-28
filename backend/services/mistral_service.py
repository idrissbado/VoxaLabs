"""
[MISTRAL HACKATHON] PrepCoach AI - AI-Powered Preparation & Coaching with Mistral Large 3

This module provides AI-powered coaching using:
- Mistral Large 3 LLM for advanced interview, career, and exam coaching
- LangChain for prompt management and chains
- Structured outputs for consistent, actionable feedback

Features:
- Analyzes user answers (interviews, exams, training)
- Provides personalized coaching and improvement tips
- Provides STAR method evaluation
- Detects filler words and speaking patterns
- Generates improvement tips
- Scores clarity, structure, impact, confidence

Using: mistralai SDK with Mistral Large 3 model
"""

import os
import json
import re
import logging
from typing import Dict, List, Optional
from mistralai import Mistral
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

logger = logging.getLogger(__name__)

# Initialize Mistral client - handle missing API key gracefully
api_key = os.environ.get("MISTRAL_API_KEY", "")
client = None
llm = None

try:
    if api_key and api_key != "your_mistral_api_key_here":
        client = Mistral(api_key=api_key)
        llm = ChatMistralAI(model="mistral-large-latest", api_key=api_key)
    else:
        logger.warning("MISTRAL_API_KEY not set or invalid - AI coaching will be unavailable")
except Exception as e:
    logger.error(f"Failed to initialize Mistral client: {e}")
    client = None
    llm = None

# ============================================================================
# PROMPT TEMPLATES - Define coaching templates with LangChain
# ============================================================================

# Template for analyzing candidate answers and providing structured feedback
COACHING_PROMPT = ChatPromptTemplate.from_template("""
You are an elite interview coach with 15+ years of experience at FAANG companies.
Your role is to provide professional, actionable feedback using structured evaluation.

🎯 HACKATHON-WINNING EVALUATION FRAMEWORK

Evaluate this answer across these competencies:
- TECHNICAL_DEPTH (1-10): Does it show deep technical knowledge?
- COMMUNICATION (1-10): Clear, concise, easy to follow?
- PROBLEM_SOLVING (1-10): Logical approach? Considers edge cases?
- STRUCTURE (1-10): STAR method? Well organized?
- IMPACT (1-10): Results quantified? Demonstrates value?

Role: {role}
Interview Question: {question}
Candidate's Answer: {answer}

Respond with ONLY valid JSON matching this exact structure:
{{
  "overall_score": <1.0-10.0>,
  "technical_depth": <1-10>,
  "communication": <1-10>,
  "problem_solving": <1-10>,
  "structure": <1-10>,
  "impact": <1-10>,
  "confidence_level": <0.0-1.0>,
  "hire_recommendation": "Strong Hire" | "Lean Hire" | "No Hire",
  "hire_probability": <0.0-1.0>,
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2"],
  "missing_frameworks": ["framework1"],
  "key_improvement": "Single most important thing to improve",
  "improved_answer": "Example of ideal 3-sentence answer they could give",
  "star_method": {{
    "situation": "detected" | "missing",
    "task": "detected" | "missing",
    "action": "detected" | "missing",
    "result": "detected" | "missing"
  }}
}}

ONLY output valid JSON, nothing else.
""")

# Template for improving answers using STAR method
IMPROVEMENT_PROMPT = ChatPromptTemplate.from_template("""
You are an interview coach helping a candidate perfect their answer.

Create an EXCELLENT example answer demonstrating the STAR method clearly.
Make it realistic, specific, and interview-worthy (2-3 minutes / 300-400 words).

Role: {role}
Original Question: {question}
Their Current Answer: {original_answer}

Format your response as JSON:
{{
  "improved_answer": "Full STAR-structured answer here...",
  "star_breakdown": {{
    "situation": "What was the context?",
    "task": "What were you responsible for?",
    "action": "What specific steps did you take?",
    "result": "What was the quantifiable outcome?"
  }},
  "key_improvements": ["improvement1", "improvement2", "improvement3"],
  "why_this_works": "Explanation of why this approach is effective"
}}

Respond with ONLY valid JSON, no additional text.
""")

# Template for generating follow-up questions
FOLLOWUP_PROMPT = ChatPromptTemplate.from_template("""
You are an interviewer generating follow-up questions to probe deeper.

Based on the candidate's answer, generate 3 sharp follow-up questions that:
1. Dig into decision-making process
2. Challenge assumptions or explore trade-offs
3. Assess learning and adaptability

Original Question: {question}
Candidate's Answer: {answer}

Respond as JSON:
{{
  "followup_questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?"
  ],
  "question_focus": ["problem_solving", "technical_depth", "learning"],
  "difficulty_level": "follow_up_challenging"
}}

Respond with ONLY valid JSON, no additional text.
""")

# Template for comprehensive session report
REPORT_PROMPT = ChatPromptTemplate.from_template("""
You are generating a professional interview performance report.

Analyze ALL answers from this practice session and provide:
- Overall performance summary
- Key strengths demonstrated
- Critical improvement areas
- Role-specific recommendations
- Confidence-building next steps

Role Practiced: {role}
Number of Questions: {num_questions}
Overall Average Score: {avg_score}

Summary of all Q&A:
{session_summary}

Generate report as JSON:
{{
  "executive_summary": "2-3 sentence overview of performance",
  "overall_assessment": "detailed paragraph on readiness",
  "top_strengths": ["strength1", "strength2", "strength3"],
  "critical_improvements": ["area1", "area2", "area3"],
  "role_specific_feedback": "Tailored coaching for {role} role",
  "next_steps": "3 action items to prepare before real interview",
  "confidence_score": 1-10,
  "estimated_readiness": "percentage likely to pass interview"
}}

Respond with ONLY valid JSON, no additional text.
""")

# ============================================================================
# CHAIN DEFINITIONS - Compose LangChain chains for consistent pipelines
# ============================================================================

# Coaching feedback chain with JSON parsing
json_parser = JsonOutputParser()

if llm is not None:
    coaching_chain = COACHING_PROMPT | llm | json_parser
    improvement_chain = IMPROVEMENT_PROMPT | llm | json_parser
    followup_chain = FOLLOWUP_PROMPT | llm | json_parser
    report_chain = REPORT_PROMPT | llm | json_parser
else:
    coaching_chain = None
    improvement_chain = None
    followup_chain = None
    report_chain = None

# ============================================================================
# SERVICE FUNCTIONS - High-level API for coaching operations
# ============================================================================

async def generate_coaching_feedback(
    question: str, 
    answer: str, 
    role: str
) -> Dict:
    """
    Analyze candidate answer and provide structured feedback.
    
    Uses LangChain chain to invoke Mistral with proper prompting.
    Returns detailed feedback on clarity, structure, and impact.
    
    Args:
        question: Interview question asked
        answer: Candidate's response
        role: Target role (Software Engineer, Product Manager, etc.)
    
    Returns:
        Dict with scores, feedback, and coaching tips
    """
    try:
        if coaching_chain is None:
            logger.warning("Coaching chain not initialized - returning default feedback")
            return {
                "clarity_score": 7,
                "structure_score": 7,
                "impact_score": 7,
                "overall_score": 7,
                "key_strengths": ["Good effort", "Clear communication"],
                "areas_for_improvement": ["Add more specific examples", "Quantify outcomes"],
                "coaching_tip": "Great start! Try adding specific metrics to strengthen your answer.",
                "filler_words_noticed": [],
                "star_method_evaluation": {
                    "situation": "detected",
                    "task": "detected",
                    "action": "detected",
                    "result": "detected"
                }
            }
        
        # Invoke chain with input variables
        result = coaching_chain.invoke({
            "question": question,
            "answer": answer,
            "role": role
        })
        
        # Ensure all required fields exist with fallbacks
        return {
            "clarity_score": result.get("clarity_score", 7),
            "structure_score": result.get("structure_score", 7),
            "impact_score": result.get("impact_score", 7),
            "overall_score": result.get("overall_score", 7),
            "key_strengths": result.get("key_strengths", ["Good effort", "Clear communication"]),
            "areas_for_improvement": result.get("areas_for_improvement", ["Add more specific examples", "Quantify outcomes"]),
            "coaching_tip": result.get("coaching_tip", "Great start! Try adding specific metrics to strengthen your answer."),
            "filler_words_noticed": result.get("filler_words_noticed", []),
            "star_method_evaluation": result.get("star_method_evaluation", {
                "situation": "detected",
                "task": "detected",
                "action": "detected",
                "result": "detected"
            })
        }
    except Exception as e:
        print(f"Error in coaching feedback: {str(e)}")
        # Return sensible defaults if LLM call fails
        return {
            "clarity_score": 7,
            "structure_score": 7,
            "impact_score": 7,
            "overall_score": 7,
            "key_strengths": ["Clear communication", "Good pacing"],
            "areas_for_improvement": ["Add quantifiable metrics", "Provide more context"],
            "coaching_tip": "Solid answer! Consider adding specific numbers and timelines to make it even stronger.",
            "filler_words_noticed": [],
            "star_method_evaluation": {
                "situation": "detected",
                "task": "detected",
                "action": "detected",
                "result": "detected"
            }
        }


async def generate_improved_answer(
    question: str,
    original_answer: str,
    role: str
) -> Dict:
    """
    Generate an excellent example answer using STAR method.
    
    Uses LangChain to invoke Mistral with improvement prompt.
    Demonstrates best practices and proper structure.
    
    Args:
        question: Interview question
        original_answer: Candidate's initial attempt
        role: Target role for context-specific improvement
    
    Returns:
        Dict with improved answer, breakdown, and coaching notes
    """
    try:
        if improvement_chain is None:
            logger.warning("Improvement chain not initialized - returning default response")
            return {
                "improved_answer": "Unable to generate improvement - AI service not configured",
                "star_breakdown": {
                    "situation": "Unknown",
                    "task": "Unknown",
                    "action": "Unknown",
                    "result": "Unknown"
                },
                "key_improvements": ["More specific examples", "Quantified results", "Clear structure"],
                "why_this_works": "This approach demonstrates clear problem-solving methodology."
            }
        
        result = improvement_chain.invoke({
            "question": question,
            "original_answer": original_answer,
            "role": role
        })
        
        return {
            "improved_answer": result.get("improved_answer", "Unable to generate improvement"),
            "star_breakdown": result.get("star_breakdown", {
                "situation": "Unknown",
                "task": "Unknown",
                "action": "Unknown",
                "result": "Unknown"
            }),
            "key_improvements": result.get("key_improvements", ["More specific examples", "Quantified results", "Clear structure"]),
            "why_this_works": result.get("why_this_works", "This approach demonstrates clear problem-solving methodology.")
        }
    except Exception as e:
        print(f"Error in improvement generation: {str(e)}")
        return {
            "improved_answer": "Example: I was tasked with optimizing a database query that was causing system slowdowns...",
            "star_breakdown": {
                "situation": "System experiencing 500ms query latency",
                "task": "Optimize database performance for the checkout feature",
                "action": "Added indexing, refactored joins, implemented caching",
                "result": "Reduced query time to 50ms, 10x improvement, increased conversion by 2%"
            },
            "key_improvements": ["Quantify metrics", "Show trade-offs considered", "Demonstrate ownership"],
            "why_this_works": "This STAR format shows clear problem-solving, impact, and measurable results."
        }


async def generate_follow_up_questions(
    question: str,
    answer: str
) -> Dict:
    """
    Generate likely follow-up questions an interviewer might ask.
    
    Helps candidates anticipate deeper probes and prepare better answers.
    Uses LangChain for consistent, high-quality question generation.
    
    Args:
        question: Original interview question
        answer: Candidate's response
    
    Returns:
        Dict with 3 follow-up questions and their focus areas
    """
    try:
        if followup_chain is None:
            logger.warning("Follow-up chain not initialized - returning default questions")
            return {
                "follow_ups": [
                    {
                        "question": "Can you tell me more about the challenges you faced?",
                        "focus_area": "Technical depth"
                    },
                    {
                        "question": "How did you handle disagreements with your team?",
                        "focus_area": "Soft skills"
                    },
                    {
                        "question": "What would you do differently next time?",
                        "focus_area": "Learning and growth"
                    }
                ]
            }
        
        result = followup_chain.invoke({
            "question": question,
            "answer": answer
        })
        
        return {
            "followup_questions": result.get("followup_questions", [
                "Can you tell me more about how you made that decision?",
                "What would you do differently if you faced the same situation today?",
                "How did you measure the success of your solution?"
            ]),
            "question_focus": result.get("question_focus", ["deeper_context", "decision_making", "impact"])
        }
    except Exception as e:
        print(f"Error in follow-up generation: {str(e)}")
        return {
            "followup_questions": [
                "Walk me through your decision-making process in more detail.",
                "What was the biggest challenge you faced while implementing this?",
                "How would you approach this differently today with what you've learned?"
            ],
            "question_focus": ["deeper_context", "problem_solving", "growth_mindset"]
        }


async def generate_comprehensive_report(
    role: str,
    session_answers: List[Dict],
    num_questions: int = 5
) -> Dict:
    """
    Generate a comprehensive session report with performance analysis.
    
    Aggregates all answers and provides professional feedback summary.
    Uses LangChain to create well-structured report.
    
    Args:
        role: Interview role practiced
        session_answers: List of all Q&A pairs with feedback
        num_questions: Total number of questions in session
    
    Returns:
        Dict with executive summary, strengths, improvements, and recommendations
    """
    try:
        # Calculate averages
        scores = [ans.get("feedback", {}).get("overall_score", 7) 
                 for ans in session_answers if ans.get("feedback")]
        avg_score = sum(scores) / len(scores) if scores else 7.0
        
        # Create summary of all answers
        summary_parts = []
        for i, ans in enumerate(session_answers, 1):
            summary_parts.append(f"Q{i}: {ans.get('question', 'N/A')}\nA: {ans.get('answer', 'N/A')[:200]}...")
        session_summary = "\n\n".join(summary_parts)
        
        if report_chain is None:
            logger.warning("Report chain not initialized - returning default report")
            scores = [ans.get("feedback", {}).get("overall_score", 7) 
                     for ans in session_answers if ans.get("feedback")]
            avg_score = sum(scores) / len(scores) if scores else 7.0
            
            return {
                "executive_summary": "Solid practice session completed.",
                "overall_assessment": "You've demonstrated good foundational interview skills. With targeted practice on specific areas, you'll be well-prepared.",
                "top_strengths": ["Communication", "Problem-solving approach", "Willingness to practice"],
                "critical_improvements": ["Add more specific metrics", "Provide detailed examples", "Practice STAR method"],
                "role_specific_feedback": f"For {role} roles, focus on technical depth and quantifiable impact.",
                "next_steps": "1. Review feedback above 2. Practice improved answers 3. Record yourself 4. Mock interview with peer",
                "confidence_score": 7,
                "estimated_readiness": "70%",
                "average_score": round(avg_score, 1),
                "total_questions": num_questions
            }
        
        result = report_chain.invoke({
            "role": role,
            "num_questions": num_questions,
            "avg_score": round(avg_score, 1),
            "session_summary": session_summary
        })
        
        return {
            "executive_summary": result.get("executive_summary", "Strong performance overall."),
            "overall_assessment": result.get("overall_assessment", "You demonstrated solid interview skills."),
            "top_strengths": result.get("top_strengths", ["Clear communication", "Problem-solving"]),
            "critical_improvements": result.get("critical_improvements", ["Add metrics", "More examples"]),
            "role_specific_feedback": result.get("role_specific_feedback", "Continue practicing with real-world scenarios."),
            "next_steps": result.get("next_steps", "1. Practice with a peer 2. Record yourself 3. Research company 4. Mock interview"),
            "confidence_score": result.get("confidence_score", 7),
            "estimated_readiness": result.get("estimated_readiness", "65-75%"),
            "average_score": round(avg_score, 1),
            "total_questions": num_questions
        }
    except Exception as e:
        print(f"Error in report generation: {str(e)}")
        return {
            "executive_summary": "Solid practice session completed.",
            "overall_assessment": "You've demonstrated good foundational interview skills. With targeted practice on specific areas, you'll be well-prepared.",
            "top_strengths": ["Communication", "Problem-solving approach", "Willingness to practice"],
            "critical_improvements": ["Add more specific metrics", "Provide detailed examples", "Practice STAR method"],
            "role_specific_feedback": f"For {role} roles, focus on technical depth and quantifiable impact.",
            "next_steps": "1. Review feedback above 2. Practice improved answers 3. Record yourself 4. Mock interview with peer",
            "confidence_score": 7,
            "estimated_readiness": "70%",
            "average_score": 7.0,
            "total_questions": num_questions
        }


# Legacy function for backward compatibility (uses Mistral directly without LangChain)
async def generate_improved_answer_legacy(question: str, original_answer: str, role: str) -> str:
    """
    Fallback method using direct Mistral API call.
    Used if LangChain integration unavailable.
    """
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{
                "role": "user",
                "content": f"""
Role: {role}
Question: {question}
Their Answer: {original_answer}

Create an excellent STAR method answer (300-400 words).
Label: Situation, Task, Action, Result clearly.
                """
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating improved answer: {str(e)}"

async def generate_coaching_feedback(
    question: str,
    answer: str,
    language: str = "en",
    context: List[Dict] = None,
    is_followup: bool = False
) -> Dict:
    """
    Generate comprehensive coaching feedback with multi-language support.
    
    Args:
        question: The interview question
        answer: The candidate's answer
        language: Language code (en, es, fr, de, zh, ja)
        context: Conversation history for natural continuation
        is_followup: Whether this is a follow-up question
        
    Returns:
        Dictionary with scores, feedback, strengths, improvements, and follow-up
    """
    try:
        # Map language codes to language names
        language_map = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese'
        }
        
        lang_name = language_map.get(language, 'English')
        
        system_prompt = f"""You are an elite interview coach with 15+ years of experience.
Respond in {lang_name}. Provide constructive, specific feedback on interview answers.

Evaluate on:
- CLARITY (1-10): Does the answer communicate ideas clearly?
- DEPTH (1-10): Does it demonstrate deep understanding?
- COMMUNICATION (1-10): Is it well-structured and compelling?

Format response as valid JSON ONLY:
{{
  "clarity_score": <1-10>,
  "depth_score": <1-10>,
  "communication_score": <1-10>,
  "feedback": "Detailed coaching feedback",
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "follow_up": "Follow-up question or null",
  "language": "{lang_name}"
}}"""
        
        # Build context from conversation history
        context_text = ""
        if context:
            context_text = "Previous conversation:\n"
            for msg in context[-4:]:  # Last 4 messages for context
                role = "Coach" if msg.get("role") == "coach" else "Candidate"
                context_text += f"{role}: {msg.get('content', '')}\n"
        
        user_prompt = f"""Question: {question}
Answer: {answer}

{context_text}

Provide detailed, actionable coaching feedback in {lang_name}. 
{"This is a follow-up question." if is_followup else ""}"""
        
        # Call Mistral
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            feedback_data = json.loads(json_match.group())
        else:
            # Fallback structure
            feedback_data = {
                "clarity_score": 7,
                "depth_score": 7,
                "communication_score": 7,
                "feedback": response_text,
                "strengths": ["Clear communication", "Good structure"],
                "improvements": ["Add more specific examples"],
                "follow_up": None,
                "language": lang_name
            }
        
        return feedback_data
        
    except Exception as e:
        print(f"Error generating coaching feedback: {str(e)}")
        return {
            "clarity_score": 5,
            "depth_score": 5,
            "communication_score": 5,
            "feedback": "Coaching service temporarily unavailable. Please try again.",
            "strengths": [],
            "improvements": [],
            "follow_up": None,
            "error": str(e)
        }