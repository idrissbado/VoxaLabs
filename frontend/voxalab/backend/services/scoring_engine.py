import os
import json
from mistralai import Mistral

# Initialize Mistral client - requires MISTRAL_API_KEY in environment
client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY", ""))

QUESTION_BANK = {
    "Software Engineer": [
        "Tell me about yourself and why you want this role.",
        "Describe a time you debugged a complex production issue. How did you approach it?",
        "How do you handle disagreements with teammates on technical decisions?",
        "Tell me about a project you're most proud of and why.",
        "Describe a time you had to learn a new technology quickly under pressure.",
        "How do you ensure code quality in your team?",
        "Tell me about a time you failed and what you learned from it.",
        "How do you prioritize tasks when everything feels urgent?",
    ],
    "Product Manager": [
        "Tell me about yourself and your product philosophy.",
        "How do you decide what to build next?",
        "Describe a time you shipped a product that failed. What happened?",
        "How do you work with engineering teams who push back on your roadmap?",
        "Tell me about a product decision you're most proud of.",
        "How do you define and measure product success?",
        "Describe a time you used data to change your product direction.",
        "How do you handle competing stakeholder priorities?",
    ],
    "Designer": [
        "Walk me through your design process from brief to delivery.",
        "Tell me about a design you're most proud of.",
        "How do you handle feedback that you disagree with?",
        "Describe a time your design failed and what you learned.",
        "How do you balance user needs with business constraints?",
        "Tell me about a time you had to advocate for the user.",
        "How do you approach designing for accessibility?",
        "Describe your collaboration style with engineers.",
    ],
    "Data Scientist": [
        "Tell me about yourself and your approach to data science.",
        "Describe a model you built that had real business impact.",
        "How do you communicate technical findings to non-technical stakeholders?",
        "Tell me about a time your model performed poorly in production.",
        "How do you decide which algorithm to use for a problem?",
        "Describe a time you found a surprising insight in data.",
        "How do you handle missing or dirty data?",
        "Tell me about a time you had to convince someone using data.",
    ],
    "Marketing": [
        "Tell me about yourself and your marketing philosophy.",
        "Describe a campaign you ran that exceeded expectations.",
        "How do you measure the success of a marketing campaign?",
        "Tell me about a time a campaign flopped. What did you learn?",
        "How do you approach understanding your target audience?",
        "Describe your experience with growth marketing.",
        "How do you stay creative under tight deadlines and budgets?",
        "Tell me about a time you had to market something with limited resources.",
    ]
}


def get_questions(role: str) -> list:
    """Get interview questions for a specific role."""
    return QUESTION_BANK.get(role, QUESTION_BANK["Software Engineer"])

def detect_filler_words(transcript: str) -> list:
    """
    Scan transcript for common filler words that reduce confidence.
    Returns a list with word and occurrence count.
    """
    # These are the most common filler words in English speech
    filler_words = ["um", "uh", "like", "you know", "basically", "literally", 
                    "actually", "so", "right", "okay", "kind of", "sort of", "i mean"]
    
    found = []
    transcript_lower = transcript.lower()
    
    # Count occurrences of each filler word
    for filler in filler_words:
        count = transcript_lower.count(f" {filler} ")
        if count > 0:
            found.append({"word": filler, "count": count})
    
    return found


def check_star_method(transcript: str) -> dict:
    """
    Check if the answer follows the STAR method structure.
    STAR = Situation, Task, Action, Result
    This is the gold standard for behavioral interview answers.
    """
    transcript_lower = transcript.lower()
    
    # Check for indicators of each STAR component
    situation = any(w in transcript_lower for w in ["when i", "at my", "in my previous", 
                                                      "i was working", "we were", "the situation"])
    task = any(w in transcript_lower for w in ["my job was", "i was responsible", 
                                                "i needed to", "my task", "i had to"])
    action = any(w in transcript_lower for w in ["i decided", "i took", "i implemented", 
                                                  "i created", "i worked", "i built", "i developed"])
    result = any(w in transcript_lower for w in ["as a result", "which resulted", "we achieved", 
                                                  "increased", "decreased", "reduced", "improved", "the outcome"])
    
    return {
        "situation": situation,
        "task": task,
        "action": action,
        "result": result,
        "complete": all([situation, task, action, result])  # True if all 4 parts present
    }

async def generate_full_report(sessions: list, role: str) -> dict:
    """Generate a comprehensive report after all practice sessions."""
    session_summaries = "\n".join([
        f"Q{i+1}: {s['question']}\nScore: {s['overall']}/10\nKey feedback: {s['tip']}"
        for i, s in enumerate(sessions)
    ])
    
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{
            "role": "user",
            "content": f"""
            You are an expert interview coach. Based on these {len(sessions)} practice sessions for a {role} role:
            
            {session_summaries}
            
            Generate a comprehensive improvement report with:
            1. Overall performance summary
            2. Top 3 strengths demonstrated
            3. Top 3 areas for improvement
            4. Specific exercises to improve weak areas
            5. Readiness assessment (Ready / Almost Ready / Needs More Practice)
            
            Be specific, actionable, and encouraging.
            """
        }]
    )
    
    return {
        "report": response.choices[0].message.content,
        "sessions_count": len(sessions),
        "avg_score": sum(s.get("overall", 5) for s in sessions) / len(sessions) if sessions else 0
    }
