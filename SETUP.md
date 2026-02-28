# Setup Guide

Complete setup instructions for VoxaLab AI.

---

## About VoxaLab AI

VoxaLab AI is a real-time interview coaching platform powered by Mistral Large 3. It provides personalized feedback on interview performance with instant analysis.

Built as a production-ready application with professional UI and real AI coaching.

---

## Quick Start (5 minutes)

### Prerequisites
- Python 3.10 or later
- Node.js 16 or later
- Mistral API Key from https://console.mistral.ai

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

echo "MISTRAL_API_KEY=your_api_key_here" > .env

python main.py
```

Backend runs on http://localhost:8000

### Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs on http://localhost:3000

---

## Features

### Interview Practice
- Multiple roles for practice
- Real-time AI feedback
- Performance scoring
- Question navigation
- Session tracking

### Supported Roles
- Backend Engineer
- Frontend Engineer
- DevOps Engineer
- Data Scientist
- Product Manager

### Scoring Metrics
- Clarity (0-10)
- Depth (0-10)
- Communication (0-10)
- Overall feedback

### Input Methods
- Text typing
- Audio recording
- Real-time transcription

---

## Environment Configuration

Create .env file in backend folder:

```
MISTRAL_API_KEY=your-mistral-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
HOST=0.0.0.0
PORT=8000
ENV=production
```

Get API keys from:
- Mistral: https://console.mistral.ai/
- ElevenLabs: https://elevenlabs.io/

---

## How It Works

1. Select your interview role
2. Choose input method (text or audio)
3. Answer the interview question
4. Get AI feedback and scores
5. Review transcript (for audio input)
6. Navigate to next question
7. View session summary

---

## API Endpoints

Session Management:
- POST /session/create
- GET /session/{id}
- GET /session/questions

Analysis:
- POST /analysis/audio
- POST /analysis/feedback

Text-to-Speech:
- POST /tts/speak
- GET /tts/voices

Reports:
- GET /report/{id}

---

## Project Structure

```
voicecoach-ai/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   └── services/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── public/
├── README.md
├── QUICK_START.md
└── DEPLOY.md
```

---

## Troubleshooting

Backend won't start:
- Check Python version: python --version (need 3.10+)
- Install dependencies: pip install -r requirements.txt
- Verify .env file has MISTRAL_API_KEY

Frontend won't start:
- Clear cache: rm -rf node_modules && npm install
- Check Node version: node --version (need 16+)

---

## Documentation

- README.md - Project overview
- QUICK_START.md - Getting started
- DEPLOY.md - Deployment guide
- TROUBLESHOOTING.md - Common issues
- API docs: http://localhost:8000/docs

---

## Technology Stack

- Python 3.10+
- Node.js 16+
- FastAPI
- React 18.2
- Mistral Large 3
- LangChain
- Docker

---

## Next Steps

1. Install dependencies
2. Add API keys to .env
3. Start backend and frontend
4. Open http://localhost:3000
5. Select role and practice
GET /session/{session_id}         - Get session details
POST /session/{session_id}/next   - Advance to next question
```

### Analysis
```
POST /analysis/text               - Analyze text answer
POST /analysis/audio              - Analyze audio answer
POST /analysis/improved-answer    - Get example great answer
```

### Reports
```
POST /report/generate             - Generate full session report
```

---

## 🛠️ Architecture

```
Frontend (React)
    ↓ (HTTP/REST)
Backend (FastAPI)
    ↓
Mistral Large 3 API
    ↓
AI Analysis & Coaching
```

### Tech Stack
- **Frontend**: React 18, Axios, Responsive CSS
- **Backend**: FastAPI, Python 3.9+
- **AI**: Mistral Large 3 (via Mistral AI SDK)
- **Audio**: Web Audio API (browser recording)

---

## 🎨 Environment Variables

### Backend (.env)
```
MISTRAL_API_KEY=sk-your-key-here
PORT=8000
```

### Frontend
API base URL is configured to `http://localhost:8000`  
For production, update `API_BASE` in `src/App.js`

---

## 📦 Dependency Management

### Backend (requirements.txt)
```
fastapi>=0.109.0          - Web framework
uvicorn>=0.27.0           - ASGI server
mistralai>=1.0.0          - Mistral AI SDK
python-multipart>=0.0.9   - File uploads
pydantic>=2.8.2           - Data validation
python-dotenv>=1.0.0      - Environment variables
httpx>=0.27.0             - HTTP client
```

### Frontend (package.json)
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-scripts": "5.0.1",
  "axios": "^1.6.0"
}
```

---

## 🚀 Deployment

### Option 1: Vercel + Railway (Recommended)

**Backend to Railway:**
1. Push to GitHub
2. Create Railway account at railway.app
3. Connect GitHub repo
4. Set `MISTRAL_API_KEY` environment variable
5. Railway auto-detects Python and deploys

**Frontend to Vercel:**
1. Update API base URL in `frontend/src/App.js`:
   ```javascript
   const API_BASE = 'https://your-railway-app.railway.app';
   ```
2. Push to GitHub
3. Connect to vercel.com
4. Deploy (auto-detected)

### Option 2: Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

---

## 🎓 Interview Questions Included

Each role has 8 tailored questions covering:
- Technical skills
- Problem-solving
- Team collaboration
- Failure/learning
- Decision-making
- Success metrics

---

## 💡 Tips for Best Results

1. **Speak Clearly**: Enunciate to ensure accurate transcription
2. **Use STAR Method**: Situation → Task → Action → Result
3. **Be Specific**: Use concrete examples from your experience
4. **Skip Fillers**: Avoid "um", "like", "basically"
5. **Answer Completely**: Don't rush through your response
6. **Practice Multiple Roles**: Each has different requirements

---

## 🐛 Troubleshooting

### Microphone Not Working
- Check browser permissions (Settings → Microphone)
- Try a different browser (Chrome/Edge work best)
- Ensure no other app is using the microphone

### Backend Connection Error
- Verify backend is running: `http://localhost:8000/health`
- Check firewall settings
- Restart backend if needed

### API Key Error
- Verify `MISTRAL_API_KEY` is set in `.env`
- Get a new key from https://console.mistral.ai
- Restart backend after changing API key

### Audio Analysis Failed
- Try submitting as text instead
- Check internet connection
- Restart the session

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs for errors
3. Verify all dependencies are installed
4. Ensure API key is valid and has credits

---

## 📝 License

Built for the Mistral Hackathon 2026 - Track 2: Anything Goes

Created by: **Idriss Olivier Bado**  
Former Head of Data & Software Engineer

---

## 🔮 Future Enhancements

- Real-time video analysis (face expressions, body language)
- Custom question templates
- Mock interview recording/playback
- Peer comparison and leaderboard
- Interview transcription history
- Resume parsing and role-specific prep
- Mobile app (iOS/Android)
- Real-time Voxtral audio streaming

---

Enjoy your interview practice! 🎤✨
