import os
import json
from mistralai import Mistral
import logging

logger = logging.getLogger(__name__)

# Initialize Mistral client - requires MISTRAL_API_KEY in environment
client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY", ""))

# Translation dictionary for questions in multiple languages
QUESTION_BANK_MULTI_LANGUAGE = {
    "Software Engineer": {
        "en": [
            "Tell me about yourself and why you want this role.",
            "Describe a time you debugged a complex production issue. How did you approach it?",
            "How do you handle disagreements with teammates on technical decisions?",
            "Tell me about a project you're most proud of and why.",
            "Describe a time you had to learn a new technology quickly under pressure.",
            "How do you ensure code quality in your team?",
            "Tell me about a time you failed and what you learned from it.",
            "How do you prioritize tasks when everything feels urgent?",
            "Describe your approach to system design for scalability.",
            "Tell me about a time you optimized performance significantly.",
        ],
        "es": [
            "Cuéntame sobre ti y por qué quieres este puesto.",
            "Describe un momento en que depuraste un problema complejo en producción. ¿Cómo lo abordaste?",
            "¿Cómo manejas desacuerdos con compañeros de equipo sobre decisiones técnicas?",
            "Cuéntame sobre un proyecto del que estés más orgulloso y por qué.",
            "Describe un momento en que tuviste que aprender una nueva tecnología rápidamente bajo presión.",
            "¿Cómo aseguras la calidad del código en tu equipo?",
            "Cuéntame sobre un momento en que fallaste y qué aprendiste.",
            "¿Cómo priorizas tareas cuando todo parece urgente?",
            "Describe tu enfoque para diseño de sistemas escalable.",
            "Cuéntame sobre una optimización de rendimiento significativa.",
        ],
        "fr": [
            "Parlez-moi de vous et pourquoi vous voulez ce rôle.",
            "Décrivez un moment où vous avez débogué un problème complexe en production. Comment avez-vous approché cela?",
            "Comment gérez-vous les désaccords avec les coéquipiers sur les décisions techniques?",
            "Parlez-moi d'un projet dont vous êtes le plus fier et pourquoi.",
            "Décrivez un moment où vous avez dû apprendre une nouvelle technologie rapidement sous pression.",
            "Comment assurez-vous la qualité du code dans votre équipe?",
            "Parlez-moi d'un moment où vous avez échoué et ce que vous en avez appris.",
            "Comment priorisez-vous les tâches quand tout semble urgent?",
            "Décrivez votre approche du design système pour la scalabilité.",
            "Parlez-moi d'une optimisation de performance significative.",
        ]
    },
    "Product Manager": {
        "en": [
            "Tell me about yourself and your product philosophy.",
            "How do you decide what to build next?",
            "Describe a time you shipped a product that failed. What happened?",
            "How do you work with engineering teams who push back on your roadmap?",
            "Tell me about a product decision you're most proud of.",
            "How do you define and measure product success?",
            "Describe a time you used data to change your product direction.",
            "How do you handle competing stakeholder priorities?",
            "Tell me about your approach to competitive analysis.",
            "Describe how you gather and prioritize user feedback.",
        ],
        "es": [
            "Cuéntame sobre ti y tu filosofía de producto.",
            "¿Cómo decides qué construir a continuación?",
            "Describe un momento en que lanzaste un producto que falló. ¿Qué pasó?",
            "¿Cómo trabajas con equipos de ingeniería que se oponen a tu hoja de ruta?",
            "Cuéntame sobre una decisión de producto de la que estés más orgulloso.",
            "¿Cómo defines y mides el éxito del producto?",
            "Describe un momento en que usaste datos para cambiar la dirección del producto.",
            "¿Cómo manejas prioridades en conflicto entre stakeholders?",
            "Cuéntame sobre tu enfoque del análisis competitivo.",
            "Describe cómo recopila y prioriza la retroalimentación del usuario.",
        ]
    },
    "Designer": {
        "en": [
            "Walk me through your design process from brief to delivery.",
            "Tell me about a design you're most proud of.",
            "How do you handle feedback that you disagree with?",
            "Describe a time your design failed and what you learned.",
            "How do you balance user needs with business constraints?",
            "Tell me about a time you had to advocate for the user.",
            "How do you approach designing for accessibility?",
            "Describe your collaboration style with engineers.",
            "How do you stay current with design trends?",
            "Tell me about a complex design problem you solved.",
        ],
        "es": [
            "Camina conmigo a través de tu proceso de diseño desde el briefing hasta la entrega.",
            "Cuéntame sobre un diseño del que estés más orgulloso.",
            "¿Cómo manejas la retroalimentación con la que no estás de acuerdo?",
            "Describe un momento en que tu diseño falló y qué aprendiste.",
            "¿Cómo equilibras las necesidades del usuario con las limitaciones comerciales?",
            "Cuéntame sobre un momento en que tuviste que abogar por el usuario.",
            "¿Cómo abordas el diseño de accesibilidad?",
            "Describe tu estilo de colaboración con ingenieros.",
            "¿Cómo te mantienes actualizado con las tendencias de diseño?",
            "Cuéntame sobre un problema de diseño complejo que resolviste.",
        ]
    },
    "Data Scientist": {
        "en": [
            "Tell me about yourself and your approach to data science.",
            "Describe a model you built that had real business impact.",
            "How do you communicate technical findings to non-technical stakeholders?",
            "Tell me about a time your model performed poorly in production.",
            "How do you decide which algorithm to use for a problem?",
            "Describe a time you found a surprising insight in data.",
            "How do you handle missing or dirty data?",
            "Tell me about a time you had to convince someone using data.",
            "How do you approach feature engineering?",
            "Describe your experience with A/B testing.",
        ],
        "es": [
            "Cuéntame sobre ti y tu enfoque de la ciencia de datos.",
            "Describe un modelo que construiste que tuvo un impacto comercial real.",
            "¿Cómo comunicas hallazgos técnicos a partes interesadas no técnicas?",
            "Cuéntame sobre un momento en que tu modelo tuvo un bajo rendimiento en producción.",
            "¿Cómo decides qué algoritmo usar para un problema?",
            "Describe un momento en que encontraste un insight sorprendente en los datos.",
            "¿Cómo manejas datos faltantes o sucios?",
            "Cuéntame sobre un momento en que convenciste a alguien usando datos.",
            "¿Cómo abordas la ingeniería de características?",
            "Describe tu experiencia con pruebas A/B.",
        ]
    },
    "Marketing": {
        "en": [
            "Tell me about yourself and your marketing philosophy.",
            "How do you approach developing a go-to-market strategy?",
            "Describe a campaign you're most proud of and its impact.",
            "How do you measure marketing success?",
            "Tell me about a time a campaign didn't perform as expected.",
            "How do you approach understanding your target audience?",
            "Describe your experience with growth marketing.",
            "How do you stay creative under tight deadlines and budgets?",
            "Tell me about a time you had to market something with limited resources.",
            "How do you approach analyzing competitor marketing strategies?",
        ],
        "es": [
            "Cuéntame sobre ti y tu filosofía de marketing.",
            "¿Cómo abordas el desarrollo de una estrategia de lanzamiento?",
            "Describe una campaña de la que estés más orgulloso y su impacto.",
            "¿Cómo mides el éxito del marketing?",
            "Cuéntame sobre un momento en que una campaña no funcionó como se esperaba.",
            "¿Cómo abordas la comprensión de tu audiencia objetivo?",
            "Describe tu experiencia con marketing de crecimiento.",
            "¿Cómo mantienes la creatividad bajo plazos y presupuestos ajustados?",
            "Cuéntame sobre un momento en que tuviste que comercializar algo con recursos limitados.",
            "¿Cómo abordas el análisis de estrategias de marketing de competidores?",
        ]
    }
}

# Fallback: Original English question bank
QUESTION_BANK = {
    "Software Engineer": [
        "Tell me about yourself and why you want this role.",
        "Describe a time you debugged a complex production issue. How did you approach it?",
        "How do you handle disagreements with teammates on technical decisions?",
        "Tell me about a project you're most proud of and why.",
        "Describe a time you had to learn a new technology quickly under pressure.",
    ],
    "Product Manager": [
        "Tell me about yourself and your product philosophy.",
        "How do you decide what to build next?",
        "Describe a time you shipped a product that failed. What happened?",
        "How do you work with engineering teams who push back on your roadmap?",
        "Tell me about a product decision you're most proud of.",
    ],
    "Designer": [
        "Walk me through your design process from brief to delivery.",
        "Tell me about a design you're most proud of.",
        "How do you handle feedback that you disagree with?",
        "Describe a time your design failed and what you learned.",
        "How do you balance user needs with business constraints?",
    ],
    "Data Scientist": [
        "Tell me about yourself and your approach to data science.",
        "Describe a model you built that had real business impact.",
        "How do you communicate technical findings to non-technical stakeholders?",
        "Tell me about a time your model performed poorly in production.",
        "How do you decide which algorithm to use for a problem?",
    ],
    "Marketing": [
        "Tell me about yourself and your marketing philosophy.",
        "How do you approach developing a go-to-market strategy?",
        "Describe a campaign you're most proud of and its impact.",
        "How do you measure marketing success?",
        "Tell me about a time a campaign didn't perform as expected.",
    ]
}


def get_questions(role: str, language: str = "en") -> list:
    """Get interview questions for a specific role and language."""
    if role in QUESTION_BANK_MULTI_LANGUAGE:
        questions = QUESTION_BANK_MULTI_LANGUAGE[role].get(language)
        if questions:
            return questions  # Return ALL questions (10 per role)
    
    # Fallback to English
    return QUESTION_BANK.get(role, [])  # Return all questions

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
