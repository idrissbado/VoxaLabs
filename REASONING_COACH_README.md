# 🧠 Interactive Mathematical Reasoning Coach

## System Overview

A step-by-step **interactive reasoning validation system** powered by Mistral Large that transforms students into problem-solvers rather than answer-seekers.

**Philosophy:** Never give the answer. Always guide the reasoning.

---

## Architecture

### Three Core Phases

#### Phase 1: Problem Classification
- **Endpoint:** `POST /math/reasoning/start`
- **Input:** Problem text or PDF content
- **Process:**
  - Classify topic, subtopic, difficulty (1-5)
  - Identify required concepts
  - Generate first guiding question
- **Output:** Session ID + classification + first question

#### Phase 2: Interactive Validation Loop
- **Endpoint:** `POST /math/reasoning/validate-step`
- **Input:** Student's answer to current step
- **Process:**
  - Validate mathematical correctness
  - Detect error type (algebraic, logical, conceptual, incomplete)
  - Provide specific explanation
  - Determine next action
- **Output:** Validation result + feedback + next direction

#### Phase 3: Progressive Hints
- **Endpoint:** `POST /math/reasoning/hint`
- **Hint Levels:**
  - Level 1: Small nudge ("What information do you have?")
  - Level 2: Concept reminder ("Remember integrating factors?")
  - Level 3: Structural guidance ("Method: identify type → find factor → apply")
  - Level 4: Partial reveal ("You're very close, just verify...")
- **Output:** Appropriate hint at requested level

#### Phase 4: Solution Reveal
- **Endpoint:** `POST /math/reasoning/reveal-solution`
- **Output:**
  - Complete step-by-step solution
  - Clean LaTeX formatting
  - Boxed final answer
  - Common mistakes
  - Practice problems

---

## API Reference

### 1. Start Reasoning Session

```
POST /math/reasoning/start
Content-Type: application/json

{
  "problem_text": "Solve: y' + 2y = e^(-x)",
  "format_type": "text"
}

Response:
{
  "success": true,
  "session_id": "2026-03-01T12:34:56.789123",
  "problem_text": "Solve: y' + 2y = e^(-x)",
  "classification": {
    "topic": "Differential Equations",
    "subtopic": "First-Order Linear ODEs",
    "difficulty": 3,
    "required_concepts": ["First-order linear DE", "Integrating factors", "Exponential functions"],
    "estimated_steps": 5,
    "difficulty_badge": "3/5"
  },
  "first_question": "What type of differential equation is this? Look at the form y' + P(x)y = Q(x)",
  "hint_level": 1,
  "coaching_mode": "step_by_step",
  "next_action": "request_student_answer"
}
```

### 2. Validate Student Step

```
POST /math/reasoning/validate-step
Content-Type: application/json

{
  "session_id": "2026-03-01T12:34:56.789123",
  "step_number": 1,
  "student_answer": "This is a first-order linear differential equation because it has the form y' + P(x)y = Q(x)",
  "context": [
    {"role": "system", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}

Response:
{
  "success": true,
  "session_id": "2026-03-01T12:34:56.789123",
  "step_number": 1,
  "is_correct": true,
  "confidence": 0.95,
  "explanation": "Excellent! You've correctly identified the type. P(x) = 2 and Q(x) = e^(-x).",
  "error_type": null,
  "justification": "The standard form y' + P(x)y = Q(x) is the definition of first-order linear ODEs.",
  "next_action": "request_next_step",
  "feedback": {
    "quality": "excellent",
    "is_on_track": true
  }
}
```

### 3. Get Adaptive Hint

```
POST /math/reasoning/hint
Content-Type: application/json

{
  "session_id": "2026-03-01T12:34:56.789123",
  "step_number": 2,
  "current_attempt": "Um... I need to find something?",
  "hint_level": 1
}

Response:
{
  "success": true,
  "session_id": "2026-03-01T12:34:56.789123",
  "step_number": 2,
  "hint_level": 1,
  "hint": "For first-order linear ODEs, we need a special function. What method do we use?",
  "guidance": "Think about what function multiplies both sides to make the left side a derivative.",
  "direction": "Look for integrating factor technique",
  "can_request_higher_level": true,
  "next_hint_level": 2
}
```

### 4. Reveal Full Solution

```
POST /math/reasoning/reveal-solution
Content-Type: application/json

{
  "session_id": "2026-03-01T12:34:56.789123",
  "steps_history": [
    {"number": 1, "work": "Identified as first-order linear ODE"},
    {"number": 2, "work": "Found integrating factor: e^(2x)"}
  ]
}

Response:
{
  "success": true,
  "session_id": "2026-03-01T12:34:56.789123",
  "solution": {
    "steps": [
      {
        "step": 1,
        "description": "Identify problem type",
        "latex": "y' + 2y = e^{-x} \\text{ is a first-order linear ODE}"
      },
      {
        "step": 2,
        "description": "Find integrating factor",
        "latex": "\\mu(x) = e^{\\int 2 dx} = e^{2x}"
      },
      ...
    ],
    "final_answer": "y = e^(-x) + C*e^(-2x)",
    "final_answer_latex": "\\boxed{y = e^{-x} + Ce^{-2x}}",
    "concepts": ["Linear ODE", "Integrating factors", "Integration"],
    "common_mistakes": [
      "Forgetting the constant of integration",
      "Incorrect integrating factor formula",
      "Algebraic errors in simplification"
    ],
    "practice_problems": [
      "Solve: y' + 3y = e^(2x)",
      "Solve: y' + y = sin(x)"
    ]
  },
  "coaching_session_complete": true
}
```

---

## Error Detection Capabilities

### Error Types

1. **Algebraic Error**
   - Wrong computation
   - Simplification mistake
   - Example: "3x + 2x = 6x" (should be 5x)

2. **Logical Error**
   - Missing step
   - Incorrect sequence
   - Example: Applying integration before simplification

3. **Conceptual Error**
   - Misunderstanding of principle
   - Wrong theorem application
   - Example: Using wrong integrating factor formula

4. **Incomplete Reasoning**
   - Insufficient justification
   - Missing critical step
   - Example: "Therefore, y = e^x" without showing work

5. **Notation Error**
   - Incorrect mathematical symbols
   - Improper LaTeX usage

---

## Hint Progression Strategy

```
User gets stuck on Step N

Level 1: "What variables do you have? What are you solving for?"
         ↓ (still stuck)
         
Level 2: "Remember the principle of [key theorem]. How does it apply?"
         ↓ (still stuck)
         
Level 3: "The approach is: [Step A] → [Step B] → [Step C]. Try Step A."
         ↓ (still stuck)
         
Level 4: "Calculate [specific calculation]. Your answer should be [form]."
         ↓ (still stuck or wants to see)
         
REVEAL FULL SOLUTION with complete LaTeX formatting
```

---

## Session State Management

Each session maintains:
- `session_id` - unique identifier
- `problem_text` - original problem
- `classification` - topic, difficulty, concepts
- `steps_history` - all submitted steps
- `hint_levels` - max hint level used per step
- `error_count` - total errors made
- `completion_status` - percentage through solution
- `solution_revealed` - whether full solution shown

---

## Frontend Integration

### UI Flow

```
1. User submits problem
   ↓
2. System shows classification badge + FIRST QUESTION
   ↓
3. User enters answer → submit
   ↓
4. System validates → shows feedback
   ↓
   [If correct] → "Great! Now for Step 2..."
   [If incorrect] → "Not quite. [Explanation]"
                    [Hint Button] [Try Again] [Request Hint]
   ↓
5. User can request hints (Progressive levels 1-4)
   ↓
6. After correct answer: Next question
   ↓
7. After completion: [Reveal Full Solution] button appears
   ↓
8. Full solution shown with LaTeX + practice problems
```

### Component Usage

```javascript
<ReasoningCoach 
  problemText={problem}
  onComplete={handleComplete}
  renderHints={true}
  maxHintLevel={4}
/>
```

---

## Demo Mode Behavior

When Mistral API not available:
- Uses hardcoded but intelligent demo responses
- Shows same UI/UX as production
- Demonstrates system capabilities
- Falls back gracefully without errors

---

## Key Features

✅ **Step-by-Step Reasoning** - Forces logical progression
✅ **Error Detection** - Identifies error types, not just "wrong"
✅ **Adaptive Hints** - Progressive levels based on difficulty
✅ **LaTeX Support** - Publication-quality mathematical output
✅ **Session Persistence** - Complete interaction history
✅ **Practice Generation** - Similar problems for reinforcement
✅ **Pedagogical AI** - Tutor behavior, not calculator behavior
✅ **Concept Mapping** - Tracks which concepts the student knows

---

## Example Session

### Problem: Solve differential equation y' + 2y = e^(-x)

**Step 1 - Classification:**
```
Topic: Differential Equations
Difficulty: 3/5 (Intermediate)
Required: First-order linear ODE theory, integrating factors, integration

Question: "What type of differential equation is this?"
```

**Step 2 - User Answer:**
```
"It's a first-order linear differential equation"
```

**System Response:**
```
✅ CORRECT! 

Why: The form y' + P(x)y = Q(x) is exactly the definition of first-order 
linear ODEs. You've correctly identified P(x)=2 and Q(x)=e^(-x).

Next: What method should we use to solve first-order linear ODEs?
```

**Step 3 - User Stuck, Requests Hint:**
```
User: [Click "Hint Level 1"]

Hint: "Think of a function that, when multiplied by both sides, 
makes the left side a perfect derivative. What's this function called?"

User tries again, gets it right: "Integrating factor!"
```

...continues until complete or solution revealed...

---

## Backend Architecture

```
/services/reasoning_coach.py
├── classify_problem() - Topic/difficulty/concepts
├── validate_step() - Check correctness + error type
├── generate_adaptive_hint() - Level 1-4 hints
├── generate_final_solution() - Complete solution
└── detect_completion() - Know when done

/routers/math_tutor.py
├── POST /reasoning/start
├── POST /reasoning/validate-step
├── POST /reasoning/hint
└── POST /reasoning/reveal-solution
```

---

## Status

✅ **Backend:** Fully implemented with Mistral integration
✅ **Demo Mode:** Working (no API key required)
🟡 **Frontend:** Needs UI implementation
🟡 **Session Storage:** Needs database integration
✅ **Error Handling:** Graceful fallbacks in place

