"""
Coaching Team Configuration

This module defines the specialized coaching team for VoiceCoach AI.
Each coach is an expert in their domain and provides tailored feedback
for interview preparation in their specific role.
"""

from typing import Dict, List

# Define the specialized coaching team
COACHING_TEAM = {
    "Software Engineer": {
        "coach_name": "Alex Chen",
        "coach_title": "Senior Architect",
        "company": "Google",
        "bio": "Senior Architect at Google with 12+ years in system design and scalability. Conducted 500+ technical interviews.",
        "specializations": ["System Design", "Algorithms", "Code Quality", "Scalability", "Debugging"],
        "approach": "Focuses on clarity of technical thinking, ability to handle trade-offs, and communicating complex ideas simply.",
        "questions_focus": [
            "Design patterns and architectural thinking",
            "Problem-solving methodology",
            "Trade-off analysis",
            "Communication of technical concepts",
            "Handling ambiguity in requirements"
        ],
        "emoji": "💻"
    },
    "Product Manager": {
        "coach_name": "Maya Patel",
        "coach_title": "Director of Product",
        "company": "Meta",
        "bio": "Director of Product at Meta with 10+ years building products used by billions. Experienced in PM interviews and hiring.",
        "specializations": ["Product Strategy", "Metrics & Analytics", "User Research", "Roadmap Planning", "Cross-functional Leadership"],
        "approach": "Emphasizes data-driven thinking, user empathy, and ability to prioritize ruthlessly while communicating vision.",
        "questions_focus": [
            "Product strategy and vision",
            "Metrics selection and success criteria",
            "User research methodology",
            "Trade-off decision making",
            "Cross-functional collaboration"
        ],
        "emoji": "📊"
    },
    "Designer": {
        "coach_name": "Jordan Smith",
        "coach_title": "Principal Designer",
        "company": "Apple",
        "bio": "Principal Designer at Apple leading design of consumer products. 8+ years mentoring designers through interviews.",
        "specializations": ["UX Thinking", "Design Process", "User-Centered Design", "Communication", "Problem-Solving"],
        "approach": "Values clear communication of design thinking, ability to iterate, and making intuitive decisions with justification.",
        "questions_focus": [
            "Design thinking framework",
            "User empathy and research",
            "Iterative design process",
            "Balancing aesthetics and usability",
            "Cross-functional communication"
        ],
        "emoji": "🎨"
    },
    "Data Scientist": {
        "coach_name": "Dr. Rajesh Kumar",
        "coach_title": "ML Research Lead",
        "company": "OpenAI",
        "bio": "ML Research Lead at OpenAI. PhD in Statistics. Conducts technical interviews for research and applied ML roles.",
        "specializations": ["Statistical Analysis", "Machine Learning", "Data Modeling", "Experimentation", "Insights Communication"],
        "approach": "Prioritizes rigorous thinking, understanding assumptions, ability to communicate findings simply, and knowing limitations.",
        "questions_focus": [
            "Statistical fundamentals",
            "Modeling approach selection",
            "Experiment design",
            "Results interpretation",
            "Communication of technical concepts"
        ],
        "emoji": "📈"
    },
    "Marketing": {
        "coach_name": "Sarah Williams",
        "coach_title": "VP Growth",
        "company": "Stripe",
        "bio": "VP Growth at Stripe. 9+ years building go-to-market strategies and growth systems. Active hiring manager.",
        "specializations": ["Go-to-Market Strategy", "Customer Psychology", "Growth Metrics", "Market Analysis", "Campaign Strategy"],
        "approach": "Values strategic thinking, business acumen, ability to work cross-functionally, and communicating with data and stories.",
        "questions_focus": [
            "Market opportunity analysis",
            "Customer segmentation",
            "Channel strategy",
            "Metrics and measurement",
            "Campaign planning and execution"
        ],
        "emoji": "📱"
    }
}


def get_coach_for_role(role: str) -> Dict:
    """
    Get the specialized coach information for a specific role.
    
    Args:
        role: The interview role (e.g., "Software Engineer", "Product Manager")
    
    Returns:
        Dictionary with coach information or None if role not found
    """
    return COACHING_TEAM.get(role)


def get_all_coaches() -> Dict:
    """Get all coaches on the team."""
    return COACHING_TEAM


def get_coach_greeting(role: str) -> str:
    """Get a personalized greeting from the coach for a role."""
    coach = get_coach_for_role(role)
    if not coach:
        return "Welcome to VoiceCoach AI!"
    
    return (
        f"Hello! I'm {coach['coach_name']}, {coach['coach_title']} at {coach['company']}. "
        f"I'll be coaching you through {role} interview preparation. Let's get started!"
    )


def get_role_specific_tips(role: str) -> str:
    """Get role-specific coaching tips from the assigned coach."""
    coach = get_coach_for_role(role)
    if not coach:
        return ""
    
    tips = f"Coaching tips from {coach['coach_name']} for {role} interviews:\n\n"
    tips += f"Approach: {coach['approach']}\n\n"
    tips += "Focus on:\n"
    for i, focus in enumerate(coach['questions_focus'], 1):
        tips += f"{i}. {focus}\n"
    
    return tips


# List of all available roles
AVAILABLE_ROLES = list(COACHING_TEAM.keys())

# Questions specific guidance per role
ROLE_GUIDANCE = {
    "Software Engineer": {
        "difficulty_levels": ["Easy", "Medium", "Medium", "Hard", "Hard"],
        "evaluation_criteria": ["Technical Clarity", "Architecture Thinking", "Trade-off Analysis", "Communication", "Depth"]
    },
    "Product Manager": {
        "difficulty_levels": ["Easy", "Medium", "Medium", "Hard", "Hard"],
        "evaluation_criteria": ["Product Sense", "Data-Driven Thinking", "User Empathy", "Strategic Vision", "Communication"]
    },
    "Designer": {
        "difficulty_levels": ["Easy", "Medium", "Medium", "Hard", "Hard"],
        "evaluation_criteria": ["Design Thinking", "User Research", "Iteration", "Problem-Solving", "Communication"]
    },
    "Data Scientist": {
        "difficulty_levels": ["Easy", "Medium", "Medium", "Hard", "Hard"],
        "evaluation_criteria": ["Statistical Rigor", "Modeling Approach", "Experimentation", "Insights", "Communication"]
    },
    "Marketing": {
        "difficulty_levels": ["Easy", "Medium", "Medium", "Hard", "Hard"],
        "evaluation_criteria": ["Strategic Thinking", "Market Understanding", "Customer Psychology", "Analytics", "Communication"]
    }
}
