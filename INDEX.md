# VoxaLab AI - Documentation Index

Professional interview coaching platform powered by Mistral Large 3.

---

## Getting Started

Start here for first-time users:

**[QUICK_START.md](QUICK_START.md)** - Start the application in 30 seconds
- Backend and frontend setup
- Basic usage workflow
- Testing checklist

**[README.md](README.md)** - Project overview
- Feature summary
- Technology stack
- Architecture
- API endpoints

---

## Installation and Setup

**[SETUP.md](SETUP.md)** - Complete installation guide
- Prerequisites
- Backend setup
- Frontend setup
- Environment configuration
- Troubleshooting

**[setup.sh](setup.sh)** - Automated setup for Linux/Mac
- Runs prerequisite checks
- Creates virtual environments
- Installs dependencies

**[setup.bat](setup.bat)** - Automated setup for Windows
- Checks Python and Node.js
- Installs backend and frontend
- Generates configuration

---

## Deployment

**[DEPLOY.md](DEPLOY.md)** - Production deployment guide
- Local development setup
- Docker deployment
- Environment configuration
- Monitoring and logs
- Performance optimization

---

## Features and Capabilities

**[FEATURES.md](FEATURES.md)** - Complete feature list
- User interface features
- Interview roles
- Languages supported
- Input methods
- AI coaching features
- API endpoints

---

## Technical Documentation

**[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical overview
- Architecture
- Project structure
- Technology stack
- Dependencies
- Version history

**[AUDIO_TRANSCRIPTION_FIX.md](AUDIO_TRANSCRIPTION_FIX.md)** - Audio processing
- Real-time transcription
- Whisper integration
- Language support
- Performance metrics

---

## Troubleshooting

**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- Backend issues
- Frontend issues
- Connection problems
- Audio issues
- Performance optimization
- Docker troubleshooting

---

## Quick Reference

### Start Application

Backend (Terminal 1):
```bash
cd backend
python main.py
```

Frontend (Terminal 2):
```bash
cd frontend
npm start
```

Open: http://localhost:3000

### Check Status

Backend: http://localhost:8000
Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs

### Create Configuration

Create `backend/.env`:
```
MISTRAL_API_KEY=your-key
ELEVENLABS_API_KEY=your-key
HOST=0.0.0.0
PORT=8000
ENV=production
```

---

## File Structure

```
voicecoach-ai/
├── README.md - Main documentation
├── QUICK_START.md - 30-second setup
├── SETUP.md - Full installation
├── DEPLOY.md - Production deployment
├── TROUBLESHOOTING.md - Common issues
├── PROJECT_SUMMARY.md - Technical overview
├── FEATURES.md - Feature list
├── AUDIO_TRANSCRIPTION_FIX.md - Audio docs
├── setup.sh - Linux/Mac setup
├── setup.bat - Windows setup
├── docker-compose.yml - Docker config
├── backend/
│   ├── main.py - API server
│   ├── requirements.txt - Dependencies
│   └── services/ - Business logic
└── frontend/
    ├── src/App.js - React app
    ├── package.json - Dependencies
    └── public/ - Assets
```

---

## Key URLs

- Application: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- API Testing: http://localhost:8000/redoc
- Mistral API: https://console.mistral.ai
- ElevenLabs: https://elevenlabs.io

---

## Important Commands

### Backend

Start server:
```bash
cd backend
python main.py
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

### Frontend

Start development:
```bash
cd frontend
npm start
```

Install dependencies:
```bash
npm install
```

Build for production:
```bash
npm run build
```

### Docker

Start with Docker Compose:
```bash
docker-compose up
```

Build Docker images:
```bash
docker build -t voicecoach-backend ./backend
docker build -t voicecoach-frontend ./frontend
```

---

## Support and Resources

Documentation files are ordered by use case:

1. First time? Read QUICK_START.md
2. Need to install? Use SETUP.md
3. Ready to deploy? See DEPLOY.md
4. Having issues? Check TROUBLESHOOTING.md
5. Want details? Read PROJECT_SUMMARY.md
6. Need features list? See FEATURES.md

For API details, visit: http://localhost:8000/docs

---

## Version Information

Current Version: 1.0.0
Last Updated: February 2026

Technologies:
- Python 3.10+
- Node.js 16+
- React 18.2
- FastAPI
- Mistral Large 3
- LangChain

---

## Next Steps

1. Choose your starting point above
2. Follow the setup guide
3. Add API keys to configuration
4. Start backend and frontend
5. Open http://localhost:3000
6. Start practicing

---

## Additional Resources

- Mistral API Documentation: https://docs.mistral.ai
- FastAPI Documentation: https://fastapi.tiangolo.com
- React Documentation: https://react.dev
- LangChain Documentation: https://docs.langchain.com

