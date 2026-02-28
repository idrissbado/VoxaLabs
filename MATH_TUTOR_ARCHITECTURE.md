# Math Tutor Architecture & Integration

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    React Application                         │  │
│  │  ┌────────────────────────────────────────────────────────┐ │  │
│  │  │              App.js (Main Router)                      │ │  │
│  │  │  ┌──────────────┐  ┌─────────────────────────────┐  │ │  │
│  │  │  │ Landing Page │  │  Component Router           │  │ │  │
│  │  │  │              │  │  • Interview Page           │  │ │  │
│  │  │  │ ┌─────────┐  │  │  • Report Page              │  │ │  │
│  │  │  │ │ Mode    │  │  │  • About Page               │  │ │  │
│  │  │  │ │Selector │  │  │  • Math Tutor Page (NEW)    │  │ │  │
│  │  │  │ │ Interview│  │  │                            │  │ │  │
│  │  │  │ │ Math    │  │  │ ┌──────────────────────┐   │  │ │  │
│  │  │  │ │Tutor    │  │  │ │ MathTutor.js (NEW)   │   │  │ │  │
│  │  │  │ └─────────┘  │  │ │ • Problem Input      │   │  │ │  │
│  │  │  │              │  │ │ • Step Solver        │   │  │ │  │
│  │  │  │              │  │ │ • Solution Display   │   │  │ │  │
│  │  │  │              │  │ │ • API Integration    │   │  │ │  │
│  │  │  │              │  │ └──────────────────────┘   │  │ │  │
│  │  │  └────────────────────────────────────────────────┘  │ │  │
│  │  └────────────────────────────────────────────────────────┘  │
│  │                          ↓ HTTP Requests (Axios)              │
│  │                    API Base: /math                             │
│  └──────────────────────────────────────────────────────────────┘
│                                                                     │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ REST API (JSON)
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────────┐         ┌──────────────────────┐
│  FastAPI Backend     │         │  Existing Features   │
│                      │         │  (Interview Coach)   │
│ ┌──────────────────┐ │         │ ┌──────────────────┐ │
│ │ Math Router      │ │         │ │ Session Router   │ │
│ │ (NEW)            │ │         │ │ Analysis Router  │ │
│ │                  │ │         │ │ Report Router    │ │
│ │ ┌──────────────┐ │ │         │ │ TTS Router       │ │
│ │ │POST /analyze │ │ │         │ └──────────────────┘ │
│ │ ├──────────────┤ │ │                                │
│ │ │POST /validate│ │ │         (Using existing        │
│ │ │-step         │ │ │          infrastructure)      │
│ │ ├──────────────┤ │ │                                │
│ │ │POST /generate│ │ │                                │
│ │ │-solution     │ │ │                                │
│ │ ├──────────────┤ │ │                                │
│ │ │POST /practice│ │ │                                │
│ │ │-problem      │ │ │                                │
│ │ ├──────────────┤ │ │                                │
│ │ │GET /health   │ │ │                                │
│ │ └──────────────┘ │ │                                │
│ └──────────────────┘ │                                │
│          ↓           │                                │
│ ┌──────────────────┐ │                                │
│ │Math Tutor Service│ │                                │
│ │(NEW)             │ │                                │
│ │                  │ │                                │
│ │ Core Functions:  │ │                                │
│ │ • analyze_      │ │                                │
│ │   problem()     │ │                                │
│ │ • validate_     │ │                                │
│ │   step()        │ │                                │
│ │ • generate_     │ │                                │
│ │   solution()    │ │                                │
│ │ • generate_     │ │                                │
│ │   practice_     │ │                                │
│ │   problem()     │ │                                │
│ │ • format_latex_ │ │                                │
│ │   solution()    │ │                                │
│ └──────────────────┘ │                                │
│          ↓           │                                │
│ ┌──────────────────┐ │                                │
│ │Mistral Large 3   │ │                                │
│ │API Integration   │ │                                │
│ │ (Using existing  │ │                                │
│ │  mistralai SDK)  │ │                                │
│ └──────────────────┘ │                                │
└──────────────────────┘                                │
        ↓                                               │
        │                                               │
┌───────▼──────────────────────────────────────────────┴────────┐
│           External API Services                                 │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │ Mistral API        │  │ Existing Services  │               │
│  │ • Model: Large 3   │  │ • Whisper (audio)  │               │
│  │ • Reasoning        │  │ • ElevenLabs (TTS) │               │
│  │ • Generation       │  │ • OpenAI (embeddings)             │
│  │ • Validation       │  └────────────────────┘               │
│  └────────────────────┘                                       │
└───────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Complete User Journey

### Step 1: User Selects Math Tutor Mode
```
User Click "Math Tutor"
    ↓
App.js State: mode = 'math'
    ↓
MathTutor Component Mounts
    ↓
Problem Input Form Displays
```

### Step 2: User Submits Problem
```
User Enters: "Solve for x: 2x + 5 = 13"
    ↓
Click "Start Solving"
    ↓
API Call: POST /math/analyze
    {problem_text: "Solve for x: 2x + 5 = 13"}
    ↓
Backend: router → service → Mistral
    ↓
Response: {
  "topic": "Algebra",
  "subtopic": "Linear Equations",
  "difficulty": 2,
  "required_concepts": ["variable isolation", ...],
  "first_question": "...",
  "solution_steps_count": 2
}
    ↓
Frontend: Displays analysis + first question
```

### Step 3: User Solves Step-by-Step
```
User Enters Step 1: "2x = 8"
    ↓
Click "Validate Step"
    ↓
API Call: POST /math/validate-step
    {
      "problem_text": "Solve for x: 2x + 5 = 13",
      "step_number": 1,
      "student_step": "2x = 8",
      "context": ""
    }
    ↓
Backend: Mistral Validation
    • Checks algebraic correctness
    • Detects error types
    • Generates feedback
    ↓
Response: {
  "is_correct": true,
  "error_type": null,
  "confidence": 0.95,
  "explanation": "Correct! You isolated...",
  "hint": null,
  "reasoning_quality_score": 9
}
    ↓
Frontend: Shows ✅ feedback, allows next step
```

### Step 4: Solution Generation
```
User Clicks "Finish & See Solution"
    ↓
API Call: POST /math/generate-solution
    {
      "problem_text": "Solve for x: 2x + 5 = 13",
      "student_solution": "2x = 8\nx = 4"
    }
    ↓
Backend: Mistral Solution
    • Generates complete solution
    • Creates LaTeX formatting
    • Analyzes concepts
    • Calculates mastery score
    ↓
Response: {
  "full_solution": "...",
  "latex_solution": "\\[ x = 4 \\]",
  "final_answer": "x = 4",
  "key_concepts": [...],
  "mastery_score": 85,
  "learning_insights": "..."
}
    ↓
Frontend: Solution Display Phase
    • Shows full solution
    • Displays LaTeX
    • Shows concepts
    • Shows insights
```

### Step 5: Practice & Continuation
```
System Suggests Practice Problem
    ↓
User Can:
    • Get practice problem
    • Solve another problem
    • Return to home
```

---

## Complete Feature Status

✅ **Math Tutor Feature - COMPLETE AND PRODUCTION READY**

All components implemented, tested, documented, and integrated.
Ready for immediate deployment and use.
