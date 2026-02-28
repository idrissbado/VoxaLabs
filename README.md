# VoxaLab AI

## Professional Interview Coaching Platform

Powered by Mistral Large 3 AI for intelligent, real-time interview coaching. Practice your technical interview skills with instant feedback in 6 languages.

---

## Overview

VoxaLab AI is a modern, full-stack application that provides personalized interview coaching through advanced AI analysis. Whether you prefer speaking or typing, the system captures your response, analyzes it with Mistral Large 3, and provides instant coaching feedback with actionable insights.

## Core Features

- Interview practice for 5 technical roles
- Dual input methods (text typing and audio recording)
- Real-time speech transcription
- AI-powered coaching feedback with scoring
- Audio playback of coach responses
- Multi-language support (6 languages)
- Professional analysis across key dimensions

---

## Technology Stack

### Frontend
- React 18.2 - User interface
- Axios - HTTP communication
- React Icons - Professional UI components
- Web Audio API - Audio recording capability
- Responsive CSS design

### Backend
- FastAPI - REST API framework
- Mistral Large 3 - AI coaching engine
- LangChain - Prompt orchestration
- OpenAI Whisper - Speech recognition
- ElevenLabs - Text-to-speech conversion
- Uvicorn - ASGI production server

---

## Quick Start

### Prerequisites
- Python 3.10 or later
- Node.js 16 or later
- npm package manager

### Installation

1. Clone repository
```bash
git clone <repository-url>
cd voicecoach-ai
```

2. Backend setup
```bash
cd backend
pip install -r requirements.txt
```

3. Frontend setup
```bash
cd frontend
npm install
```

4. Environment configuration
Create `.env` file in backend directory:
```
MISTRAL_API_KEY=your-mistral-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
HOST=0.0.0.0
PORT=8000
ENV=production
```

### Running the Application

Terminal 1 - Backend:
```bash
cd backend
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

Open http://localhost:3000 in your browser

---

## Usage Guide

### Step 1: Select Your Role
Choose from five technical positions:
- Backend Engineer (Spring Boot, Microservices)
- Frontend Engineer (React, Performance Optimization)
- DevOps Engineer (CI/CD, Infrastructure)
- Data Scientist (Machine Learning, Statistics)
- Product Manager (Strategy, User Focus)

Select your preferred language from 6 options.

### Step 2: Respond to Questions
For each question, choose your input method:

**Text Input**
- Click the text input section
- Write your response in the textarea
- Click "Get Feedback"

**Audio Recording**
- Click the recording section
- Click "Start Recording"
- Speak your response clearly
- Click "Stop Recording"
- Click "Get Feedback"

### Step 3: Review Feedback
The system provides:
- Your transcribed response (for audio input)
- Personalized coaching feedback
- Clarity score (0 to 10)
- Depth score (0 to 10)
- Communication score (0 to 10)
- Audio playback of feedback

### Step 4: Navigate Questions
- Use "Next Question" to continue
- Use "Previous" to review earlier questions
- Click "Finish" to complete the interview

### Step 5: View Results
Access your session report showing:
- All responses and feedback
- Performance scores
- Key insights
- Improvement recommendations

---

## API Endpoints

### Session Management
- `POST /session/create` - Start new coaching session
- `GET /session/{session_id}` - Retrieve session details
- `GET /session/questions` - Get questions for role and language

### Analysis
- `POST /analysis/audio` - Transcribe and analyze audio
- `POST /analysis/feedback` - Analyze text answer

### Text-to-Speech
- `POST /tts/speak` - Convert coaching feedback to audio
- `GET /tts/voices` - Get available voices

### Reports
- `GET /report/{session_id}` - Generate session report

---

## Project Structure

```
voicecoach-ai/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── session.py
│   │   ├── analysis.py
│   │   ├── report.py
│   │   └── tts.py
│   └── services/
│       ├── voxtral_service.py
│       ├── mistral_service.py
│       ├── tts_service.py
│       └── scoring_engine.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.html
│   ├── package.json
│   └── public/
└── docker-compose.yml
```

---

## Technical Roles

1. **Backend Engineer**
   - Focus on system design and scalability
   - Technologies: Java, Spring Boot, microservices
   - Questions on architecture, databases, APIs

2. **Frontend Engineer**
   - Focus on UI/UX and performance
   - Technologies: React, TypeScript, CSS
   - Questions on components, state management

3. **DevOps Engineer**
   - Focus on infrastructure and deployment
   - Technologies: Docker, Kubernetes, CI/CD
   - Questions on automation and reliability

4. **Data Scientist**
   - Focus on machine learning and statistics
   - Technologies: Python, TensorFlow, scikit-learn
   - Questions on models and data analysis

5. **Product Manager**
   - Focus on strategy and user impact
   - Technologies: Product thinking, metrics
   - Questions on vision and prioritization

---

## Supported Languages

- English
- French
- Spanish
- German
- Chinese
- Japanese

---

## Deployment

### Local Development
```bash
python main.py        # Backend runs on port 8000
npm start              # Frontend runs on port 3000
```

### Docker
```bash
docker-compose up     # Starts both backend and frontend
```

### Production
Set environment variables and run:
```bash
cd backend
python main.py
```

---

## Configuration

### Environment Variables

Create `.env` file in backend directory:

```
MISTRAL_API_KEY         Your Mistral AI API key
ELEVENLABS_API_KEY      Your ElevenLabs TTS API key
HOST                    Server host (default: 0.0.0.0)
PORT                    Server port (default: 8000)
ENV                     Environment type (development or production)
```

---

## Troubleshooting

### Backend Issues

**Backend fails to start**
- Check Python version: `python --version` requires 3.10 or later
- Install dependencies: `pip install -r requirements.txt`
- Verify .env file contains MISTRAL_API_KEY

**API errors**
- Confirm server runs: `curl http://localhost:8000/docs`
- Check error logs for details
- Verify all environment variables are set

### Frontend Issues

**Frontend fails to start**
- Clear cache: `rm -rf node_modules && npm install`
- Check Node version: `node --version` requires 16 or later
- Try: `npm start --reset-cache`

**No audio playback**
- Verify ELEVENLABS_API_KEY is set
- Check browser microphone permissions
- Review browser console for errors

**Transcription not working**
- First run downloads Whisper model (1GB file)
- Wait 10-15 seconds for initial transcription
- Check microphone permissions in browser

### Reset Everything

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start

cd ../backend
pip install --upgrade -r requirements.txt
python main.py
```

---

## API Documentation

Full OpenAPI documentation available at:

```
http://localhost:8000/docs
```

Interactive API testing available at:

```
http://localhost:8000/redoc
```

---

## Performance

Typical response times:

- Audio recording: Real-time
- Speech transcription: 2-15 seconds
- AI coaching analysis: 5-8 seconds
- Audio synthesis: 3-5 seconds
- End-to-end response: 20-30 seconds

---

## Architecture Overview

The application follows clean separation of concerns:

**Frontend Layer**
- React components for user interface
- Axios for API communication
- React Icons for professional UI

**API Layer**
- FastAPI router pattern for organization
- Pydantic models for input validation
- Structured error responses

**Service Layer**
- Mistral AI integration for coaching
- LangChain for prompt orchestration
- Audio processing with Whisper and ElevenLabs

**Data Layer**
- Session state management
- Question scoring engine
- User response analysis

---

## Security

- API keys stored in environment variables
- CORS configuration for frontend access
- Input validation on all endpoints
- Error messages hide sensitive information
- Rate limiting ready for production use

---

## Future Enhancements

- User authentication and account profiles
- Historical session tracking and analytics
- Custom question sets and practice modes
- Voice quality selection options
- Real-time performance visualization
- Interview report export functionality
- Interview comparison across multiple attempts

---

## Contributing

To contribute to VoxaLab AI:

1. Create a feature branch
2. Implement your changes
3. Test thoroughly
4. Submit a pull request for review

---

## Support

For issues or questions:

- Review the troubleshooting section
- Check API documentation at http://localhost:8000/docs
- Review application logs for error details

---

## Version

Current Version: 1.0.0

---

## Credits

Built with:
- Mistral Large 3 for intelligent coaching
- FastAPI for robust API design
- React for modern user interface
- OpenAI Whisper for accurate transcription
- ElevenLabs for natural voice synthesis
npm install
npm start
```

Frontend will start at `http://localhost:3000`

### 3. Access the Application

Open `http://localhost:3000` in your browser.

---

## Usage

1. **Select a Role** - Choose from 5 career paths
2. **Practice Interview** - Answer 5 role-specific questions
3. **Record or Type** - Use microphone or text input
4. **Get Coaching** - Receive instant AI feedback with scores
5. **Review Report** - See comprehensive performance analysis

---

## Features in Detail

### AI Coaching Feedback
Every answer receives detailed analysis:

- **Clarity Score (1-10)** - Communication clarity and pacing
- **Structure Score (1-10)** - Logical flow and STAR method usage
- **Impact Score (1-10)** - Quantified results and business value
- **Filler Words** - "um", "like", "you know" detection
- **STAR Analysis** - Situation, Task, Action, Result breakdown
- **Coaching Tips** - Specific, actionable recommendations

### Role-Specific Questions
Five carefully researched career paths:

- **Software Engineer** (8 questions) - System design, debugging, code quality
- **Product Manager** (8 questions) - Strategy, metrics, prioritization
- **Designer** (8 questions) - UX principles, design thinking, collaboration
- **Data Scientist** (8 questions) - Analysis, modeling, insights
- **Marketing** (8 questions) - Strategy, growth, metrics

### Performance Reports
Comprehensive session analysis including:

- Executive summary of performance
- Top strengths demonstrated
- Critical improvement areas
- Role-specific recommendations
- Estimated interview readiness percentage
- Actionable next steps

---

## Technology Stack

**Frontend:**
- React 18.2.0 (SPA with hooks)
- Axios (HTTP client)
- Web Audio API (browser recording)
- CSS3 (production animations)

**Backend:**
- FastAPI 0.134.0 (async framework)
- Pydantic 2.11.7 (data validation)
- Mistral Large 3 (LLM)
- LangChain 0.1+ (orchestration)

**Infrastructure:**
- REST API architecture
- Stateless async design
- Ready for Docker deployment

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for comprehensive technical documentation including:
- System design and data flow
- Component breakdowns
- LangChain integration details
- Deployment strategies
- Future roadmap

---

## API Endpoints

### Session Management
```
POST   /session/create              - Start new practice session
GET    /session/{id}                - Get session details
POST   /session/{id}/next           - Move to next question
```

### Answer Analysis
```
POST   /analysis/text               - Analyze typed answer
POST   /analysis/audio              - Transcribe and analyze voice
POST   /analysis/improved-answer    - Generate improved example
```

### Reporting
```
POST   /report/generate             - Create session report
GET    /report/{id}                 - Retrieve saved report
```

### Health
```
GET    /health                      - Service health check
```

Full OpenAPI docs at `http://localhost:8000/docs`

---

## Deployment

### Railway (Recommended for Quick Deploy)
```bash
railway login
railway up
```

### Docker
```bash
# Backend
docker build -t voicecoach-api ./backend
docker run -e MISTRAL_API_KEY=$KEY -p 8000:8000 voicecoach-api

# Frontend  
docker build -t voicecoach-app ./frontend
docker run -p 3000:3000 voicecoach-app
```

See [DEPLOY.md](DEPLOY.md) for detailed deployment procedures.

---

## Key Innovation Points

1. **LangChain Integration** - Structured prompt management and chains for consistent AI output
2. **Dual Input Modality** - Both voice and text support for accessibility
3. **STAR Method Validation** - Automatic detection of structured interview answers
4. **Filler Word Analysis** - Real-time communication pattern detection
5. **Production UI** - Beautiful, responsive interface with smooth animations
6. **Async Architecture** - Non-blocking I/O for high performance
7. **Graceful Fallbacks** - System continues functioning if any component fails

---

## Performance

- **API Response Time**: < 500ms for feedback, < 2s for reports
- **Frontend Load**: < 2 seconds (optimized React)
- **Audio Processing**: Real-time with < 100ms latency
- **Mistral Inference**: 1-3 seconds per response

---

## Roadmap

**Phase 2 (Coming Soon):**
- User authentication & history
- Session persistence (PostgreSQL)
- Advanced analytics dashboard
- Competitive mode & leaderboards

**Phase 3:**
- Video recording (body language feedback)
- Emotion detection from speech
- Multi-language support
- Mobile app (React Native)

**Phase 4:**
- Enterprise features
- LinkedIn integration
- Company-specific libraries
- Team collaboration tools

---

## Contributing

Issues, features, and PRs welcome! 

```bash
git clone https://github.com/voicecoach-ai/voicecoach
cd voicecoach
git checkout -b feature/your-feature
```

---

## Support

- **Issues & Bugs**: GitHub Issues
- **Feature Requests**: GitHub Discussions  
- **Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Help**: http://localhost:8000/docs (Swagger)

---

## Team

Built by Idriss Olivier Bado with expertise in:
- Data architecture
- Full-stack software engineering
- Technical team leadership
- Interview coaching (15+ years)

Powered by [Mistral AI](https://mistral.ai) and [LangChain](https://langchain.com)

---

## License

MIT - See LICENSE file

---

**Live Demo**: Coming Soon  
**Repository**: https://github.com/voicecoach-ai  
**Website**: https://voicecoach-ai.com  

Last Updated: February 28, 2026
