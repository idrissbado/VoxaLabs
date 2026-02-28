# 🎤 VoxaLab AI - Interview & Math Coaching Platform

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-green)
![React](https://img.shields.io/badge/React-18.2%2B-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.134%2B-009688?logo=fastapi)
![Mistral AI](https://img.shields.io/badge/Mistral%20AI-Large%203-FF6B35)
![License](https://img.shields.io/badge/License-MIT-green)

**AI-Powered Coaching Platform for Technical Interviews & Mathematics Education**

[🚀 Live Demo](#live-demo) • [📚 Features](#-features) • [🏗️ Architecture](#-architecture) • [⚡ Quick Start](#-quick-start)

</div>

---

## 📋 Overview

**VoxaLab AI** is a comprehensive full-stack platform powered by **Mistral Large 3** that provides:

✅ **Interview Coaching** - Real-time AI feedback for technical interview practice  
✅ **Math Tutoring** - Step-by-step problem solving with validation  
✅ **Multi-language Support** - Practice in 6+ languages  
✅ **Real-time Feedback** - Instant analysis with visual loading state  
✅ **Audio/Voice Integration** - Whisper transcription + ElevenLabs voice synthesis  

---

## ✨ Key Features

### 1. Interview Coaching System

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
