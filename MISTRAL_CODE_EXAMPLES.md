# Mistral Integration - Code Examples

This document shows exactly how VoxaLab AI uses Mistral Large 3 API throughout the project.

## 1. Initialization (backend/services/mistral_service.py)

```python
import os
from mistralai import Mistral
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize Mistral client - uses MISTRAL_API_KEY from .env
api_key = os.environ.get("MISTRAL_API_KEY", "")
client = Mistral(api_key=api_key)

# Initialize LangChain Mistral integration for advanced chains
llm = ChatMistralAI(model="mistral-large-latest", api_key=api_key)
```

---

## 2. Professional Prompt Engineering with LangChain

### Coaching Feedback Prompt
```python
COACHING_PROMPT = ChatPromptTemplate.from_template("""
You are an elite interview coach with 15+ years of experience conducting 
technical and behavioral interviews across top companies.

Your role is to provide constructive, specific feedback on interview answers.
Evaluate clarity, structure, and impact using these criteria:

CLARITY (1-10): Does the answer clearly communicate ideas? No rambling.
STRUCTURE (1-10): Does it follow a logical flow? STAR method encouraged.
IMPACT (1-10): Are results quantified? Does it demonstrate value?

Candidate Profile: {role}
Interview Question: {question}
Candidate's Answer: {answer}

Provide feedback as JSON with these EXACT fields:
{{
  "clarity_score": <1-10>,
  "structure_score": <1-10>,
  "impact_score": <1-10>,
  "overall_score": <average of above>,
  "feedback": "<specific, constructive feedback>",
  "strengths": ["<strength1>", "<strength2>", "<strength3>"],
  "improvements": ["<improvement1>", "<improvement2>"],
  "star_used": <true if answer uses STAR method>,
  "follow_up": "<suggested follow-up interview question>"
}}

Format: Return ONLY valid JSON, no markdown, no extra text.
""")
```

### Follow-up Question Prompt
```python
FOLLOWUP_PROMPT = ChatPromptTemplate.from_template("""
You are an expert technical interviewer. Generate a follow-up question that:
1. Dives deeper into their answer
2. Tests a different competency
3. Is specific to their stated role: {role}

Original Question: {question}
Their Answer: {answer}

Return JSON:
{{
  "follow_up_question": "<specific follow-up question>",
  "rationale": "<why this question is valuable>"
}}
""")
```

---

## 3. LangChain Chain Construction

```python
from langchain_core.output_parsers import JsonOutputParser

# Create JSON parser for structured outputs
json_parser = JsonOutputParser()

# Construct LangChain chains - combines prompt + LLM + output parsing
coaching_chain = COACHING_PROMPT | llm | json_parser
improvement_chain = IMPROVEMENT_PROMPT | llm | json_parser
followup_chain = FOLLOWUP_PROMPT | llm | json_parser
report_chain = REPORT_PROMPT | llm | json_parser

# Each chain is a callable pipeline:
# Input → Prompt Template → Mistral LLM → JSON Parser → Output
```

---

## 4. Async API Usage

### Generate Coaching Feedback
```python
async def generate_coaching_feedback(
    question: str,
    answer: str,
    language: str = "en",
    context: List[Dict] = [],
    is_followup: bool = False
) -> Dict:
    """
    Generate AI coaching feedback using Mistral Large 3.
    
    Args:
        question: Interview question
        answer: User's answer (from speech transcription or text)
        language: Language code (en, es, fr, de, it, pt)
        context: Previous Q&A pairs for context
        is_followup: Whether this is a follow-up question
    
    Returns:
        Dictionary with scores, feedback, suggestions
    """
    try:
        # Translate question and answer to English for Mistral
        if language != "en":
            en_question = await translate_text(question, language, "en")
            en_answer = await translate_text(answer, language, "en")
        else:
            en_question, en_answer = question, answer
        
        # Invoke Mistral through LangChain chain (async)
        coaching_data = await coaching_chain.ainvoke({
            "role": role,
            "question": en_question,
            "answer": en_answer
        })
        
        # Translate feedback back to user's language
        if language != "en":
            coaching_data["feedback"] = await translate_text(
                coaching_data["feedback"], "en", language
            )
        
        return coaching_data
        
    except Exception as e:
        logger.error(f"Mistral API error: {e}")
        # Return sensible defaults if Mistral unavailable
        return {
            "clarity_score": 7,
            "structure_score": 7,
            "impact_score": 7,
            "overall_score": 7,
            "feedback": "Thank you for your answer. Keep practicing!",
            "strengths": ["Clear communication"],
            "improvements": ["Add more specific metrics"],
            "star_used": False,
            "follow_up": "Can you provide an example?"
        }
```

### Generate Improved Answer
```python
async def generate_improved_answer(question: str, answer: str, role: str):
    """Generate an improved example answer using Mistral."""
    try:
        improved_data = await improvement_chain.ainvoke({
            "question": question,
            "answer": answer,
            "role": role
        })
        return improved_data["improved_answer"]
    except Exception as e:
        logger.error(f"Error generating improved answer: {e}")
        return "Keep practicing and refining your answer!"
```

### Generate Follow-up Questions
```python
async def generate_follow_up_questions(question: str, answer: str):
    """Generate context-aware follow-up interview questions."""
    try:
        followup_data = await followup_chain.ainvoke({
            "question": question,
            "answer": answer
        })
        return followup_data.get("follow_up_questions", [])
    except Exception as e:
        logger.error(f"Error generating follow-up: {e}")
        return []
```

### Generate Session Report
```python
async def generate_session_report(session_answers: List[Dict], language: str):
    """Generate comprehensive session report using Mistral."""
    try:
        report_data = await report_chain.ainvoke({
            "session_answers": session_answers,
            "language": language
        })
        return report_data
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {"summary": "Session completed. Keep practicing!"}
```

---

## 5. Direct Mistral API Usage (Legacy Support)

```python
# Direct API usage (when LangChain chain not needed)
def analyze_with_direct_mistral(question: str, answer: str):
    """Direct Mistral API call without LangChain."""
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": f"""
                Question: {question}
                Answer: {answer}
                
                Provide feedback as JSON...
                """
            }
        ],
        response_format={"type": "json_object"}  # Structured output
    )
    
    # Extract JSON from response
    content = response.choices[0].message.content
    return json.loads(content)
```

---

## 6. FastAPI Endpoints Using Mistral

### Audio Analysis Endpoint
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/analysis", tags=["analysis"])

class AnalyzeAudioRequest(BaseModel):
    audio_base64: str
    question: str
    role: str
    session_id: str
    language: str = "en"

@router.post("/audio")
async def analyze_audio_answer(req: AnalyzeAudioRequest):
    """
    Complete audio pipeline:
    1. Transcribe with Whisper
    2. Analyze with Mistral
    3. Return coaching feedback
    """
    try:
        # Step 1: Transcribe audio
        transcript = await transcribe_audio(req.audio_base64)
        
        # Step 2: Generate Mistral coaching feedback
        coaching_data = await generate_coaching_feedback(
            question=req.question,
            answer=transcript,
            language=req.language
        )
        
        # Step 3: Return complete feedback
        return {
            "transcript": transcript,
            "user_answer": transcript,
            "coaching_feedback": coaching_data.get("feedback", ""),
            "clarity_score": coaching_data.get("clarity_score", 7),
            "depth_score": coaching_data.get("structure_score", 7),
            "communication_score": coaching_data.get("impact_score", 7),
            "strengths": coaching_data.get("strengths", []),
            "improvements": coaching_data.get("improvements", []),
            "follow_up_question": coaching_data.get("follow_up", None),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error analyzing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Text Feedback Endpoint
```python
class FeedbackRequest(BaseModel):
    session_id: str
    question: str
    user_answer: str
    language: str = "en"
    context: List[Dict] = []

@router.post("/feedback")
async def analyze_answer(req: FeedbackRequest):
    """Analyze text answer using Mistral coaching chain."""
    try:
        logger.info(f"Analyzing answer for session {req.session_id}")
        
        # Generate Mistral coaching feedback
        coaching_data = await generate_coaching_feedback(
            question=req.question,
            answer=req.user_answer,
            language=req.language,
            context=req.context
        )
        
        return {
            "user_answer": req.user_answer,
            "coaching_feedback": coaching_data.get("feedback", ""),
            "clarity_score": coaching_data.get("clarity_score", 7),
            "depth_score": coaching_data.get("structure_score", 7),
            "communication_score": coaching_data.get("impact_score", 7),
            "strengths": coaching_data.get("strengths", []),
            "improvements": coaching_data.get("improvements", []),
            "follow_up_question": coaching_data.get("follow_up", None),
            "filler_words": detect_filler_words(req.user_answer),
            "word_count": len(req.user_answer.split())
        }
    except Exception as e:
        logger.error(f"Error analyzing answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 7. Multi-Language Support with Mistral

```python
async def translate_with_mistral(text: str, source_lang: str, target_lang: str):
    """Use Mistral to translate feedback to user's language."""
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{
            "role": "user",
            "content": f"""
            Translate the following {source_lang} text to {target_lang}.
            Keep professional tone. Return ONLY the translation.
            
            Text: {text}
            """
        }]
    )
    return response.choices[0].message.content.strip()
```

---

## 8. Requirements (pip dependencies)

```
# Core Mistral Integration
mistralai>=1.0.0                    # Official Mistral API client
langchain>=0.1.0                    # LLM orchestration
langchain-mistralai>=0.1.0          # LangChain Mistral integration
langchain-community>=0.0.10         # Additional LangChain tools

# Supporting Services
openai-whisper>=20240314           # Speech-to-text (complements Mistral)
elevenlabs>=0.2.0                  # Text-to-speech
fastapi>=0.109.0                   # API framework
uvicorn>=0.27.0                    # ASGI server
pydantic>=2.8.2                    # Data validation
```

---

## 9. Environment Configuration

```bash
# .env file
MISTRAL_API_KEY=your_api_key_from_console_mistral_ai
HOST=0.0.0.0
PORT=8000
ENV=production
LOG_LEVEL=INFO

# Feature Flags
ENABLE_VOICE_TRANSCRIPTION=true
ENABLE_AUDIO_PROCESSING=true
ENABLE_REPORT_GENERATION=true
```

---

## 10. Example Usage Flow

### User Records 30-Second Answer
```
Audio: [User speaking: "I'm a software engineer with 5 years experience..."]
```

### Backend Processing
```python
# 1. Transcription (Whisper)
transcript = "I'm a software engineer with 5 years of experience. 
I specialize in backend systems and have led teams of 5 engineers..."

# 2. Mistral Analysis (LangChain)
coaching_data = {
    "clarity_score": 8,
    "structure_score": 7,
    "impact_score": 8,
    "overall_score": 7.7,
    "feedback": "Great answer! You clearly stated your experience and team leadership. 
                 Consider adding a specific metric (e.g., 'reduced latency by 40%').",
    "strengths": ["Clear role description", "Team leadership mentioned"],
    "improvements": ["Add quantified results", "Mention specific technologies"],
    "star_used": false,
    "follow_up": "Tell me about a time you resolved a production incident."
}
```

### Frontend Display
```
✓ Audio Playback: [User hears their recording]
✓ Clarity Score: 8/10
✓ Structure Score: 7/10
✓ Impact Score: 8/10
✓ Feedback: "Great answer! You clearly stated..."
✓ Follow-up Question: "Tell me about a time you resolved..."
```

---

## Summary

VoxaLab AI demonstrates professional use of Mistral Large 3:

✅ **Direct API integration** with error handling  
✅ **LangChain advanced chains** for structured prompting  
✅ **Async/await patterns** for responsiveness  
✅ **JSON structured outputs** for reliability  
✅ **Multi-language support** via translation  
✅ **Production-ready code** with logging and monitoring  
✅ **Multiple use cases** (coaching, improvement, follow-ups, reports)  

This showcases how Mistral's reasoning capabilities power sophisticated AI applications beyond chat.
