# 🚀 Quick Start

## Prerequisites
- Python 3.11+
- Node.js 18+
- Mistral API key (optional - demo mode works without it)

## Setup (2 minutes)

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend (new terminal)
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Interview Coach
- `POST /session/answer` - Submit answer, get AI feedback
- `GET /session/questions` - Get interview questions

### Math Tutor
- `POST /math/analyze` - Analyze math problem
- `POST /math/validate-step` - Validate solution step
- `POST /math/generate-solution` - Get complete solution

## Features

✅ Interview Coaching with AI feedback  
✅ Real-time transcription (Whisper)  
✅ Voice synthesis (ElevenLabs)  
✅ Math tutoring system  
✅ Multi-language support  
✅ Demo mode (works without API keys)  

## Documentation

- Full README: [README.md](README.md)
- API Docs: `http://localhost:8000/docs`

## Environment Variables

```env
MISTRAL_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

## Live Demo
[https://huggingface.co/spaces/mistral-hackaton-2026/voxalab](https://huggingface.co/spaces/mistral-hackaton-2026/voxalab)
