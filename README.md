---
title: VoxaLab - AI Interview Coach & Math Tutor
emoji: 🎓
colorFrom: indigo
colorTo: pink
sdk: docker
pinned: false
---

# 🎓 VoxaLab - AI Interview Coach & Math Tutor

<div align="center">

**Comprehensive AI-Powered Education Platform for Career Preparation and Math Mastery**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-green)
![React](https://img.shields.io/badge/React-18.2%2B-61DAFB?logo=react)
![Mistral](https://img.shields.io/badge/Mistral-AI%20Engine-FF6B35)
![Features](https://img.shields.io/badge/Features-Interview%20%2B%20Math-green)

**"Master Your Skills: Tech Interview Preparation + Advanced Math Tutoring in One Platform"**

[🚀 Try It Now](#try-it-now) • [📋 All Features](#-platform-features) • [🏗️ System Architecture](#-system-architecture) • [🤖 AI Capabilities](#-ai-powered-engines)</div>

---

## 🎯 Platform Overview

VoxaLab is a comprehensive AI education platform with **two core modules:**

### **Module 1: 🎤 Interview Coaching System**
Real-time AI-powered technical interview practice with live feedback and performance analytics.

### **Module 2: 📐 Advanced Math Tutoring System**  
Step-by-step mathematical reasoning coach with problem-specific guidance and interactive validation.

---

## 📋 Platform Features

### **Interview Coaching Module**

**1. Interview Practice Simulation**
- ✅ Realistic tech interview questions across multiple domains
- ✅ Real-time answer transcription (Whisper AI)
- ✅ Support for audio input or text typing
- ✅ Multi-language support (English, French, more)

**2. AI Coaching Engine**
- ✅ Live feedback on interview answers
- ✅ Strength/weakness analysis
- ✅ Personalized improvement suggestions
- ✅ Performance scoring system
- ✅ Comparison with industry benchmarks

**3. Session Management**
- ✅ Session state tracking
- ✅ Answer history preservation
- ✅ Progress tracking across multiple interviews
- ✅ Session-based coaching tips

**4. Report Generation**
- ✅ Comprehensive performance reports
- ✅ Detailed score breakdown
- ✅ Specific areas for improvement
- ✅ Recommended practice topics
- ✅ Export-ready analysis

---

### **Math Tutoring Module**

**1. Multi-Format Problem Input**
- ✅ Type math problems as text
- ✅ Upload problem photos (OCR extraction)
- ✅ Submit PDF files
- ✅ LaTeX notation support
- ✅ Auto-parsing and problem normalization

**2. Problem Classification & Analysis**
- ✅ Intelligent topic classification (Algebra, Calculus, Geometry, etc.)
- ✅ Difficulty assessment (1-5 scale)
- ✅ Required concepts identification
- ✅ Prerequisite skill detection
- ✅ Solution complexity estimation

**3. Interactive Step-by-Step Coaching**
- ✅ Problem classification with guided first question
- ✅ Student step validation with error detection
- ✅ Error type categorization (algebraic, logical, conceptual, notation)
- ✅ Confidence scoring for validations
- ✅ Detailed justification for each feedback

**4. Adaptive Hint System (4-Level)**
- ✅ **Level 1 - Nudge**: Small guidance without revealing approach
- ✅ **Level 2 - Concept**: Key theorem/formula reminder
- ✅ **Level 3 - Structure**: Logical breakdown of solution path
- ✅ **Level 4 - Reveal**: Near-complete step guidance
- ✅ Context-aware hints tailored to student's specific attempt

**5. Solution Generation**
- ✅ Complete step-by-step solutions
- ✅ LaTeX-formatted equations
- ✅ Concept explanations for each step
- ✅ Common mistakes to avoid
- ✅ Similar practice problems
- ✅ Prerequisites and advanced topics

**6. Progress Tracking**
- ✅ Completion detection
- ✅ Progress percentage calculation
- ✅ Step history tracking
- ✅ Solution attempt logging
- ✅ Learning analytics

---

## 🏗️ System Architecture

### Backend Architecture (FastAPI + Mistral AI)
```
┌─────────────────────────────────────┐
│   Frontend (React + Audio/Video)    │
├─────────────────────────────────────┤
│      REST API (FastAPI on 7860)     │
├─────────────────────────────────────┤
│  ┌────────┬──────────┬───────────┐  │
│  │Session │Interview │Math Tutor │  │
│  │Router  │Router    │Router     │  │
│  └────────┴──────────┴───────────┘  │
├─────────────────────────────────────┤
│  ┌────────┬──────────┬───────────┐  │
│  │Mistral │Whisper   │Analysis   │  │
│  │Service │Transcribe│Service    │  │
│  └────────┴──────────┴───────────┘  │
├─────────────────────────────────────┤
│   AI Engines:                       │
│   • Mistral mathstral-7b (Math)    │
│   • Whisper (Audio Transcription)  │
└─────────────────────────────────────┘
```

### Frontend Architecture (React Components)
```
App (Main Router)
├── Home (Landing Page)
├── InterviewCoach
│   ├── QuestionDisplay
│   ├── AnswerRecorder (Audio/Text)
│   ├── FeedbackDisplay
│   └── ProgressTracker
├── MathTutor
│   ├── ProblemInput (Multi-format)
│   ├── ProblemClassification
│   ├── StepValidator
│   ├── HintGenerator
│   ├── SolutionDisplay
│   └── ConversationHistory
└── Reports (Analytics & Insights)
```

---

## 🤖 AI-Powered Engines

### **1. Mistral mathstral-7b (Math Reasoning)**
Specialized mathematical reasoning model powering:
- Problem classification and difficulty assessment
- Step validation with error detection
- Adaptive hint generation at 4 levels
- Complete solution generation with LaTeX
- Progress tracking and completion detection

**Reasoning Coach Functions:**
```python
# Core functions
classify_problem(problem_text) → {topic, difficulty, concepts}
validate_step(problem, step_num, student_answer) → {correct, error_type}
generate_adaptive_hint(problem, step, attempt, level) → {hint, guidance}
generate_final_solution(problem, steps_history) → {steps, answer, concepts}
detect_completion(problem, steps_history) → {complete, progress}
```

### **2. Whisper (Audio Transcription)**
Speech-to-text for interview coaching:
- Real-time audio capture and transcription
- Multi-language support
- Automatic fallback to text input
- High accuracy transcription with noise filtering

### **3. Mistral Large (Interview Coaching)**
General-purpose AI engine for interview coaching:
- Answer evaluation and scoring
- Feedback generation
- Weakness identification
- Improvement suggestions
- Report generation

---

## 📊 Data Flow

### Interview Coaching Flow
```
1. User submits interview question → 2. AI evaluates answer
3. Real-time feedback displayed → 4. Coaching tips provided
5. Progress tracked → 6. Session saved
```

### Math Tutoring Flow
```
1. Problem input (text/photo/PDF) → 2. OCR extraction & parsing
3. Problem classified → 4. Student submits step
5. Step validated with error detection → 6. Adaptive hint provided
7. Student revises → 8. Process repeats or solution revealed
9. Complete solution with concepts → 10. Progress tracked
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **AI Models**: 
  - Mistral mathstral-7b (Math Reasoning)
  - Mistral Large 3 (Interview Coaching)
  - Whisper (Audio Transcription)
- **Server**: Uvicorn ASGI
- **Deployment**: Docker on HuggingFace Spaces

### Frontend  
- **Framework**: React 18.2+
- **Styling**: Custom CSS + KaTeX (Math Rendering)
- **Audio**: Whisper Integration
- **HTTP Client**: Axios with retry logic
- **Build**: Create React App

### Infrastructure
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: HuggingFace Spaces (serverless)
- **Demo Mode**: Works without API keys (fallback responses)

---

## 🎯 Use Cases

### For Students
✅ **Interview Prep**: Practice tech interviews with AI feedback  
✅ **Math Help**: Get hints, not just answers  
✅ **Learning**: Understand where mistakes happen  
✅ **Practice**: Unlimited problems with validation  

### For Educators  
✅ **Homework Support**: Students validate work before submission  
✅ **Concept Focus**: Spend class time on deep understanding  
✅ **Practice Assignment**: Scale student practice  
✅ **Analytics**: Track which concepts students struggle with  

### For Job Seekers
✅ **Interview Practice**: Realistic technical interview simulation  
✅ **Performance Feedback**: Know your strengths and weaknesses  
✅ **Benchmarking**: Compare against industry standards  
✅ **Progress Tracking**: Measure improvement over time  

---

## 🚀 Getting Started

### Try It Live
👉 [VoxaLab on HuggingFace Spaces](https://huggingface.co/spaces/mistral-hackaton-2026/voxalab)

### Features You Can Try
1. **Interview Coaching**: Select a question, answer in text or audio
2. **Math Tutoring**: Submit a problem, get guided step-by-step
3. **Reports**: View performance analytics
4. **Multi-language**: Switch between English/French

---

## 🎓 The Problem We Solve

**Challenge:**
- Limited access to qualified tutors and interview coaches
- Students need on-demand, 24/7 access to expert guidance
- One-size-fits-all solutions don't adapt to individual needs
- Cost barriers prevent many from accessing quality education

**Solution:**
- AI-powered coaching available anytime, anywhere
- Adaptive guidance tailored to each student
- Multi-modal learning (text, audio, visual)
- Free or low-cost access to expert-level instruction

---

## ✨ Why VoxaLab is Different

| Feature | Generic Tutoring Apps | VoxaLab |
|---------|----------------------|---------|
| Interview Practice | ❌ Limited questions | ✅ Unlimited + AI Feedback |
| Math Hints | ❌ Generic or none | ✅ 4-Level Adaptive Hints |
| Problem Input | ❌ Text only | ✅ Text/Photo/PDF/LaTeX |
| Error Detection | ❌ Wrong/Right only | ✅ Identifies error type |
| Feedback | ❌ Static | ✅ Personalized AI Analysis |
| 24/7 Available | ❌ Limited hours | ✅ Always on |
| Multi-Language | ❌ English only | ✅ English + French + more |
| Cost | ❌ Subscription | ✅ Free/Low-cost |

---



### 1. **Submit Any Math Problem - Any Way**

**Teachers don't care how you have the problem - neither do we:**

```
📝 Type it:           "Solve: 2x² + 5x - 3 = 0"
📸 Take a photo:      Photo of textbook/whiteboard problem
📄 Upload PDF:        Problem set from school
🔤 Upload LaTeX:      Academic notation with equations
```

**Our system automatically extracts and cleans the problem** - no copying, no retyping.

### 2. **Get Analyzed Like a Real Teacher**

PrepCoach reads your problem and identifies:

```json
{
  "topic": "Quadratic Equations",
  "why_it_matters": "Foundation for algebra, needed for engineering",
  "what_you_need_to_know": ["Factoring", "FOIL Method", "Zero Product Property"],
  "difficulty": "Level 2 (Beginner)",
  "common_student_mistakes": [
    "Forgetting to set factors to zero",
    "Wrong sign when factoring",
    "Not checking solutions"
  ]
}
```

**A real teacher does this analysis. Now AI does it consistently, instantly.**

### 3. **Get Guided, Not Just Answered**

Here's the key difference from other apps:

❌ **Wrong Way (Most Apps):**
```
Student: "Solve 2x² + 5x - 3 = 0"
App: "The answer is x = 1/2 or x = -3"
Student: "OK..." [doesn't understand, fails next test]
```

✅ **Right Way (PrepCoach):**
```
Student: "Solve 2x² + 5x - 3 = 0"
Coach: "💭 Think about what two numbers multiply to 6 but add to 5"
Student: "Hmm... 6 and -1?"
Coach: "Good try! But they need to add to positive 5. Try again."
Student: "Oh! 6 and... no wait. -2 and -3?"
Coach: "Even closer! But you need positive 5. Think positive numbers that multiply to 6."
Student: "2 and 3!"
Coach: "Perfect! Now write it as (2x - ?)(x + ?) = 0"
```

**You learn by thinking, not by copying.**

### 4. **Validate Every Step You Take**

Unlike homework help sites that just give answers:

```
Your step:     2x² + 5x - 3 = 0
               (2x - 1)(x + 3) = 0

Coach checks:  ✓ Algebra correct?
               ✓ Factoring valid?
               ✓ Did you use right method?
               
Feedback:      "Excellent! You've factored correctly. 
                This shows you understand FOIL in reverse.
                Now, what's the next step?"
```

**Wrong step?**
```
Your step:     (2x + 1)(x - 3) = 0

Coach checks:  ✗ Let me verify: (2x + 1)(x - 3) = 2x² - 6x + x - 3 = 2x² - 5x - 3
               This is NOT your original equation (2x² + 5x - 3)
               
Guidance:      "The signs are wrong. Let me ask you:
                - What two numbers multiply to -6?
                - Which pair adds to +5?"
```

**Real teaching: Finding mistakes and helping you fix them.**

### 5. **Download Solutions in Any Format**

When you finish, you get the complete solution:

- **📝 Markdown** - For study notes, easy to share
- **📐 LaTeX** - For writing essays, reports, theses
- **🌐 HTML** - For showing friends, posting online
- **📊 JSON** - For data analysis, tracking progress

---

## 🧠 Why MathΣtral: AI That Actually Understands Math

**Problem:** Regular AI (like ChatGPT) is good at language, not math.

- Makes arithmetic errors
- Suggests wrong approaches
- Doesn't understand proof structure
- Fails on advanced topics

**Solution: MathΣtral** - AI specifically trained for mathematics

**What MathΣtral can do:**

✅ Rigorous algebra (catches every error)  
✅ Calculus (derivatives, integrals, limits)  
✅ Linear algebra (matrices, eigenvalues)  
✅ Differential equations (ODEs, PDEs)  
✅ Abstract algebra (groups, rings, fields)  
✅ Real/complex analysis (proofs, convergence)  
✅ Discrete math (combinatorics, graph theory)  
✅ Statistics (distributions, hypothesis testing)  
✅ Physics & chemistry math  

**It validates not just algebra, but your mathematical thinking.**

---

## 💡 What Students Can Do

### 📚 Complete Your Homework

```
Friday Night Homework Due Monday:
❌ Before: Stuck on problem 5, don't know where to start
✅ After: Take photo, get guided through solution, understand concept

Result: Complete homework + Actually learn math
```

### 🧪 Practice Test Preparation

```
Exam in 2 weeks, 20 topics to cover:
❌ Before: No one to help check practice problems
✅ After: Solve practice problems, validate each step, see if you're ready

Result: Better test scores, less anxiety, actual confidence
```

### 🔍 Understand Where You Failed

```
Test back: You got it wrong. Why?
❌ Before: Teacher too busy, classmates don't know, you stay confused
✅ After: Upload test problem, coach explains exactly where logic went wrong

Result: Learn from mistakes instead of repeating them
```

### 🚀 Prepare for University

```
Competitive exam for engineering/medicine:
❌ Before: No tutors in your town, can't afford them
✅ After: Thousands of practice problems, unlimited guidance, 24/7

Result: Get into university, change your life
```

### 💼 Get a Tech Job

```
Software engineering interview in 2 months:
❌ Before: No one in your area knows tech interviews
✅ After: Practice with AI, get scored, improve weak areas

Result: Land job, earn income, support family
```

---

## 🎓 For Teachers & Educators

**Don't worry - this isn't replacing you. You're too valuable.**

**What teachers can do:**

✅ **Use PrepCoach for homework help** - Students can validate work before submission  
✅ **Focus on concepts** - Spend class time on understanding, not answering questions  
✅ **Assign practice** - Students practice unlimited problems with AI validation  
✅ **Track progress** - See which concepts students struggle with  
✅ **Free up time** - Reduce time grading routine homework  

**The result:** Teachers focus on teaching. Students actually learn.

---

## 🌍 Impact So Far

**Built by:** Idris Bado, AI Engineer (From Ivory Coast, for Africa)

**Deployed on:** Hugging Face Spaces (Free, always available)

---

## 🚀 Try It Now

Visit: [VoxaLab Hugging Face Spaces](your-hf-link-here)

Or run locally:
```bash
git clone https://github.com/idrissbado/VoxaLabs.git
cd voicecoach-ai/voicecoach-ai
# See DEPLOY.md for full setup
```

---

## 📖 Documentation

- [Quick Start Guide](MATH_TUTOR_GUIDE.md) - How to use it
- [Demo Script](DEMO_SCRIPT.md) - See it in action  
- [Session Summary](SESSION_SUMMARY.md) - Technical details

---

## 1. Interview Coaching System

#### Core Capabilities
- **5 Professional Roles** - Backend, Frontend, DevOps, Data Scientist, Product Manager
- **40+ Role-Specific Questions** - Carefully researched technical questions
- **Dual Input Methods**:
  - 🎤 **Voice Recording** - Real-time audio capture with Whisper transcription
  - ⌨️ **Text Typing** - Manual answer entry
- **Real-time Transcription** - OpenAI Whisper converts speech to text instantly

#### AI Coaching Features
- **Performance Scoring** (0-100)
  - 📊 Clarity Score (0-10) - Communication clarity and pacing
  - 📊 Structure Score (0-10) - Logical flow and organization
  - 📊 Impact Score (0-10) - Quantified results and business value
- **Detailed Feedback**
  - ✅ **Strengths** - What you did well
  - 📈 **Improvements** - Actionable areas to work on
  - 💡 **Coaching Tips** - Personalized recommendations
  - 🎯 **STAR Analysis** - Situation, Task, Action, Result evaluation
  - 🎤 **Voice Feedback** - Hear tips spoken naturally

#### Session Management
- **Session Reports** - Comprehensive analysis after completing interview
- **Performance Metrics** - Average scores, question-by-question breakdown
- **Real-time UI State** - "🤖 Analyzing..." spinner during processing
- **Score Breakdown Visualization** - Progress bars for Clarity, Structure, Impact

### 2. Math Tutoring System

#### Features
- **Problem Analysis** - Classify type, difficulty, and required concepts
- **Step Validation** - Verify each solving step is correct
- **Solution Generation** - LaTeX-formatted complete solutions
- **Practice Problems** - Generate similar problems for practice
- **3-Phase Workflow**:
  1. **Input Problem** - Enter mathematical problem
  2. **Solve & Validate** - Work through steps with validation
  3. **Review Solution** - See complete solution with explanations

#### Supported Topics
- Linear Algebra, Calculus, Probability & Statistics
- Discrete Mathematics, Physics, Chemistry
- And many more...

### 3. Advanced UI/UX

#### Real-time Feedback Display
- **Analyzing State** - Animated spinner shows "🤖 Analyzing Your Response..."
- **Instant Results** - Feedback appears immediately after analysis
- **Visual Score Bars** - Progress bars show Clarity, Structure, Impact
- **Formatted Lists** - Strengths and improvements displayed clearly
- **Voice Feedback** - "Hear Coach Voice" button plays audio

#### Responsive Design
- 📱 Mobile-friendly interface
- 🌙 Dark theme with professional aesthetics
- ✨ Smooth animations and transitions
- ♿ Accessible keyboard navigation

### 4. Multi-Language Support
- 🇬🇧 English
- 🇫🇷 Français
- 🇪🇸 Español
- 🇩🇪 Deutsch
- 🇨🇳 中文
- 🇯🇵 日本語

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    VoxaLab AI Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Frontend (React 18.2)                       │   │
│  │  Landing | Interview Coach | Math Tutor | Reports    │   │
│  │  - Audio Recording (Web Audio API)                   │   │
│  │  - Real-time Analyzing State with spinner            │   │
│  │  - Feedback with scores & lists                      │   │
│  │  - LaTeX Math Rendering                              │   │
│  │  - Dark theme animations                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                    ↓ (Axios HTTP)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Backend (FastAPI + Uvicorn)                   │   │
│  │  ┌─────────────────────────────────────────────────┐ │   │
│  │  │ API Routers (25+ endpoints)                    │ │   │
│  │  │ ├── /session - Session management             │ │   │
│  │  │ ├── /analysis - Audio & text analysis         │ │   │
│  │  │ ├── /report - Reports                         │ │   │
│  │  │ ├── /tts - Text-to-speech                     │ │   │
│  │  │ └── /math - Math tutor                        │ │   │
│  │  └─────────────────────────────────────────────────┘ │   │
│  │  ┌─────────────────────────────────────────────────┐ │   │
│  │  │ Core Services                                  │ │   │
│  │  │ ├── Mistral Service (LLM coaching)            │ │   │
│  │  │ ├── Math Tutor Service                        │ │   │
│  │  │ ├── Scoring Engine                            │ │   │
│  │  │ ├── Voxtral Service (Transcription)           │ │   │
│  │  │ └── TTS Service (Voice synthesis)             │ │   │
│  │  └─────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│                     ↓                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │       External AI & Services                        │   │
│  │  • Mistral Large 3 (AI coaching engine)            │   │
│  │  • OpenAI Whisper (Speech-to-text)                 │   │
│  │  • ElevenLabs (Text-to-speech)                     │   │
│  │  • LangChain (Prompt orchestration)                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: Interview Coaching

```
1. User Input (Voice/Text)
        ↓
2. Frontend Records Audio / Accepts Text
        ↓
3. POST /session/answer {question, answer, role, language}
        ↓
4. Backend: Transcribe (if audio) + Analyze
        ↓
5. Mistral AI: Generate Coaching Feedback
        ↓
6. Response: {
     score: 78/100,
     feedback: "Good Response",
     tips: "Add specific metrics...",
     strengths: ["Clear", "Good structure"],
     improvements: ["Add examples"],
     clarity_score: 8,
     structure_score: 7,
     impact_score: 8
   }
        ↓
7. Frontend: Show "🤖 Analyzing..." for 2-5 seconds
        ↓
8. Display Complete Feedback Panel:
   - Score circle (78/100)
   - Coaching tips
   - Strengths list
   - Improvements list
   - Score bars (Clarity, Structure, Impact)
   - Voice button + Next Question
```

### Component Architecture

**Frontend:**
```
App.js (Main Container - 849 lines)
├── Landing Page
├── Interview Coach
│   ├── Role Selection
│   ├── Question Display
│   ├── Input Method Selector (Voice/Text)
│   ├── Recording Component
│   ├── Analyzing State (Loading with spinner)
│   ├── Feedback Panel (Score + Details)
│   └── Navigation
├── Math Tutor (MathTutor.js - 399 lines)
├── About Page
└── Report Page

App.css (2500+ lines)
├── Dark theme variables
├── Component styling
├── Animations & transitions
├── Responsive breakpoints
└── Accessibility rules
```

**Backend:**
```
main.py / app.py (Entry point)
├── Router Registration
│   ├── /session
│   ├── /analysis
│   ├── /report
│   ├── /tts
│   └── /math
│
├── Services
│   ├── mistral_service.py (547 lines)
│   │   └── generate_coaching_feedback()
│   ├── math_tutor.py (361 lines)
│   ├── scoring_engine.py (200+ lines)
│   ├── voxtral_service.py (100+ lines)
│   └── tts_service.py (80 lines)
│
└── Error Handling & Logging
```

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18.2.0 | UI Framework |
| Axios | 1.6.0+ | HTTP Client |
| React Icons | Latest | UI Components |
| Web Audio API | Native | Audio Recording |
| MathJax | Latest | LaTeX Rendering |
| CSS3 | Native | Styling & Animations |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.134.0+ | REST API |
| Pydantic | 2.11.7+ | Data Validation |
| Uvicorn | 0.25.0+ | ASGI Server |
| Python | 3.11+ | Language |
| AsyncIO | Native | Async Operations |

### AI & ML
| Technology | Purpose |
|-----------|---------|
| Mistral Large 3 | LLM Coaching Engine |
| LangChain | Prompt Orchestration |
| OpenAI Whisper | Speech-to-Text |
| ElevenLabs | Text-to-Speech |

### Deployment
| Technology | Purpose |
|-----------|---------|
| Docker | Containerization |
| HuggingFace Spaces | Production Deployment |
| Git/GitHub | Version Control |

---

## 🚀 Quick Start

### 1-Minute: Live Demo
Visit: https://huggingface.co/spaces/mistral-hackaton-2026/voxalab

### 5-Minute: Local Setup

#### Prerequisites
```bash
python --version      # Must be 3.10+
node --version        # Must be 16+
```

#### Step 1: Clone
```bash
git clone https://github.com/idrissbado/VoxaLabs.git
cd VoxaLabs
```

#### Step 2: Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Step 3: Frontend Setup
```bash
cd ../frontend
npm install
```

#### Step 4: Configure
Create `backend/.env`:
```
MISTRAL_API_KEY=your-key-from-console.mistral.ai
ELEVENLABS_API_KEY=your-elevenlabs-key
HOST=0.0.0.0
PORT=8000
ENV=development
```

#### Step 5: Run

**Terminal 1:**
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

**Terminal 2:**
```bash
cd frontend
npm start
# Runs on http://localhost:3000
```

Open: http://localhost:3000 ✅

---

## 📚 Full Documentation

### Installation Guide
See detailed setup in [ARCHITECTURE.md](ARCHITECTURE.md)

### Usage Guide

#### Interview Coaching
1. Select Role (Backend Engineer, Frontend, etc.)
2. Select Language
3. Answer questions via voice or text
4. Get instant AI feedback
5. View performance report

#### Math Tutoring
1. Enter mathematical problem
2. System analyzes and provides hints
3. Solve step-by-step
4. View complete solution

### API Endpoints

**Session Management**
```
GET    /session/questions?role=backend&language=en
POST   /session/answer {question, user_answer, language, role}
```

**Analysis**
```
POST   /analysis/transcribe {audio_data}
POST   /analysis/feedback {question, answer}
```

**Math Tutor**
```
POST   /math/analyze {problem}
POST   /math/validate-step {problem, step}
POST   /math/generate-solution {problem}
```

**Full API Docs**: http://localhost:8000/docs (Swagger UI)

---

## 📁 Project Structure

```
VoxaLabs/
├── frontend/
│   ├── src/
│   │   ├── App.js (849 lines - Main React component)
│   │   ├── MathTutor.js (399 lines - Math interface)
│   │   ├── App.css (2500+ lines - Styling)
│   │   └── index.html
│   ├── build/ (Production build)
│   │   └── static/
│   │       ├── js/main.2e73ceaf.js (70.48 kB gzipped)
│   │       └── css/main.c8080534.css (6.67 kB gzipped)
│   └── package.json
│
├── backend/
│   ├── main.py (FastAPI app)
│   ├── app.py (HF Spaces entry point)
│   ├── requirements.txt (All dependencies)
│   ├── routers/
│   │   ├── session.py (Session management)
│   │   ├── analysis.py (Audio/text analysis)
│   │   ├── report.py (Reports)
│   │   ├── tts.py (Text-to-speech)
│   │   └── math_tutor.py (Math endpoints)
│   └── services/
│       ├── mistral_service.py (LLM integration)
│       ├── math_tutor.py (Math logic)
│       ├── scoring_engine.py (Scoring)
│       ├── voxtral_service.py (Transcription)
│       └── tts_service.py (Voice synthesis)
│
├── README.md (This file)
├── ARCHITECTURE.md (Technical docs)
└── DEPLOY.md (Deployment guide)
```

---

## ⚙️ Configuration

### Environment Variables

Create `backend/.env`:

```bash
# Required
MISTRAL_API_KEY=your-36-char-key

# Optional
ELEVENLABS_API_KEY=your-elevenlabs-key
HOST=0.0.0.0
PORT=8000
ENV=production
LOG_LEVEL=INFO
DEBUG=false
```

### Get API Keys

- **Mistral**: https://console.mistral.ai (Free tier available)
- **ElevenLabs**: https://elevenlabs.io (Optional, for voice feedback)

---

## 🚀 Deployment

### Option 1: HuggingFace Spaces (Recommended)

Already live at: https://huggingface.co/spaces/mistral-hackaton-2026/voxalab

**To deploy your own:**
1. Fork repo on GitHub
2. Create HF Space
3. Connect to GitHub fork
4. Set MISTRAL_API_KEY secret
5. Deploy automatically ✅

### Option 2: Docker

```bash
docker build -t voicecoach-backend ./backend
docker run -e MISTRAL_API_KEY=$KEY -p 8000:8000 voicecoach-backend
```

### Option 3: Traditional Server

```bash
# Backend
cd backend && pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

# Frontend
cd frontend && npm run build && serve -s build -l 3000
```

---

## 🐛 Troubleshooting

### Backend Issues

**"RuntimeError: Directory not found"**
```bash
cd frontend && npm run build
git add -f frontend/build/static && git push
```

**"MISTRAL_API_KEY not found"**
- Create `.env` file in backend directory
- Add: `MISTRAL_API_KEY=your-key`
- Restart server

**"Whisper import failed"**
```bash
pip install openai-whisper torch torchaudio
python main.py  # First run takes 1-2 min
```

### Frontend Issues

**"Module not found"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install && npm start
```

**"Port 3000 already in use"**
```bash
# Change port or kill process
npm start -- --port 3001
```

---

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Audio Recording | Real-time | Browser-based |
| Speech-to-Text | 2-5s | First: 10-15s (model load) |
| AI Analysis | 5-8s | Mistral API |
| Voice Synthesis | 3-5s | ElevenLabs |
| **Total Response** | **15-25s** | End-to-end |

**Build Sizes:**
- Frontend JS: 70.48 kB (gzipped)
- Frontend CSS: 6.67 kB (gzipped)
- Total: ~77 kB

---

## 🤝 Contributing

```bash
# 1. Fork and clone
git clone https://github.com/idrissbado/VoxaLabs.git

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes
# ... edit files ...

# 4. Test locally
cd backend && python main.py
cd frontend && npm start

# 5. Commit and push
git add .
git commit -m "feat: description"
git push origin feature/your-feature

# 6. Create Pull Request
```

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🔗 Links

- **Live Demo**: https://huggingface.co/spaces/mistral-hackaton-2026/voxalab
- **GitHub**: https://github.com/idrissbado/VoxaLabs
- **API Docs**: http://localhost:8000/docs
- **Mistral**: https://mistral.ai

---

## 📞 Support

- **Documentation**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: [GitHub Issues](https://github.com/idrissbado/VoxaLabs/issues)
- **API Help**: http://localhost:8000/docs

---

<div align="center">

### Built with ❤️ using Mistral AI

**Star ⭐ this repository if you found it helpful!**

[GitHub](https://github.com/idrissbado/VoxaLabs) • [Live Demo](https://huggingface.co/spaces/mistral-hackaton-2026/voxalab)

Last Updated: February 28, 2026

</div>
