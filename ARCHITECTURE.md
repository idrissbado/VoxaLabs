# VoiceCoach AI - System Architecture

## Problem Statement

**Interview preparation is broken.** Candidates lack real-time feedback on their communication skills, body language isn't captured, and most practice resources only provide generic tips. They need an intelligent, personalized AI coach that:

- Provides **instant feedback** on clarity, structure, and impact
- Detects **filler words** and communication patterns
- Validates use of the **STAR method** (Situation, Task, Action, Result)
- Adapts to **different roles** (Software Engineer, Product Manager, Data Scientist, Designer, Marketing)
- Offers **voice recording** with AI transcription and analysis
- Generates **detailed reports** to track improvement

**VoiceCoach AI** solves this by combining cutting-edge AI (Mistral Large 3), real-time voice capture, and intelligent coaching to simulate authentic interview conditions.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│                    (React 18.2.0 SPA)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Landing Page    │ Practice Page    │ Report Page        │  │
│  │ • Role Select   │ • Q&A Interface  │ • Performance      │  │
│  │ • Coach Bio     │ • Voice Record   │ • Scores           │  │
│  │ • Features      │ • Feedback Loop  │ • Insights         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  Web Audio API │ Axios HTTP │ CSS Animations                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓ REST API
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                          │
│                    (FastAPI 0.134.0)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ CORS Middleware  │  Request Validation  │ Error Handler  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  Routers: /session │ /analysis │ /report                      │
└─────────────────────────────────────────────────────────────────┘
             ↓                 ↓                 ↓
    ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐
    │ SESSION ROUTER │  │ANALYSIS ROUTER  │  │ REPORT ROUTER    │
    │ Create Session │  │ Analyze Text    │  │ Generate Report  │
    │ Get Questions  │  │ Analyze Audio   │  │ Summary Stats    │
    │ Track Progress │  │ Improved Answer │  │ Recommendations  │
    └────────────────┘  └─────────────────┘  └──────────────────┘
             ↓                 ↓                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICES LAYER (Business Logic)              │
│                                                                  │
│  ┌────────────────────┐  ┌──────────────────┐                  │
│  │ MistralAI Service  │  │ Scoring Engine   │                  │
│  │ • Chat Completion  │  │ • Filler Words   │                  │
│  │ • Prompt Chains    │  │ • STAR Validator │                  │
│  │ • Answer Coaching  │  │ • Question Bank  │                  │
│  │ • Follow-ups       │  │ • Report Builder │                  │
│  └────────────────────┘  └──────────────────┘                  │
│                                                                  │
│  ┌────────────────────┐  ┌──────────────────┐                  │
│  │ Voxtral Service    │  │ LangChain Chains │                  │
│  │ • Voice to Text    │  │ • Memory         │                  │
│  │ • Audio Process    │  │ • Chain Pipeline │                  │
│  │ • Speech Analysis  │  │ • Prompt Mgmt    │                  │
│  └────────────────────┘  └──────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────────────────────────┐
│              EXTERNAL AI SERVICES & TOOLS                        │
│                                                                  │
│  Mistral Large 3 API (Advanced Language Model)                 │
│  ├─ 128K Context Window                                        │
│  ├─ Multi-turn Conversations                                   │
│  ├─ JSON Structured Output                                     │
│  └─ Real-time Inference                                        │
│                                                                  │
│  LangChain Framework (Orchestration & Memory)                   │
│  ├─ Prompt Templates                                           │
│  ├─ LLM Chains                                                 │
│  ├─ Session Memory                                             │
│  └─ Output Parsing                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### Frontend (React 18.2.0 + Axios)

**State Management:**
- `page`: Current view (landing, practice, report)
- `selectedRole`: Interview role (5 options)
- `sessionId`: Current practice session ID
- `currentQuestion`: Active interview question
- `feedback`: AI coaching response
- `sessionAnswers`: Array of all answers + feedback
- `isRecording`: Audio recording state
- `recordingTime`: Duration counter

**Key Components:**
1. **Landing Page** - Role selection, Coach bio (Idriss), features overview
2. **Practice Page** - Question display, voice/text input, real-time feedback
3. **Report Page** - Performance metrics, strengths, areas to improve

**Audio Pipeline:**
```
getUserMedia() → MediaRecorder → Blob → Base64 → API → Transcription → Analysis
```

### Backend (FastAPI + Pydantic)

**Router Architecture:**

#### `/session` Router
- `POST /session/create` - Initialize practice session with role
- `GET /session/{id}` - Retrieve session details
- `POST /session/{id}/next` - Get next question

#### `/analysis` Router
- `POST /analysis/text` - Analyze typed answer
- `POST /analysis/audio` - Transcribe and analyze audio
- `POST /analysis/improved-answer` - Generate improved version with STAR method

#### `/report` Router
- `POST /report/generate` - Create comprehensive session report
- `GET /report/{id}` - Retrieve saved report

### Services Layer

#### 1. **Mistral AI Service** (`mistral_service.py`)
Handles all AI-powered coaching using Mistral Large 3:

```python
async def generate_improved_answer(question, answer, role)
├─ System Prompt: "You are an elite interview coach..."
├─ User Prompt: "Improve this {role} answer using STAR method"
└─ Returns: Structured JSON with example, explanation, tips

async def generate_follow_up_questions(question, answer)
├─ Creates 3 likely follow-up questions
├─ Bases on answer quality and depth
└─ Integrates with LangChain for memory

async def generate_coaching_feedback(transcript, question, role)
├─ Analyzes communication patterns
├─ Scores clarity, structure, impact
├─ Identifies opportunities
└─ Returns: Detailed feedback object
```

#### 2. **LangChain Integration** (NEW)
Orchestrates complex AI workflows with memory and chains:

```python
# Prompt Templates
├─ COACHING_PROMPT: For answer analysis
├─ IMPROVEMENT_PROMPT: For STAR method examples
├─ FOLLOWUP_PROMPT: For question generation
└─ REPORT_PROMPT: For comprehensive summary

# LLM Chain
├─ Connects Mistral model with prompts
├─ Manages token counting
├─ Handles streaming responses
└─ Fallback mechanisms

# Memory Management
├─ Session-based conversation history
├─ Context awareness across questions
├─ User performance tracking
└─ Role-specific coaching history
```

#### 3. **Scoring Engine** (`scoring_engine.py`)
Local NLP analysis without external APIs:

```python
detect_filler_words(transcript)
├─ Common filler patterns: "um", "uh", "like", "you know"
├─ Counts frequency
└─ Returns: List with word + count

check_star_method(transcript)
├─ Situation: Initial context detection
├─ Task: Objective/challenge identification
├─ Action: Steps taken analysis
├─ Result: Outcome/impact assessment
└─ Returns: Completion percentage + details

get_questions(role)
├─ 8 role-specific interview questions
├─ Difficulty progression
├─ Varies by role (Software Engineer, PM, Designer, etc.)
└─ Returns: Ordered list for session

generate_full_report(session_answers, role)
├─ Aggregates all answers
├─ Calls Mistral for comprehensive analysis
├─ Generates strengths, improvements, tips
└─ Returns: Professional report summary
```

#### 4. **Voice Service** (`voxtral_service.py`)
Handles audio processing and transcription:

```python
transcribe_audio(audio_base64)
├─ Production: Integrates with Voxtral-Realtime API
├─ Current: Demo transcription (shows realistic examples)
└─ Returns: Cleaned transcript text

analyze_voice_answer(transcript, question, role)
├─ Calls Mistral for coaching feedback
├─ Parses JSON response (scores, insights)
└─ Returns: Voice analysis feedback object
```

---

## Data Flow

### 1. Session Initialization
```
User selects role
        ↓
POST /session/create
        ↓
Backend creates session
        ↓
Backend returns first question
        ↓
Frontend displays question
```

### 2. Answer Analysis (Text Path)
```
User types answer
        ↓
User clicks "Submit Answer"
        ↓
POST /analysis/text {question, answer, role}
        ↓
Scoring Engine analyzes
        ↓
Mistral Service generates feedback
        ↓
Backend returns feedback object {scores, filler_words, recommendations}
        ↓
Frontend displays coaching feedback
```

### 3. Answer Analysis (Voice Path)
```
User clicks 🎤 Record
        ↓
Browser captures audio (MediaRecorder API)
        ↓
User speaks answer
        ↓
User clicks Stop
        ↓
Browser converts audio to Base64
        ↓
POST /analysis/audio {audio_base64, question, role}
        ↓
Backend transcribes (Voxtral API or demo)
        ↓
Same analysis as text path
        ↓
Frontend displays transcript + feedback
```

### 4. Report Generation
```
User completes 5 questions
        ↓
User clicks "Generate Final Report"
        ↓
POST /report/generate {session_id, role, all_answers}
        ↓
Scoring Engine aggregates statistics
        ↓
Mistral Service generates comprehensive report
        ↓
Backend returns report {summary, strengths, improvements, tips}
        ↓
Frontend displays beautiful report view
```

---

## Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI framework, state management |
| Axios | 1.6.0 | HTTP client for API calls |
| CSS3 | Latest | Animations, dark theme, responsive |
| Web Audio API | Native | Browser microphone access |
| JavaScript ES6+ | Latest | Modern async/await patterns |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.134.0 | REST API framework, auto-docs |
| Pydantic | 2.11.7 | Data validation, typing |
| Uvicorn | 0.41.0 | ASGI server |
| Python | 3.11+ | Core language |
| python-dotenv | 1.1.1 | Environment configuration |
| Mistral AI SDK | 1.12.4 | LLM API client |
| LangChain | 0.1+ | Orchestration & chains |
| Regex | Built-in | Pattern matching for analysis |

### External Services
| Service | Purpose |
|---------|---------|
| Mistral Large 3 | Advanced language model for coaching |
| LangChain | Prompt management, chains, memory |
| Voxtral-Realtime | Production audio transcription |

---

## Question Bank Structure

### 5 Interview Roles × 8 Questions Each = 40 Total Questions

**Roles:**
1. **Software Engineer** - Algorithm design, debugging, system design
2. **Product Manager** - Product strategy, metrics, user research
3. **Designer** - Design thinking, user experience, collaboration
4. **Data Scientist** - Statistical analysis, modeling, insights
5. **Marketing** - Campaign strategy, market analysis, growth

**Question Progression:**
- Q1-3: Warm-up questions (easier, confidence building)
- Q4-6: Medium difficulty (core competencies)
- Q7-8: Challenge questions (advanced problem-solving)

---

## Security & Scalability

### Security Measures
- **CORS Configuration**: Controlled origin access
- **Input Validation**: Pydantic for all requests
- **Environment Variables**: Sensitive keys in `.env` (not committed)
- **Error Handling**: Generic error messages to client
- **HTTPS Ready**: Production deployment requires SSL certificates

### Scalability Considerations
- **Stateless API**: Sessions stored in memory (upgradeable to Redis/Database)
- **Async Operations**: All I/O operations are async
- **LangChain Caching**: Reduces redundant API calls
- **Token Optimization**: Prompt engineering to minimize token usage
- **Rate Limiting**: Can be added per endpoint
- **Database Integration**: Ready for PostgreSQL/MongoDB for persistence

### Future Enhancements
- User authentication (OAuth2/JWT)
- Session persistence (PostgreSQL)
- Advanced voice features (emotion detection, accent analysis)
- Video recording (body language feedback)
- Peer comparison (anonymized benchmarking)
- Mobile app (React Native)
- Multi-language support
- Integration with LinkedIn/job boards

---

## Deployment Architecture

```
┌─────────────────┐
│   Candidate     │
│   Browser       │
└────────┬────────┘
         │
    HTTPS/HTTP
         │
  ┌──────▼───────┐
  │  CDN/Static  │  (Vercel/Netlify)
  │  React App   │
  └──────┬───────┘
         │
    REST API
         │
  ┌──────▼──────────┐
  │   FastAPI       │  (Railway/Render)
  │   Backend       │
  └────────┬────────┘
           │
   ┌──────┴────────┐
   │               │
┌──▼──┐      ┌────▼─────┐
│Mistral│  │LangChain  │
│  API  │  │Framework  │
└───────┘  └───────────┘
```

---

## Getting Started

### Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

### Testing the Flow
1. Open http://localhost:3000
2. Select a role (e.g., "Software Engineer")
3. Click "Start Practice Session"
4. Type or record an answer to Question 1
5. Review AI coaching feedback
6. Progress through 5 questions
7. Generate comprehensive report

---

## Performance Metrics

- **API Response Time**: < 500ms for text analysis, < 2s for report generation
- **Frontend Load Time**: < 2s (React app compiled)
- **Audio Recording**: Real-time with < 100ms latency
- **Mistral API Call**: 1-3 seconds (depends on response length)
- **LangChain Chain Execution**: < 500ms with caching

---

## Contributing & Maintenance

See [DEPLOY.md](DEPLOY.md) for production deployment procedures and [README.md](README.md) for user-facing documentation.

For technical questions or improvements, refer to this architecture document and the inline code comments throughout the codebase.
